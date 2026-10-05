/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: "var(--color-bg)",
        darkPanel: "var(--color-panel)",
        darkBorder: "var(--color-border)",
        darkHover: "var(--color-hover)",
        accentCyan: "var(--color-accent-cyan)",
        accentBlue: "var(--color-accent-blue)",
        statusGood: "#059669",
        statusWarn: "#d97706",
        statusError: "#dc2626",
        textMain: "var(--color-text-main)",
        textMuted: "var(--color-text-muted)",
      }
    },
  },
  plugins: [],
}
