/** أنواع وثوابت مشتركة بين السيرفر والواجهة. */

export const PROJECT_NAME = "AI Living Civilization";
export const PROJECT_NAME_AR = "مدينة الذكاء الاصطناعي الحية";

/** أسماء أحداث Socket.io (مكان واحد عشان ما نغلط في الأسماء). */
export const SOCKET_EVENTS = {
  hello: "server:hello",
} as const;

export type LlmProviderMode = "fake" | "openai";

/** رد /health */
export interface HealthResponse {
  ok: true;
  name: string;
  version: string;
  uptimeSec: number;
  llm: { provider: LlmProviderMode; model: string | null };
}

/** إعدادات الوقت اللي تنعرض للواجهة (ما فيها أي أسرار). */
export interface PublicTimeConfig {
  minutesPerRealSecond: number;
  presets: Record<string, number>;
}

/** رد /api/config */
export interface PublicConfig {
  name: string;
  time: PublicTimeConfig;
  llm: { provider: LlmProviderMode; model: string | null };
}
