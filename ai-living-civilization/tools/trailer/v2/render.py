"""Renders the 60s trailer frame by frame (numpy/cv2) and pipes it to ffmpeg. All motion, light and typography are generated here."""
import argparse, math, os, subprocess, sys
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ap = argparse.ArgumentParser()
ap.add_argument("--sp"); ap.add_argument("--ff"); ap.add_argument("--audio"); ap.add_argument("--out")
ap.add_argument("--scale", type=float, default=1.0); ap.add_argument("--t0", type=float, default=0); ap.add_argument("--t1", type=float, default=60)
ap.add_argument("--crf", default="21")
A = ap.parse_args()
SP, FF = A.sp, A.ff
W, H, CH, FPS, DUR = 1920, 1080, 816, 30, 60.0
Y0 = (H - CH) // 2
ASSET = f"{SP}/tr_work"; FONTS = f"{SP}/vid_assets"
SRC = f"{SP}/vid_in/input.mp4"
smooth = lambda x: (lambda c: c * c * (3 - 2 * c))(min(1.0, max(0.0, x)))
lerp = lambda a, b, x: a + (b - a) * x

def load(path, rgba=False):
    im = Image.open(path).convert("RGBA" if rgba else "RGB"); return np.array(im)

# ---------------- assets ----------------
hero = load(f"{ASSET}/hero.png").astype(np.float32)               # 546x512 painting (both characters)
fig = {k: load(f"{ASSET}/{k}_cut.png", True) for k in ("khalid_front", "noura_front")}
EXPR = ["joy", "sad", "fear", "surprise", "anger", "think"]
faces = {(w, e): load(f"{ASSET}/face_{w}_{e}.png", True) for w in ("khalid", "noura") for e in EXPR}

yy, xx = np.mgrid[0:CH, 0:W].astype(np.float32)
rr = ((xx - W / 2) / (W / 2)) ** 2 + ((yy - CH / 2) / (CH / 2)) ** 2
VIG = np.clip(1 - 0.50 * np.clip(rr - 0.15, 0, 1.2) ** 1.1, 0.25, 1)[..., None].astype(np.float32)
BOTTOM = np.clip((yy - CH * 0.55) / (CH * 0.45), 0, 1)[..., None] ** 1.5 * 0.55

def blur_bg(img, sigma=38, dark=0.55):
    b = cv2.resize(img, (W, CH), interpolation=cv2.INTER_CUBIC)
    return cv2.GaussianBlur(b, (0, 0), sigma) * dark

def grade(f, contrast=1.0, sat=1.0, tint=(1, 1, 1), gamma=1.0, lift=0.0):
    f = np.clip(f / 255.0, 0, 1)
    if gamma != 1.0: f = f ** gamma
    if contrast != 1.0: f = (f - 0.5) * contrast + 0.5
    if sat != 1.0:
        lum = (f * np.array([0.3, 0.59, 0.11], np.float32)).sum(-1, keepdims=True); f = lum + (f - lum) * sat
    f = f * np.array(tint, np.float32) + lift
    return np.clip(f, 0, 1) * 255

def bloom(f, thr=165, strength=0.4, sigma=22):
    s = cv2.resize(f, (W // 4, CH // 4), interpolation=cv2.INTER_AREA)
    b = np.clip(s - thr, 0, 255); b = cv2.GaussianBlur(b, (0, 0), sigma / 4)
    return f + cv2.resize(b, (W, CH), interpolation=cv2.INTER_CUBIC) * strength

def glitch(f, amt, rng):
    if amt < 0.02: return f
    for _ in range(int(2 + amt * 9)):
        y0 = int(rng.integers(0, CH - 12)); hh = int(rng.integers(5, int(14 + amt * 100))); dx = int(rng.normal(0, amt * 80))
        f[y0:y0 + hh] = np.roll(f[y0:y0 + hh], dx, axis=1)
    sh = int(amt * 16); f[..., 0] = np.roll(f[..., 0], sh, axis=1); f[..., 2] = np.roll(f[..., 2], -sh, axis=1)
    if amt > 0.5: f[::2] *= 0.88
    return f

class Dust:
    def __init__(self, n=130, seed=3, color=(255, 226, 170), speed=16):
        r = np.random.default_rng(seed); self.p = r.random((n, 6)); self.c = np.array(color, np.float32); self.speed = speed
    def render(self, t, k=1.0):
        L = np.zeros((CH, W), np.float32)
        for x0, y0, z, ph, vx, vy in self.p:
            x = (x0 * W + (vx - 0.35) * t * self.speed * (0.4 + z * 1.6)) % W; y = (y0 * CH - (0.25 + vy) * t * self.speed * 0.8 * (0.4 + z)) % CH
            a = (0.35 + 0.65 * z) * (0.55 + 0.45 * math.sin(t * 1.9 + ph * 6.28))
            cv2.circle(L, (int(x), int(y)), int(1 + 2 * z), float(a), -1, cv2.LINE_AA)
        L = cv2.GaussianBlur(L, (0, 0), 1.8)
        return L[..., None] * self.c * (42 * k)

def paste(canvas, rgba, cx, by, height, alpha=1.0, fade_bottom=0.0, flip=False, rot=0.0):
    """Paste an RGBA cut-out, bottom-aligned at by, horizontally centred on cx, scaled to `height`."""
    h0, w0 = rgba.shape[:2]; s = height / h0; w1 = max(2, int(w0 * s)); h1 = int(height)
    im = cv2.resize(rgba, (w1, h1), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    if flip: im = im[:, ::-1]
    if rot:
        M = cv2.getRotationMatrix2D((w1 / 2, h1 * 0.7), rot, 1.0); im = cv2.warpAffine(im, M, (w1, h1), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
    a = im[..., 3].astype(np.float32) / 255 * alpha
    if fade_bottom > 0:
        ramp = np.clip((h1 - np.arange(h1)) / (h1 * fade_bottom), 0, 1)[:, None]; a = a * ramp ** 1.4
    x0, y0 = int(cx - w1 / 2), int(by - h1)
    xa, xb = max(0, x0), min(W, x0 + w1); ya, yb = max(0, y0), min(CH, y0 + h1)
    if xa >= xb or ya >= yb: return canvas
    sub = a[ya - y0:yb - y0, xa - x0:xb - x0, None]; src = im[ya - y0:yb - y0, xa - x0:xb - x0, :3].astype(np.float32)
    canvas[ya:yb, xa:xb] = canvas[ya:yb, xa:xb] * (1 - sub) + src * sub
    return canvas

# ---------------- footage decoder ----------------
class Footage:
    def __init__(self, t0, dur, y0=140, speed=1.0, reverse=False):
        vf = f"crop=1550:660:0:{y0 + 30},scale={W}:{CH}:flags=lanczos,fps={FPS}"
        if speed != 1.0: vf = f"setpts=PTS/{speed}," + vf
        if reverse: vf += ",reverse"
        need = dur * speed + 0.5
        self.p = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-ss", str(t0), "-t", str(need), "-i", SRC, "-an", "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                                  stdout=subprocess.PIPE, bufsize=W * CH * 3 * 4)
        self.last = np.zeros((CH, W, 3), np.float32)
    def next(self):
        b = self.p.stdout.read(W * CH * 3)
        if len(b) == W * CH * 3: self.last = np.frombuffer(b, np.uint8).reshape(CH, W, 3).astype(np.float32)
        return self.last.copy()

# ---------------- text layers ----------------
def font(name, size, wght=None):
    f = ImageFont.truetype(f"{FONTS}/{name}", size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
class Cap:
    def __init__(self, lines, s, e, fn="Tajawal-Bold.ttf", size=64, y=0.80, color=(255, 255, 255), kufi=False, fi=0.5, fo=0.5):
        self.s, self.e, self.fi, self.fo = s, e, fi, fo
        fnt = font("ReemKufi[wght].ttf" if kufi else fn, size, 700 if kufi else None)
        lay = Image.new("RGBA", (W, CH), (0, 0, 0, 0)); sh = Image.new("RGBA", (W, CH), (0, 0, 0, 0))
        n = len(lines); cy = int(CH * y) - (n - 1) * int(size * 0.62)
        for i, ln in enumerate(lines):
            for dr, col, dy in ((ImageDraw.Draw(sh), (0, 0, 0, 235), 4), (ImageDraw.Draw(lay), color + (255,), 0)):
                dr.text((W // 2, cy + i * int(size * 1.28) + dy), ln, font=fnt, fill=col, anchor="ma", direction="rtl", language="ar")
        sh = sh.filter(ImageFilter.GaussianBlur(10)); sh.alpha_composite(lay)
        arr = np.array(sh).astype(np.float32); self.a = arr[..., 3:4] / 255; self.c = arr[..., :3]
        ys = np.where(self.a[..., 0].max(1) > 0.01)[0]; self.r0, self.r1 = max(0, ys.min() - 4), min(CH, ys.max() + 4)
    def apply(self, f, t):
        if t < self.s or t > self.e: return f
        k = min(1.0, (t - self.s) / self.fi) * min(1.0, (self.e - t) / self.fo); k = smooth(k)
        a = self.a[self.r0:self.r1] * k; f[self.r0:self.r1] = f[self.r0:self.r1] * (1 - a) + self.c[self.r0:self.r1] * a
        return f

CAPS = [
    Cap(["كل صباح…", "يستيقظان على السؤال نفسه."], 1.2, 5.3),
    Cap(["خالد… ونورة."], 6.4, 9.6, size=92, kufi=True, color=(255, 244, 214)),
    Cap(["لا أحد أخبرهما من صنعهما."], 12.4, 16.6),
    Cap(["ويتذكران أشياء لم يعيشاها."], 18.0, 22.6, y=0.86),
    Cap(["ثم وجدا أثراً…"], 24.0, 27.4),
    Cap(["ورسالة بخط لا يعرفانه."], 27.8, 30.4),
    Cap(["هو يريد الحقيقة."], 30.8, 33.8, y=0.88),
    Cap(["وهي تريد أن تبقى."], 34.0, 37.2, y=0.88),
    Cap(["الحب… أم الحقيقة؟"], 38.0, 43.4, size=104, kufi=True, color=(255, 244, 214), y=0.5),
    Cap(["ماذا لو كان كل ما نحبه…"], 44.9, 48.6, y=0.84),
    Cap(["مكتوباً؟"], 48.8, 52.2, size=118, kufi=True, color=(255, 214, 160), y=0.84),
    Cap(["هل يوجد أحد مثلنا؟"], 53.2, 57.0, size=100, kufi=True, color=(255, 244, 214), y=0.84, fi=0.9),
]

def text_overlay(lines_fonts, w=W, h=CH):
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for text, fnt, x, y, col, ar, anchor in lines_fonts:
        kw = {"direction": "rtl", "language": "ar"} if ar else {}
        d.text((x, y), text, font=fnt, fill=col, anchor=anchor, **kw)
    arr = np.array(lay).astype(np.float32); return arr[..., :3], arr[..., 3:4] / 255

# ---------------- shots ----------------
dust_warm, dust_cool = Dust(140, 3), Dust(120, 8, (190, 225, 255))
HERO_BG = blur_bg(hero)
def hero_frame(t, dur, z0=1.0, z1=1.18, memory=0.0, pan=(0, 0), flare=0.0, pull=False):
    k = smooth(t / dur); z = lerp(z0, z1, k)
    hf = CH * z; sc = hf / 512.0; w1 = int(546 * sc)
    im = cv2.resize(hero, (w1, int(hf)), interpolation=cv2.INTER_CUBIC)
    f = HERO_BG.copy()
    cx = W / 2 + pan[0] * k; top = int((CH - hf) / 2 + pan[1] * k)
    x0 = int(cx - w1 / 2)
    ya, yb = max(0, top), min(CH, top + im.shape[0]); xa, xb = max(0, x0), min(W, x0 + w1)
    sub = im[ya - top:yb - top, xa - x0:xb - x0]
    edge = np.minimum(np.arange(xb - xa) + (xa - x0), (w1 - 1) - (np.arange(xb - xa) + (xa - x0))); m = np.clip(edge / 70.0, 0, 1)[None, :, None]
    f[ya:yb, xa:xb] = f[ya:yb, xa:xb] * (1 - m) + sub * m
    if memory > 0:
        f = cv2.GaussianBlur(f, (0, 0), 1 + 16 * memory); f = grade(f, 1.0, 1 - 0.7 * memory, (1, 1, 1), 1.0, 0.0)
    # two suns -> warm flares
    if flare > 0:
        for sx, sy, r in ((119, 73, 90), (404, 46, 70)):
            px, py = x0 + sx * sc, top + sy * sc
            g = np.exp(-(((xx - px) / (r * sc * 0.9)) ** 2 + ((yy - py) / (r * sc * 0.9)) ** 2))[..., None] * np.array([255, 205, 130], np.float32)
            f += g * 0.35 * flare
    return f

def fb(f): return f  # placeholder

# S1: fog dawn footage
S1 = None
def build_shots():
    shots = []
    def add(start, name, fn, xin=0.0): shots.append(dict(start=start, name=name, fn=fn, xin=xin))
    # S1 0-6
    st = {}
    def s1(t, i):
        if "f" not in st: st["f"] = Footage(21.5, 6.8, y0=180)
        f = grade(st["f"].next(), 1.12, 0.9, (0.92, 1.0, 1.1), 1.0, 0.0)
        return f + dust_cool.render(t, 0.7)
    add(0.0, "s1", s1)
    # S2 5.6-12: hero painting, memory resolve
    def s2(t, i):
        f = hero_frame(t, 6.8, 1.0, 1.2, memory=max(0, 1 - t / 2.4) ** 1.5, flare=smooth((t - 1.5) / 2.0))
        f = grade(f, 1.08, 1.12, (1.04, 1.0, 0.94))
        return f + dust_warm.render(t, 1.0)
    add(5.6, "s2", s2, 0.9)
    # S3 11.6-18: tent footage + ghost cutouts
    st3 = {}
    def s3(t, i):
        if "f" not in st3: st3["f"] = Footage(2.0, 7.0, y0=150)
        f = grade(st3["f"].next(), 1.1, 1.05, (1.05, 1.0, 0.92))
        for key, cx, ph in (("khalid_front", 520, 0.0), ("noura_front", 1390, 1.7)):
            a = 0.34 * smooth((t - 0.6) / 1.2) * smooth((6.4 - t) / 1.0) * (0.7 + 0.3 * math.sin(t * 1.3 + ph))
            ghost = np.zeros_like(f); ghost = paste(ghost, fig[key], cx + 16 * math.sin(t * 0.6 + ph), CH + 30 - 8 * math.sin(t * 0.9 + ph), 790, 1.0, 0.0)
            ghost = cv2.GaussianBlur(ghost, (0, 0), 2.2); f = f * (1 - a * 0.35) + ghost * a * 1.1
        return f + dust_warm.render(t, 0.8)
    add(11.6, "s3", s3, 0.9)
    # S4 17.6-23.2: faces montage
    order = [("khalid", "joy"), ("noura", "joy"), ("khalid", "sad"), ("noura", "sad"), ("khalid", "fear"), ("noura", "fear"),
             ("khalid", "surprise"), ("noura", "surprise"), ("khalid", "anger"), ("noura", "anger"), ("khalid", "think"), ("noura", "think")]
    def face_shot(order, per, t, tint, seed):
        n = min(int(t / per), len(order) - 1); lt = t - n * per; who, ex = order[n]
        f = HERO_BG * 0.6 + np.array([8, 22, 30], np.float32)
        s = 1.0 + 0.05 * (1 - smooth(lt / 0.3)) + 0.02 * lt / per
        x = W * (0.40 if who == "khalid" else 0.60) + (math.sin(t * 2 + n) * 10)
        glow = np.zeros_like(f); glow = paste(glow, faces[(who, ex)], x, CH + 40, 790 * s, 1.0, 0.3)
        halo = cv2.GaussianBlur(glow, (0, 0), 40) * 0.55; f = f + halo * np.array([1.0, 0.7, 0.45], np.float32)
        f = paste(f, faces[(who, ex)], x, CH + 40, 790 * s, 1.0, 0.3)
        f = grade(f, 1.1, 0.95, tint)
        f = glitch(f, 0.9 * (1 - smooth(lt / 0.22)), np.random.default_rng(seed + n))
        if lt < 0.06: f = f + 38
        return f + dust_cool.render(t, 0.8)
    add(17.6, "s4", lambda t, i: face_shot(order, 5.6 / 12, t, (1.0, 1.0, 1.0), 10))
    # S5 23.2-30.4: dusk->night footage, gate fades in
    st5 = {}
    def s5(t, i):
        if "f" not in st5: st5["f"] = Footage(14.0, 7.8, y0=170)
        f = grade(st5["f"].next(), 1.15, 1.0, (0.85, 0.98, 1.12), 1.05)
        # the old gate (ruin from the painting) rises as a faint double exposure
        a = 0.5 * smooth((t - 3.8) / 2.2) * smooth((7.4 - t) / 0.9)
        if a > 0.01:
            ruin = hero[100:250, 330:546]; ru = cv2.resize(ruin, (int(ruin.shape[1] * 4.2), int(ruin.shape[0] * 4.2)), interpolation=cv2.INTER_CUBIC)
            lay = np.zeros_like(f); h2, w2 = ru.shape[:2]; y0_ = int(CH * 0.14); x0_ = int(W * 0.5 - w2 / 2)
            hh = min(h2, CH - y0_); lay[y0_:y0_ + hh, x0_:x0_ + w2] = ru[:hh]
            lay = cv2.GaussianBlur(lay, (0, 0), 3.0) * np.array([0.9, 1.0, 1.1], np.float32)
            msk = np.clip(1 - rr * 0.9, 0, 1)[..., None]; f = f * (1 - a * 0.35 * msk) + lay * a * 0.9 * msk
        return f + dust_cool.render(t, 1.1)
    add(23.2, "s5", s5, 0.6)
    # S6 30-37.4: standoff
    st6 = {}
    def s6(t, i):
        if "f" not in st6: st6["f"] = Footage(18.5, 8.0, y0=200)
        bg = grade(st6["f"].next(), 1.2, 0.8, (0.8, 0.95, 1.12), 1.15)
        bg = cv2.GaussianBlur(bg, (0, 0), 5.5) * 0.52
        k = smooth(t / 7.4); f = bg
        for key, cx, hgt, ph in (("khalid_front", 520, 770, 0.0), ("noura_front", 1400, 735, 2.0)):
            cxx = cx + lerp(-18, 18, k) * (1 if key[0] == "k" else -1)
            lay = np.zeros_like(f); lay = paste(lay, fig[key], cxx, CH + 60, hgt * lerp(1.0, 1.07, k), 1.0, 0.0)
            rim = cv2.GaussianBlur(lay, (0, 0), 28) * np.array([1.0, 0.62, 0.35], np.float32) * 0.55
            f = f + rim; f = paste(f, fig[key], cxx, CH + 60, hgt * lerp(1.0, 1.07, k), 1.0, 0.0)
        f = grade(f, 1.12, 1.0, (0.96, 1.0, 1.04))
        return f + dust_warm.render(t, 0.7)
    add(30.0, "s6", s6, 0.5)
    # S7 37-44.4: faces fast + flashes of time-lapse
    st7 = {}
    order7 = [("khalid", "think"), ("noura", "fear"), ("khalid", "surprise"), ("noura", "think"), ("khalid", "anger"), ("noura", "sad"), ("khalid", "fear"), ("noura", "anger"),
              ("khalid", "sad"), ("noura", "surprise"), ("khalid", "anger"), ("noura", "fear"), ("khalid", "think"), ("noura", "think"), ("khalid", "fear"), ("noura", "surprise")]
    def s7(t, i):
        if "f" not in st7: st7["f"] = Footage(0.0, 7.6, y0=170, speed=3.5)
        tl = st7["f"].next()
        f = face_shot(order7, 0.46, t, (1.0, 0.96, 0.92), 50)
        a = 0.28 + 0.1 * math.sin(t * 7); f = f * (1 - a) + grade(tl, 1.3, 0.6, (0.9, 1.0, 1.1)) * a
        return glitch(f, 0.18 + 0.3 * smooth((t - 4) / 3), np.random.default_rng(900 + i))
    add(37.0, "s7", s7)
    # S8 44-52.4: terminal "changelog" over reversed footage
    st8 = {}
    mono, taj = font("IBMPlexMono-Medium.ttf", 44), font("Tajawal-Medium.ttf", 46)
    LINES = [("memory.khalid  —  v1 → v2 → v3", mono, False, (150, 255, 220)), ("memory.noura  —  v1 → v2", mono, False, (150, 255, 220)),
             ("ذكرى «النهر»: عُدّلت", taj, True, (190, 235, 230)), ("affinity(khalid, noura) = 0.62", mono, False, (150, 255, 220)), ("edited_by = ???", mono, False, (255, 120, 90))]
    LAY = [text_overlay([(txt, fnt, W // 2, int(CH * 0.2 + i * 100), col + (255,), ar, "ma")]) for i, (txt, fnt, ar, col) in enumerate(LINES)]
    def s8(t, i):
        if "f" not in st8: st8["f"] = Footage(4.0, 8.8, y0=170, speed=1.0, reverse=True)
        f = grade(st8["f"].next(), 1.25, 0.45, (0.85, 1.05, 1.0)) * 0.5
        for j, (c, a) in enumerate(LAY):
            ts = 0.5 + j * 0.8; k = smooth((t - ts) / 0.25) * (0.75 + 0.25 * math.sin(t * 26 + j))
            if t > 3.6: k *= 1 - smooth((t - 3.6) / 0.5)
            f = f * (1 - a * k) + c * a * k
        g = 0.55 + 0.4 * smooth((t - 3) / 3)
        f = glitch(f, g if (int(t * 8) % 3 == 0) else g * 0.35, np.random.default_rng(2000 + i))
        f[::3] *= 0.9
        return f + dust_cool.render(t, 0.4)
    add(44.0, "s8", s8)
    # S9 52-57.6: hero, calm return, pull back
    def s9(t, i):
        f = hero_frame(t, 6.6, 1.28, 1.0, flare=0.9)
        f = grade(f, 1.06, 1.12, (1.05, 1.0, 0.92)); return f + dust_warm.render(t, 1.1)
    add(52.0, "s9", s9, 1.0)
    # S10 57.2-60: title card
    tf = font("ReemKufi[wght].ttf", 124, 700); mf = font("IBMPlexMono-Medium.ttf", 34); sf = font("Tajawal-Medium.ttf", 40)
    TC, TA = text_overlay([("مدينة الذكاء الاصطناعي الحية", tf, W // 2, int(CH * 0.36), (255, 244, 214, 255), True, "ma"),
                           ("شخصيات ذكاء اصطناعي · كل ما تراه يحدث من تلقاء نفسه", sf, W // 2, int(CH * 0.82), (225, 225, 225, 255), True, "ma")])
    def s10(t, i):
        f = HERO_BG * 0.45 + np.array([4, 8, 12], np.float32)
        k = smooth((t - 0.2) / 1.0); f = f * (1 - TA * k) + TC * TA * k
        # accent line + latin subtitle
        cv2.line(f, (W // 2 - 150, int(CH * 0.36 + 190)), (W // 2 + 150, int(CH * 0.36 + 190)), (227 * k, 166 * k, 64 * k), 3, cv2.LINE_AA)
        txt = "AI  LIVING  CIVILIZATION"; pil = Image.fromarray(np.zeros((60, W, 3), np.uint8)); d = ImageDraw.Draw(pil)
        d.text((W // 2, 8), txt, font=mf, fill=(int(230 * k),) * 3, anchor="ma"); f[int(CH * 0.36 + 215):int(CH * 0.36 + 275)] += np.array(pil).astype(np.float32)
        return f + dust_warm.render(t, 0.8)
    add(57.2, "s10", s10, 0.8)
    return shots

SHOTS = build_shots()
for i, s in enumerate(SHOTS): s["end"] = (SHOTS[i + 1]["start"] + SHOTS[i + 1]["xin"]) if i + 1 < len(SHOTS) else DUR + 0.1
HB = list(np.arange(23.4, 37.0, 1.0)) + list(np.arange(37.0, 43.6, 0.7))

enc = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", A.audio,
                        "-vf", f"scale={int(W * A.scale) // 2 * 2}:{int(H * A.scale) // 2 * 2}:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", A.crf, "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "192k", "-ss", str(A.t0), "-t", str(A.t1 - A.t0), "-movflags", "+faststart", A.out], stdin=subprocess.PIPE) if False else None

def main():
    N0, N1 = int(A.t0 * FPS), int(A.t1 * FPS)
    raw = subprocess.Popen([FF, "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                            "-ss", str(A.t0), "-i", A.audio, "-vf", f"scale={int(W * A.scale) // 2 * 2}:{int(H * A.scale) // 2 * 2}:flags=lanczos",
                            "-c:v", "libx264", "-preset", "medium", "-crf", A.crf, "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", str(A.t1 - A.t0), "-movflags", "+faststart", A.out],
                           stdin=subprocess.PIPE)
    grain_rng = np.random.default_rng(5)
    local = {s["name"]: 0 for s in SHOTS}
    for n in range(N0, N1):
        t = n / FPS
        out = None
        for s in SHOTS:
            if s["start"] <= t < s["end"]:
                # make sure sequential decoders have advanced to this local frame
                want = int(round((t - s["start"]) * FPS))
                f = None
                while local[s["name"]] <= want:
                    f = s["fn"](local[s["name"]] / FPS, local[s["name"]]); local[s["name"]] += 1
                if f is None: f = s["fn"](want / FPS, want)
                a = smooth((t - s["start"]) / s["xin"]) if s["xin"] > 0 else 1.0
                out = f if out is None else out * (1 - a) + f * a
        if out is None: out = np.zeros((CH, W, 3), np.float32)
        # heartbeat pulse
        pulse = max([math.exp(-((t - h) / 0.09) ** 2) + 0.6 * math.exp(-((t - h - 0.27) / 0.09) ** 2) for h in HB if abs(t - h) < 0.5] + [0.0])
        out = bloom(out, 165, 0.38 + 0.18 * pulse); out *= VIG * (1 + 0.06 * pulse)
        out = out * (1 - BOTTOM * 0.5)
        out += grain_rng.normal(0, 5.0, (CH, W, 1)).astype(np.float32)
        for c in CAPS: out = c.apply(out, t)
        if t > 57.2:
            k = smooth((t - 57.9) / 0.8) * 1.0
        # global fades
        g = smooth(t / 1.4) * smooth((DUR - t) / 0.9)
        out = out * g
        canvas = np.zeros((H, W, 3), np.uint8); canvas[Y0:Y0 + CH] = np.clip(out, 0, 255).astype(np.uint8)
        raw.stdin.write(canvas.tobytes())
        if n % 60 == 0: print("frame", n, f"t={t:.1f}", flush=True)
    raw.stdin.close(); raw.wait(); print("done", A.out)

main()
