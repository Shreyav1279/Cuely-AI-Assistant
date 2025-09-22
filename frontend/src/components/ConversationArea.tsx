import { ChatMessage } from "./ChatMessage";

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: string;
}

interface ConversationAreaProps {
  messages: Message[];
}

export function ConversationArea({ messages }: ConversationAreaProps) {
  return (
    <div className="flex-1 p-6 overflow-y-auto bg-gray-50/30">
      <div className="max-w-4xl mx-auto">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-br from-blue-100 to-purple-100 flex items-center justify-center">
                <span className="text-2xl">🎤</span>
              </div>
              <h3 className="text-lg font-medium text-foreground mb-2">
                Welcome to Cuely
              </h3>
              <p className="text-muted-foreground">
                Click the microphone below to start a conversation
              </p>
            </div>
          </div>
        ) : (
          <div className="space-y-1">
            {messages.map((message) => (
              <ChatMessage
                key={message.id}
                message={message.text}
                isUser={message.isUser}
                timestamp={message.timestamp}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}