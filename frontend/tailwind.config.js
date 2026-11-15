/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        forest: {
          light: '#2d6a4f',
          DEFAULT: '#1a4d2e',
          dark: '#11331e'
        },
        sand: {
          light: '#fdfbf7',
          DEFAULT: '#f4e8c1',
          dark: '#e0ce99'
        },
        accent: {
          light: '#f39c12',
          DEFAULT: '#e67e22',
          dark: '#d35400'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      }
    },
  },
  plugins: [],
}
