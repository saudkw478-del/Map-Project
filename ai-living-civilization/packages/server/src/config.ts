import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import dotenv from "dotenv";
import { z } from "zod";
import type { LlmProviderMode, PublicConfig } from "@civ/shared";

const here = path.dirname(fileURLToPath(import.meta.url));
/** جذر المشروع (نفس العمق في src وفي dist). */
export const ROOT_DIR = path.resolve(here, "../../..");

/** خطأ إعدادات برسالة عربية واضحة. */
export class ConfigError extends Error {
  constructor(public readonly problems: string[]) {
    super("في مشكلة بالإعدادات:\n - " + problems.join("\n - "));
    this.name = "ConfigError";
  }
}

const unit = z.number().min(0).max(1);

const WorldSchema = z.object({
  name: z.string().min(1),
  time: z.object({
    minutesPerRealSecond: z.number().min(0),
    startHour: z.number().min(0).max(23),
    presets: z.record(z.string(), z.number().min(0)).refine((p) => "paused" in p && "normal" in p && "fast" in p, {
      message: "لازم تكون فيه ثلاث سرعات: paused و normal و fast",
    }),
    maxCatchUpDays: z.number().positive(),
  }),
  llm: z.object({
    limits: z.object({
      requestsPerMinute: z.number().int().positive(),
      requestsPerDay: z.number().int().positive(),
      maxRetries: z.number().int().min(0).max(10),
      retryBaseMs: z.number().int().min(100),
    }),
    maxTokensPerRequest: z.number().int().positive(),
  }),
});

const CharacterSchema = z.object({
  id: z.string().regex(/^[a-z][a-z0-9_]*$/, "المعرف حروف إنجليزية صغيرة وأرقام و _ فقط"),
  name: z.string().min(1),
  sex: z.enum(["M", "F"]),
  age: z.number().int().min(18).max(90),
  job: z.string().min(1),
  home: z.string().min(1),
  workplace: z.string().min(1),
  money: z.number().int().min(0),
  personality: z.object({
    summary: z.string().min(1),
    bigFive: z.object({ openness: unit, conscientiousness: unit, extraversion: unit, agreeableness: unit, neuroticism: unit }),
    traits: z.object({ ambition: unit, riskTaking: unit, thrift: unit, humor: unit }),
  }),
  goals: z.object({ shortTerm: z.array(z.string()).min(1), longTerm: z.array(z.string()).min(1) }),
  fears: z.array(z.string()).min(1),
  skills: z.record(z.string(), z.number().min(0).max(10)),
  speech: z.object({
    dialect: z.string().min(1),
    formality: unit,
    verbosity: unit,
    humor: unit,
    quirks: z.array(z.string()),
    samples: z.array(z.string()).min(1),
  }),
});
const CharactersSchema = z.object({ characters: z.array(CharacterSchema).min(1) });

const SafetySchema = z.object({
  version: z.number().int(),
  replacement: z.string().min(1),
  blockedWords: z.array(z.string()),
  blockedPatterns: z.array(z.string()),
});

const EnvSchema = z
  .object({
    PORT: z.coerce.number().int().min(1).max(65535).default(3000),
    LOG_LEVEL: z.enum(["fatal", "error", "warn", "info", "debug", "trace", "silent"]).default("info"),
    DATA_DIR: z.string().default("./data"),
    LLM_PROVIDER: z.enum(["fake", "openai"]).default("fake"),
    LLM_BASE_URL: z.string().url().default("https://generativelanguage.googleapis.com/v1beta/openai/"),
    LLM_API_KEY: z.string().optional(),
    LLM_MODEL: z.string().min(1).default("gemini-2.5-flash"),
    ADMIN_TOKEN: z.string().optional(),
  })
  .refine((e) => e.LLM_PROVIDER === "fake" || !!e.LLM_API_KEY?.trim(), {
    path: ["LLM_API_KEY"],
    message: "LLM_PROVIDER=openai يحتاج مفتاح في LLM_API_KEY (بملف .env). أو خل LLM_PROVIDER=fake للتجربة.",
  });

export type WorldConfig = z.infer<typeof WorldSchema>;
export type Character = z.infer<typeof CharacterSchema>;
export type SafetyConfig = z.infer<typeof SafetySchema>;
export type EnvConfig = z.infer<typeof EnvSchema>;

export interface AppConfig {
  env: EnvConfig;
  world: WorldConfig;
  characters: Character[];
  safety: SafetyConfig;
  dataDir: string;
  clientDir: string;
}

function readJson<T>(file: string, schema: z.ZodType<T>, problems: string[]): T | undefined {
  let raw: unknown;
  try {
    raw = JSON.parse(readFileSync(file, "utf8"));
  } catch (e) {
    problems.push(`${path.basename(file)}: ما قدرت أقرأ الملف (${(e as Error).message})`);
    return undefined;
  }
  const r = schema.safeParse(raw);
  if (!r.success) {
    for (const i of r.error.issues) problems.push(`${path.basename(file)} → ${i.path.join(".") || "(الجذر)"}: ${i.message}`);
    return undefined;
  }
  return r.data;
}

export interface LoadOptions {
  /** متغيرات البيئة (للاختبار). الافتراضي: process.env بعد قراءة .env */
  env?: Record<string, string | undefined>;
  configDir?: string;
}

export function loadConfig(opts: LoadOptions = {}): AppConfig {
  if (!opts.env) dotenv.config({ path: path.join(ROOT_DIR, ".env"), quiet: true });
  const source = opts.env ?? process.env;
  const problems: string[] = [];

  // القيم الفاضية في .env (مثل LLM_API_KEY=) نعتبرها غير موجودة
  const cleaned: Record<string, string | undefined> = {};
  for (const k of Object.keys(EnvSchema.shape)) cleaned[k] = source[k] === "" ? undefined : source[k];

  const envR = EnvSchema.safeParse(cleaned);
  if (!envR.success) for (const i of envR.error.issues) problems.push(`.env → ${i.path.join(".")}: ${i.message}`);

  const dir = opts.configDir ?? source.CONFIG_DIR ?? path.join(ROOT_DIR, "config");
  const world = readJson(path.join(dir, "world.json"), WorldSchema, problems);
  const chars = readJson(path.join(dir, "characters.json"), CharactersSchema, problems);
  const safety = readJson(path.join(dir, "safety.json"), SafetySchema, problems);

  if (chars) {
    const ids = chars.characters.map((c) => c.id);
    if (new Set(ids).size !== ids.length) problems.push("characters.json: في معرفات مكررة");
  }
  if (problems.length || !envR.success || !world || !chars || !safety) throw new ConfigError(problems);

  const env = envR.data;
  const dataDir = path.resolve(ROOT_DIR, env.DATA_DIR);
  return { env, world, characters: chars.characters, safety, dataDir, clientDir: path.join(ROOT_DIR, "packages/client/dist") };
}

/** الإعدادات اللي تنعرض للواجهة. ما فيها أي مفتاح. */
export function toPublicConfig(cfg: AppConfig): PublicConfig {
  const provider: LlmProviderMode = cfg.env.LLM_PROVIDER;
  return {
    name: cfg.world.name,
    time: { minutesPerRealSecond: cfg.world.time.minutesPerRealSecond, presets: cfg.world.time.presets },
    llm: { provider, model: provider === "openai" ? cfg.env.LLM_MODEL : null },
  };
}

export function clientBuilt(cfg: AppConfig): boolean {
  return existsSync(path.join(cfg.clientDir, "index.html"));
}
