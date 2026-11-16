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
        },
        ethereal: {
          bg: '#06120D',
          dark: '#030805',
          card: 'rgba(255, 255, 255, 0.04)',
          border: 'rgba(255, 255, 255, 0.08)',
          mint: '#4ADE80',
          emerald: '#10B981',
          gold: '#F59E0B',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        serif: ['"Playfair Display"', 'Georgia', 'serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        'glow-mint': '0 0 25px -5px rgba(74, 222, 128, 0.35)',
        'glow-emerald': '0 0 30px -5px rgba(16, 185, 129, 0.35)',
        'glow-gold': '0 0 25px -5px rgba(245, 158, 11, 0.35)',
        'luxury': '0 25px 50px -12px rgba(6, 18, 13, 0.85)',
      }
    },
  },
  plugins: [],
}
