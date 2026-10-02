import { cpSync, mkdtempSync, readFileSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { describe, expect, it } from "vitest";
import { ConfigError, loadConfig, ROOT_DIR, toPublicConfig } from "../src/config.js";

const realConfig = path.join(ROOT_DIR, "config");
const withCopy = (mutate: (dir: string) => void) => {
  const dir = mkdtempSync(path.join(tmpdir(), "civ-cfg-"));
  cpSync(realConfig, dir, { recursive: true });
  mutate(dir);
  return dir;
};

describe("الإعدادات", () => {
  it("تقرأ الإعدادات الحقيقية وتستخدم الموديل الوهمي افتراضياً", () => {
    const cfg = loadConfig({ env: {} });
    expect(cfg.env.LLM_PROVIDER).toBe("fake");
    expect(cfg.characters.map((c) => c.id)).toEqual(["khalid", "noura"]);
    expect(cfg.world.time.presets).toMatchObject({ paused: 0, normal: 1 });
  });

  it("القيم الفاضية في .env تُعتبر غير موجودة", () => {
    const cfg = loadConfig({ env: { LLM_API_KEY: "", LLM_PROVIDER: "" } });
    expect(cfg.env.LLM_PROVIDER).toBe("fake");
  });

  it("openai بدون مفتاح يعطي رسالة عربية واضحة", () => {
    expect(() => loadConfig({ env: { LLM_PROVIDER: "openai" } })).toThrow(/LLM_API_KEY/);
    try {
      loadConfig({ env: { LLM_PROVIDER: "openai" } });
    } catch (e) {
      expect(e).toBeInstanceOf(ConfigError);
    }
  });

  it("openai مع مفتاح يمشي، والإعدادات العامة ما فيها المفتاح", () => {
    const cfg = loadConfig({ env: { LLM_PROVIDER: "openai", LLM_API_KEY: "SECRET-VALUE-123", LLM_MODEL: "my-model" } });
    const pub = JSON.stringify(toPublicConfig(cfg));
    expect(pub).not.toContain("SECRET-VALUE-123");
    expect(JSON.parse(pub).llm).toEqual({ provider: "openai", model: "my-model" });
  });

  it("يرفض سرعة وقت ناقصة", () => {
    const dir = withCopy((d) => {
      const p = path.join(d, "world.json");
      const w = JSON.parse(readFileSync(p, "utf8"));
      delete w.time.presets.fast;
      writeFileSync(p, JSON.stringify(w));
    });
    expect(() => loadConfig({ env: {}, configDir: dir })).toThrow(/paused و normal و fast/);
  });

  it("يرفض حد طلبات سالب", () => {
    const dir = withCopy((d) => {
      const p = path.join(d, "world.json");
      const w = JSON.parse(readFileSync(p, "utf8"));
      w.llm.limits.requestsPerMinute = -1;
      writeFileSync(p, JSON.stringify(w));
    });
    expect(() => loadConfig({ env: {}, configDir: dir })).toThrow(/requestsPerMinute/);
  });

  it("يرفض شخصية بقيمة طبع خارج 0 إلى 1", () => {
    const dir = withCopy((d) => {
      const p = path.join(d, "characters.json");
      const c = JSON.parse(readFileSync(p, "utf8"));
      c.characters[0].personality.bigFive.openness = 1.5;
      writeFileSync(p, JSON.stringify(c));
    });
    expect(() => loadConfig({ env: {}, configDir: dir })).toThrow(/openness/);
  });

  it("يرفض معرفات شخصيات مكررة", () => {
    const dir = withCopy((d) => {
      const p = path.join(d, "characters.json");
      const c = JSON.parse(readFileSync(p, "utf8"));
      c.characters[1].id = c.characters[0].id;
      writeFileSync(p, JSON.stringify(c));
    });
    expect(() => loadConfig({ env: {}, configDir: dir })).toThrow(/مكررة/);
  });
});
