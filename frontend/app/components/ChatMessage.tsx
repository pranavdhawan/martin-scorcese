import React from 'react';
import { motion } from 'framer-motion';

type ChatMessageProps = {
    message: {
        role: string;
        content: string;
    };
};

export default function ChatMessage({ message }: ChatMessageProps) {
    const isUser = message.role === 'user';

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`mb-4 ${isUser ? 'text-right' : 'text-left'}`}
        >
            <div
                className={`inline-block p-4 rounded-2xl max-w-[80%] shadow-sm ${isUser
                    ? 'bg-blue-600 text-white rounded-tr-none'
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-none'
                    }`}
            >
                <p className="text-sm md:text-base">{message.content}</p>
            </div>
        </motion.div>
    );
}