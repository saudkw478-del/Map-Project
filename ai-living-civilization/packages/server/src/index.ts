import pino from "pino";
import { createApp } from "./app.js";
import { clientBuilt, ConfigError, loadConfig } from "./config.js";

let cfg;
try {
  cfg = loadConfig();
} catch (e) {
  if (e instanceof ConfigError) {
    console.error("\n❌ " + e.message + "\n\nراجع ملف .env والملفات اللي في مجلد config/\n");
    process.exit(1);
  }
  throw e;
}

const log = pino({ level: cfg.env.LOG_LEVEL });
const running = createApp(cfg, log);

running.http.listen(cfg.env.PORT, () => {
  log.info(
    { port: cfg.env.PORT, llm: cfg.env.LLM_PROVIDER, model: cfg.env.LLM_PROVIDER === "openai" ? cfg.env.LLM_MODEL : null, characters: cfg.characters.map((c) => c.name) },
    "✅ السيرفر شغال",
  );
  if (!clientBuilt(cfg)) log.info("الواجهة غير مبنية. في التطوير افتح http://localhost:5173 (npm run dev).");
  if (cfg.env.LLM_PROVIDER === "fake") log.info("الذكاء الاصطناعي: موديل وهمي (بدون مفتاح). غيّر LLM_PROVIDER في .env لما تجهز.");
});

const stop = (sig: string) => {
  log.info({ sig }, "جاري الإيقاف...");
  void running.close().then(() => process.exit(0));
  setTimeout(() => process.exit(0), 3000).unref();
};
process.on("SIGINT", () => stop("SIGINT"));
process.on("SIGTERM", () => stop("SIGTERM"));
