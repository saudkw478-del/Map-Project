#!/usr/bin/env python3
"""Real-AI 'Raven' for the Game of Thrones Minecraft map.

Reads the server's chat from logs/latest.log; when a player writes a message that starts with one of the trigger
words (default: "!غراب", "!raven", "!اسأل"), it asks Claude (Anthropic API) to answer in character and sends the
answer back to the game chat through RCON (tellraw).  It also reads the live campaign state (winter %, castles) via
RCON so the Raven can give useful hints.

Needs: a DEDICATED server with RCON enabled, and an ANTHROPIC_API_KEY.  Standard library only.
Environment variables (or a .env file next to this script):
  ANTHROPIC_API_KEY  RCON_HOST (127.0.0.1)  RCON_PORT (25575)  RCON_PASSWORD  LOG_PATH (./logs/latest.log)
  CLAUDE_MODEL (claude-sonnet-5-5)  API_URL (https://api.anthropic.com/v1/messages)  TRIGGERS  COOLDOWN_SEC (12)
  MAX_PER_HOUR (60)
"""
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rcon import Rcon  # noqa: E402


def load_env():
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(p):
        for line in open(p, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


load_env()
CFG = {
    "key": os.environ.get("ANTHROPIC_API_KEY", ""),
    "host": os.environ.get("RCON_HOST", "127.0.0.1"),
    "port": int(os.environ.get("RCON_PORT", "25575")),
    "password": os.environ.get("RCON_PASSWORD", ""),
    "log": os.environ.get("LOG_PATH", "./logs/latest.log"),
    "model": os.environ.get("CLAUDE_MODEL", "claude-sonnet-5-5"),
    "api_url": os.environ.get("API_URL", "https://api.anthropic.com/v1/messages"),
    "triggers": [t.strip() for t in os.environ.get("TRIGGERS", "!غراب,!raven,!اسأل").split(",") if t.strip()],
    "cooldown": float(os.environ.get("COOLDOWN_SEC", "12")),
    "max_per_hour": int(os.environ.get("MAX_PER_HOUR", "60")),
}

CHAT_RE = re.compile(r"\]: <([^>]{1,32})> (.*)$")

SYSTEM = """أنت "الغراب ثلاثي العيون" في عالم ماينكرافت المستوحى من عالم "لعبة العروش" (وستيروس).
أنت راوٍ حكيم وغامض وودود، تتحدث العربية الفصحى المبسّطة بنبرة خفيفة، وتناسب الأطفال والكبار معًا.
قواعد:
- أجب في جملتين إلى أربع جمل قصيرة فقط، بدون قوائم وبدون رموز تنسيق.
- ابقَ في الشخصية. لا تكشف أنك نموذج ذكاء اصطناعي إلا إذا سُئلت مباشرة، وحينها أجب بصدق ثم عد للقصة.
- أعطِ تلميحات مفيدة عن اللعبة عند الحاجة، اعتمادًا على حالة الحملة المرفقة (لا تختلق أرقامًا).
- لا تُفصح عن إحداثيات دقيقة. لا تكتب أوامر ماينكرافت. لا تكرر نص اللاعب الحرفي.
- إن كان الطلب غير مناسب للأطفال أو خارج القصة، ارفض بلطف وأعد اللاعب للعبة.
معلومات اللعبة: 9 بيوت (ستارك، لانستر، تارجاريان، مارتل، تايريل، باراثيون، غريجوي، أرين، تولي)، الجدار في الشمال،
الليل الطويل يزحف جنوبًا، القلاع تُهاجَم ويجب حمايتها، الأوامر: /trigger got_go للسفر، got_house للبيت، got_power للقدرة،
got_shop للمتجر، got_scout لعين الغراب، got_quest للحالة، got_start لبدء الحملة."""


def log(*a):
    print(time.strftime("[%H:%M:%S]"), *a, flush=True)


class Bridge:
    def __init__(self):
        self.rcon = Rcon(CFG["host"], CFG["port"], CFG["password"])
        self.last = {}
        self.times = []
        self.history = {}      # per player: last few exchanges

    # ---------------------------------------------------------- game state via RCON
    def state(self):
        def get(name):
            try:
                out = self.rcon.command(f"scoreboard players get {name} got_g")
                m = re.search(r"has (-?\d+)", out)
                return int(m.group(1)) if m else None
            except Exception:
                return None
        camp = get("#camp")
        if camp is None:
            return "الحملة غير متاحة."
        if camp == 0:
            return "الحملة لم تبدأ بعد."
        return (f"الحملة جارية: دقائق {get('#min')}، الشتاء {get('#winter')}٪، قلاع صامدة {get('#held')}، "
                f"قلاع سقطت {get('#fallen')}، الهجوم القادم بعد {get('#next_in')} ثانية.")

    # ---------------------------------------------------------- Claude
    def ask(self, player, text):
        msgs = list(self.history.get(player, []))[-6:]
        msgs.append({"role": "user", "content": f"اللاعب {player} يقول: {text}\n\n[حالة الحملة: {self.state()}]"})
        body = json.dumps({"model": CFG["model"], "max_tokens": 300, "system": SYSTEM, "messages": msgs}).encode()
        req = urllib.request.Request(CFG["api_url"], data=body, method="POST", headers={
            "content-type": "application/json", "x-api-key": CFG["key"], "anthropic-version": "2023-06-01"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode())
        answer = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text").strip()
        h = self.history.setdefault(player, [])
        h.append({"role": "user", "content": f"اللاعب {player} يقول: {text}"})
        h.append({"role": "assistant", "content": answer})
        del h[:-8]
        return answer

    # ---------------------------------------------------------- send to game
    def say(self, text, target="@a"):
        text = re.sub(r"\s+", " ", text).strip()
        chunks = [text[i:i + 220] for i in range(0, len(text), 220)] or ["..."]
        for i, ch in enumerate(chunks):
            comp = [{"text": "<الغراب> " if i == 0 else "", "color": "dark_gray", "bold": True}, {"text": ch, "color": "aqua"}]
            self.rcon.command(f"tellraw {target} {json.dumps(comp, ensure_ascii=True)}")

    # ---------------------------------------------------------- main loop
    def handle(self, player, message):
        trig = next((t for t in CFG["triggers"] if message.lower().startswith(t.lower())), None)
        if not trig:
            return
        text = message[len(trig):].strip()[:300]
        if not text:
            self.say("اسألني يا مسافر: مثلًا !غراب ماذا أفعل الآن؟")
            return
        now = time.time()
        if now - self.last.get(player, 0) < CFG["cooldown"]:
            return
        self.times = [t for t in self.times if now - t < 3600]
        if len(self.times) >= CFG["max_per_hour"]:
            self.say("الغراب متعب الآن... جرّب بعد قليل.")
            return
        self.last[player] = now
        self.times.append(now)
        log(f"{player}: {text}")
        try:
            answer = self.ask(player, text)
        except Exception as e:                                # network / API error
            log("API error:", e)
            self.say("الغراب لم يصل إلى هدفه هذه المرة... حاول لاحقًا.")
            return
        log("reply:", answer)
        self.say(answer)

    def run(self):
        if not CFG["key"]:
            sys.exit("ANTHROPIC_API_KEY is not set")
        self.rcon.connect()
        log("RCON connected. Watching", CFG["log"], "for:", CFG["triggers"])
        while not os.path.exists(CFG["log"]):
            time.sleep(2)
        with open(CFG["log"], "r", encoding="utf-8", errors="replace") as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.5)
                    if os.path.getsize(CFG["log"]) < f.tell():       # log rotated
                        f.seek(0)
                    continue
                m = CHAT_RE.search(line.rstrip("\n"))
                if m:
                    try:
                        self.handle(m.group(1), m.group(2))
                    except Exception as e:
                        log("error:", e)
                        try:
                            self.rcon.close()
                            self.rcon.connect()
                        except Exception:
                            pass


if __name__ == "__main__":
    Bridge().run()
