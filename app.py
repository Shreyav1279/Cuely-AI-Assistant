import gradio as gr
import sounddevice as sd
import numpy as np
import queue
import tempfile
import threading
import whisper
import soundfile as sf
import ollama  

# -------------------------------
# CONFIG
# -------------------------------
SAMPLE_RATE = 16000
BLOCKSIZE = 1024

model = whisper.load_model("small")        #This model used then we use CPU
# model = whisper.load_model("large")      #This model used then we use GPU
q = queue.Queue()
recording = False
frames = []

# -------------------------------
# AUDIO STREAMING
# -------------------------------
def audio_callback(indata, frames_count, time, status):
    if recording:
        q.put(indata.copy())

def start_recording():
    global recording, frames
    recording = True
    frames = []
    threading.Thread(target=record_audio).start()
    return "Recording started..."

def record_audio():
    with sd.InputStream(callback=audio_callback,
                        channels=1,
                        samplerate=SAMPLE_RATE,
                        blocksize=BLOCKSIZE):
        while recording:
            try:
                frames.append(q.get(timeout=1))
            except queue.Empty:
                pass

def stop_and_transcribe():
    global recording
    recording = False
    if not frames:
        return "No audio recorded", ""

    audio = np.concatenate(frames, axis=0)

    # Save to temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        sf.write(f.name, audio, SAMPLE_RATE)
        file_path = f.name

    # Transcribe with Whisper
    result = model.transcribe(file_path)
    question = result["text"]

    # Ask Ollama Gemma:2b
    try:
        response = ollama.chat(model="gemma:2b", messages=[
            {"role": "user", "content": question}
        ])
        answer = response["message"]["content"]
    except Exception as e:
        answer = f"❌ Ollama error: {e}"

    return question, answer

# -------------------------------
# GRADIO UI
# -------------------------------
with gr.Blocks() as demo:
    gr.Markdown("## 🎤 Real-Time Speech to Text (Whisper + Ollama)")

    with gr.Row():
        start_btn = gr.Button("Start Recording")
        stop_btn = gr.Button("Stop & Ask Ollama")

    transcript = gr.Textbox(label="Your Question (from Speech)")
    answer = gr.Textbox(label="Gemma's Answer")

    start_btn.click(start_recording, outputs=transcript)
    stop_btn.click(stop_and_transcribe, outputs=[transcript, answer])

demo.launch()





# import sounddevice as sd
# import numpy as np
# import queue
# import threading
# import whisper
# import subprocess
# import gradio as gr
# import time

# # -------------------------------
# # CONFIG
# # -------------------------------
# SAMPLE_RATE = 16000
# BLOCKSIZE = 1024
# CHANNELS = 1

# model = whisper.load_model("small")      #This model used for CPU
# # model = whisper.Load_model("large")    #This model used for GPU

# audio_queue = queue.Queue()
# is_recording = False
# transcript_text = ""
# answer_text = ""

# # -------------------------------
# # AUDIO STREAMING
# # -------------------------------
# def audio_callback(indata, frames, time_info, status):
#     if is_recording:
#         audio_queue.put(indata.copy())

# def start_recording():
#     global is_recording, transcript_text
#     transcript_text = ""
#     is_recording = True
#     threading.Thread(target=process_audio, daemon=True).start()
#     return "🎙️ Recording started..."

# def stop_recording():
#     global is_recording
#     is_recording = False
#     return "⏹️ Recording stopped."

# # -------------------------------
# # PROCESS AUDIO WITH WHISPER
# # -------------------------------
# def process_audio():
#     global transcript_text, answer_text
#     buffer = np.zeros((0, CHANNELS), dtype=np.float32)

#     while is_recording:
#         try:
#             data = audio_queue.get(timeout=1)
#             buffer = np.concatenate((buffer, data), axis=0)

#             if len(buffer) > SAMPLE_RATE * 5:
#                 audio_chunk = buffer[:, 0]
#                 result = model.transcribe(audio_chunk, fp16=False)
#                 transcript_text += " " + result["text"]

#                 # Query Ollama
#                 answer_text = query_ollama(result["text"])
#                 buffer = np.zeros((0, CHANNELS), dtype=np.float32)

#         except queue.Empty:
#             continue

# # -------------------------------
# # QUERY OLLAMA
# # -------------------------------
# def query_ollama(prompt):
#     try:
#         process = subprocess.Popen(
#             ["ollama", "run", "gemma:2b"],
#             stdin=subprocess.PIPE,
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True
#         )
#         out, _ = process.communicate(prompt, timeout=30)
#         return out.strip()
#     except Exception as e:
#         return f"Error querying Ollama: {e}"

# # -------------------------------
# # UPDATE UI LOOP (Gradio 4.x safe)
# # -------------------------------
# def live_updates():
#     while True:
#         yield transcript_text, answer_text
#         time.sleep(1)

# # -------------------------------
# # GRADIO UI
# # -------------------------------
# with gr.Blocks() as demo:
#     gr.Markdown("## 🎙️ Live Speech-to-Answer Assistant (Cluely-style)")

#     with gr.Row():
#         start_btn = gr.Button("▶️ Start Recording")
#         stop_btn = gr.Button("⏹️ Stop Recording")

#     transcript_box = gr.Textbox(label="Live Transcript", interactive=False, lines=8)
#     answer_box = gr.Textbox(label="AI Answer", interactive=False, lines=6)

#     start_btn.click(start_recording, outputs=transcript_box)
#     stop_btn.click(stop_recording, outputs=transcript_box)

#     # ✅ In Gradio 4.x we use generator + .load
#     demo.load(live_updates, None, [transcript_box, answer_box])

# demo.launch()
