/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx,ts,tsx}'],
  theme: {
    extend: {
      colors: {
        slate: {
          950: '#07111f'
        },
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#2563eb',
          600: '#0f766e',
          700: '#1d4ed8'
        }
      },
      boxShadow: {
        glow: '0 20px 60px rgba(37, 99, 235, 0.18)'
      }
    }
  },
  plugins: []
};
