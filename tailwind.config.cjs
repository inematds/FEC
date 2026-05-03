/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./curso/**/*.html",
    "./assets/banners/*.html",
    "./docs/**/*.html"
  ],
  // Sem darkMode — single mode (dark) para v1.0; light mode será adicionado em v1.1
  // quando todo o CSS estiver coberto.
  safelist: [
    // Cores das 6 trilhas — TODAS as variantes que o gerador usa, FORÇADAS
    // no CSS mesmo se não aparecerem em ARQUIVOS HTML que o purge analisa.
    {
      pattern: /(text|bg|border|from|to|via|hover:bg|hover:text|hover:border)-(emerald|blue|purple|amber|teal|rose)-(400|500|600|700|800|900)(\/(10|20|30|40|50))?/,
    },
    // Primary (custom)
    "text-primary",
    "bg-primary",
    "border-primary",
    "hover:bg-yellow-300",
    "hover:text-yellow-300",
    "from-primary",
    "bg-primary/10",
    "border-primary/40",
  ],
  theme: {
    extend: {
      colors: {
        primary: '#FACC15',
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
            '--tw-prose-code': theme('colors.yellow.400'),
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
