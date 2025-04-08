import React, { useState } from 'react';
import { motion } from 'framer-motion';

type ChatInputProps = {
    onSendMessage: (message: string) => void;
    disabled: boolean;
};

export default function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
    const [input, setInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim()) return;

        onSendMessage(input);
        setInput('');
    };

    return (
        <motion.form
            onSubmit={handleSubmit}
            className="flex gap-2 items-center"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
        >
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                className="flex-1 p-3 border border-gray-300 dark:border-gray-700 rounded-full bg-white dark:bg-gray-900 text-gray-800 dark:text-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
                placeholder="Ask Scorsese something..."
                disabled={disabled}
            />
            <motion.button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-full flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                disabled={disabled || !input.trim()}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
            >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
            </motion.button>
        </motion.form>
    );
}