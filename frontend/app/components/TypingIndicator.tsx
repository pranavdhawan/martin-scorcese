import React from 'react';
import { motion } from 'framer-motion';

export default function TypingIndicator() {
    return (
        <div className="flex items-center space-x-2 p-4 rounded-2xl bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 rounded-tl-none inline-block mb-4">
            <motion.div
                className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity, repeatType: 'loop' }}
            />
            <motion.div
                className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity, repeatType: 'loop', delay: 0.2 }}
            />
            <motion.div
                className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity, repeatType: 'loop', delay: 0.4 }}
            />
        </div>
    );
}