/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './app/**/*.{js,ts,jsx,tsx}',
        './components/**/*.{js,ts,jsx,tsx}',
    ],
    darkMode: 'media',
    theme: {
        extend: {
            colors: {
                blue: {
                    600: '#2563eb',
                    700: '#1d4ed8',
                },
            },
            animation: {
                'bounce-slow': 'bounce 3s infinite',
            },
        },
    },
    plugins: [
        require('tailwind-scrollbar'),
    ],
};