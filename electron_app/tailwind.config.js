/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        military: {
          50: '#f0f4f0',
          100: '#dce8dc',
          200: '#b9d1b9',
          300: '#8fb88f',
          400: '#6a9d6a',
          500: '#4a7c4a',
          600: '#3a643a',
          700: '#2e4d2e',
          800: '#253d25',
          900: '#1e321e',
        },
        tactical: {
          bg: '#1a1a1a',
          surface: '#2d2d2d',
          border: '#404040',
          text: '#e0e0e0',
        }
      }
    },
  },
  plugins: [],
}
