"""Generates caption overlays (PNG) and the soundtrack (WAV) for the trailer. Original synthesis, no external samples."""
import math, os, sys, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

A = sys.argv[1]      # assets dir (fonts)
O = sys.argv[2]      # output build dir
os.makedirs(O, exist_ok=True)

def font(name, size, wght=None):
    f = ImageFont.truetype(os.path.join(A, name), size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f
KUFI, TAJ, TAJM, MONO = "ReemKufi[wght].ttf", "Tajawal-Bold.ttf", "Tajawal-Medium.ttf", "IBMPlexMono-Medium.ttf"

def draw_line(img, text, fnt, cx, cy, fill=(255, 255, 255, 255), shadow=True, latin=False, spacing=0):
    """Arabic is drawn by Pillow's raqm engine (shaping + RTL), so we pass the raw logical string."""
    d = ImageDraw.Draw(img)
    kw = {} if latin else {"direction": "rtl", "language": "ar"}
    if latin and spacing:
        w = sum(d.textlength(c, font=fnt) for c in text) + spacing * (len(text) - 1)
        def put(dr, dy, col):
            x = cx - w / 2
            for c in text: dr.text((x, cy + dy), c, font=fnt, fill=col); x += dr.textlength(c, font=fnt) + spacing
    else:
        def put(dr, dy, col): dr.text((cx, cy + dy), text, font=fnt, fill=col, anchor="ma", **kw)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); put(ImageDraw.Draw(sh), 4, (0, 0, 0, 230))
        sh = sh.filter(ImageFilter.GaussianBlur(9)); img.alpha_composite(sh)
    put(ImageDraw.Draw(img), 0, fill)

def layer(W, H): return Image.new("RGBA", (W, H), (0, 0, 0, 0))

def build(tag, W, H, k):
    """k = scale factor relative to 1080p-wide layout; positions differ per format."""
    vertical = H > W
    cap_y = int(H * (0.72 if vertical else 0.80))
    big, mid, small = int(86 * k), int(64 * k), int(40 * k)
    # bottom gradient (legibility)
    g = np.zeros((H, W, 4), dtype=np.uint8); h0 = int(H * (0.55 if vertical else 0.62))
    ramp = np.clip((np.arange(H) - h0) / (H - h0), 0, 1) ** 1.6 * 175
    g[:, :, 3] = ramp[:, None].astype(np.uint8)
    Image.fromarray(g, "RGBA").save(f"{O}/{tag}_grad.png")
    # captions: (id, lines, font, size)
    caps = [
        ("c1", ["عالم صغير… وشخصان فقط."], TAJ, mid),
        ("c2", ["خالد ونورة…", "لا أحد أخبرهما من صنعهما."], TAJ, mid),
        ("c3", ["يوم كامل… في أربع وعشرين ثانية."], TAJ, mid),
        ("c4", ["ثم يأتي الليل…"], TAJ, big),
        ("c5", ["ويتذكران أشياء", "لم يعيشاها."], TAJ, mid),
        ("c6", ["هل يوجد أحد مثلنا؟"], KUFI, int(big * 1.25)),
    ]
    for cid, lines, fn, sz in caps:
        im = layer(W, H); fnt = font(fn, sz, 700 if fn == KUFI else None)
        n = len(lines); y = cap_y - (n - 1) * int(sz * 0.62)
        for i, ln in enumerate(lines): draw_line(im, ln, fnt, W // 2, y + i * int(sz * 1.25))
        im.save(f"{O}/{tag}_{cid}.png")
    # title card
    im = layer(W, H); ty = int(H * (0.40 if vertical else 0.36))
    draw_line(im, "مدينة الذكاء الاصطناعي الحية", font(KUFI, int(112 * k * (0.78 if vertical else 1)), 700), W // 2, ty, fill=(255, 244, 214, 255))
    ImageDraw.Draw(im).rectangle([W // 2 - int(150 * k), ty + int(190 * k), W // 2 + int(150 * k), ty + int(193 * k)], fill=(227, 166, 64, 255))
    draw_line(im, "AI LIVING CIVILIZATION", font(MONO, int(34 * k), None), W // 2, ty + int(215 * k), fill=(230, 230, 230, 255), latin=True, spacing=int(10 * k))
    im.save(f"{O}/{tag}_title.png")
    # end card
    dim = Image.new("RGBA", (W, H), (4, 8, 14, 168)); dim.save(f"{O}/{tag}_dim.png")
    Image.new("RGBA", (W, H), (3, 6, 10, 120)).save(f"{O}/{tag}_tdim.png")
    im = layer(W, H); ey = int(H * (0.36 if vertical else 0.34))
    draw_line(im, "كل ما تراه", font(KUFI, int(108 * k), 700), W // 2, ey, fill=(255, 244, 214, 255))
    draw_line(im, "يحدث من تلقاء نفسه.", font(KUFI, int(108 * k), 700), W // 2, ey + int(140 * k), fill=(255, 244, 214, 255))
    ImageDraw.Draw(im).rectangle([W // 2 - int(110 * k), ey + int(330 * k), W // 2 + int(110 * k), ey + int(333 * k)], fill=(227, 166, 64, 255))
    draw_line(im, "شخصيات ذكاء اصطناعي · بدون سكربت", font(TAJM, int(44 * k), None), W // 2, ey + int(362 * k), fill=(235, 235, 235, 255))
    draw_line(im, "مدينة الذكاء الاصطناعي الحية", font(TAJM, int(36 * k), None), W // 2, ey + int(440 * k), fill=(227, 166, 64, 255))
    im.save(f"{O}/{tag}_end.png")
    # clock sequence (one frame per world second = 1 simulated hour)
    cx = int(W * (0.5 if vertical else 0.0)) if vertical else 0
    for i in range(25):
        hh = 5.5 + i; day = 33 if hh < 24 else 34; hh %= 24
        t = f"{int(hh):02d}:{int((hh - int(hh)) * 60):02d}"
        im = layer(W, H)
        px = int(70 * k) if not vertical else int(60 * k); py = int(48 * k) if not vertical else int(70 * k)
        panel = Image.new("RGBA", (int(300 * k), int(118 * k)), (6, 12, 18, 120)); mask = Image.new("L", panel.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, panel.size[0] - 1, panel.size[1] - 1], radius=int(18 * k), fill=255)
        im.paste(panel, (px, py), mask)
        draw_line(im, t, font(MONO, int(60 * k), None), px + int(150 * k), py + int(8 * k), shadow=False, latin=True, fill=(255, 244, 214, 255))
        dn = str(day).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))
        draw_line(im, f"اليوم {dn} · الشتاء", font(TAJM, int(26 * k), None), px + int(150 * k), py + int(76 * k), shadow=False, fill=(220, 220, 220, 255))
        im.save(f"{O}/{tag}_clk_{i:02d}.png")

build("h", 1920, 1080, 1.0)
build("v", 1080, 1920, 0.80)

# ---------------- soundtrack ----------------
SR, DUR = 48000, 29.4
N = int(SR * DUR); t = np.arange(N) / SR
rng = np.random.default_rng(7)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def smooth(x): return x * x * (3 - 2 * x)
def env(t0, t1, a, r):
    e = np.zeros(N); i0, i1 = int(t0 * SR), min(N, int(t1 * SR))
    tt = (np.arange(i0, i1) / SR)
    e[i0:i1] = smooth(np.clip((tt - t0) / a, 0, 1)) * smooth(np.clip((t1 - tt) / r, 0, 1))
    return e
def pad(f, e, detune=0.004, harm=7, pan=0.0):
    L = np.zeros(N); R = np.zeros(N)
    for d in (-detune, 0, detune):
        for h in range(1, harm + 1):
            w = np.sin(2 * np.pi * f * (1 + d) * h * t + rng.uniform(0, 6.28)) / h ** 1.3
            L += w * (0.5 - pan / 2 * 0); R += w * (0.5 + pan * 0)
    return L * e, R * e
mixL = np.zeros(N); mixR = np.zeros(N)
chords = [(57, 60, 64), (53, 57, 60), (60, 64, 67), (55, 59, 62)]  # Am F C G (midi)
seg = DUR / 4
for ci, ch in enumerate(chords):
    t0, t1 = ci * seg - 1.2, (ci + 1) * seg + 1.2
    e = env(max(0, t0), min(DUR, t1), 1.6, 1.8)
    for nn in ch:
        l, r = pad(hz(nn), e); mixL += l * 0.055; mixR += r * 0.055
    sub = np.sin(2 * np.pi * hz(ch[0] - 24) * t) * env(max(0, t0), min(DUR, t1), 1.0, 1.4) * 0.22
    mixL += sub; mixR += sub
# dark swell into the question, then hush
hush = np.ones(N); hush[int(21.0 * SR):int(21.6 * SR)] = np.linspace(1, 0.25, int(0.6 * SR)); hush[int(21.6 * SR):int(24.8 * SR)] = 0.45
for a, b in ((int(24.8 * SR), int(25.8 * SR)),):
    hush[a:b] = np.linspace(0.45, 1.0, b - a); hush[b:] = 1.0
mixL *= hush; mixR *= hush
# bell arpeggio (pentatonic), from the first caption
pent = [69, 72, 74, 76, 79, 81]
def bell(t0, m, vel=0.12, ln=2.8):
    i0 = int(t0 * SR); i1 = min(N, i0 + int(ln * SR))
    if i0 >= N: return
    tt = np.arange(i1 - i0) / SR; f = hz(m)
    w = (np.sin(2 * np.pi * f * tt) + 0.5 * np.sin(2 * np.pi * f * 2.76 * tt) * np.exp(-tt * 4) + 0.3 * np.sin(2 * np.pi * f * 5.4 * tt) * np.exp(-tt * 9)) * np.exp(-tt * 1.7)
    pan = rng.uniform(0.3, 0.7); mixL[i0:i1] += w * vel * (1 - pan); mixR[i0:i1] += w * vel * pan
k = 0
for tb in np.arange(3.2, 20.6, 0.9):
    bell(tb, pent[(k * 2 + (k // 3)) % len(pent)] - (12 if 14.4 < tb < 20.6 else 0), vel=0.10 if tb < 14 else 0.07); k += 1
bell(21.7, 76, vel=0.26, ln=5.0); bell(21.72, 83, vel=0.12, ln=5.0)    # the question
for j, m in enumerate((72, 76, 79, 84, 88)): bell(25.3 + j * 0.34, m, vel=0.14, ln=3.2)  # resolution
# heartbeat
def thump(t0, amp):
    i0 = int(t0 * SR); n = int(0.28 * SR)
    if i0 + n >= N: return
    tt = np.arange(n) / SR; f = 62 * np.exp(-tt * 9) + 38
    w = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 13) * amp
    mixL[i0:i0 + n] += w; mixR[i0:i0 + n] += w
for tb in np.arange(14.6, 20.9, 0.95): thump(tb, 0.40); thump(tb + 0.27, 0.24)
# riser (filtered noise)
n0, n1 = int(18.8 * SR), int(21.0 * SR); nz = rng.normal(0, 1, n1 - n0)
nz = np.cumsum(nz) * 0.0; nz = rng.normal(0, 1, n1 - n0)
ramp = np.linspace(0, 1, n1 - n0) ** 2.2
hp = nz - np.convolve(nz, np.ones(24) / 24, mode="same")
mixL[n0:n1] += hp * ramp * 0.07; mixR[n0:n1] += np.roll(hp, 31) * ramp * 0.07
# title boom
tb0 = int(0.7 * SR); nb = int(2.4 * SR); tt = np.arange(nb) / SR
boom = np.sin(2 * np.pi * (48 * np.exp(-tt * 1.4) + 30) * tt) * np.exp(-tt * 1.3) * 0.5
mixL[tb0:tb0 + nb] += boom; mixR[tb0:tb0 + nb] += boom
# reverb
irn = int(2.4 * SR); irt = np.arange(irn) / SR
def ir(seed): return np.random.default_rng(seed).normal(0, 1, irn) * np.exp(-irt * 2.1)
def conv(x, h):
    n = 1 << int(np.ceil(np.log2(len(x) + len(h)))); return np.fft.irfft(np.fft.rfft(x, n) * np.fft.rfft(h, n), n)[:len(x)]
wetL, wetR = conv(mixL, ir(1)), conv(mixR, ir(2))
sc = 0.0035
L = mixL * 0.72 + wetL * sc * 0.9; R = mixR * 0.72 + wetR * sc * 0.9
fin = np.minimum(1, t / 1.2) * np.minimum(1, (DUR - t) / 2.6)
L *= fin; R *= fin
pk = max(np.abs(L).max(), np.abs(R).max()); g = 0.89 / pk; L *= g; R *= g
st = np.stack([L, R], 1)
with wave.open(f"{O}/music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype("<i2").tobytes())
rms = 20 * np.log10(np.sqrt(np.mean(st ** 2)) + 1e-9)
print(f"music ok: peak -1dB, rms {rms:.1f} dBFS")
