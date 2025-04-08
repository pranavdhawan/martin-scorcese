'use client';
import { useState } from 'react';
import ChatInput from './components/ChatInput';
import ReactMarkdown from 'react-markdown';

const API_URL = 'http://localhost:8000';

export default function Home() {
  const [messages, setMessages] = useState<Array<{ role: string; content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async (message: string) => {
    try {
      setIsLoading(true);
      setMessages(prev => [...prev, { role: 'user', content: message }]);

      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        mode: 'cors',
        body: JSON.stringify({ question: message }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Server error');
      }

      const data = await response.json();
      setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
    } catch (error: any) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${error.message || 'Failed to connect to server'}`
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="w-full max-w-2xl space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`p-4 rounded-lg ${msg.role === 'user'
              ? 'bg-blue-500 text-white ml-auto'
              : 'bg-gray-200 text-gray-900'
              } max-w-[80%] ${msg.role === 'user' ? 'ml-auto' : 'mr-auto'}`}
          >
            <div className="prose dark:prose-invert max-w-none">
              <ReactMarkdown
                components={{
                  em: ({ node, ...props }) => <em className="italic" {...props} />,
                  strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
                }}
              >
                {msg.content}
              </ReactMarkdown>
            </div>

          </div>
        ))}
        <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
      </div>
    </main>
  );
}