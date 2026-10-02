import type { AddressInfo } from "node:net";
import { io as connect } from "socket.io-client";
import pino from "pino";
import { afterAll, beforeAll, describe, expect, it } from "vitest";
import { SOCKET_EVENTS } from "@civ/shared";
import { createApp, type RunningApp } from "../src/app.js";
import { loadConfig } from "../src/config.js";

let app: RunningApp;
let base = "";

beforeAll(async () => {
  const cfg = loadConfig({ env: { LLM_PROVIDER: "openai", LLM_API_KEY: "SECRET-VALUE-123" } });
  app = createApp(cfg, pino({ level: "silent" }));
  await new Promise<void>((r) => app.http.listen(0, r));
  base = `http://127.0.0.1:${(app.http.address() as AddressInfo).port}`;
});
afterAll(async () => {
  await app.close();
});

describe("السيرفر", () => {
  it("/health يرد ok", async () => {
    const r = await fetch(`${base}/health`);
    const j = (await r.json()) as { ok: boolean; llm: { provider: string } };
    expect(r.status).toBe(200);
    expect(j.ok).toBe(true);
    expect(j.llm.provider).toBe("openai");
  });

  it("ما يسرّب المفتاح بأي رد عام", async () => {
    for (const p of ["/health", "/api/config"]) {
      const txt = await (await fetch(base + p)).text();
      expect(txt).not.toContain("SECRET-VALUE-123");
    }
  });

  it("/api/config فيه سرعات الوقت", async () => {
    const j = (await (await fetch(`${base}/api/config`)).json()) as { time: { presets: Record<string, number> } };
    expect(j.time.presets.paused).toBe(0);
  });

  it("Socket.io يرسل hello عند الاتصال", async () => {
    const socket = connect(base, { transports: ["websocket"] });
    const hello = await new Promise<{ name: string }>((resolve, reject) => {
      socket.on(SOCKET_EVENTS.hello, resolve);
      socket.on("connect_error", reject);
    });
    socket.close();
    expect(hello.name).toContain("مدينة");
  });
});
