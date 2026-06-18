import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
})

/*
# SOURCES:
// https://vite.dev/config/
// https://tailwindcss.com/docs/installation/using-vite
*/
