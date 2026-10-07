import subprocess, sys
SP, FF = sys.argv[1], sys.argv[2]
B, SRC, OUT = f"{SP}/vid_build", f"{SP}/vid_in/input.mp4", f"{SP}/vid_out"
D = 29.4
CAPS = [("title", 0.5, 3.6), ("c1", 3.6, 6.7), ("c2", 7.0, 10.3), ("c3", 10.6, 14.1), ("c4", 14.5, 17.7), ("c5", 18.0, 21.3), ("c6", 21.6, 24.7)]

def run(tag, W, H, vertical):
    args = [FF, "-hide_banner", "-loglevel", "error", "-y", "-i", SRC]
    n = 1
    idx = {}
    for name in ["grad", "tdim"] + [c[0] for c in CAPS] + ["dim", "end"]:
        args += ["-loop", "1", "-t", str(D), "-framerate", "30", "-i", f"{B}/{tag}_{name}.png"]; idx[name] = n; n += 1
    args += ["-framerate", "1", "-start_number", "0", "-i", f"{B}/{tag}_clk_%02d.png"]; idx["clk"] = n; n += 1
    args += ["-i", f"{B}/music.wav"]; idx["aud"] = n
    grade = "eq=contrast=1.08:saturation=1.16:gamma=0.98,unsharp=5:5:0.5:5:5:0.0"
    base = f"[0:v]trim=duration={D},setpts=PTS-STARTPTS,crop=1550:934:135:30"
    if not vertical:
        f = [base + f",scale=2100:-2:flags=lanczos,crop=1920:1080:x='(in_w-1920)/2+45*sin(t*0.33)':y='(in_h-1080)/2+22*sin(t*0.25+1)',{grade},vignette=PI/4.5,noise=alls=3:allf=t,format=yuv420p[b0]"]
    else:
        f = [base + ",split[a][b]",
             f"[a]scale=-2:1920:flags=lanczos,crop=1080:1920,gblur=sigma=26,eq=brightness=-0.13:saturation=1.1,format=yuv420p[bg]",
             f"[b]scale=1080:-2:flags=lanczos,{grade},vignette=PI/5,format=yuv420p[fg]",
             "[bg][fg]overlay=0:(H-h)/2-40,noise=alls=3:allf=t,format=yuv420p[b0]"]
    f.append(f"[b0]fade=t=in:st=0:d=0.8,fade=t=out:st={D-0.8}:d=0.8[b1]")
    cur = "b1"; k = 0
    f.append(f"[{cur}][{idx['grad']}:v]overlay=0:0[g0]"); cur = "g0"
    f.append(f"[{idx['tdim']}:v]format=rgba,fade=t=in:st=0:d=0.6:alpha=1,fade=t=out:st=3.0:d=0.9:alpha=1[td]")
    f.append(f"[{cur}][td]overlay=0:0:enable='lte(t,4)'[g1]"); cur = "g1"
    for name, s, e in CAPS:
        k += 1
        f.append(f"[{idx[name]}:v]format=rgba,fade=t=in:st={s}:d=0.5:alpha=1,fade=t=out:st={e-0.5}:d=0.5:alpha=1[o{k}]")
        f.append(f"[{cur}][o{k}]overlay=0:0:enable='between(t,{s},{e})'[x{k}]"); cur = f"x{k}"
    f.append(f"[{idx['clk']}:v]format=rgba,fade=t=out:st=24:d=0.8:alpha=1[clk]")
    f.append(f"[{cur}][clk]overlay=0:0:eof_action=pass[y0]"); cur = "y0"
    f.append(f"[{idx['dim']}:v]format=rgba,fade=t=in:st=24.9:d=1.0:alpha=1[dm]")
    f.append(f"[{cur}][dm]overlay=0:0:enable='gte(t,24.9)'[y1]")
    f.append(f"[{idx['end']}:v]format=rgba,fade=t=in:st=25.4:d=0.8:alpha=1,fade=t=out:st={D-0.9}:d=0.7:alpha=1[en]")
    f.append(f"[y1][en]overlay=0:0:enable='gte(t,25.4)',format=yuv420p[vout]")
    f.append(f"[{idx['aud']}:a]volume=0.8,afade=t=in:st=0:d=0.5,afade=t=out:st={D-2.4}:d=2.4[aout]")
    with open(f"{SP}/vid_build/{tag}_graph.txt", "w") as fh: fh.write(";\n".join(f))
    out = f"{OUT}/trailer_{tag}.mp4"
    args += ["-filter_complex_script", f"{SP}/vid_build/{tag}_graph.txt", "-map", "[vout]", "-map", "[aout]", "-t", str(D), "-r", "30",
             "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out]
    r = subprocess.run(args, capture_output=True, text=True)
    print(tag, "rc", r.returncode, r.stderr[-1500:])

run("h", 1920, 1080, False)
run("v", 1080, 1920, True)
