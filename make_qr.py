#!/usr/bin/env python3
"""Bitez Dondurma — logolu QR + bastırılabilir masa kartı üretir."""
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.expanduser("~"), "bitez-qr")
os.makedirs(OUT, exist_ok=True)

URL   = "https://dagdelenbatu14-pixel.github.io/bitez-dondurma-link/"
NAVY  = (14, 42, 69)
BLUE  = (14, 114, 190)
ICE   = (237, 245, 252)
WHITE = (255, 255, 255)
INKSOFT = (90, 115, 136)

def font(path, size):
    return ImageFont.truetype(path, size)

F_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"
F_BLK  = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
F_SER  = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"

# ---------- 1) Logolu QR ----------
def make_qr(box=20, border=4):
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=box, border=border)
    qr.add_data(URL); qr.make(fit=True)
    img = qr.make_image(fill_color=NAVY, back_color=WHITE).convert("RGBA")
    W, H = img.size
    # logo merkez (beyaz yuvarlak zemin)
    logo = Image.open(os.path.join(ROOT, "images", "bitez-logo.png")).convert("RGBA")
    target = int(W * 0.22)
    lw = target
    lh = int(logo.height * target / logo.width)
    logo = logo.resize((lw, lh), Image.LANCZOS)
    pad = int(target * 0.18)
    plate = Image.new("RGBA", (lw + pad*2, lh + pad*2), (255,255,255,255))
    pd = ImageDraw.Draw(plate)
    # yuvarlak köşeli beyaz zemin
    plate2 = Image.new("RGBA", plate.size, (0,0,0,0))
    ImageDraw.Draw(plate2).rounded_rectangle([0,0,plate.size[0]-1,plate.size[1]-1],
                                             radius=int(pad*1.2), fill=(255,255,255,255))
    plate2.alpha_composite(logo, (pad, pad))
    px = (W - plate2.size[0])//2; py = (H - plate2.size[1])//2
    img.alpha_composite(plate2, (px, py))
    return img

qr_img = make_qr()
qr_img.save(os.path.join(OUT, "bitez-qr.png"))

# ---------- 2) Masa kartı (A6, 300dpi = 1240x1748) ----------
def card():
    W, H = 1240, 1748
    c = Image.new("RGB", (W, H), ICE)
    d = ImageDraw.Draw(c)
    # üst-alt mavi şerit
    d.rectangle([0,0,W,16], fill=BLUE)
    d.rectangle([0,H-16,W,H], fill=BLUE)
    # beyaz panel
    m = 70
    d.rounded_rectangle([m, m+30, W-m, H-m-30], radius=46, fill=WHITE)
    # logo
    logo = Image.open(os.path.join(ROOT, "images", "bitez-logo.png")).convert("RGBA")
    lw = 560; lh = int(logo.height*lw/logo.width); logo = logo.resize((lw,lh), Image.LANCZOS)
    c.paste(logo, ((W-lw)//2, m+90), logo)
    y = m + 90 + lh + 40
    # başlık
    f1 = font(F_SER, 78)
    t = "Menü & Değerlendirme"
    tw = d.textlength(t, font=f1); d.text(((W-tw)//2, y), t, font=f1, fill=NAVY); y += 110
    # alt başlık
    f2 = font(F_REG, 40)
    t2 = "Tüm lezzetler, fiyatlar ve fazlası"
    tw = d.textlength(t2, font=f2); d.text(((W-tw)//2, y), t2, font=f2, fill=INKSOFT); y += 90
    # QR
    q = qr_img.convert("RGB")
    qs = 720; q = q.resize((qs, qs), Image.NEAREST)
    qx = (W-qs)//2
    # ince çerçeve
    d.rounded_rectangle([qx-18, y-18, qx+qs+18, y+qs+18], radius=28, outline=(225,233,242), width=4)
    c.paste(q, (qx, y)); y += qs + 50
    # CTA
    f3 = font(F_BLK, 58)
    t3 = "Karekodu Okutun"
    tw = d.textlength(t3, font=f3); d.text(((W-tw)//2, y), t3, font=f3, fill=BLUE); y += 78
    f4 = font(F_REG, 36)
    t4 = "Scan to view our menu"
    tw = d.textlength(t4, font=f4); d.text(((W-tw)//2, y), t4, font=f4, fill=INKSOFT)
    return c

card_img = card()
card_img.save(os.path.join(OUT, "bitez-masa-karti.png"))
card_img.save(os.path.join(OUT, "bitez-masa-karti.pdf"), "PDF", resolution=300)
print("OK ->", OUT)
print(os.listdir(OUT))
