#!/usr/bin/env python3
"""
MedRouteIndia Explainer Video Generator v3
- Frame-by-frame animations (slide-in, fade-in, counters, progress bars)
- Properly synced voiceover per scene (accounts for crossfade overlap)
- Fixed pronunciation: "Med Route India" in VO text
- Ambient background music
"""

import asyncio, os, math, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoClip, ImageClip, CompositeVideoClip, concatenate_videoclips,
    AudioFileClip, CompositeAudioClip, vfx, afx,
)
import edge_tts

# ── Config ────────────────────────────────────────────────────────────
W, H       = 1920, 1080
FPS        = 30
XFADE      = 0.7
VOICE      = "en-US-AndrewNeural"

NAVY       = (10, 22, 40)
TEAL       = (0, 201, 167)
GOLD       = (201, 168, 76)
WHITE      = (255, 255, 255)
DARK       = (6, 14, 28)
LGRAY      = (180, 190, 200)

BASE       = os.path.dirname(os.path.abspath(__file__))
VO_DIR     = os.path.join(BASE, "_vo_parts")
OUT        = os.path.join(BASE, "MedRouteIndia_Explainer_Video.mp4")

FONT_REG   = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_BOLD  = "/System/Library/Fonts/Avenir Next.ttc"
FONT_LITE  = "/System/Library/Fonts/Avenir.ttc"


def fnt(sz, bold=False, light=False):
    p = FONT_BOLD if bold else (FONT_LITE if light else FONT_REG)
    return ImageFont.truetype(p, sz)


# ── Easing & animation helpers ────────────────────────────────────────

def ease_out_cubic(t):
    return 1 - (1 - t) ** 3

def ease_in_out(t):
    return 3 * t * t - 2 * t * t * t

def anim(t, start, dur, ease=ease_out_cubic):
    if t < start:
        return 0.0
    if t >= start + dur:
        return 1.0
    return ease((t - start) / dur)

def lerp(a, b, p):
    return a + (b - a) * p

def clamp(v, lo=0, hi=1):
    return max(lo, min(hi, v))


# ── Drawing helpers ───────────────────────────────────────────────────

def gradient_img(c1, c2, w=W, h=H):
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    return img


_glow_cache = {}
def radial_glow(img, cx, cy, radius, color, alpha=60):
    key = (id(img), cx, cy, radius, color, alpha)
    if key in _glow_cache:
        return _glow_cache[key]
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for r in range(radius, 0, -4):
        a = int(alpha * (r / radius) ** 0.5)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    img_rgba = img.convert("RGBA")
    result = Image.alpha_composite(img_rgba, overlay).convert("RGB")
    _glow_cache[key] = result
    return result


_bg_cache = {}
def get_bg(key, c1, c2, glows=None, particles_seed=None):
    if key in _bg_cache:
        return _bg_cache[key].copy()
    bg = gradient_img(c1, c2)
    if glows:
        for cx, cy, radius, color, alpha in glows:
            bg = radial_glow(bg, cx, cy, radius, color, alpha)
    if particles_seed is not None:
        rng = np.random.RandomState(particles_seed)
        draw = ImageDraw.Draw(bg)
        for _ in range(45):
            x, y = rng.randint(0, W), rng.randint(0, H)
            r = rng.randint(1, 4)
            draw.ellipse([x-r, y-r, x+r, y+r], fill=TEAL if rng.rand() > 0.5 else GOLD)
    _bg_cache[key] = bg
    return bg.copy()


def rrect(draw, xy, r, fill=None, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def text_w(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]


def centered_text(draw, y, text, f, fill=WHITE):
    tw = text_w(draw, text, f)
    draw.text(((W - tw) // 2, y), text, font=f, fill=fill)


def accent_bar(draw, cx, y, w, color=GOLD, h=4):
    draw.rectangle([cx - w // 2, y, cx + w // 2, y + h], fill=color)


def circle_filled(draw, cx, cy, r, fill):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)


# ── TTS ───────────────────────────────────────────────────────────────

async def _tts(text, path):
    comm = edge_tts.Communicate(text, VOICE, rate="-5%", pitch="+0Hz")
    await comm.save(path)

def gen_vo(text, fname):
    path = os.path.join(VO_DIR, fname)
    if not os.path.exists(path):
        asyncio.run(_tts(text, path))
    return path


# ── Background music ─────────────────────────────────────────────────

def gen_bgm(dur, path, sr=44100):
    t = np.linspace(0, dur, int(sr * dur), endpoint=False)
    freqs = [110, 164.81, 220, 329.63]
    sig = np.zeros_like(t)
    for i, f in enumerate(freqs):
        env = 0.15 * (1 + 0.3 * np.sin(2 * np.pi * 0.05 * (i + 1) * t))
        sig += env * np.sin(2 * np.pi * f * t)
    sig *= 0.08
    fade_s = int(sr * 3)
    sig[:fade_s] *= np.linspace(0, 1, fade_s)
    sig[-fade_s:] *= np.linspace(1, 0, fade_s)
    sig = np.clip(sig, -1, 1)
    samples = (sig * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return path


# ══════════════════════════════════════════════════════════════════════
#  ANIMATED SCENES  — each returns a moviepy clip
# ══════════════════════════════════════════════════════════════════════

SCENE_LIST = []

def register(name, dur, vo_text):
    def decorator(func):
        SCENE_LIST.append((name, dur, vo_text, func))
        return func
    return decorator


# ── Scene 1: Hook (questions fade in/out) ─────────────────────────────

@register("Hook", 16, (
    "Is the health condition of a loved one troubling you? "
    "Is medical treatment in your country too expensive? "
    "Are you stuck on a waiting list while time runs out? "
    "Or are you simply looking for world-class treatment at an affordable price?"
))
def scene_hook():
    bg = get_bg("hook", NAVY, DARK,
                glows=[(W//2, H//2, 500, TEAL, 25)], particles_seed=10)

    questions = [
        "Is the health condition of a\nloved one troubling you?",
        "Is medical treatment in your\ncountry too expensive?",
        "Are you stuck on a waiting list\nwhile time runs out?",
        "Looking for world-class treatment\nat an affordable price?",
    ]
    q_dur = 4.0

    def make_frame(t):
        frame = bg.copy()
        draw = ImageDraw.Draw(frame)
        qi = min(int(t / q_dur), len(questions) - 1)
        local_t = t - qi * q_dur

        fade = clamp(local_t / 0.6) * (1.0 - clamp((local_t - 3.2) / 0.6))
        slide_y = int(lerp(40, 0, clamp(local_t / 0.8, 0, 1)))

        bar_w = int(100 * clamp(local_t / 0.5))
        accent_bar(draw, W // 2, H // 2 - 120 + slide_y, bar_w, GOLD)

        alpha = int(255 * fade)
        txt_overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        td = ImageDraw.Draw(txt_overlay)
        lines = questions[qi].split("\n")
        y = H // 2 - 70 + slide_y
        for line in lines:
            tw = text_w(td, line, fnt(54, bold=True))
            td.text(((W - tw) // 2, y), line, font=fnt(54, bold=True),
                    fill=(*WHITE, alpha))
            y += 70

        frame_rgba = frame.convert("RGBA")
        frame = Image.alpha_composite(frame_rgba, txt_overlay).convert("RGB")

        draw2 = ImageDraw.Draw(frame)
        centered_text(draw2, H - 70, "MedRouteIndia", fnt(22, light=True), LGRAY)
        return np.array(frame)

    return VideoClip(make_frame, duration=16).with_fps(FPS)


# ── Scene 2: Brand Reveal (scale + slide) ─────────────────────────────

@register("Brand Reveal", 8, (
    "Meet Med Route India. Your bridge to world-class healthcare in India. "
    "We make medical tourism hassle-free, safe, and affordable."
))
def scene_brand_reveal():
    bg = get_bg("brand", (0, 60, 80), NAVY,
                glows=[(W//2, H//2 - 50, 600, TEAL, 30)], particles_seed=100)

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_logo = anim(t, 0.3, 1.0)
        logo_alpha = int(255 * p_logo)
        logo_y = int(lerp(H // 2 - 100, H // 2 - 130, p_logo))
        f_logo = fnt(120, bold=True)
        tw = text_w(d, "MedRouteIndia", f_logo)
        d.text(((W - tw) // 2, logo_y), "MedRouteIndia", font=f_logo,
               fill=(*WHITE, logo_alpha))

        p_bar = anim(t, 1.2, 0.6)
        bar_w = int(180 * p_bar)
        if bar_w > 0:
            bar_y = H // 2 + 10
            d.rectangle([W // 2 - bar_w // 2, bar_y,
                         W // 2 + bar_w // 2, bar_y + 4], fill=(*GOLD, 255))

        p_tag = anim(t, 1.8, 0.8)
        tag_alpha = int(255 * p_tag)
        tag_y = int(lerp(H // 2 + 60, H // 2 + 40, p_tag))
        f_tag = fnt(38, light=True)
        tag = "Your Bridge to World-Class Healthcare in India"
        ttw = text_w(d, tag, f_tag)
        d.text(((W - ttw) // 2, tag_y), tag, font=f_tag,
               fill=(*TEAL, tag_alpha))

        p_sub = anim(t, 2.8, 0.6)
        sub_alpha = int(255 * p_sub)
        f_sub = fnt(28, light=True)
        sub = "Hassle-Free  •  Safe  •  Affordable"
        stw = text_w(d, sub, f_sub)
        d.text(((W - stw) // 2, H // 2 + 110), sub, font=f_sub,
               fill=(*LGRAY, sub_alpha))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=8).with_fps(FPS)


# ── Scene 3: Stats (counter animation + card slide-up) ────────────────

@register("Stats", 10, (
    "Over 500 patients treated. More than 50 partner hospitals. "
    "Patients save up to 90 percent compared to treatment costs back home."
))
def scene_stats():
    bg = get_bg("stats", DARK, NAVY,
                glows=[(W//2, 400, 400, TEAL, 20)], particles_seed=200)

    data = [("500+", "Patients Treated", TEAL, 500),
            ("50+", "Partner Hospitals", GOLD, 50),
            ("90%", "Cost Savings", TEAL, 90)]
    cw, ch = 460, 280
    gap = 60
    x0 = (W - 3 * cw - 2 * gap) // 2
    cy_final = H // 2 - 70

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        title_alpha = int(255 * p_title)
        f_title = fnt(50, bold=True)
        title = "Trusted by Patients Worldwide"
        ttw = text_w(d, title, f_title)
        d.text(((W - ttw) // 2, 100), title, font=f_title,
               fill=(*WHITE, title_alpha))

        bar_p = anim(t, 0.6, 0.4)
        if bar_p > 0:
            bw = int(120 * bar_p)
            d.rectangle([W//2 - bw//2, 175, W//2 + bw//2, 179],
                        fill=(*TEAL, 255))

        for i, (label, subtitle, acc, max_val) in enumerate(data):
            card_p = anim(t, 1.0 + i * 0.4, 0.8)
            count_p = anim(t, 1.5 + i * 0.4, 1.5)
            alpha = int(255 * card_p)
            slide_y = int(lerp(60, 0, card_p))

            cx = x0 + i * (cw + gap)
            cy = cy_final + slide_y

            d.rounded_rectangle((cx, cy, cx + cw, cy + ch), radius=20,
                                fill=(*((18, 32, 55)), alpha),
                                outline=(*acc, alpha), width=2)

            bw2 = int(70 * card_p)
            if bw2 > 0:
                d.rectangle([cx + cw//2 - bw2//2, cy + 30,
                             cx + cw//2 + bw2//2, cy + 33],
                            fill=(*acc, alpha))

            current = int(max_val * count_p)
            if "%" in label:
                num_str = f"Up to {current}%"
            else:
                num_str = f"{current}+"
            f_num = fnt(68, bold=True)
            nw = text_w(d, num_str, f_num)
            d.text((cx + (cw - nw) // 2, cy + 60), num_str, font=f_num,
                   fill=(*WHITE, alpha))

            f_lbl = fnt(24, light=True)
            lw = text_w(d, subtitle, f_lbl)
            d.text((cx + (cw - lw) // 2, cy + 170), subtitle, font=f_lbl,
                   fill=(*LGRAY, alpha))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=10).with_fps(FPS)


# ── Scene 4: Meet Your Doctor (cards appear one by one) ───────────────

@register("Meet Your Doctor", 18, (
    "Introducing the Meet Your Doctor package for just 150 dollars. "
    "Our representative physically visits the doctor of your choice in India "
    "with your prepared case study. You join via video call, get a second opinion, "
    "understand the full procedure, and receive a complete arrival to departure plan."
))
def scene_meet_doctor():
    bg = get_bg("myd", NAVY, (15, 30, 50),
                glows=[(W//2, 200, 400, GOLD, 25)], particles_seed=300)

    benefits = [
        ("1", "Our Rep Visits\nthe Doctor\nPhysically", TEAL),
        ("2", "Your Case Study\nPresented\nIn Person", GOLD),
        ("3", "Live Video Call\nWith Your\nDoctor", TEAL),
        ("4", "Complete Arrival-\nto-Departure\nPlan", GOLD),
    ]
    cw_card, ch_card = 390, 240
    gap = 35
    x0 = (W - 4 * cw_card - 3 * gap) // 2
    cy_cards = 270

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        a = int(255 * p_title)
        f_t = fnt(54, bold=True)
        title = "Meet Your Doctor Package"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 60), title, font=f_t, fill=(*WHITE, a))

        p_bar = anim(t, 0.6, 0.4)
        if p_bar > 0:
            bw = int(100 * p_bar)
            d.rectangle([W//2 - bw//2, 138, W//2 + bw//2, 142],
                        fill=(*GOLD, 255))

        p_badge = anim(t, 1.0, 0.6)
        badge_alpha = int(255 * p_badge)
        scale = 0.8 + 0.2 * p_badge
        pulse = 1.0 + 0.03 * math.sin(t * 3)
        badge_w = int(200 * scale * pulse)
        badge_h = int(60 * scale * pulse)
        bx = (W - badge_w) // 2
        by = 170
        d.rounded_rectangle((bx, by, bx + badge_w, by + badge_h), radius=30,
                            fill=(*GOLD, badge_alpha))
        f_price = fnt(38, bold=True)
        pw = text_w(d, "$150", f_price)
        d.text((bx + (badge_w - pw) // 2, by + 8), "$150", font=f_price,
               fill=(*DARK, badge_alpha))

        for i, (num, txt, acc) in enumerate(benefits):
            p = anim(t, 2.0 + i * 0.8, 0.7)
            alpha = int(255 * p)
            slide_x = int(lerp(-80, 0, p))

            cx = x0 + i * (cw_card + gap) + slide_x
            cy = cy_cards
            d.rounded_rectangle((cx, cy, cx + cw_card, cy + ch_card), radius=16,
                                fill=(14, 26, 48, alpha), outline=(*acc, alpha), width=2)

            circle_r = int(22 * p)
            if circle_r > 2:
                d.ellipse([cx + cw_card // 2 - circle_r, cy + 38 - circle_r,
                           cx + cw_card // 2 + circle_r, cy + 38 + circle_r],
                          fill=(*acc, alpha))
                f_n = fnt(24, bold=True)
                nw = text_w(d, num, f_n)
                d.text((cx + cw_card // 2 - nw // 2, cy + 24), num, font=f_n,
                       fill=(*DARK, alpha))

            lines = txt.split("\n")
            ly = cy + 80
            for line in lines:
                f_l = fnt(23)
                lw = text_w(d, line, f_l)
                d.text((cx + (cw_card - lw) // 2, ly), line, font=f_l,
                       fill=(*WHITE, alpha))
                ly += 34

        p_footer = anim(t, 5.5, 0.6)
        fa = int(255 * p_footer)
        f_foot = fnt(26, light=True)
        foot = "Everything starts from what the doctor recommends."
        fw = text_w(d, foot, f_foot)
        d.text(((W - fw) // 2, H - 170), foot, font=f_foot,
               fill=(*LGRAY, fa))

        f_cities = fnt(22, light=True)
        cities = "Delhi  •  Jaipur  •  Mumbai  •  Bangalore  •  Kolkata  •  Chennai"
        cw2 = text_w(d, cities, f_cities)
        d.text(((W - cw2) // 2, H - 120), cities, font=f_cities,
               fill=(*TEAL, fa))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=18).with_fps(FPS)


# ── Scene 5: Services (cards slide from alternating sides) ────────────

@register("Services", 16, (
    "Med Route India handles everything. From visa assistance and flight bookings "
    "to premium hotel accommodation, daily transport, and a personal companion "
    "who speaks your language. After your treatment, we stay connected with "
    "post-treatment follow-up care."
))
def scene_services():
    bg = get_bg("services", (0, 40, 60), NAVY,
                glows=[(W//2, 500, 500, TEAL, 18)], particles_seed=400)

    svcs = [
        ("Visa Assistance &\nDocumentation", TEAL),
        ("Flight Booking\nEconomy to Business", GOLD),
        ("Hotel &\nAccommodation", TEAL),
        ("Daily Transport\n& Transfers", GOLD),
        ("Personal Companion\n& Interpreter", TEAL),
        ("Post-Treatment\nFollow-Up Care", GOLD),
    ]
    cw_s, ch_s = 550, 155
    gx, gy = 45, 25
    x0 = (W - 3 * cw_s - 2 * gx) // 2

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        ta = int(255 * p_title)
        f_t = fnt(52, bold=True)
        title = "We Handle Everything"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 65), title, font=f_t, fill=(*WHITE, ta))

        p_bar = anim(t, 0.6, 0.4)
        if p_bar > 0:
            bw = int(120 * p_bar)
            d.rectangle([W//2 - bw//2, 140, W//2 + bw//2, 144],
                        fill=(*TEAL, 255))

        p_sub = anim(t, 1.0, 0.5)
        sa = int(255 * p_sub)
        f_sub = fnt(28, light=True)
        sub = "So you can focus on what matters — your health."
        sw = text_w(d, sub, f_sub)
        d.text(((W - sw) // 2, 165), sub, font=f_sub, fill=(*LGRAY, sa))

        y0 = 230
        for i, (txt, acc) in enumerate(svcs):
            col, row = i % 3, i // 3
            p = anim(t, 1.5 + i * 0.5, 0.6)
            alpha = int(255 * p)
            direction = -1 if col == 0 else (1 if col == 2 else (-1 if row == 0 else 1))
            slide_x = int(lerp(direction * 100, 0, p))

            cx = x0 + col * (cw_s + gx) + slide_x
            cy = y0 + row * (ch_s + gy)
            d.rounded_rectangle((cx, cy, cx + cw_s, cy + ch_s), radius=14,
                                fill=(14, 26, 48, alpha), outline=(*acc, alpha), width=2)

            bw2 = int(50 * p)
            if bw2 > 0:
                d.rectangle([cx + 25, cy + 18, cx + 25 + bw2, cy + 21],
                            fill=(*acc, alpha))

            lines = txt.split("\n")
            ly = cy + 38
            for line in lines:
                d.text((cx + 30, ly), line, font=fnt(27), fill=(*WHITE, alpha))
                ly += 38

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=16).with_fps(FPS)


# ── Scene 6: Treatments (animated progress bars) ──────────────────────

@register("Treatments", 14, (
    "Whether it is a hair transplant, dental implants, cosmetic surgery, "
    "IVF, or joint replacement, patients save 70 to 90 percent compared to "
    "the US, UK, and Australia. Expert second opinions start at just 150 dollars."
))
def scene_treatments():
    bg = get_bg("treatments", DARK, NAVY,
                glows=[(W//2, 400, 450, GOLD, 20)], particles_seed=500)

    data = [
        ("Hair Transplant", 85, TEAL),
        ("Dental Implants", 80, GOLD),
        ("Cosmetic Surgery", 75, TEAL),
        ("IVF Treatment", 70, GOLD),
        ("Knee / Hip Replacement", 85, TEAL),
        ("Second Opinion — $150", 100, GOLD),
    ]
    cw_c, ch_c = 550, 130
    gx2, gy2 = 45, 22
    x0 = (W - 3 * cw_c - 2 * gx2) // 2
    y0 = 210

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        ta = int(255 * p_title)
        f_t = fnt(50, bold=True)
        title = "Save 70–90% on World-Class Treatment"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 70), title, font=f_t, fill=(*WHITE, ta))

        p_bar0 = anim(t, 0.6, 0.4)
        if p_bar0 > 0:
            bw = int(120 * p_bar0)
            d.rectangle([W//2 - bw//2, 145, W//2 + bw//2, 149],
                        fill=(*GOLD, 255))

        for i, (name, pct, acc) in enumerate(data):
            col, row = i % 3, i // 3
            p_card = anim(t, 1.0 + i * 0.3, 0.6)
            p_fill = anim(t, 1.5 + i * 0.3, 1.2)
            alpha = int(255 * p_card)

            cx = x0 + col * (cw_c + gx2)
            cy = y0 + row * (ch_c + gy2)
            slide_y = int(lerp(30, 0, p_card))
            cy += slide_y

            d.rounded_rectangle((cx, cy, cx + cw_c, cy + ch_c), radius=12,
                                fill=(14, 26, 48, alpha), outline=(*acc, alpha), width=2)

            d.text((cx + 25, cy + 18), name, font=fnt(26, bold=True),
                   fill=(*WHITE, alpha))

            label = f"Save up to {int(pct * p_fill)}%" if "Opinion" not in name else f"Just $150"
            d.text((cx + 25, cy + 58), label, font=fnt(20, light=True),
                   fill=(*acc, alpha))

            bar_x, bar_y = cx + 25, cy + 92
            bar_w, bar_h = cw_c - 50, 14
            d.rounded_rectangle((bar_x, bar_y, bar_x + bar_w, bar_y + bar_h),
                                radius=7, fill=(28, 42, 65, alpha))
            fill_w = int(bar_w * (pct / 100) * p_fill)
            if fill_w > 4:
                d.rounded_rectangle((bar_x, bar_y, bar_x + fill_w, bar_y + bar_h),
                                    radius=7, fill=(*acc, alpha))

        p_foot = anim(t, 4.0, 0.5)
        fa = int(255 * p_foot)
        f_f = fnt(24, light=True)
        foot = "Compared to US, UK, and Australia"
        fw = text_w(d, foot, f_f)
        d.text(((W - fw) // 2, H - 150), foot, font=f_f, fill=(*LGRAY, fa))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=14).with_fps(FPS)


# ── Scene 7: Packages (cards rise staggered) ──────────────────────────

@register("Packages", 12, (
    "Choose from three curated packages. Essential, Premium, or Royal. "
    "All inclusive of a companion. Or build your own package and customize every detail."
))
def scene_packages():
    bg = get_bg("packages", NAVY, (15, 30, 50),
                glows=[(W//2, 450, 500, GOLD, 18)], particles_seed=600)

    pkgs = [
        ("Essential", "$3,500+", ["Quality care", "Comfortable stay",
         "3-star hotel", "Daily transport"], TEAL, (18, 35, 58)),
        ("Premium", "$6,000+", ["Premium hospitals", "4-star hotel",
         "Personal companion", "Priority scheduling"], GOLD, (22, 32, 52)),
        ("Royal", "$12,000+", ["VIP concierge", "Luxury suite",
         "5-star hotel", "12-month follow-up"], GOLD, (30, 28, 48)),
    ]
    cw_p, ch_p = 510, 530
    gap_p = 45
    x0 = (W - 3 * cw_p - 2 * gap_p) // 2
    cy_final = 195

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        ta = int(255 * p_title)
        f_t = fnt(54, bold=True)
        title = "Choose Your Package"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 65), title, font=f_t, fill=(*WHITE, ta))

        p_bar = anim(t, 0.6, 0.4)
        if p_bar > 0:
            bw = int(100 * p_bar)
            d.rectangle([W//2 - bw//2, 143, W//2 + bw//2, 147],
                        fill=(*TEAL, 255))

        for i, (name, price, feats, acc, bg_c) in enumerate(pkgs):
            p = anim(t, 1.0 + i * 0.5, 0.8)
            alpha = int(255 * p)
            slide_y = int(lerp(80, 0, p))

            cx = x0 + i * (cw_p + gap_p)
            cy = cy_final + slide_y
            outline = GOLD if name == "Royal" else acc
            w = 3 if name == "Royal" else 2
            d.rounded_rectangle((cx, cy, cx + cw_p, cy + ch_p), radius=18,
                                fill=(*bg_c, alpha), outline=(*outline, alpha), width=w)
            if name == "Royal":
                d.rectangle([cx, cy, cx + cw_p, cy + 5], fill=(*GOLD, alpha))

            f_name = fnt(38, bold=True)
            nw2 = text_w(d, name, f_name)
            d.text((cx + (cw_p - nw2) // 2, cy + 30), name, font=f_name,
                   fill=(*acc, alpha))

            bw2 = int(70 * p)
            if bw2 > 0:
                d.rectangle([cx + cw_p//2 - bw2//2, cy + 85,
                             cx + cw_p//2 + bw2//2, cy + 88],
                            fill=(*acc, alpha))

            f_price = fnt(56, bold=True)
            pw = text_w(d, price, f_price)
            d.text((cx + (cw_p - pw) // 2, cy + 110), price, font=f_price,
                   fill=(*WHITE, alpha))

            fy = cy + 210
            for j, feat in enumerate(feats):
                fp = anim(t, 1.5 + i * 0.5 + j * 0.2, 0.4)
                fa = int(255 * fp)
                ft_str = f"✓  {feat}"
                f_feat = fnt(24)
                ftw = text_w(d, ft_str, f_feat)
                d.text((cx + (cw_p - ftw) // 2, fy), ft_str, font=f_feat,
                       fill=(*LGRAY, fa))
                fy += 48

        p_foot = anim(t, 4.0, 0.5)
        fa = int(255 * p_foot)
        f_f = fnt(21, light=True)
        foot = "All packages include patient + 1 companion  •  Indicative pricing"
        fw = text_w(d, foot, f_f)
        d.text(((W - fw) // 2, H - 70), foot, font=f_f, fill=(*LGRAY, fa))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=12).with_fps(FPS)


# ── Scene 8: Cities (pop-in one by one) ───────────────────────────────

@register("Cities", 8, (
    "We operate across India's top medical hubs. "
    "Delhi, Jaipur, Mumbai, Bangalore, Kolkata, and Chennai."
))
def scene_cities():
    bg = get_bg("cities", (0, 40, 55), NAVY,
                glows=[(W//2, H//2, 500, TEAL, 22)], particles_seed=700)

    names = ["Delhi", "Jaipur", "Mumbai", "Bangalore", "Kolkata", "Chennai"]
    cw_city = 260
    gap_city = 40
    x0 = (W - 6 * cw_city - 5 * gap_city) // 2
    cy_city = H // 2 - 50

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        ta = int(255 * p_title)
        f_t = fnt(50, bold=True)
        title = "Present Across India's Top Medical Hubs"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 160), title, font=f_t, fill=(*WHITE, ta))

        p_bar = anim(t, 0.6, 0.4)
        if p_bar > 0:
            bw = int(120 * p_bar)
            d.rectangle([W//2 - bw//2, 235, W//2 + bw//2, 239],
                        fill=(*TEAL, 255))

        for i, city in enumerate(names):
            p = anim(t, 1.2 + i * 0.3, 0.5)
            alpha = int(255 * p)
            scale = p
            acc = TEAL if i % 2 == 0 else GOLD

            cx = x0 + i * (cw_city + gap_city)
            card_w = int(cw_city * scale)
            card_h = int(110 * scale)
            card_x = cx + (cw_city - card_w) // 2
            card_y = cy_city + (110 - card_h) // 2

            if card_w > 10 and card_h > 10:
                d.rounded_rectangle((card_x, card_y, card_x + card_w, card_y + card_h),
                                    radius=int(14 * scale),
                                    fill=(14, 26, 48, alpha), outline=(*acc, alpha), width=2)

                dot_r = int(10 * scale)
                if dot_r > 2:
                    d.ellipse([card_x + card_w // 2 - dot_r, card_y + int(28 * scale) - dot_r,
                               card_x + card_w // 2 + dot_r, card_y + int(28 * scale) + dot_r],
                              fill=(*acc, alpha))

                f_c = fnt(max(10, int(30 * scale)), bold=True)
                cnw = text_w(d, city, f_c)
                d.text((card_x + (card_w - cnw) // 2, card_y + int(50 * scale)),
                       city, font=f_c, fill=(*WHITE, alpha))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=8).with_fps(FPS)


# ── Scene 9: Payment Flow (sequential reveal) ─────────────────────────

@register("Payment Flow", 12, (
    "Getting started is simple. Book a free consultation. "
    "Then pay just 150 dollars for the Meet Your Doctor package. "
    "Enroll with your first installment. "
    "And make the final payment when your treatment begins."
))
def scene_payment():
    bg = get_bg("payment", DARK, NAVY,
                glows=[(W//2, H//2, 450, GOLD, 20)], particles_seed=800)

    steps = [
        ("Free\nConsultation", TEAL),
        ("$150\nMeet Your Doctor", GOLD),
        ("1st Installment\nEnrollment", TEAL),
        ("Final Payment\nTreatment Day", GOLD),
    ]
    sw, sh = 350, 210
    gap_s = 45
    x0 = (W - 4 * sw - 3 * gap_s) // 2
    cy_steps = H // 2 - 90

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_title = anim(t, 0.2, 0.7)
        ta = int(255 * p_title)
        f_t = fnt(50, bold=True)
        title = "Simple, Transparent Payment"
        tw = text_w(d, title, f_t)
        d.text(((W - tw) // 2, 130), title, font=f_t, fill=(*WHITE, ta))

        p_bar = anim(t, 0.6, 0.4)
        if p_bar > 0:
            bw = int(120 * p_bar)
            d.rectangle([W//2 - bw//2, 205, W//2 + bw//2, 209],
                        fill=(*GOLD, 255))

        for i, (txt, acc) in enumerate(steps):
            p = anim(t, 1.2 + i * 1.0, 0.7)
            alpha = int(255 * p)
            slide_y = int(lerp(50, 0, p))

            cx = x0 + i * (sw + gap_s)
            cy = cy_steps + slide_y

            d.rounded_rectangle((cx, cy, cx + sw, cy + sh), radius=16,
                                fill=(14, 26, 48, alpha), outline=(*acc, alpha), width=2)

            cr = int(26 * p)
            if cr > 4:
                d.ellipse([cx + sw // 2 - cr, cy + 40 - cr,
                           cx + sw // 2 + cr, cy + 40 + cr],
                          fill=(*acc, alpha))
                num = str(i + 1)
                f_n = fnt(28, bold=True)
                nw = text_w(d, num, f_n)
                d.text((cx + sw // 2 - nw // 2, cy + 23), num, font=f_n,
                       fill=(*DARK, alpha))

            lines = txt.split("\n")
            ly = cy + 85
            for line in lines:
                f_l = fnt(25)
                lw = text_w(d, line, f_l)
                d.text((cx + (sw - lw) // 2, ly), line, font=f_l,
                       fill=(*WHITE, alpha))
                ly += 38

            if i < len(steps) - 1:
                p_arrow = anim(t, 1.8 + i * 1.0, 0.4)
                aa = int(255 * p_arrow)
                ax = cx + sw + 8
                d.text((ax, cy + sh // 2 - 14), "→", font=fnt(34, bold=True),
                       fill=(*LGRAY, aa))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=12).with_fps(FPS)


# ── Scene 10: CTA (converge + pulse) ──────────────────────────────────

@register("CTA", 10, (
    "Med Route India. World-class healthcare, made accessible. "
    "Book your free consultation today at med route india dot com."
))
def scene_cta():
    bg = get_bg("cta", (0, 50, 70), NAVY,
                glows=[(W//2, H//2 - 80, 600, TEAL, 30),
                       (W//2, H//2 + 100, 400, GOLD, 15)],
                particles_seed=900)

    def make_frame(t):
        frame = bg.copy()
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay)

        p_logo = anim(t, 0.3, 1.0)
        la = int(255 * p_logo)
        f_logo = fnt(110, bold=True)
        tw = text_w(d, "MedRouteIndia", f_logo)
        logo_y = int(lerp(H // 2 - 200, H // 2 - 230, p_logo))
        d.text(((W - tw) // 2, logo_y), "MedRouteIndia", font=f_logo,
               fill=(*WHITE, la))

        p_bar = anim(t, 1.2, 0.5)
        if p_bar > 0:
            bw = int(180 * p_bar)
            d.rectangle([W//2 - bw//2, H//2 - 95, W//2 + bw//2, H//2 - 91],
                        fill=(*GOLD, 255))

        p_tag = anim(t, 1.6, 0.7)
        tag_a = int(255 * p_tag)
        f_tag = fnt(38, light=True)
        tag = "World-Class Healthcare, Made Accessible."
        ttw = text_w(d, tag, f_tag)
        d.text(((W - ttw) // 2, H // 2 - 65), tag, font=f_tag,
               fill=(*TEAL, tag_a))

        p_btn = anim(t, 2.5, 0.6)
        btn_a = int(255 * p_btn)
        pulse = 1.0 + 0.02 * math.sin(t * 4)
        btn_w = int(580 * p_btn * pulse)
        btn_h = int(70 * p_btn)
        bx = (W - btn_w) // 2
        by = H // 2 + 20
        if btn_w > 20 and btn_h > 10:
            d.rounded_rectangle((bx, by, bx + btn_w, by + btn_h), radius=35,
                                fill=(*GOLD, btn_a))
            bt = "Book Your Free Consultation Today"
            f_btn = fnt(28, bold=True)
            btw = text_w(d, bt, f_btn)
            d.text(((W - btw) // 2, by + 17), bt, font=f_btn,
                   fill=(*DARK, btn_a))

        p_url = anim(t, 3.5, 0.5)
        ua = int(255 * p_url)
        d.text(((W - text_w(d, "www.medrouteindia.com", fnt(34))) // 2, H // 2 + 130),
               "www.medrouteindia.com", font=fnt(34), fill=(*LGRAY, ua))
        d.text(((W - text_w(d, "care@medrouteindia.com", fnt(24, light=True))) // 2, H // 2 + 180),
               "care@medrouteindia.com", font=fnt(24, light=True), fill=(*LGRAY, ua))

        p_cities = anim(t, 4.0, 0.5)
        ca = int(255 * p_cities)
        cities = "Delhi  •  Jaipur  •  Mumbai  •  Bangalore  •  Kolkata  •  Chennai"
        f_c = fnt(22, light=True)
        cw2 = text_w(d, cities, f_c)
        d.text(((W - cw2) // 2, H - 70), cities, font=f_c, fill=(*LGRAY, ca))

        frame_rgba = frame.convert("RGBA")
        return np.array(Image.alpha_composite(frame_rgba, overlay).convert("RGB"))

    return VideoClip(make_frame, duration=10).with_fps(FPS)


# ══════════════════════════════════════════════════════════════════════
#  BUILD
# ══════════════════════════════════════════════════════════════════════

def build():
    os.makedirs(VO_DIR, exist_ok=True)

    # 1) Generate all voiceovers
    print("=== Generating voiceovers ===")
    vo_paths = []
    for i, (name, dur, vo_text, _) in enumerate(SCENE_LIST):
        fname = f"scene_{i:02d}_{name.replace(' ', '_')}.mp3"
        print(f"  VO {i+1}/{len(SCENE_LIST)}: {name}")
        vo_paths.append(gen_vo(vo_text, fname))

    # 2) Build scene clips
    print("\n=== Building animated scenes ===")
    clips = []
    durations = []
    for i, (name, dur, _, builder) in enumerate(SCENE_LIST):
        print(f"  Scene {i+1}/{len(SCENE_LIST)}: {name} ({dur}s)")
        clip = builder()
        clips.append(clip)
        durations.append(dur)

    total_raw = sum(durations)
    print(f"\nRaw total: {total_raw:.1f}s")

    # 3) Apply crossfade transitions
    print("Applying transitions...")
    final_clips = [clips[0].with_effects([vfx.FadeIn(0.8)])]
    for c in clips[1:]:
        final_clips.append(c.with_effects([vfx.CrossFadeIn(XFADE)]))
    final_clips[-1] = final_clips[-1].with_effects(
        [vfx.CrossFadeIn(XFADE), vfx.FadeOut(1.5)])
    video = concatenate_videoclips(final_clips, method="compose")

    # 4) Compute CORRECT audio start times (accounting for crossfade overlap)
    print("Syncing voiceover to scenes...")
    starts = [0.0]
    for i in range(1, len(durations)):
        starts.append(starts[-1] + durations[i - 1] - XFADE)

    vo_clips = []
    for i, vp in enumerate(vo_paths):
        vo = AudioFileClip(vp)
        max_dur = durations[i] - 0.5
        if vo.duration > max_dur:
            vo = vo.subclipped(0, max_dur)
        vo_clips.append(vo.with_start(starts[i] + 0.3))

    # 5) Background music
    print("Generating background music...")
    bgm_path = os.path.join(BASE, "_bgm.wav")
    gen_bgm(video.duration + 2, bgm_path)
    bgm = (AudioFileClip(bgm_path)
           .with_effects([afx.AudioFadeIn(2), afx.AudioFadeOut(3)])
           .with_volume_scaled(0.2))

    # 6) Mix audio
    print("Mixing audio...")
    mixed = CompositeAudioClip([bgm] + vo_clips)
    video = video.with_audio(mixed)

    # 7) Render
    print(f"Rendering to {OUT} ...")
    video.write_videofile(
        OUT, fps=FPS, codec="libx264", audio_codec="aac",
        preset="medium", threads=4, logger="bar",
    )

    # Cleanup
    import shutil
    if os.path.exists(VO_DIR):
        shutil.rmtree(VO_DIR)
    if os.path.exists(bgm_path):
        os.remove(bgm_path)

    print(f"\nDone! Video: {OUT}")
    print(f"Duration: {video.duration:.1f}s | {W}x{H} | {FPS}fps")


if __name__ == "__main__":
    build()
