export default {
  darkMode: 'class', // ✅ this line is key
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: { extend: {} },
  plugins: [require('@tailwindcss/line-clamp')],
}