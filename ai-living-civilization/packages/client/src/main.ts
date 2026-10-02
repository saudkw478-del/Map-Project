import { io } from "socket.io-client";
import { SOCKET_EVENTS, type HealthResponse, type PublicConfig } from "@civ/shared";

const $ = (id: string) => document.getElementById(id) as HTMLElement;

function show(id: string, text: string, ok?: boolean) {
  const el = $(id);
  el.textContent = text;
  el.className = ok === undefined ? "" : ok ? "ok" : "bad";
}

async function load() {
  try {
    const h = (await (await fetch("/health")).json()) as HealthResponse;
    show("server", `شغال (نسخة ${h.version})`, true);
    const c = (await (await fetch("/api/config")).json()) as PublicConfig;
    show("llm", c.llm.provider === "fake" ? "موديل وهمي (بدون مفتاح)" : `Gemini/OpenAI: ${c.llm.model}`);
    const names: Record<string, string> = { paused: "إيقاف", normal: "عادي", fast: "سريع" };
    show("speeds", Object.entries(c.time.presets).map(([k, v]) => `${names[k] ?? k}: ${v}`).join(" · "));
  } catch {
    show("server", "ما قدرت أوصل للسيرفر", false);
  }
}

const socket = io();
socket.on(SOCKET_EVENTS.hello, () => show("socket", "متصل", true));
socket.on("disconnect", () => show("socket", "انقطع الاتصال", false));
socket.on("connect_error", () => show("socket", "ما قدرت أتصل", false));

void load();
