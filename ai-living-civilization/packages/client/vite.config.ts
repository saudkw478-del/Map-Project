import { defineConfig } from "vite";

// في التطوير: الواجهة على 5173 والسيرفر على 3000، والطلبات تتحول له.
export default defineConfig({
  server: {
    port: 5173,
    proxy: {
      "/api": "http://localhost:3000",
      "/health": "http://localhost:3000",
      "/socket.io": { target: "http://localhost:3000", ws: true },
    },
  },
  build: { outDir: "dist", emptyOutDir: true },
});
