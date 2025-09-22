interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

export function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div
        className={`max-w-[70%] px-4 py-3 rounded-2xl shadow-sm ${
          isUser
            ? 'bg-blue-100 text-blue-900 rounded-br-lg'
            : 'bg-white border border-border text-foreground rounded-bl-lg'
        }`}
      >
        <p className="text-sm leading-relaxed">{message}</p>
        {timestamp && (
          <p className="text-xs text-muted-foreground mt-1">{timestamp}</p>
        )}
      </div>
    </div>
  );
}