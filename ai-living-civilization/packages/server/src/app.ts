import { createServer, type Server as HttpServer } from "node:http";
import express from "express";
import { Server as IoServer } from "socket.io";
import pino, { type Logger } from "pino";
import { PROJECT_NAME, SOCKET_EVENTS, type HealthResponse } from "@civ/shared";
import { clientBuilt, toPublicConfig, type AppConfig } from "./config.js";

export const VERSION = "0.1.0";

export interface RunningApp {
  http: HttpServer;
  io: IoServer;
  log: Logger;
  close(): Promise<void>;
}

export function createApp(cfg: AppConfig, log: Logger = pino({ level: cfg.env.LOG_LEVEL })): RunningApp {
  const app = express();
  app.disable("x-powered-by");
  const startedAt = Date.now();

  app.get("/health", (_req, res) => {
    const body: HealthResponse = {
      ok: true,
      name: PROJECT_NAME,
      version: VERSION,
      uptimeSec: Math.round((Date.now() - startedAt) / 1000),
      llm: toPublicConfig(cfg).llm,
    };
    res.json(body);
  });

  app.get("/api/config", (_req, res) => {
    res.json(toPublicConfig(cfg));
  });

  if (clientBuilt(cfg)) app.use(express.static(cfg.clientDir));

  const http = createServer(app);
  const io = new IoServer(http, { serveClient: false });
  io.on("connection", (socket) => {
    socket.emit(SOCKET_EVENTS.hello, { name: cfg.world.name, serverTime: new Date().toISOString() });
  });

  return {
    http,
    io,
    log,
    close: () =>
      new Promise<void>((resolve) => {
        void io.close(() => resolve());
      }),
  };
}
