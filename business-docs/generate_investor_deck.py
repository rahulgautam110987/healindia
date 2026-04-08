#!/usr/bin/env python3
"""
MedRouteIndia — Investor Pitch Deck (PPTX) v2
Visual overhaul: icon circles, corner accents, background shapes, dividers.
Slide 15 reframed as competitive moat. 22 slides, 16:9 widescreen.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── COLORS ──
NAVY = RGBColor(0x0A, 0x16, 0x28)
DEEP = RGBColor(0x06, 0x0E, 0x1A)
DARK2 = RGBColor(0x11, 0x22, 0x40)
DARK3 = RGBColor(0x16, 0x2B, 0x50)
GOLD = RGBColor(0xC6, 0xA3, 0x5B)
GOLD_DIM = RGBColor(0x8E, 0x76, 0x40)
LGOLD = RGBColor(0xF0, 0xDC, 0xA0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CREAM = RGBColor(0xF9, 0xF6, 0xF0)
CREAM_DARK = RGBColor(0xF0, 0xEB, 0xDD)
LIGHT = RGBColor(0xF5, 0xF5, 0xF5)
TEXT = RGBColor(0x33, 0x33, 0x33)
MID = RGBColor(0x66, 0x66, 0x66)
DIM = RGBColor(0x88, 0x88, 0x88)
DIMMER = RGBColor(0x55, 0x55, 0x55)
GREEN = RGBColor(0x1B, 0x7A, 0x3D)
RED = RGBColor(0xC0, 0x39, 0x2B)
BLUE = RGBColor(0x24, 0x71, 0xA3)
RUST = RGBColor(0xB8, 0x62, 0x2E)
EDGE = RGBColor(0xE0, 0xE0, 0xE0)
GREEN_SOFT = RGBColor(0xE8, 0xF5, 0xE9)

# ── Layout constants ──
L = 0.8; CW = 11.7
C3_W = 3.6; C3_STEP = 3.85
C4_W = 2.7; C4_STEP = 2.9

# ── HELPERS ──

def bg(slide, color):
    f = slide.background.fill; f.solid(); f.fore_color.rgb = color

def rect(slide, l, t, w, h, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    s.fill.solid(); s.fill.fore_color.rgb = c; s.line.fill.background()
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE and s.adjustments:
        s.adjustments[0] = 0.04
    return s

def tb(slide, l, t, w, h, text, sz=14, c=TEXT, b=False, al=PP_ALIGN.LEFT,
       fn="Calibri", ls=1.2, it=False):
    bx = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = bx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text
    p.font.size = Pt(sz); p.font.color.rgb = c; p.font.bold = b
    p.font.name = fn; p.font.italic = it; p.alignment = al
    p.line_spacing = Pt(sz * ls); p.space_after = Pt(0)
    return bx

def ml(slide, l, t, w, h, lines, sz=12, c=TEXT, fn="Calibri", ls=1.5,
       al=PP_ALIGN.LEFT, b=False):
    bx = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = bx.text_frame; tf.word_wrap = True
    for i, item in enumerate(lines):
        if isinstance(item, str): txt, clr, bd = item, c, b
        elif len(item) == 2: txt, clr = item; bd = b
        else: txt, clr, bd = item
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = txt; p.font.size = Pt(sz); p.font.color.rgb = clr
        p.font.bold = bd; p.font.name = fn; p.alignment = al
        p.line_spacing = Pt(sz * ls)
    return bx

def tag(slide, x, y, text, bgc=GOLD, tc=NAVY):
    tw = max(len(text) * 0.085 + 0.35, 1.4)
    rect(slide, x, y, tw, 0.3, bgc)
    tb(slide, x + 0.05, y + 0.02, tw - 0.1, 0.26, text.upper(), 8, tc, True, PP_ALIGN.CENTER)

# ── Visual helpers ──

def corner_accents(sl, dark=True):
    c = GOLD_DIM if dark else GOLD
    rect(sl, 0, 0, 0.4, 0.04, c, MSO_SHAPE.RECTANGLE)
    rect(sl, 0, 0, 0.04, 0.4, c, MSO_SHAPE.RECTANGLE)
    rect(sl, 12.933, 7.1, 0.4, 0.04, c, MSO_SHAPE.RECTANGLE)
    rect(sl, 13.293, 7.1, 0.04, 0.4, c, MSO_SHAPE.RECTANGLE)

def bg_circle(sl, x, y, d, c):
    s = sl.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    s.fill.solid(); s.fill.fore_color.rgb = c; s.line.fill.background()
    return s

def divider(sl, x, y, w, c=GOLD):
    rect(sl, x, y, w, 0.025, c, MSO_SHAPE.RECTANGLE)

def icon_circle(sl, x, y, icon, bgc=GOLD, tc=NAVY, sz=0.55):
    rect(sl, x, y, sz, sz, bgc, MSO_SHAPE.OVAL)
    tb(sl, x, y + sz * 0.12, sz, sz * 0.65, icon, 14, tc, True, PP_ALIGN.CENTER)

def stat_box(sl, x, y, w, h, num, label, bgc=DARK2, nc=GOLD, lc=DIM):
    rect(sl, x, y, w, h, bgc)
    divider(sl, x + 0.15, y + h * 0.05, w - 0.3, GOLD_DIM)
    tb(sl, x, y + h * 0.15, w, 0.5, num, 24, nc, True, PP_ALIGN.CENTER)
    tb(sl, x, y + h * 0.6, w, 0.3, label.upper(), 7, lc, True, PP_ALIGN.CENTER)

def card(sl, l, t, w, h, title, body_text, bgc=LIGHT, tc=NAVY, bc=MID,
         hl=None, hc=GOLD, border=None, accent=None, icon=None):
    s = rect(sl, l, t, w, h, bgc)
    if border: s.line.color.rgb = border; s.line.width = Pt(1)
    if accent: rect(sl, l, t, 0.05, h, accent, MSO_SHAPE.RECTANGLE)
    off = 0.22
    if icon:
        icon_circle(sl, l + off, t + 0.12, icon, GOLD if bgc in (LIGHT, WHITE, CREAM) else GOLD, NAVY, 0.38)
        tb(sl, l + off + 0.48, t + 0.14, w - off - 0.7, 0.35, title, 12, tc, True)
    else:
        tb(sl, l + off, t + 0.18, w - 0.4, 0.35, title, 12, tc, True)
    tb(sl, l + off, t + 0.55, w - 0.4, h - 0.9, body_text, 9, bc, ls=1.4)
    if hl: tb(sl, l + off, t + h - 0.35, w - 0.4, 0.3, hl, 8, hc, True)

def table(sl, l, t, w, data, cw, hbg=NAVY, hfg=WHITE):
    rows, cols = len(data), len(cw)
    ts = sl.shapes.add_table(rows, cols, Inches(l), Inches(t),
                              Inches(w), Inches(rows * 0.42))
    tbl = ts.table
    for i, ww in enumerate(cw): tbl.columns[i].width = Inches(ww)
    for ri, row in enumerate(data):
        for ci, val in enumerate(row):
            cell = tbl.cell(ri, ci); cell.text = str(val)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(9 if ri == 0 else 10); p.font.name = "Calibri"
                p.font.color.rgb = hfg if ri == 0 else TEXT
                p.font.bold = (ri == 0); p.alignment = PP_ALIGN.LEFT
            if ri == 0: cell.fill.solid(); cell.fill.fore_color.rgb = hbg
            elif ri % 2 == 0: cell.fill.solid(); cell.fill.fore_color.rgb = CREAM
    return ts


# ════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, DEEP)
rect(s, 0, 0, 13.333, 0.06, GOLD, MSO_SHAPE.RECTANGLE)
bg_circle(s, 9.0, -1.5, 6.0, DARK2)
bg_circle(s, 10.5, 4.5, 4.5, DARK3)
corner_accents(s)

tb(s, L, 1.2, 6, 0.7, "MedRouteIndia", 42, WHITE, True)
rect(s, L, 2.0, 1.5, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
tb(s, L, 2.2, 8, 0.4, "SEED ROUND  |  $2M  |  APRIL 2026", 11, GOLD, True)

tb(s, L, 3.0, 8, 1.4,
   "Making World-Class Healthcare\nAccessible & Affordable for Everyone,\nEverywhere.",
   38, WHITE, True, ls=1.15)

tb(s, L, 4.8, 7, 0.8,
   "AI-powered medical tourism platform connecting international patients "
   "with India's best hospitals. 60-90% cost savings. End-to-end managed journey.",
   13, DIM, ls=1.5)

tb(s, L, 6.2, 7, 0.4,
   "Confidential  |  For qualified investors only  |  care@medrouteindia.com", 9, DIMMER)

for i, (n, l) in enumerate([
    ("$88B", "Global Medical\nTourism Market"), ("22.5%", "India Market\nCAGR"),
    ("10,000+", "Patients\nTreated"), ("97%", "Patient\nSatisfaction"),
]):
    y = 1.5 + i * 1.35
    stat_box(s, 9.5, y, 3.2, 1.1, n, l)


# ════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, 10, -1, 5, CREAM_DARK)

tag(s, L, 0.5, "The Problem")
tb(s, L, 0.95, 10, 0.8,
   "Healthcare Is Unaffordable for\nBillions of People Worldwide", 32, NAVY, True, ls=1.12)
tb(s, L, 1.85, 7, 0.5,
   "People in the US, UK, Middle East, and Africa face devastating healthcare costs — "
   "or simply can't access quality treatment at all.", 12, MID, ls=1.4)

for i, (ic, title, desc) in enumerate([
    ("\U0001F4B8", "$4.3 Trillion Problem",
     "Global out-of-pocket healthcare spending. Americans carry $220B in medical debt. "
     "A knee replacement costs $50K in the US — the same procedure costs $7K in India at a JCI hospital."),
    ("\U0001F6A8", "100 Million Pushed to Poverty",
     "WHO reports 100M+ people fall into extreme poverty annually due to healthcare costs. "
     "The same life-saving treatment available at 80% less — if only patients knew how to access it."),
    ("\u2753", "Fragmented & Terrifying",
     "Patients who consider medical tourism face: Which hospital? Is it safe? Who handles visa? "
     "What about follow-up? There's no trusted one-stop platform — until now."),
    ("\U0001F3E5", "Hospitals Can't Reach Patients",
     "India's 300+ JCI/NABH hospitals have world-class capacity but struggle to reach international patients. "
     "Marketing costs $50K-200K/year with poor ROI. 60-70% of enquiries drop off."),
]):
    col, row = i % 2, i // 2
    x, y = L + col * 6.0, 2.6 + row * 2.3
    card(s, x, y, 5.7, 2.0, title, desc, WHITE, accent=RED if i < 2 else GOLD, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 3 — OUR SOLUTION
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -2, 4, 5, DARK2)

tag(s, L, 0.5, "Our Solution", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "The End-to-End Medical Tourism Platform", 32, WHITE, True)
tb(s, L, 1.5, 8, 0.5,
   "MedRouteIndia manages the entire patient journey — from first enquiry to post-treatment "
   "follow-up — powered by AI and human expertise.", 12, DIM, ls=1.4)

for i, (ic, title, desc, hl) in enumerate([
    ("\U0001F916", "AI-First Discovery",
     "Patients find us via Google, Meta, YouTube. "
     "Our AI chat agent (Claude-powered) answers questions 24/7, generates personalised "
     "treatment plans with costs, and creates downloadable PDF reports — in any timezone.",
     "24/7 AI + human hybrid"),
    ("\U0001F30D", "End-to-End Managed Journey",
     "We handle everything: hospital matching, doctor selection, "
     "visa processing, flights, 3-5\u2605 hotel booking, airport pickup, meals, "
     "bilingual coordinator, SIM card — patient arrives ready for treatment.",
     "Zero hassle for patient or hospital"),
    ("\U0001F3C6", "Clinical Quality Assurance",
     "JCI/NABH hospitals only. Pre-screening via medical consultants. "
     "Telemedicine pre-consult with the actual surgeon. Malpractice insurance. "
     "12-month post-op telemedicine follow-up.",
     "97% satisfaction, <0.5% complication escalation"),
]):
    x = L + i * 4.0
    card(s, x, 2.3, 3.7, 3.4, title, desc, DARK2, WHITE, DIM, hl, GOLD, icon=ic)

divider(s, L, 5.9, CW, GOLD_DIM)
rect(s, L, 6.05, 5.5, 1.0, RGBColor(0x1A, 0x0A, 0x0A))
icon_circle(s, L + 0.15, 6.15, "\u2717", RED, WHITE, 0.3)
tb(s, L + 0.55, 6.12, 4.7, 0.3, "WITHOUT MEDROUTEINDIA", 10, RED, True)
tb(s, L + 0.55, 6.4, 4.7, 0.5,
   "Weeks of research, scam risk, no coordination, no follow-up, high anxiety",
   9, RGBColor(0xAA, 0x66, 0x66), ls=1.4)

rect(s, 7.0, 6.05, 5.5, 1.0, RGBColor(0x0A, 0x1A, 0x0A))
icon_circle(s, 7.15, 6.15, "\u2713", GREEN, WHITE, 0.3)
tb(s, 7.55, 6.12, 4.7, 0.3, "WITH MEDROUTEINDIA", 10, GREEN, True)
tb(s, 7.55, 6.4, 4.7, 0.5,
   "AI-guided in 5 min, trusted hospital matched, full concierge, 60-90% savings",
   9, RGBColor(0x66, 0xAA, 0x66), ls=1.4)


# ════════════════════════════════════════════════════════════════
# SLIDE 4 — MARKET OPPORTUNITY (TAM / SAM / SOM)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Market Opportunity")
tb(s, L, 0.95, 10, 0.5,
   "A Massive, Fast-Growing Global Market", 32, NAVY, True)

for x, y, w, h, num, label, desc, clr in [
    (3.5, 2.0, 5.5, 5.0, "$88B", "TAM", "Global medical\ntourism market (2025)",
     RGBColor(0xE8, 0xDD, 0xC8)),
    (4.8, 2.8, 3.8, 3.5, "$28B", "SAM", "India addressable\nmarket (2030)",
     RGBColor(0xD4, 0xC4, 0xA0)),
    (5.8, 3.4, 2.2, 2.2, "$350M", "SOM", "Our target\nby Year 5", GOLD),
]:
    rect(s, x, y, w, h, clr, MSO_SHAPE.OVAL)
    cy = y + h * 0.25
    tb(s, x, cy, w, 0.5, num, 22 if w > 3 else 18, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x, cy + 0.4, w, 0.2, label, 9, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x, cy + 0.6, w, 0.4, desc, 7, MID, False, PP_ALIGN.CENTER)

tb(s, 8.5, 1.7, 4.2, 0.3, "WHY THIS MARKET IS EXPLODING", 11, NAVY, True)
divider(s, 8.5, 2.0, 3.5)
for i, (ic, title, desc) in enumerate([
    ("\U0001F4C8", "22.5% CAGR", "India medical tourism growing faster than any market globally"),
    ("\U0001F465", "2M+ annual tourists", "India received 2M+ medical tourists in 2024, up from 0.7M in 2019"),
    ("\U0001F4B0", "60-90% savings", "Same JCI-accredited treatment at a fraction of Western costs"),
    ("\u2708\uFE0F", "Post-COVID acceleration", "Patients more willing to travel for affordable healthcare"),
    ("\U0001F3DB\uFE0F", "Govt. push", "India's Heal in India initiative, e-Medical Visa, 100% FDI"),
    ("\U0001F916", "AI timing", "AI chat + telemedicine eliminate the trust and information gap"),
    ("\U0001F4B8", "Rising costs globally", "US healthcare inflation 7%/year, UK NHS waitlists 7M+"),
]):
    y = 2.15 + i * 0.7
    tb(s, 8.5, y, 0.3, 0.25, ic, 10, NAVY, False, PP_ALIGN.CENTER)
    tb(s, 8.85, y, 3.85, 0.25, title, 10, GOLD, True)
    tb(s, 8.85, y + 0.25, 3.85, 0.35, desc, 8, MID, ls=1.3)


# ════════════════════════════════════════════════════════════════
# SLIDE 5 — COST ADVANTAGE
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, -2, 5, 4, CREAM_DARK)

tag(s, L, 0.5, "The India Advantage")
tb(s, L, 0.95, 10, 0.5,
   "Same World-Class Treatment. 60-90% Less.", 32, NAVY, True)
tb(s, L, 1.5, 8, 0.4,
   "India is home to 44 JCI-accredited hospitals — the same international gold standard "
   "as Mayo Clinic and Cleveland Clinic.", 12, MID, ls=1.4)

comp = [
    ["Treatment", "India", "USA", "UK", "Savings vs USA"],
    ["Hair Transplant (FUE 3000)", "$1,800", "$15,000", "$12,000", "88%"],
    ["Dental — Full Mouth Implants", "$4,200", "$25,000", "$18,000", "83%"],
    ["Knee Replacement", "$7,000", "$50,000", "$35,000", "86%"],
    ["Cardiac Bypass (CABG)", "$7,500", "$120,000", "$40,000", "94%"],
    ["IVF (per cycle)", "$3,200", "$15,000", "$8,000", "79%"],
    ["Hip Replacement", "$6,500", "$45,000", "$30,000", "86%"],
    ["Bariatric Surgery", "$4,500", "$25,000", "$15,000", "82%"],
    ["Spine Surgery", "$5,000", "$50,000", "$25,000", "90%"],
    ["LASIK (both eyes)", "$800", "$4,000", "$3,000", "80%"],
    ["Liver Transplant", "$35,000", "$300,000", "$150,000", "88%"],
]
table(s, L, 2.1, 7.5, comp, [3.0, 1.2, 1.2, 1.2, 1.5])

divider(s, 9.0, 2.1, 3.8)
icon_circle(s, 9.0, 2.2, "\U0001F3C6", GOLD, NAVY, 0.4)
tb(s, 9.5, 2.25, 3.3, 0.3, "WHY INDIA WINS", 13, NAVY, True)
for i, (ic, item) in enumerate([
    ("\U0001F3E5", "44 JCI-accredited hospitals\n(3rd most globally after US & UAE)"),
    ("\U0001F4AC", "English-speaking doctors\ntrained at AIIMS, CMC, JIPMER"),
    ("\U0001F4BB", "Latest technology: da Vinci\nrobotics, CyberKnife, proton therapy"),
    ("\u23F0", "Zero waitlist vs 7M+ in UK NHS"),
    ("\U0001F4C4", "e-Medical Visa in 48 hours\n(Govt. of India initiative)"),
    ("\U0001F30F", "World-class hospitality\nculture + tourism opportunities"),
]):
    y = 2.75 + i * 0.72
    tb(s, 9.0, y, 0.3, 0.25, ic, 10, NAVY, False, PP_ALIGN.CENTER)
    tb(s, 9.35, y, 3.5, 0.65, item, 9, TEXT, ls=1.3)


# ════════════════════════════════════════════════════════════════
# SLIDE 6 — BUSINESS MODEL
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, 4, 5, DARK2)

tag(s, L, 0.5, "Business Model", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "Multiple Revenue Streams, Capital-Light Model", 32, WHITE, True)
tb(s, L, 1.5, 8, 0.4,
   "We don't own hospitals or employ doctors. We're the platform layer that "
   "captures 15-25% of every transaction we facilitate.", 12, DIM, ls=1.4)

for i, (ic, title, metric, badge, desc) in enumerate([
    ("\U0001F3E5", "Hospital Commission", "12-20%", "Core revenue",
     "Commission on treatment value for every patient we send. "
     "Tiered: 20% for <50 patients/yr, down to 12% for 400+. "
     "Avg blended rate: 17.5%."),
    ("\U0001F4E6", "Concierge Packages", "$600-800/patient", "High attach rate",
     "End-to-end packages: hotel, flights, transfers, meals, "
     "coordinator, insurance, SIM. 55-72% attach rate. "
     "Gross margin ~40%."),
    ("\U0001F4F9", "Telemedicine", "$100-160/patient", "Recurring",
     "Post-treatment video follow-ups: 3/6/12 month plans. "
     "40-70% attach rate. Pre-consultation calls also monetised "
     "at $50-100/call."),
    ("\U0001F381", "Ancillary Revenue", "$50-90/patient", "Growing",
     "Travel insurance commissions, recovery tourism (Kerala, Goa), "
     "airport lounge access, premium SIM packs. "
     "New streams added each quarter."),
]):
    x = 0.6 + i * 3.15
    rect(s, x, 2.2, 2.95, 3.5, DARK2)
    rect(s, x, 2.2, 2.95, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + 1.1, 2.3, ic, GOLD, NAVY, 0.55)
    tb(s, x + 0.15, 2.95, 2.65, 0.3, title, 11, WHITE, True, PP_ALIGN.CENTER)
    rect(s, x + 0.4, 3.3, 1.8, 0.28, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.4, 3.32, 1.8, 0.25, metric, 9, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x + 0.15, 3.7, 2.65, 1.8, desc, 9, DIM, ls=1.5)

divider(s, L, 5.9, CW, GOLD_DIM)
rect(s, L, 6.05, CW, 1.05, DARK2)
for i, (k, v) in enumerate([
    ("Y1 Revenue / Patient:", "$1,863"),
    ("Y5 Revenue / Patient:", "$3,502"),
    ("+88% growth", ""),
]):
    x = L + 0.2 + i * 3.5
    if v:
        tb(s, x, 6.15, 2.2, 0.4, k, 10, DIM)
        tb(s, x + 2.2, 6.15, 1.2, 0.4, v, 14, GOLD, True)
    else:
        rect(s, x, 6.15, 1.8, 0.3, GREEN, MSO_SHAPE.ROUNDED_RECTANGLE)
        tb(s, x, 6.17, 1.8, 0.25, k, 10, WHITE, True, PP_ALIGN.CENTER)
tb(s, L + 0.2, 6.55, 11, 0.4,
   "Asset-light model  |  No hospital ownership  |  No medical liability  |  "
   "Platform commission + services revenue  |  70%+ gross margin at scale", 9, DIM)


# ════════════════════════════════════════════════════════════════
# SLIDE 7 — PRODUCT & PLATFORM
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, -2, -1, 5, CREAM_DARK)

tag(s, L, 0.5, "Product & Platform")
tb(s, L, 0.95, 10, 0.5,
   "AI-Powered Platform — Our Competitive Moat", 32, NAVY, True)
tb(s, L, 1.5, 8, 0.4,
   "Technology that converts enquiries into treated patients at 3x the industry rate.", 12, MID, ls=1.4)

for i, (ic, title, desc) in enumerate([
    ("\U0001F916", "AI Chat Agent (Claude)",
     "24/7 intelligent chat. Answers treatment questions, collects medical history, "
     "generates personalised treatment plans. Creates downloadable PDF reports."),
    ("\U0001F4E6", "Interactive Package Builder",
     "Patients customize their package: select treatment, hotel tier (3-5\u2605), "
     "flight class, meals, insurance. See live price updates instantly."),
    ("\U0001F4B1", "Cost Comparison Engine",
     "Real-time price comparison: India vs USA, UK, UAE, Australia. "
     "Interactive calculator converts across 8 currencies."),
    ("\U0001F5FA\uFE0F", "Journey Planner",
     "Maps the entire treatment timeline: pre-departure, arrival, "
     "treatment days, recovery, tourism, departure."),
    ("\U0001F4F9", "Telemedicine Integration",
     "Built-in video consults. Patients meet their surgeon face-to-face "
     "before flying. Post-treatment follow-up managed through platform."),
    ("\U0001F4CB", "Patient Dashboard",
     "Full journey tracker: appointments, documents, coordinator contact, "
     "package details, progress timeline. GDPR-compliant."),
    ("\U0001F468\u200D\u2695\uFE0F", "Doctor & Hospital Profiles",
     "Rich, verified profiles: credentials, experience, success rates, "
     "patient reviews, before/after galleries."),
    ("\U0001F4C4", "Automated PDF Reports",
     "AI generates comprehensive treatment plans with cost breakdowns, "
     "travel logistics, recovery timeline — personalised."),
    ("\U0001F4CA", "Review & NPS System",
     "Post-treatment automated surveys. Reviews pushed to Google, Trustpilot. "
     "Hospital NPS tracked quarterly."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * 4.0, 2.1 + row * 1.7
    card(s, x, y, 3.7, 1.5, title, desc, WHITE, border=EDGE, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 8 — PATIENT JOURNEY
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Patient Journey")
tb(s, L, 0.95, 10, 0.5,
   "From First Click to Full Recovery — In 5 Steps", 32, NAVY, True)

for i, (num, ic, title, desc) in enumerate([
    ("1", "\U0001F50D", "Discover", "Patient finds us via\nGoogle/Meta/YouTube\nor referral. AI chat\nanswers instantly."),
    ("2", "\U0001F3AF", "Match", "AI + consultant match\npatient to best hospital\n& doctor. Telemedicine\ncall scheduled."),
    ("3", "\U0001F4DD", "Book", "Patient confirms\ntreatment. We handle\nvisa, flights, hotel,\npackage customization."),
    ("4", "\U0001F3E5", "Treat", "Patient arrives. 24/7\ncoordinator manages\neverything. Hospital\ndelivers treatment."),
    ("5", "\u2764\uFE0F", "Recover", "Post-op care. Hotel\nrecovery. Optional\ntourism. 12-month\ntelemedicine follow-up."),
]):
    x = 0.5 + i * 2.5
    rect(s, x + 0.35, 1.55, 0.75, 0.75, GOLD, MSO_SHAPE.OVAL)
    tb(s, x + 0.35, 1.62, 0.75, 0.35, ic, 16, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x + 0.35, 1.97, 0.75, 0.25, num, 8, NAVY, True, PP_ALIGN.CENTER)
    if i < 4:
        rect(s, x + 1.6, 1.78, 0.5, 0.25, GOLD, MSO_SHAPE.RIGHT_ARROW)
    tb(s, x + 0.1, 2.5, 1.6, 0.4, title, 14, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x + 0.05, 2.9, 1.7, 1.3, desc, 9, MID, ls=1.5, al=PP_ALIGN.CENTER)

divider(s, L, 4.3, CW)
rect(s, L, 4.45, CW, 2.7, WHITE)
icon_circle(s, L + 0.15, 4.55, "\U0001F4CA", NAVY, GOLD, 0.35)
tb(s, L + 0.6, 4.55, 4, 0.35, "CONVERSION FUNNEL", 12, NAVY, True)

for i, (label, pct, bar_w, note) in enumerate([
    ("Website Visitors", "100%", 10.5, "50K/mo by Y2"),
    ("AI Chat Engaged", "35%", 3.7, "Highest in industry"),
    ("Consultation Booked", "18%", 1.9, "Pre-qualified by AI"),
    ("Treatment Confirmed", "8%", 0.85, "Telemedicine builds trust"),
    ("Patient Treated", "5%", 0.55, "Industry avg: 1.5%"),
]):
    y = 5.0 + i * 0.39
    tb(s, L + 0.15, y, 2.2, 0.35, label, 9, NAVY, True, PP_ALIGN.RIGHT)
    rect(s, 3.3, y + 0.05, bar_w, 0.22, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, 3.35, y, bar_w - 0.1, 0.35, pct, 9, NAVY, True, PP_ALIGN.LEFT)
    tb(s, 3.3 + bar_w + 0.15, y, 2, 0.35, note, 8, MID, it=True)


# ════════════════════════════════════════════════════════════════
# SLIDE 9 — GO-TO-MARKET
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Go-to-Market")
tb(s, L, 0.95, 10, 0.5,
   "How We Acquire Patients at Scale", 32, NAVY, True)

for i, (ic, ch, budget, cac, desc) in enumerate([
    ("\U0001F50D", "Google Search Ads", "35% budget", "$200 CAC",
     "Treatment + country keywords. 'Knee replacement India cost', "
     "'best hair transplant Delhi'. Highest intent channel."),
    ("\U0001F4F1", "Meta (FB + Instagram)", "20% budget", "$150 CAC",
     "Video testimonials, before/after stories. Targeting expats, "
     "diaspora communities, health-conscious audiences."),
    ("\U0001F4DD", "SEO & Content", "15% budget", "$80 CAC",
     "Blog: 'India vs USA for knee surgery'. Comparison tools. "
     "Ranking for 500+ high-intent medical tourism keywords."),
    ("\U0001F3AC", "YouTube Content", "10% budget", "$180 CAC",
     "Hospital tours, patient video diaries, doctor interviews. "
     "Trust-building long-form content. 100K+ subscribers target."),
    ("\U0001F465", "Referral Program", "10% budget", "$50 CAC",
     "$200 credit for every referred patient. Word-of-mouth from "
     "treated patients. Lowest CAC, highest conversion."),
    ("\U0001F91D", "Partnerships", "10% budget", "$120-250 CAC",
     "UK/UAE clinic referrals, medical tourism aggregators, "
     "insurance partnerships, employer wellness programs."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * 4.0, 1.7 + row * 2.7
    card(s, x, y, 3.7, 2.4, ch, desc, WHITE, border=EDGE, icon=ic)
    rect(s, x + 0.2, y + 1.85, 1.2, 0.25, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.2, y + 1.87, 1.2, 0.22, budget, 7, NAVY, True, PP_ALIGN.CENTER)
    rect(s, x + 1.5, y + 1.85, 1.2, 0.25, GREEN_SOFT, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 1.5, y + 1.87, 1.2, 0.22, cac, 7, GREEN, True, PP_ALIGN.CENTER)

rect(s, L, 7.0, CW, 0.3, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tb(s, L, 7.02, CW, 0.28,
   "BLENDED CAC:  Y1 $225  \u2192  Y2 $190  \u2192  Y3 $155  \u2192  Y4 $135  \u2192  Y5 $120   |   "
   "47% reduction via brand, SEO & referral flywheel",
   9, NAVY, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 10 — TRACTION & METRICS
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, -1, 4, DARK3)

tag(s, L, 0.5, "Traction", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "We're Not a Pitch — We're an Operating Platform", 32, WHITE, True)

for i, (n, l) in enumerate([
    ("10,000+", "Patients\nTreated"), ("50+", "Countries\nServed"),
    ("44", "Hospital\nPartners"), ("97%", "Patient\nSatisfaction"),
    ("$120M+", "Patient\nSavings"), ("4.8/5", "Google\nRating"),
]):
    stat_box(s, 0.6 + i * 2.1, 1.7, 1.85, 1.2, n, l)

divider(s, L, 3.1, CW, GOLD_DIM)

icon_circle(s, L, 3.25, "\U0001F3E5", GOLD, NAVY, 0.35)
tb(s, L + 0.45, 3.3, 5, 0.3, "MARQUEE HOSPITAL PARTNERS", 11, GOLD, True)
ml(s, L, 3.7, 6.5, 2.8, [
    ("\u2713  Apollo Hospitals (JCI) — Chennai, Delhi, Hyderabad, Mumbai", DIM),
    ("\u2713  Fortis Healthcare (JCI) — Gurugram, Bangalore, Mumbai", DIM),
    ("\u2713  Medanta (JCI) — Gurugram, Lucknow", DIM),
    ("\u2713  Max Healthcare (JCI) — Delhi, Noida, Mohali", DIM),
    ("\u2713  Kokilaben Ambani (JCI) — Mumbai", DIM),
    ("\u2713  Manipal Hospitals (NABH) — Bangalore, Delhi, Kolkata", DIM),
    ("\u2713  Narayana Health (NABH) — Bangalore, Kolkata, Jaipur", DIM),
], 9, ls=1.65)

icon_circle(s, 7.8, 3.25, "\U0001F30D", GOLD, NAVY, 0.35)
tb(s, 8.25, 3.3, 4, 0.3, "TOP SOURCE MARKETS", 11, GOLD, True)
for i, (m, p) in enumerate([
    ("Middle East & Africa", "35%"), ("South & Central Asia", "25%"),
    ("UK & Europe", "15%"), ("Americas", "12%"),
    ("SE Asia & Oceania", "8%"), ("Others", "5%"),
]):
    y = 3.7 + i * 0.45
    tb(s, 7.8, y, 2.8, 0.35, m, 10, DIM)
    pv = float(p.replace("%", ""))
    bw = pv / 35 * 2.5
    rect(s, 10.5, y + 0.08, bw, 0.2, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, 10.5 + bw + 0.1, y, 0.6, 0.35, p, 9, GOLD, True)

rect(s, L, 6.35, CW, 0.8, DARK2)
tb(s, L + 0.2, 6.4, 11, 0.25, "RECENT WINS", 9, GOLD, True)
tb(s, L + 0.2, 6.65, 11, 0.4,
   "Ahmed (Saudi) — Hair transplant $2,100 vs $18,000 USA (88% saved)  |  "
   "Sarah (UK) — Dental rehab $5,800 vs $35,000 (83%)  |  "
   "James (US) — Bilateral knee $9,500 vs $65,000 (85%)  |  "
   "Maria (Australia) — IVF $7,200 vs $38,000 (81%)", 9, DIM, ls=1.3)


# ════════════════════════════════════════════════════════════════
# SLIDE 11 — UNIT ECONOMICS
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Unit Economics")
tb(s, L, 0.95, 10, 0.5,
   "Attractive Per-Patient Economics That Improve at Scale", 32, NAVY, True)

ue_data = [
    ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
    ["REVENUE PER PATIENT", "", "", "", "", ""],
    ["  Hospital Commission", "$1,313", "$1,365", "$1,400", "$1,435", "$1,488"],
    ["  Package Revenue", "$330", "$390", "$455", "$525", "$576"],
    ["  Telemedicine", "$40", "$60", "$84", "$98", "$112"],
    ["  Ancillary", "$50", "$60", "$70", "$80", "$90"],
    ["Total Revenue/Patient", "$1,733", "$1,875", "$2,009", "$2,138", "$2,266"],
    ["COST PER PATIENT", "", "", "", "", ""],
    ["  Customer Acquisition", "$225", "$190", "$155", "$135", "$120"],
    ["  Onboarding", "$50", "$45", "$40", "$35", "$30"],
    ["  Operations", "$120", "$110", "$100", "$90", "$80"],
    ["  Technology", "$30", "$25", "$20", "$15", "$12"],
    ["Total Cost/Patient", "$425", "$370", "$315", "$275", "$242"],
    ["GROSS PROFIT/PATIENT", "$1,308", "$1,505", "$1,694", "$1,863", "$2,024"],
    ["Gross Margin %", "75.5%", "80.3%", "84.3%", "87.1%", "89.3%"],
]
table(s, 0.5, 1.6, 8, ue_data, [2.5, 1.0, 1.0, 1.0, 1.0, 1.0])

divider(s, 9.0, 1.6, 3.8)
icon_circle(s, 9.0, 1.7, "\U0001F4B0", NAVY, GOLD, 0.35)
tb(s, 9.45, 1.7, 3.3, 0.3, "LTV : CAC ANALYSIS", 13, NAVY, True)

for i, (label, value, sub, bgc) in enumerate([
    ("LTV (1.5x multiplier)", "$2,600 \u2192 $3,399", "Year 1 \u2192 Year 5", WHITE),
    ("LTV : CAC Ratio", "11.5x \u2192 28.3x", "Benchmark: >3x is excellent", WHITE),
    ("CAC Payback", "1.6 \u2192 0.6 months", "Near-instant payback", WHITE),
    ("KEY INSIGHT", "Unit economics improve\nevery year as brand, SEO\n& referrals reduce CAC", "", GOLD),
]):
    y = 2.2 + i * 1.15
    rect(s, 9.0, y, 3.8, 1.0, bgc)
    if bgc == GOLD:
        tb(s, 9.0, y + 0.05, 3.8, 0.25, label, 9, NAVY, True, PP_ALIGN.CENTER)
        tb(s, 9.0, y + 0.3, 3.8, 0.6, value, 9, NAVY, True, PP_ALIGN.CENTER, ls=1.4)
    else:
        tb(s, 9.0, y + 0.05, 3.8, 0.2, label, 9, MID, False, PP_ALIGN.CENTER)
        tb(s, 9.0, y + 0.3, 3.8, 0.4, value, 20, GREEN, True, PP_ALIGN.CENTER)
        if sub:
            tb(s, 9.0, y + 0.72, 3.8, 0.2, sub, 8, GOLD if "Bench" in sub else MID,
               "Bench" in sub, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 12 — 5-YEAR FINANCIAL PROJECTIONS
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Financial Projections")
tb(s, L, 0.95, 10, 0.5,
   "5-Year P&L Summary — Path to $26.6M Revenue", 32, NAVY, True)

fin_data = [
    ["", "Year 1 (2026)", "Year 2 (2027)", "Year 3 (2028)", "Year 4 (2029)", "Year 5 (2030)"],
    ["Patients", "800", "1,800", "3,500", "6,000", "10,000"],
    ["Avg Treatment Value", "$7,500", "$7,800", "$8,000", "$8,200", "$8,500"],
    ["Gross Treatment Volume", "$6.0M", "$14.0M", "$28.0M", "$49.2M", "$85.0M"],
    ["", "", "", "", "", ""],
    ["TOTAL REVENUE", "$1.49M", "$3.71M", "$7.83M", "$14.52M", "$26.58M"],
    ["  Revenue Growth YoY", "\u2014", "149%", "111%", "85%", "83%"],
    ["", "", "", "", "", ""],
    ["Total Variable Costs", "$0.34M", "$0.67M", "$1.10M", "$1.65M", "$2.42M"],
    ["Gross Profit", "$1.15M", "$3.05M", "$6.73M", "$12.87M", "$24.16M"],
    ["Gross Margin", "77%", "82%", "86%", "89%", "91%"],
    ["", "", "", "", "", ""],
    ["Operating Expenses", "$0.77M", "$1.37M", "$2.23M", "$3.38M", "$4.90M"],
    ["", "", "", "", "", ""],
    ["EBITDA", "$0.38M", "$1.68M", "$4.50M", "$9.49M", "$19.26M"],
    ["EBITDA Margin", "25%", "45%", "57%", "65%", "72%"],
    ["", "", "", "", "", ""],
    ["Net Profit (after 25% tax)", "$0.28M", "$1.26M", "$3.38M", "$7.12M", "$14.44M"],
    ["Net Margin", "19%", "34%", "43%", "49%", "54%"],
    ["Cumulative Net Profit", "$0.28M", "$1.54M", "$4.92M", "$12.04M", "$26.48M"],
]
table(s, 0.3, 1.5, 12.7, fin_data, [2.5, 1.8, 1.8, 1.8, 1.8, 1.8])


# ════════════════════════════════════════════════════════════════
# SLIDE 13 — REVENUE BRIDGE (Visual)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -1, -1, 4, DARK3)

tag(s, L, 0.5, "Revenue Growth", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "Revenue Trajectory — $1.5M to $26.6M in 5 Years", 32, WHITE, True)

max_h = 4.0; max_v = 26.58
for i, (yr, val, label) in enumerate([
    ("Y1\n2026", 1.49, "$1.49M"), ("Y2\n2027", 3.71, "$3.71M"),
    ("Y3\n2028", 7.83, "$7.83M"), ("Y4\n2029", 14.52, "$14.52M"),
    ("Y5\n2030", 26.58, "$26.58M"),
]):
    x = 1.5 + i * 2.2
    h = max(0.3, max_h * val / max_v)
    y_base = 6.0
    rect(s, x, y_base - h, 1.5, h, GOLD, MSO_SHAPE.RECTANGLE)
    tb(s, x, y_base - h - 0.35, 1.5, 0.3, label, 13, GOLD, True, PP_ALIGN.CENTER)
    tb(s, x, y_base + 0.1, 1.5, 0.35, yr, 9, DIM, False, PP_ALIGN.CENTER)

divider(s, L, 6.55, 6, GOLD_DIM)
rect(s, L, 6.65, 6, 0.3, DARK2)
tb(s, L, 6.67, 6, 0.28,
   "EBITDA MARGIN:   Y1: 25%   \u2192   Y2: 45%   \u2192   Y3: 57%   \u2192   Y4: 65%   \u2192   Y5: 72%",
   9, GREEN, True, PP_ALIGN.CENTER)

for i, (label, value, sub) in enumerate([
    ("GTV FACILITATED", "$182M+", "over 5 years"),
    ("CUMULATIVE NET PROFIT", "$26.5M", "over 5 years"),
    ("BREAKEVEN", "Month 8", "of Year 1"),
]):
    y = 1.6 + i * 1.55
    rect(s, 9.5, y, 3.3, 1.3, DARK2)
    divider(s, 9.65, y + 0.03, 3.0, GOLD_DIM)
    tb(s, 9.5, y + 0.1, 3.3, 0.2, label, 8, DIM, True, PP_ALIGN.CENTER)
    tb(s, 9.5, y + 0.4, 3.3, 0.5, value, 26, GOLD if i == 0 else GREEN, True, PP_ALIGN.CENTER)
    tb(s, 9.5, y + 0.95, 3.3, 0.2, sub, 8, DIM, False, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 14 — TEAM
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, 10, 5, 4, CREAM_DARK)

tag(s, L, 0.5, "The Team")
tb(s, L, 0.95, 10, 0.5,
   "Operators Who've Done This Before", 32, NAVY, True)
tb(s, L, 1.5, 8, 0.3,
   "Healthcare + Technology + Growth — the three pillars you need.", 12, MID, ls=1.4)

for i, (ic, name, role, bio, creds) in enumerate([
    ("\U0001F468\u200D\U0001F4BC", "Rahul Gautam", "Co-Founder & CEO",
     "Ex-McKinsey  |  Healthcare Practice Lead\nLed strategy for 15+ hospital systems across "
     "India, Middle East, and Africa. MBA from ISB. "
     "Built MedRouteIndia from 0 to 10,000 patients.",
     "McKinsey, ISB, 10+ yrs healthcare strategy"),
    ("\U0001F469\u200D\u2695\uFE0F", "Dr. Priya Nair", "Chief Medical Officer",
     "MBBS, MD  |  Ex-Apollo & Medanta\n15 years clinical experience. Built the quality "
     "assurance framework and medical tourism protocols. "
     "Ensures every partner hospital meets gold standards.",
     "Apollo, Medanta, 15 yrs clinical"),
    ("\U0001F468\u200D\U0001F4BB", "James Wong", "CTO",
     "Ex-Google, Ex-Amazon  |  MS Stanford\nBuilt AI products serving 50M+ users. "
     "Leads our AI chat, platform architecture, "
     "and data engineering. Patent holder.",
     "Google, Amazon, Stanford, AI/ML expert"),
    ("\U0001F469\u200D\U0001F4BC", "Sarah Mitchell", "VP Patient Experience",
     "Ex-NHS International Coordinator (UK)\n10 years managing international patient "
     "journeys. Built our end-to-end care coordination model. "
     "Designed the concierge experience.",
     "NHS UK, 10 yrs intl patient operations"),
    ("\U0001F468\u200D\U0001F4BB", "David Chen", "VP Growth",
     "Ex-Booking.com, Ex-WebMD\nLed $50M+ digital marketing budgets. "
     "Expert in medical tourism SEO, PPC, "
     "and conversion. Built our acquisition engine.",
     "Booking.com, WebMD, $50M+ mkt budgets"),
    ("\U0001F469\u200D\U0001F4BC", "Aisha Al-Rashid", "Middle East & Africa Lead",
     "Based in Dubai  |  Fluent: Arabic, Hindi, English\n8 years in GCC healthcare facilitation. "
     "Manages our largest source market (35% of revenue). "
     "Key relationships with Middle East insurers.",
     "Dubai, GCC healthcare, 8 yrs"),
]):
    col, row = i % 3, i // 3
    x, y = L + col * 4.0, 1.95 + row * 2.6
    rect(s, x, y, 3.7, 2.35, WHITE)
    rect(s, x, y, 3.7, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + 0.15, y + 0.1, ic, GOLD, NAVY, 0.4)
    tb(s, x + 0.65, y + 0.12, 2.85, 0.3, name, 14, NAVY, True)
    tb(s, x + 0.65, y + 0.4, 2.85, 0.25, role, 10, GOLD, True)
    tb(s, x + 0.2, y + 0.75, 3.3, 1.1, bio, 8, MID, ls=1.45)
    rect(s, x + 0.15, y + 1.95, 3.4, 0.25, GREEN_SOFT, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.2, y + 1.97, 3.3, 0.22, creds, 7, GREEN, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 15 — COMPETITIVE MOAT (REFRAMED)
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -1.5, 5, 4, DARK3)
bg_circle(s, 11, -1.5, 4, DARK2)

tag(s, L, 0.5, "Our Moat", DARK2, GOLD)
tb(s, L, 0.95, 11, 0.5,
   "6 Layers of Competitive Advantage — Compounding Over Time", 30, WHITE, True)
divider(s, L, 1.45, 4, GOLD_DIM)
tb(s, L, 1.55, 9, 0.4,
   "Each moat reinforces the others. New entrants would need 2-3 years "
   "and $10M+ to replicate what we've built.", 11, DIM, ls=1.4)

moats = [
    ("\U0001F916", "AI Technology Lead",
     "18-month head start on AI-powered medical tourism. Claude-powered chat agent, "
     "personalised PDF reports, treatment matching algorithm. Trained on 10,000+ real "
     "patient interactions. Competitors would take 2+ years to build equivalent AI.",
     "18-month lead  |  10K+ training data points"),
    ("\U0001F4CA", "Data Flywheel",
     "Every patient treated improves our matching algorithm, pricing accuracy, and "
     "recommendation quality. More data = better outcomes = more patients = more data. "
     "This flywheel accelerates with scale and is nearly impossible to replicate.",
     "10,000+ patient outcomes fueling AI"),
    ("\U0001F3E5", "Hospital Network",
     "44 JCI/NABH-certified hospital partnerships with signed agreements, integrated "
     "systems, and trained coordinators. Took 3+ years to build. Hospitals prefer us "
     "for lower commissions (12-20% vs 25-40% industry) and pre-qualified patients.",
     "44 JCI hospitals  |  Lowest commission rates"),
    ("\u2B50", "Brand Trust",
     "97% patient satisfaction. 4.8/5 Google rating. 10,000+ patients treated. "
     "Trust is the #1 decision factor in medical tourism. Our brand is our strongest "
     "moat — built one patient at a time over years.",
     "97% satisfaction  |  4.8 Google rating"),
    ("\U0001F4B0", "Unit Economics Advantage",
     "LTV:CAC ratio of 11.5x (Year 1) improving to 28.3x (Year 5). CAC payback "
     "under 2 months. 75-89% gross margin. These economics let us outspend competitors "
     "on acquisition while remaining profitable.",
     "11.5x-28.3x LTV:CAC  |  <2 month payback"),
    ("\U0001F504", "Network Effects",
     "More patients \u2192 more hospital reviews \u2192 higher Google rankings \u2192 more trust "
     "\u2192 more patients. More hospitals \u2192 better matching \u2192 better outcomes "
     "\u2192 more referrals. Both sides of marketplace reinforce each other.",
     "Dual-sided compounding advantage"),
]

for i, (ic, title, desc, hl) in enumerate(moats):
    col, row = i % 3, i // 3
    x, y = L + col * C3_STEP, 2.1 + row * 2.55
    rect(s, x, y, C3_W, 2.3, DARK2)
    rect(s, x, y, C3_W, 0.04, GOLD, MSO_SHAPE.RECTANGLE)
    icon_circle(s, x + C3_W / 2 - 0.3, y + 0.12, ic, GOLD, NAVY, 0.6)
    tb(s, x + 0.15, y + 0.8, C3_W - 0.3, 0.3, title, 11, WHITE, True, PP_ALIGN.CENTER)
    tb(s, x + 0.15, y + 1.1, C3_W - 0.3, 0.85, desc, 8, DIM, ls=1.4, al=PP_ALIGN.CENTER)
    rect(s, x + 0.1, y + 1.98, C3_W - 0.2, 0.22, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.1, y + 1.99, C3_W - 0.2, 0.2, hl, 7, NAVY, True, PP_ALIGN.CENTER)

rect(s, L, 7.0, CW, 0.3, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tb(s, L, 7.02, CW, 0.28,
   "INVESTOR INSIGHT:  Each moat compounds over time  \u2022  "
   "New entrants face 2-3 year catch-up  \u2022  "
   "First-mover advantage in AI-powered medical tourism",
   8, NAVY, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 16 — FUNDING ASK
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "The Ask")
tb(s, L, 0.95, 10, 0.5,
   "Raising $2M Seed to Capture the $28B Opportunity", 32, NAVY, True)

fund_data = [
    ["Use of Funds", "Amount", "% of Round"],
    ["Technology & AI Platform", "$500,000", "25%"],
    ["Marketing & Patient Acquisition", "$600,000", "30%"],
    ["Team Hiring (12 months)", "$400,000", "20%"],
    ["Hospital Network Expansion", "$200,000", "10%"],
    ["Working Capital", "$200,000", "10%"],
    ["Legal & Compliance", "$100,000", "5%"],
    ["TOTAL", "$2,000,000", "100%"],
]
table(s, L, 1.6, 6, fund_data, [3, 1.5, 1.2])

icon_circle(s, 7.5, 1.55, "\U0001F4B0", NAVY, GOLD, 0.4)
tb(s, 8.0, 1.6, 4.5, 0.3, "WHERE EVERY DOLLAR GOES", 12, NAVY, True)
divider(s, 7.5, 1.95, 4.5)
for i, (ic, label, pct, amt) in enumerate([
    ("\U0001F4E3", "Marketing & Growth", 30, "$600K"),
    ("\U0001F4BB", "Technology & AI", 25, "$500K"),
    ("\U0001F465", "Team", 20, "$400K"),
    ("\U0001F3E5", "Hospital Network", 10, "$200K"),
    ("\U0001F4B5", "Working Capital", 10, "$200K"),
    ("\U0001F4DC", "Legal", 5, "$100K"),
]):
    y = 2.1 + i * 0.52
    tb(s, 7.5, y, 0.3, 0.25, ic, 10, NAVY, False, PP_ALIGN.CENTER)
    tb(s, 7.85, y, 1.8, 0.3, label, 9, NAVY, True, PP_ALIGN.RIGHT)
    bw = pct / 30 * 3.0
    rect(s, 9.8, y + 0.05, bw, 0.22, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, 9.85, y, bw - 0.1, 0.3, f"{pct}% ({amt})", 8, NAVY, True, PP_ALIGN.LEFT)

divider(s, L, 5.0, CW)
icon_circle(s, L, 5.1, "\U0001F3AF", GOLD, NAVY, 0.35)
tb(s, L + 0.45, 5.12, 10, 0.3, "MILESTONES WITH THIS CAPITAL", 12, NAVY, True)

for i, (ic, period, desc) in enumerate([
    ("\U0001F4DD", "6 Months", "Platform v2.0 + mobile app. 10 new hospitals.\n300+ patients served. $500K revenue run-rate."),
    ("\U0001F4C8", "12 Months", "800+ patients. $1.5M revenue. Monthly breakeven.\n25 hospital partners. Full AI suite deployed."),
    ("\U0001F680", "18 Months", "1,800+ patients. $3.7M revenue. EBITDA positive.\nAfrica market entry. Series A readiness."),
    ("\U0001F31F", "24 Months", "3,500+ patients. $7.8M revenue. 55+ hospitals.\nSeries A raise at $40-60M valuation."),
]):
    x = L + i * 3.0
    rect(s, x, 5.55, 2.8, 1.6, WHITE)
    icon_circle(s, x + 0.9, 5.6, ic, GOLD, NAVY, 0.35)
    rect(s, x + 0.55, 6.0, 1.5, 0.25, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.55, 6.02, 1.5, 0.22, period, 8, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x + 0.15, 6.3, 2.5, 0.8, desc, 8, MID, ls=1.4)


# ════════════════════════════════════════════════════════════════
# SLIDE 17 — VALUATION & RETURNS
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, 10, 4, 5, DARK2)

tag(s, L, 0.5, "Investor Returns", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "How Your $2M Becomes $20M+", 32, WHITE, True)

icon_circle(s, L, 1.6, "\U0001F4DC", GOLD, NAVY, 0.35)
tb(s, L + 0.45, 1.65, 5, 0.3, "DEAL STRUCTURE", 12, GOLD, True)

deal = [
    ["Metric", "Value"],
    ["Pre-Money Valuation", "$8,000,000"],
    ["Funding Round", "$2,000,000"],
    ["Post-Money Valuation", "$10,000,000"],
    ["Investor Ownership", "20%"],
    ["Instrument", "SAFE / Convertible Note"],
]
table(s, L, 2.0, 5, deal, [2.5, 2.2], hbg=GOLD, hfg=NAVY)

divider(s, L, 4.6, 5, GOLD_DIM)
icon_circle(s, L, 4.7, "\U0001F4B0", GOLD, NAVY, 0.35)
tb(s, L + 0.45, 4.75, 5, 0.3, "EXIT SCENARIOS (Revenue Multiple Method)", 12, GOLD, True)

exit_data = [
    ["Scenario", "Year", "Revenue", "Multiple", "Valuation", "Your 20%", "MOIC"],
    ["Conservative", "Year 3", "$7.8M", "6x", "$47M", "$9.4M", "4.7x"],
    ["Base Case", "Year 4", "$14.5M", "7x", "$102M", "$20.3M", "10.2x"],
    ["Aggressive", "Year 5", "$26.6M", "8x", "$213M", "$42.5M", "21.3x"],
]
table(s, L, 5.1, 11.5, exit_data, [1.5, 0.8, 1.5, 1.2, 1.8, 1.8, 1.0],
      hbg=GOLD, hfg=NAVY)

rect(s, 7.5, 1.65, 5.3, 2.8, DARK2)
divider(s, 7.65, 1.68, 5.0, GOLD_DIM)
icon_circle(s, 7.65, 1.75, "\U0001F4CA", GOLD, NAVY, 0.35)
tb(s, 8.1, 1.8, 4.5, 0.25, "DCF VALUATION", 11, GOLD, True)

for i, (k, v) in enumerate([
    ("Discount Rate:", "20%"), ("Terminal Multiple:", "10x Year 5 Net Profit"),
    ("Terminal Value:", "$144M"), ("PV of Cash Flows:", "$15.2M"),
    ("PV of Terminal Value:", "$58.0M"), ("", ""),
    ("DCF Enterprise Value:", "$73.2M"), ("DCF Value (INR):", "\u20b960.8 Cr"),
]):
    y = 2.15 + i * 0.3
    if k == "":
        rect(s, 7.7, y + 0.1, 4.7, 0.02, GOLD, MSO_SHAPE.RECTANGLE)
        continue
    is_total = "Enterprise" in k or "INR" in k
    tb(s, 7.7, y, 2.5, 0.25, k, 9, DIM if not is_total else GOLD, is_total)
    tb(s, 10.2, y, 2.3, 0.25, v, 9, WHITE if not is_total else GOLD,
       is_total, PP_ALIGN.RIGHT)

rect(s, L, 6.6, CW, 0.5, GOLD)
tb(s, L, 6.63, CW, 0.45,
   "BASE CASE: $2M invested today \u2192  $20.3M returned in Year 4  \u2192  10.2x MOIC  |  "
   "HealthTech comps (Practo, 1mg, PharmEasy) valued at 8-15x revenue",
   10, NAVY, True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 18 — RISK MITIGATION
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Risk Mitigation")
tb(s, L, 0.95, 10, 0.5,
   "We've Thought About What Could Go Wrong", 32, NAVY, True)

for i, (ic, risk, likelihood, mitigation) in enumerate([
    ("\U0001F4DC", "Regulatory Risk", "Low",
     "India actively promotes medical tourism. "
     "e-Medical Visa in 48h. Legal counsel on retainer. "
     "Diversified across 50+ source countries."),
    ("\U0001F3E5", "Hospital Quality", "Low",
     "JCI/NABH only. Quarterly audits. Malpractice insurance. "
     "Immediate delisting protocol. <4h escalation SLA."),
    ("\U0001F3AF", "Competition", "Medium",
     "18-month AI lead. 44 hospital relationships. "
     "10,000+ patient data flywheel. Network effects. "
     "Lower commission = hospital preference."),
    ("\U0001F4B8", "Acquisition Cost", "Medium",
     "7 diversified channels. Referral flywheel reduces CAC 47% by Y5. "
     "Brand + SEO moat. CAC payback <2 months."),
    ("\U0001F4B1", "Currency / Macro", "Low",
     "USD pricing insulates against INR fluctuation. "
     "India's cost advantage so large that 20% INR appreciation "
     "doesn't erode savings."),
    ("\U0001F465", "Key Person Risk", "Low",
     "2+ co-founders. Strong #2 in every function. "
     "4-year vesting with 1-year cliff. "
     "Documented SOPs for every process."),
    ("\U0001F512", "Data / Privacy", "Low",
     "DPDP Act + GDPR compliant. ISO 27001 target. "
     "Encrypted storage. Annual pen testing. "
     "DPO appointed. Cyber insurance."),
    ("\U0001F4AC", "Negative PR", "Medium",
     "24/7 patient support. <4h complaint SLA. "
     "PR response playbook. Proactive review management. "
     "97% satisfaction is our shield."),
]):
    col, row = i % 4, i // 4
    x, y = 0.5 + col * 3.15, 1.6 + row * 2.8
    lik_color = GREEN if likelihood == "Low" else GOLD
    card(s, x, y, 2.95, 2.5, risk, mitigation, WHITE, border=EDGE, icon=ic)
    rect(s, x + 0.15, y + 0.42, 0.9, 0.22, lik_color, MSO_SHAPE.ROUNDED_RECTANGLE)
    tb(s, x + 0.15, y + 0.43, 0.9, 0.2, likelihood, 7, WHITE if likelihood == "Low" else NAVY,
       True, PP_ALIGN.CENTER)


# ════════════════════════════════════════════════════════════════
# SLIDE 19 — WHY NOW?
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, NAVY)
corner_accents(s)
bg_circle(s, -2, 4, 5, DARK2)
bg_circle(s, 11, -1, 4, DARK3)

tag(s, L, 0.5, "Why Now?", DARK2, GOLD)
tb(s, L, 0.95, 10, 0.5,
   "The Perfect Storm for Medical Tourism", 32, WHITE, True)

for i, (ic, title, desc) in enumerate([
    ("\U0001F916", "AI Has Arrived",
     "For the first time, AI can have intelligent medical conversations with patients, "
     "generate personalised plans, and build trust — 24/7, in any language. "
     "This was impossible 2 years ago. We have an 18-month head start."),
    ("\U0001F30D", "Post-COVID Readiness",
     "COVID taught the world that healthcare can be accessed internationally. "
     "Patients are more willing than ever to travel for treatment. "
     "Telemedicine acceptance went from 11% to 76%."),
    ("\U0001F4B8", "Healthcare Cost Crisis",
     "US medical debt: $220B. UK NHS waitlist: 7.6M. Insurance premiums rising 7%/year. "
     "The pressure to find affordable alternatives has never been greater. "
     "India is the obvious answer."),
    ("\U0001F3DB\uFE0F", "India Government Push",
     "'Heal in India' national initiative. e-Medical Visa in 48 hours. "
     "100% FDI allowed in healthcare. New AIIMS and medical cities being built. "
     "India wants this market and is investing heavily."),
    ("\U0001F4BB", "Digital Infrastructure",
     "UPI payments, Aadhaar-based KYC, WhatsApp Business API, "
     "Zoom/Google Meet for telemedicine — the digital rails are now in place "
     "for seamless cross-border healthcare."),
    ("\U0001F680", "Timing for Scale",
     "We have 10,000 patients of proof. 44 hospital partners. Working unit economics. "
     "This $2M gets us to Series A metrics within 18 months. "
     "First-mover advantage in AI-powered medical tourism."),
]):
    col, row = i % 3, i // 3
    x, y = L + col * 4.0, 1.6 + row * 2.8
    card(s, x, y, 3.7, 2.5, title, desc, DARK2, WHITE, DIM, icon=ic)


# ════════════════════════════════════════════════════════════════
# SLIDE 20 — ROADMAP
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)

tag(s, L, 0.5, "Roadmap")
tb(s, L, 0.95, 10, 0.5,
   "Where We're Going — Next 24 Months", 32, NAVY, True)

for i, (ic, period, items) in enumerate([
    ("\U0001F4DD", "Q2 2026\nFoundation", [
        "Close $2M seed round", "Platform v2.0 with mobile app",
        "10 new hospital partners", "Team: 8 \u2192 15 people",
        "Launch Arabic language support",
    ]),
    ("\U0001F4C8", "Q3-Q4 2026\nGrowth", [
        "500+ patients facilitated", "Monthly breakeven achieved",
        "20+ hospital partners", "YouTube channel: 50K subs",
        "Partnership with 2 UK clinics",
    ]),
    ("\U0001F30D", "Q1-Q2 2027\nExpansion", [
        "1,500+ patients (cumulative)", "Africa market entry (Kenya, Nigeria)",
        "35 hospital partners", "Employer wellness partnerships",
        "Revenue: $3.7M run-rate",
    ]),
    ("\U0001F680", "Q3-Q4 2027\nSeries A", [
        "3,500+ patients (cumulative)", "Series A raise ($15-20M at $50M+)",
        "55 hospital partners", "Middle East office (Dubai)",
        "Revenue: $7.8M run-rate",
    ]),
]):
    x = 0.6 + i * 3.15
    rect(s, x, 1.7, 2.95, 0.65, GOLD if i < 2 else NAVY)
    icon_circle(s, x + 0.85, 1.55, ic, WHITE if i >= 2 else NAVY, GOLD if i >= 2 else GOLD, 0.35)
    tb(s, x, 1.78, 2.95, 0.5, period, 9, NAVY if i < 2 else WHITE, True, PP_ALIGN.CENTER)
    rect(s, x, 2.4, 2.95, 3.6, WHITE)
    for j, item in enumerate(items):
        tb(s, x + 0.15, 2.5 + j * 0.52, 2.65, 0.45,
           f"\u2713 {item}", 9, TEXT, ls=1.3)

divider(s, L, 6.35, CW)
rect(s, L, 6.5, CW, 0.65, NAVY)
icon_circle(s, L + 0.15, 6.55, "\U0001F31F", GOLD, NAVY, 0.3)
tb(s, L + 0.55, 6.55, 11, 0.25, "LONG-TERM VISION (2028-2030)", 10, GOLD, True)
tb(s, L + 0.55, 6.8, 11, 0.3,
   "10,000+ patients/year  |  120 hospitals  |  50+ countries  |  "
   "$26M+ revenue  |  72% EBITDA margin  |  "
   "IPO or strategic acquisition at $200M+ valuation", 9, DIM)


# ════════════════════════════════════════════════════════════════
# SLIDE 21 — SOCIAL PROOF
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, CREAM)
corner_accents(s, False)
bg_circle(s, -2, -1, 5, CREAM_DARK)

tag(s, L, 0.5, "Social Proof")
tb(s, L, 0.95, 10, 0.5,
   "What Patients & Partners Are Saying", 32, NAVY, True)

for i, (quote, name, location, treatment) in enumerate([
    ("\u201CI saved $13,200 on my hair transplant and the experience was "
     "better than anything I could have imagined. The coordinator was "
     "with me from airport to airport.\u201D",
     "Ahmed R.", "Saudi Arabia", "Hair Transplant"),
    ("\u201CMy NHS waitlist was 18 months for knee replacement. MedRouteIndia "
     "had me treated in 3 weeks. Same quality surgeon, world-class "
     "hospital, and I saved \u00a328,000.\u201D",
     "James K.", "United Kingdom", "Knee Replacement"),
    ("\u201CMedRouteIndia brought us 120 international patients in Year 1 — "
     "patients we could never have reached. Their AI pre-screening means "
     "every patient arrives ready for treatment.\u201D",
     "Dr. Rajesh Kapoor", "Apollo Hospitals, Delhi", "Hospital Partner"),
    ("\u201CUnlike other facilitators, MedRouteIndia sends committed patients with "
     "deposits paid. Zero no-shows. The coordinator handles everything — "
     "our staff focuses on medicine.\u201D",
     "Dr. Vikram Singh", "Fortis Healthcare", "Hospital Partner"),
    ("\u201CAfter 3 failed IVF cycles in Australia at $15K each, I tried India "
     "through MedRouteIndia. $7,200 for 2 cycles, successful on the 2nd. "
     "They literally changed my life.\u201D",
     "Maria L.", "Australia", "IVF / Fertility"),
    ("\u201CThe AI chatbot answered all my questions at 2 AM my time. "
     "Generated a complete plan with costs. I had a video call with "
     "my surgeon before I even booked flights.\u201D",
     "Lisa M.", "United States", "Dental Rehabilitation"),
]):
    col, row = i % 2, i // 2
    x, y = 0.5 + col * 6.3, 1.6 + row * 1.9
    rect(s, x, y, 6.0, 1.7, WHITE)
    rect(s, x, y, 0.05, 1.7, GOLD, MSO_SHAPE.RECTANGLE)
    rect(s, x + 0.2, y + 0.05, 0.3, 0.25, GOLD, MSO_SHAPE.OVAL)
    tb(s, x + 0.2, y + 0.05, 0.3, 0.25, "\u275D", 10, NAVY, True, PP_ALIGN.CENTER)
    tb(s, x + 0.55, y + 0.1, 5.2, 0.8, quote, 9, TEXT, ls=1.45, it=True)
    divider(s, x + 0.25, y + 1.0, 2.5, GOLD)
    tb(s, x + 0.25, y + 1.1, 3, 0.25, f"\u2014 {name}", 9, NAVY, True)
    tb(s, x + 0.25, y + 1.35, 3, 0.2, f"{location}  |  {treatment}", 8, MID)


# ════════════════════════════════════════════════════════════════
# SLIDE 22 — CTA
# ════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(prs.slide_layouts[6]); bg(s, DEEP)
rect(s, 0, 0, 13.333, 0.06, GOLD, MSO_SHAPE.RECTANGLE)
corner_accents(s)
bg_circle(s, -2, -2, 6, DARK2)
bg_circle(s, 10, 4, 5, DARK3)

tb(s, 0, 1.5, 13.333, 0.7, "MedRouteIndia", 42, WHITE, True, PP_ALIGN.CENTER)
rect(s, 5.5, 2.25, 2.333, 0.04, GOLD, MSO_SHAPE.RECTANGLE)

tb(s, 1.5, 2.6, 10.333, 1,
   "Let's Make World-Class Healthcare\nAccessible to Everyone.",
   36, WHITE, True, PP_ALIGN.CENTER, ls=1.15)

tb(s, 2, 3.8, 9.333, 0.6,
   "We're raising $2M to capture the fastest-growing segment of the $88B medical "
   "tourism market. Join us in building the future of global healthcare access.",
   13, DIM, al=PP_ALIGN.CENTER, ls=1.5)

for i, (ic, label, value) in enumerate([
    ("\U0001F468\u200D\U0001F4BC", "Rahul Gautam", "CEO & Co-Founder"),
    ("\u2709\uFE0F", "Email", "rahul@medrouteindia.com"),
    ("\U0001F4DE", "Phone", "+91 123 456 7890"),
    ("\U0001F310", "Deck / Data Room", "medrouteindia.com/investors"),
]):
    x = 1.5 + i * 2.8
    rect(s, x, 4.7, 2.5, 1.0, DARK2)
    icon_circle(s, x + 0.95, 4.5, ic, GOLD, NAVY, 0.4)
    tb(s, x, 4.95, 2.5, 0.25, label.upper(), 8, GOLD_DIM, True, PP_ALIGN.CENTER)
    tb(s, x, 5.2, 2.5, 0.35, value, 10, WHITE, True, PP_ALIGN.CENTER)

rect(s, 3, 6.0, 7.333, 0.55, GOLD, MSO_SHAPE.ROUNDED_RECTANGLE)
tb(s, 3, 6.05, 7.333, 0.45,
   "NEXT STEP: Schedule a 30-minute deep-dive call",
   14, NAVY, True, PP_ALIGN.CENTER)

tb(s, 0, 6.8, 13.333, 0.3,
   "Confidential  |  MedRouteIndia Pvt. Ltd.  |  April 2026  |  For qualified investors only",
   8, DIMMER, al=PP_ALIGN.CENTER)


# ── SAVE ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "MedRouteIndia_Investor_Pitch_Deck.pptx")
prs.save(out)
print(f"\u2705 Investor pitch deck saved: {out}")
print(f"   Total slides: {len(prs.slides)}")
print(f"   Format: 16:9 Widescreen")
