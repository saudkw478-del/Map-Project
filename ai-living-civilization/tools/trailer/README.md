# مولّد التريلر (Trailer builder)

يحوّل تسجيل شاشة لعالمك إلى فيديو جاهز بنسختين (أفقي 16:9 وعمودي 9:16) مع عناوين عربية وموسيقى أصلية مولّدة بالكود.

## المتطلبات
- Python 3.11 مع: `pip install pillow numpy` (وPillow لازم يدعم raqm لشكل الحروف العربية)
- ffmpeg (أي نسخة فيها libx264 وlibfreetype)
- الخطوط (رخصة OFL من مستودع google/fonts): Reem Kufi، Tajawal-Bold، Tajawal-Medium، IBM Plex Mono Medium. حطها في مجلد واحد.

## التشغيل
```bash
python make_assets.py <مجلد_الخطوط> <مجلد_البناء>          # صور العناوين + الموسيقى
python build_video.py <مجلد_العمل> <مسار_ffmpeg>            # يقرا <مجلد_العمل>/vid_in/input.mp4
```
الأوقات مضبوطة على تسجيل مدته 29.4 ثانية (ساعة محاكاة لكل ثانية). عدّل `CAPS` في `build_video.py` والنصوص في `make_assets.py` لو غيرت التسجيل.
