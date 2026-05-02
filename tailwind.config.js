/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./curso/**/*.html",
    "./assets/banners/*.html",
    "./docs/**/*.html"
  ],
  darkMode: 'media',
  theme: {
    extend: {
      colors: {
        primary: '#FACC15',
        'primary-light': '#a16207',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Menlo', 'monospace'],
      },
      typography: ({ theme }) => ({
        DEFAULT: {
          css: {
            '--tw-prose-body': theme('colors.zinc.300'),
            '--tw-prose-headings': theme('colors.zinc.50'),
            '--tw-prose-links': theme('colors.sky.400'),
            '--tw-prose-bold': theme('colors.zinc.50'),
            '--tw-prose-code': theme('colors.primary'),
            'a': { textDecoration: 'none' },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
