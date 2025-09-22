import { useState, useRef } from "react";
import { Mic, MicOff } from "lucide-react";

interface VoiceInputBarProps {
  onSendMessage: (message: string) => void;
}

export function VoiceInputBar({ onSendMessage }: VoiceInputBarProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [supported, setSupported] = useState<boolean | null>(null);
  const recognitionRef = useRef<any>(null);

  // initialize SpeechRecognition if available
  const ensureRecognition = () => {
    if (recognitionRef.current) return recognitionRef.current;
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setSupported(false);
      return null;
    }
    setSupported(true);
    const recog = new SpeechRecognition();
    recog.lang = "en-US";
    recog.interimResults = false;
    recog.maxAlternatives = 1;
    recognitionRef.current = recog;
    return recog;
  };

  const handleMicClick = () => {
    const recog = ensureRecognition();
    if (!recog) {
      // Not supported: fallback to prompt
      const typed = prompt("Your browser doesn't support SpeechRecognition. Type your question instead:");
      if (typed) onSendMessage(typed);
      return;
    }

    if (!isRecording) {
      // start
      try {
        recog.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setIsRecording(false);
          onSendMessage(transcript);
        };
        recog.onerror = (e: any) => {
          console.error("Speech recognition error", e);
          setIsRecording(false);
        };
        recog.onend = () => {
          setIsRecording(false);
        };
        recog.start();
        setIsRecording(true);
      } catch (e) {
        console.error("Failed to start recognition", e);
        setIsRecording(false);
      }
    } else {
      // stop
      try {
        recog.stop();
      } catch (e) {
        console.error("Failed to stop recognition", e);
      }
      setIsRecording(false);
    }
  };

  const handleManualSend = (e: React.KeyboardEvent<HTMLInputElement>) => {
    const val = (e.target as HTMLInputElement).value;
    if (e.key === "Enter" && val.trim().length > 0) {
      onSendMessage(val.trim());
      (e.target as HTMLInputElement).value = "";
    }
  };

  return (
    <div className="p-4 border-t border-border bg-muted">
      <div className="max-w-[900px] mx-auto flex items-center gap-3">
        <input
          placeholder="Click mic & speak your question, or type and press Enter..."
          className="flex-1 px-4 py-3 rounded-md border border-border bg-transparent outline-none"
          onKeyDown={handleManualSend}
        />
        <button
          onClick={handleMicClick}
          className={`p-3 rounded-full transition-transform ${
            isRecording ? 'bg-red-500 hover:bg-red-600 scale-110' : 'bg-blue-500 hover:bg-blue-600 hover:scale-105'
          }`}
          title={isRecording ? "Stop recording" : "Start recording"}
        >
          {isRecording ? (
            <MicOff className="w-5 h-5 text-white" />
          ) : (
            <Mic className="w-5 h-5 text-white" />
          )}
        </button>
      </div>
    </div>
  );
}
