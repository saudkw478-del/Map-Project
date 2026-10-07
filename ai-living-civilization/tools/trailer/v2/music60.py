import numpy as np, wave, sys
SR=44100; N=SR*60; rng=np.random.default_rng(7)
out=np.zeros((N,2))
def add(sig,t,pan=0.0,g=1.0):
    i=int(t*SR); 
    if i>=N: return
    s=sig[:N-i]; out[i:i+len(s),0]+=s*g*(1-pan)/1; out[i:i+len(s),1]+=s*g*(1+pan)/1
def tt(d): return np.arange(int(d*SR))/SR
def lp(x,a):
    y=np.empty_like(x); c=0
    for i in range(len(x)): c+=a*(x[i]-c); y[i]=c
    return y
def lpf(x,fc):
    # fast one-pole via cumulative using scipy-less FFT
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X/= (1+(f/fc)**2); return np.fft.irfft(X,len(x))
def bell(f,d=4.0):
    t=tt(d); s=sum(a*np.sin(2*np.pi*f*r*t+ph)*np.exp(-t*dk) for a,r,dk,ph in [(1,1,0.9,0),(.5,2.76,1.6,1),(.3,5.4,2.4,2),(.2,8.9,3.5,3)])
    return s*(1-np.exp(-t*80))*0.3
def pad(freqs,d,fa=1.5):
    t=tt(d); s=0
    for f in freqs:
        for dt in (-0.4,0,0.5): s=s+np.sin(2*np.pi*(f+dt)*t+rng.uniform(0,6))
    env=np.minimum(1,t/fa)*np.minimum(1,(d-t)/fa)
    return lpf(s,900)*env*0.05
def kick(d=0.5,f0=120,f1=40):
    t=tt(d); ph=2*np.pi*(f1*t+(f0-f1)*(1-np.exp(-t*25))/25)
    return np.sin(ph)*np.exp(-t*7)*0.9
def hb(): 
    t=tt(0.4); return np.sin(2*np.pi*55*t)*np.exp(-t*14)*0.9
def noise(d): return rng.standard_normal(int(d*SR))
def hat(): t=tt(0.08); n=noise(0.08); n=n-lpf(n,5000); return n*np.exp(-t*50)*0.12
def riser(a,b,d):
    t=tt(d); n=noise(d); f=np.linspace(a,b,len(t)); 
    x=np.sin(2*np.pi*np.cumsum(f)/SR)*0.5+n*0.3
    return x*(t/d)**2*0.25
def boom(d=4.0):
    t=tt(d); s=np.sin(2*np.pi*(38+60*np.exp(-t*6))*t)*np.exp(-t*1.1)
    n=lpf(noise(d),1500)*np.exp(-t*2)*0.6
    return (s*0.9+n)*0.9
# wind/drone 0-60
w=lpf(noise(60),400)*0.25
w*= (0.5+0.5*np.sin(np.arange(N)/SR*0.25))*0.8+0.2
add(w,0,0,1.0)
# drone
drone=pad([55,82.4,110],60,4); add(drone*2.2,0)
# bell motif
notes=[329.6,392,440,392,329.6,293.7]
for i,tm in enumerate([5.0,7.0,9.0,11.0]): add(bell(notes[i%6]),tm,(-1)**i*0.4)
# pads
add(pad([220,261.6,329.6],7),10,0,1.8)
add(pad([196,246.9,293.7],8),17,0,1.8)
# arpeggio 11-17
arp=[220,261.6,329.6,392,329.6,261.6]
t=11.0;i=0
while t<17: add(bell(arp[i%6]*2,1.5)*0.5,t,np.sin(i)*0.5); t+=0.5;i+=1
# ticks 17.6-23.2
t=17.6; 
while t<23.2:
    tk=tt(0.05); add(np.sin(2*np.pi*1800*tk)*np.exp(-tk*90)*0.25,t); t+=0.4 if t<20.4 else 0.2
add(riser(200,2000,5.6),17.6)
# heartbeat
HB=list(np.arange(23.4,37.0,1.0))+list(np.arange(37.0,43.6,0.7))
for h in HB: add(hb(),h,0,1.0); add(hb(),h+0.27,0,0.6)
# pulse chords
for k,tm in enumerate(np.arange(30,37,1.0)): add(pad([110,164.8,220] if k%2==0 else [98,146.8,196],1.2,0.1),tm,0,2.0)
# kick/hat build
t=37.0
while t<43.6: add(kick(),t,0,0.5+ (t-37)/6.6*0.5); t+=0.7
t=38.0
while t<43.6: add(hat(),t,0.3); t+=0.35
add(riser(300,3500,3.6),40.0)
# silent drop 43.6-44.0: duck
out[int(43.55*SR):int(44.0*SR)]*=0.02
add(boom(5.0),44.0,0,1.3)
# glitch hits
for tm in [44.0,44.9,45.4,46.2,47.0]: 
    n=tt(0.12); add(noise(0.12)*np.exp(-n*25)*0.5,tm)
for i,tm in enumerate(np.arange(44.0,52.0,0.7)): add(kick(),tm,0,0.7)
add(pad([110,138.6,164.8,220],8,0.3),44,0,2.2)
# quiet 52-57
out[int(52*SR):int(57.0*SR)]*=0.6
for i,tm in enumerate([52.5,54.0,55.5]): add(bell([392,440,329.6][i],5),tm,0,1.2)
add(pad([164.8,196,246.9],6,1.5),52,0,2.0)
# final boom
add(boom(3.0),57.3,0,1.6); add(bell(329.6,3.0)*1.5,57.3)
# reverb tail: simple feedback delays
for dly,g in [(0.23,.35),(0.37,.28),(0.53,.2)]:
    d=int(dly*SR); y=out.copy()
    for k in range(1,4): y[d*k:]+=out[:-d*k]*(g**k)
    out=y*0.9+out*0.1
# fades, normalize
f=np.ones(N); f[:int(1.5*SR)]=np.linspace(0,1,int(1.5*SR)); f[-int(1.2*SR):]=np.linspace(1,0,int(1.2*SR)); out*=f[:,None]
out/=np.abs(out).max()/0.92
with wave.open(sys.argv[1],'wb') as wf:
    wf.setnchannels(2); wf.setsampwidth(2); wf.setframerate(SR); wf.writeframes((out*32767).astype('<i2').tobytes())
print("ok")
