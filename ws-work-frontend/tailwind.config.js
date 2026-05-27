/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        ws: {
          yellow: '#FACC15', // amarelo da logo e sublinhados
          darkBlue: '#0A0B1A', // azul escuro do rodapé
          purple: '#2A1B54', // roxo do gradiente
          inputBg: '#1C1D3B', // fundo dos campos do formulário
          inputBorder: '#393A5C', // borda dos campos
        }
      },
      backgroundImage: {
        'ws-gradient': 'linear-gradient(to right, #0A0B1A, #2A1B54)',
      }
    },
  },
  plugins: [],
}