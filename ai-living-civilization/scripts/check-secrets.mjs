// يفحص ملفات المشروع (غير المتجاهلة) ويتأكد ما فيها مفاتيح حقيقية.
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const patterns = [
  [/AIza[0-9A-Za-z_\-]{35}/, "مفتاح Google/Gemini"],
  [/\bsk-[A-Za-z0-9_\-]{20,}/, "مفتاح بصيغة sk-"],
  [/\bgsk_[A-Za-z0-9]{20,}/, "مفتاح Groq"],
  [/\bghp_[A-Za-z0-9]{30,}/, "رمز GitHub"],
  [/-----BEGIN [A-Z ]*PRIVATE KEY-----/, "مفتاح خاص"],
];

let files;
try {
  files = execFileSync("git", ["ls-files", "--cached", "--others", "--exclude-standard", "--", "."], { encoding: "utf8" })
    .split("\n")
    .filter(Boolean);
} catch {
  console.log("ما قدرت أستخدم git، تخطيت فحص المفاتيح.");
  process.exit(0);
}

const bad = [];
for (const f of files) {
  if (f.endsWith("package-lock.json")) continue;
  let text;
  try { text = readFileSync(f, "utf8"); } catch { continue; }
  for (const [re, label] of patterns) if (re.test(text)) bad.push(`${f}: ${label}`);
}
if (bad.length) {
  console.error("⚠️ لقيت أشياء تشبه المفاتيح:\n" + bad.join("\n"));
  process.exit(1);
}
console.log(`✅ ما لقيت مفاتيح في ${files.length} ملف.`);
