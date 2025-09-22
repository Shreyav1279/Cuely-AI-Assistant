from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import tempfile, os, asyncio

# Optional imports
try:
    import whisper
    WHISPER_AVAILABLE = True
    whisper_model = None
except Exception:
    WHISPER_AVAILABLE = False
    whisper_model = None

try:
    import ollama
    OLLAMA_AVAILABLE = True
except Exception:
    OLLAMA_AVAILABLE = False

app = FastAPI(title="Cuely Backend")

# Allow requests from local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust to specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    text: str

class AskResponse(BaseModel):
    answer: str

@app.on_event("startup")
async def startup_event():
    global whisper_model
    if WHISPER_AVAILABLE:
        # load whisper model lazily at startup (small model)
        try:
            whisper_model = whisper.load_model("small")
            print("Whisper model loaded.")
        except Exception as e:
            print("Failed to load Whisper model at startup:", e)

@app.post("/api/ask", response_model=AskResponse)
async def ask(req: AskRequest):
    if not OLLAMA_AVAILABLE:
        raise HTTPException(status_code=500, detail="Ollama python package not available on server.")
    text = req.text
    try:
        resp = ollama.chat(model=os.environ.get("OLLAMA_MODEL", "gemma:2b"), messages=[
            {"role": "user", "content": text}
        ])
        answer = resp.get("message", {}).get("content", "")
        return AskResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama error: {e}")

@app.post("/api/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not WHISPER_AVAILABLE:
        raise HTTPException(status_code=500, detail="Whisper not available on server.")
    # save uploaded file to temp
    suffix = os.path.splitext(file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name
    try:
        # ensure model loaded
        global whisper_model
        if whisper_model is None:
            whisper_model = whisper.load_model("small")
        result = whisper_model.transcribe(tmp_path)
        text = result.get("text", "")
        # Optionally, ask Ollama for an answer
        answer = ""
        if OLLAMA_AVAILABLE:
            try:
                resp = ollama.chat(model=os.environ.get("OLLAMA_MODEL", "gemma:2b"), messages=[
                    {"role": "user", "content": text}
                ])
                answer = resp.get("message", {}).get("content", "")
            except Exception as e:
                answer = f"Ollama error: {e}"
        return {"text": text, "answer": answer}
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
