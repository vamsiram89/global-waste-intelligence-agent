/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: "#0A2342",
        navy: "#092A4D",
        leaf: "#1E9E67",
        mint: "#E8F7EF",
        sky: "#2F80ED",
        amber: "#F59E0B",
        danger: "#E5484D",
        paper: "#F7FAFC",
      },
      boxShadow: {
        soft: "0 18px 50px rgba(10, 35, 66, 0.10)",
        card: "0 10px 30px rgba(10, 35, 66, 0.08)",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "Segoe UI", "sans-serif"],
      },
    },
  },
  plugins: [],
};
