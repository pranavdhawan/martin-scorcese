import React, { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import TypingIndicator from './TypingIndicator';

type Message = {
    role: string;
    content: string;
};

type ChatProps = {
    messages: Message[];
    loading: boolean;
    onSendMessage: (message: string) => void;
};

export default function Chat({ messages, loading, onSendMessage }: ChatProps) {
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, loading]);

    return (
        <div className="flex flex-col h-full">
            <motion.div
                className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-300 dark:scrollbar-thumb-gray-700 scrollbar-track-transparent"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full">
                        <motion.div
                            className="text-center text-gray-500 dark:text-gray-400"
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.5, delay: 0.2 }}
                        >
                            <h2 className="text-xl font-semibold mb-2">Welcome to Scorsese Chat</h2>
                            <p>Ask anything about Martin Scorsese's films and career</p>
                        </motion.div>
                    </div>
                ) : (
                    <>
                        {messages.map((message, index) => (
                            <ChatMessage key={index} message={message} />
                        ))}
                        {loading && <TypingIndicator />}
                        <div ref={messagesEndRef} />
                    </>
                )}
            </motion.div>
            <div className="p-4 border-t border-gray-200 dark:border-gray-800">
                <ChatInput onSendMessage={onSendMessage} disabled={loading} />
            </div>
        </div>
    );
}