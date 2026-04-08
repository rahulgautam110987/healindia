#!/usr/bin/env python3
"""
MedRouteIndia — Client Package Cost Calculator (Excel)
Put your actual costs in yellow cells → get min/max package range in USD + INR.
Covers: Treatment, Hospital Room, Hotel, Flights, Visa, Transfers, Meals, 
Coordinator, Insurance, Telemedicine, SIM, Recovery Tourism, Companion, Misc.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

wb = openpyxl.Workbook()

# ── Styles ──
NAVY = "0A1628"; GOLD = "C6A35B"; WHITE = "FFFFFF"
INPUT_BG = "FFF2CC"; LIGHT = "F5F5F5"; GREEN_BG = "E8F5E9"
GREEN = "1B7A3D"; RED = "C0392B"; BLUE = "2471A3"; MID_GRAY = "D9D9D9"
RANGE_LO = "E3F2FD"; RANGE_HI = "FFF3E0"

title_font = Font(name="Calibri", size=14, bold=True, color=WHITE)
h2 = Font(name="Calibri", size=11, bold=True, color=NAVY)
hdr_font = Font(name="Calibri", size=10, bold=True, color=WHITE)
body = Font(name="Calibri", size=10, color="333333")
body_b = Font(name="Calibri", size=10, bold=True, color="333333")
input_f = Font(name="Calibri", size=10, bold=True, color=NAVY)
green_b = Font(name="Calibri", size=11, bold=True, color=GREEN)
gold_b = Font(name="Calibri", size=11, bold=True, color=GOLD)
small_gray = Font(name="Calibri", size=9, italic=True, color="999999")
total_f = Font(name="Calibri", size=12, bold=True, color=WHITE)

navy_fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
gold_fill = PatternFill(start_color=GOLD, end_color=GOLD, fill_type="solid")
input_fill = PatternFill(start_color=INPUT_BG, end_color=INPUT_BG, fill_type="solid")
light_fill = PatternFill(start_color=LIGHT, end_color=LIGHT, fill_type="solid")
green_fill = PatternFill(start_color=GREEN_BG, end_color=GREEN_BG, fill_type="solid")
white_fill = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")
lo_fill = PatternFill(start_color=RANGE_LO, end_color=RANGE_LO, fill_type="solid")
hi_fill = PatternFill(start_color=RANGE_HI, end_color=RANGE_HI, fill_type="solid")
total_fill = PatternFill(start_color="1B7A3D", end_color="1B7A3D", fill_type="solid")

thin = Border(left=Side("thin", MID_GRAY), right=Side("thin", MID_GRAY),
              top=Side("thin", MID_GRAY), bottom=Side("thin", MID_GRAY))
ctr = Alignment(horizontal="center", vertical="center", wrap_text=True)
lft = Alignment(horizontal="left", vertical="center", wrap_text=True)
rgt = Alignment(horizontal="right", vertical="center")

USD = '#,##0'
INR = '[$₹-4009] #,##0'
PCT = '0.0%'
NUM = '#,##0'

def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

def title_row(ws, r, n, txt):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=n)
    c = ws.cell(r, 1, txt); c.font = title_font; c.fill = navy_fill; c.alignment = lft
    ws.row_dimensions[r].height = 30

def section_row(ws, r, n, txt):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=n)
    c = ws.cell(r, 1, txt); c.font = h2; c.fill = light_fill; c.alignment = lft
    ws.row_dimensions[r].height = 22

def hdr(ws, r, vals, fill=gold_fill):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = hdr_font; c.fill = fill; c.alignment = ctr; c.border = thin

def C(ws, r, c, val=None, fmt=None, font=body, fill=None, align=rgt, formula=None):
    cl = ws.cell(r, c)
    if formula: cl.value = formula
    elif val is not None: cl.value = val
    cl.font = font; cl.border = thin; cl.alignment = align
    if fill: cl.fill = fill
    if fmt: cl.number_format = fmt
    return cl

def inp(ws, r, c, val, fmt=USD):
    return C(ws, r, c, val=val, fmt=fmt, font=input_f, fill=input_fill)

def lbl(ws, r, c, txt, font=body):
    cl = ws.cell(r, c, txt); cl.font = font; cl.border = thin; cl.alignment = lft; return cl

# Column layout: A=Item, B=Low(USD), C=High(USD), D=Your Cost(USD), E=Low(INR), F=High(INR), G=Your Cost(INR), H=Notes
NCOLS = 8

# ════════════════════════════════════════════════════════════════
# SHEET 1: PACKAGE CALCULATOR
# ════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Package Calculator"
ws.sheet_properties.tabColor = GOLD
set_widths(ws, [34, 14, 14, 16, 16, 16, 18, 36])

title_row(ws, 1, NCOLS, "MEDROUTEINDIA — CLIENT PACKAGE COST CALCULATOR")
r = 2
ws.merge_cells(f"A{r}:H{r}")
ws.cell(r, 1, "⚠️  YELLOW = your input. Enter costs in USD columns → INR auto-calculates. Or vice-versa.").font = Font(name="Calibri", size=9, bold=True, color=RED)
r = 3

# FX Rate
section_row(ws, r, NCOLS, "CURRENCY SETTINGS"); r += 1
lbl(ws, r, 1, "USD → INR Exchange Rate")
inp(ws, r, 2, 83, NUM)
ws.merge_cells(f"C{r}:D{r}")
C(ws, r, 3, "Change this rate → all INR values update", font=small_gray, align=lft)
FX = f"$B${r}"
r += 2

# Headers
hdr(ws, r, ["Item", "Low (USD)", "High (USD)", "Your Cost (USD)", "Low (INR)", "High (INR)", "Your Cost (INR)", "Notes / Details"])
r += 1
HDR_R = r - 1  # header row for reference

# ────────────────────────────
# Helper to add a cost row: returns the row number used
# ────────────────────────────
all_rows = []  # track row numbers for totals

def cost_row(ws, r, item, low, high, your, note, fmt_usd=USD, is_per_unit=False, unit_label=""):
    lbl(ws, r, 1, item)
    inp(ws, r, 2, low, fmt_usd)    # Low USD
    inp(ws, r, 3, high, fmt_usd)   # High USD
    inp(ws, r, 4, your, fmt_usd)   # Your Cost USD
    C(ws, r, 5, fmt=INR, formula=f"B{r}*{FX}", fill=lo_fill)    # Low INR
    C(ws, r, 6, fmt=INR, formula=f"C{r}*{FX}", fill=hi_fill)    # High INR
    C(ws, r, 7, fmt=INR, formula=f"D{r}*{FX}", fill=green_fill) # Your INR
    C(ws, r, 8, note, font=small_gray, align=lft)
    all_rows.append(r)
    return r

# ── SECTION: TREATMENT ──
section_row(ws, r, NCOLS, "1. TREATMENT COST"); r += 1
R_TREAT = cost_row(ws, r, "Treatment / Procedure Fee", 800, 35000, 3500,
    "Core hospital + surgeon fee. Depends on procedure."); r += 1
R_HOSP_ROOM = cost_row(ws, r, "Hospital Room (per night)", 30, 250, 80,
    "General ward $30 | Semi-private $80 | Private $150 | Suite $250"); r += 1
R_HOSP_NIGHTS = r
lbl(ws, r, 1, "  Hospital Stay (nights)")
inp(ws, r, 2, 1, NUM); inp(ws, r, 3, 7, NUM); inp(ws, r, 4, 3, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
C(ws, r, 8, "Number of nights in hospital", font=small_gray, align=lft)
r += 1

R_HOSP_TOTAL = r
lbl(ws, r, 1, "  Hospital Room Total", font=body_b)
C(ws, r, 2, fmt=USD, font=body_b, formula=f"B{R_HOSP_ROOM}*B{R_HOSP_NIGHTS}")
C(ws, r, 3, fmt=USD, font=body_b, formula=f"C{R_HOSP_ROOM}*C{R_HOSP_NIGHTS}")
C(ws, r, 4, fmt=USD, font=body_b, formula=f"D{R_HOSP_ROOM}*D{R_HOSP_NIGHTS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
r += 1

R_MEDS = cost_row(ws, r, "Medicines & Consumables", 50, 500, 150,
    "Post-op meds, dressings, implants if any"); r += 1
R_DIAG = cost_row(ws, r, "Diagnostics / Lab Tests", 30, 300, 100,
    "Blood work, imaging, pre-op tests"); r += 2
# Remove R_HOSP_ROOM from all_rows (we use R_HOSP_TOTAL instead)
all_rows.remove(R_HOSP_ROOM)
# Remove R_HOSP_NIGHTS too
if R_HOSP_NIGHTS in all_rows: all_rows.remove(R_HOSP_NIGHTS)

# ── SECTION: ACCOMMODATION ──
section_row(ws, r, NCOLS, "2. HOTEL / ACCOMMODATION"); r += 1
R_HOTEL = cost_row(ws, r, "Hotel (per night)", 25, 200, 85,
    "3★ $25-45 | 4★ $60-100 | 5★ $120-200 (Taj/Oberoi)"); r += 1
R_HOTEL_NIGHTS = r
lbl(ws, r, 1, "  Hotel Stay (nights)")
inp(ws, r, 2, 2, NUM); inp(ws, r, 3, 14, NUM); inp(ws, r, 4, 5, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
C(ws, r, 8, "Pre + post hospital stay nights", font=small_gray, align=lft)
r += 1
R_HOTEL_TOTAL = r
lbl(ws, r, 1, "  Hotel Total", font=body_b)
C(ws, r, 2, fmt=USD, font=body_b, formula=f"B{R_HOTEL}*B{R_HOTEL_NIGHTS}")
C(ws, r, 3, fmt=USD, font=body_b, formula=f"C{R_HOTEL}*C{R_HOTEL_NIGHTS}")
C(ws, r, 4, fmt=USD, font=body_b, formula=f"D{R_HOTEL}*D{R_HOTEL_NIGHTS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
all_rows.remove(R_HOTEL)
r += 2

# ── SECTION: FLIGHTS ──
section_row(ws, r, NCOLS, "3. FLIGHTS (Round Trip)"); r += 1
R_FL_ECO = cost_row(ws, r, "Economy Class", 300, 900, 600,
    "Depends on origin: ME $300-500 | UK $500-700 | US $600-900"); r += 1
R_FL_PREM = cost_row(ws, r, "Premium Economy", 600, 1800, 1200,
    "Extra legroom, priority boarding, better meals"); r += 1
R_FL_BIZ = cost_row(ws, r, "Business Class", 1500, 5000, 3500,
    "Lie-flat, lounge access — Emirates/Qatar/Etihad/BA"); r += 1
# Only one flight class will be used — add a selector
R_FL_CHOICE = r
lbl(ws, r, 1, "Selected Flight Class (1=Eco,2=Prem,3=Biz)")
inp(ws, r, 2, 1, NUM); inp(ws, r, 3, 3, NUM); inp(ws, r, 4, 1, NUM)
C(ws, r, 8, "Enter 1, 2, or 3 to select flight class", font=small_gray, align=lft)
r += 1
R_FL_TOTAL = r
lbl(ws, r, 1, "  Flight Cost (selected class)", font=body_b)
for col_i, col_l in [(2,"B"),(3,"C"),(4,"D")]:
    C(ws, r, col_i, fmt=USD, font=body_b,
      formula=f"CHOOSE({col_l}{R_FL_CHOICE},{col_l}{R_FL_ECO},{col_l}{R_FL_PREM},{col_l}{R_FL_BIZ})")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
# Remove individual flight rows from total (we use selected)
for rr in [R_FL_ECO, R_FL_PREM, R_FL_BIZ]: all_rows.remove(rr)
r += 2

# ── SECTION: VISA ──
section_row(ws, r, NCOLS, "4. VISA & DOCUMENTATION"); r += 1
R_VISA = cost_row(ws, r, "e-Medical Visa Fee", 25, 80, 25,
    "India e-Medical Visa: $25 (most countries) — $80 (US/UK)"); r += 1
R_VISA_ASSIST = cost_row(ws, r, "Visa Assistance Service", 0, 50, 0,
    "MedRouteIndia provides free. Premium service $50."); r += 1
R_INVITE = cost_row(ws, r, "Hospital Invitation Letter", 0, 0, 0,
    "Provided free by MedRouteIndia / hospital"); r += 2

# ── SECTION: TRANSFERS ──
section_row(ws, r, NCOLS, "5. AIRPORT & LOCAL TRANSFERS"); r += 1
R_AP_PICK = cost_row(ws, r, "Airport Pickup (one way)", 15, 60, 20,
    "Sedan $15-20 | SUV $30-40 | Luxury $50-60"); r += 1
R_AP_DROP = cost_row(ws, r, "Airport Drop (one way)", 15, 60, 20,
    "Same as pickup — sedan to luxury"); r += 1
R_LOCAL = cost_row(ws, r, "Local Transfers (hotel↔hospital)", 5, 30, 10,
    "Per trip. Budget 4-6 trips."); r += 1
R_LOCAL_TRIPS = r
lbl(ws, r, 1, "  Number of Local Trips")
inp(ws, r, 2, 3, NUM); inp(ws, r, 3, 8, NUM); inp(ws, r, 4, 5, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
r += 1
R_LOCAL_TOTAL = r
lbl(ws, r, 1, "  Local Transfers Total", font=body_b)
C(ws, r, 2, fmt=USD, font=body_b, formula=f"B{R_LOCAL}*B{R_LOCAL_TRIPS}")
C(ws, r, 3, fmt=USD, font=body_b, formula=f"C{R_LOCAL}*C{R_LOCAL_TRIPS}")
C(ws, r, 4, fmt=USD, font=body_b, formula=f"D{R_LOCAL}*D{R_LOCAL_TRIPS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
all_rows.remove(R_LOCAL)
r += 2

# ── SECTION: MEALS ──
section_row(ws, r, NCOLS, "6. MEALS & FOOD"); r += 1
R_MEAL_HOSP = cost_row(ws, r, "Hospital Meals (per day, included)", 0, 0, 0,
    "Usually included in hospital room charge"); r += 1
R_MEAL_OUT = cost_row(ws, r, "Outside Meals (per day)", 8, 40, 15,
    "Street food $8 | Mid-range $15 | Fine dining $40"); r += 1
R_MEAL_DAYS = r
lbl(ws, r, 1, "  Meal Days (outside hospital)")
inp(ws, r, 2, 2, NUM); inp(ws, r, 3, 14, NUM); inp(ws, r, 4, 5, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
r += 1
R_MEAL_TOTAL = r
lbl(ws, r, 1, "  Meals Total", font=body_b)
C(ws, r, 2, fmt=USD, font=body_b, formula=f"B{R_MEAL_OUT}*B{R_MEAL_DAYS}")
C(ws, r, 3, fmt=USD, font=body_b, formula=f"C{R_MEAL_OUT}*C{R_MEAL_DAYS}")
C(ws, r, 4, fmt=USD, font=body_b, formula=f"D{R_MEAL_OUT}*D{R_MEAL_DAYS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
all_rows.remove(R_MEAL_HOSP)
all_rows.remove(R_MEAL_OUT)
r += 2

# ── SECTION: CARE COORDINATOR ──
section_row(ws, r, NCOLS, "7. CARE COORDINATOR & SUPPORT"); r += 1
R_COORD = cost_row(ws, r, "Dedicated Care Coordinator", 100, 300, 200,
    "Basic $100 (hospital only) | Full $200 (24/7) | Premium $300"); r += 1
R_TRANS = cost_row(ws, r, "Translation / Interpreter", 0, 100, 0,
    "English-speaking cities: free. Arabic/Russian: $50-100"); r += 2

# ── SECTION: INSURANCE ──
section_row(ws, r, NCOLS, "8. TRAVEL & MEDICAL INSURANCE"); r += 1
R_INS = cost_row(ws, r, "Travel + Medical Insurance", 40, 250, 80,
    "Basic $40-80 | Standard $80-120 | Comprehensive $150-250"); r += 2

# ── SECTION: TELEMEDICINE ──
section_row(ws, r, NCOLS, "9. TELEMEDICINE FOLLOW-UP"); r += 1
R_TELE = cost_row(ws, r, "Post-Treatment Telemedicine", 0, 200, 75,
    "3-mo FREE | 6-mo $75 | 12-mo $150-200"); r += 2

# ── SECTION: SIM & CONNECTIVITY ──
section_row(ws, r, NCOLS, "10. SIM CARD & CONNECTIVITY"); r += 1
R_SIM = cost_row(ws, r, "Indian SIM + Data Pack", 5, 20, 10,
    "Basic $5 | Unlimited data $10 | Data + Intl calling $20"); r += 2

# ── SECTION: COMPANION ──
section_row(ws, r, NCOLS, "11. COMPANION / ATTENDANT"); r += 1
R_COMP_VIS = cost_row(ws, r, "Companion Visa", 25, 80, 25,
    "Attendant visa for spouse/family"); r += 1
R_COMP_HOTEL = cost_row(ws, r, "Companion Hotel (shared room surcharge)", 0, 50, 0,
    "$0 if shared room, $30-50/night if separate room"); r += 1
R_COMP_MEAL = cost_row(ws, r, "Companion Meals (per day)", 8, 40, 15,
    "Same rates as patient meals"); r += 1
R_COMP_DAYS = r
lbl(ws, r, 1, "  Companion Stay (days)")
inp(ws, r, 2, 0, NUM); inp(ws, r, 3, 14, NUM); inp(ws, r, 4, 0, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
C(ws, r, 8, "Set to 0 if no companion", font=small_gray, align=lft)
r += 1
R_COMP_TOTAL = r
lbl(ws, r, 1, "  Companion Total", font=body_b)
for col_i, col_l in [(2,"B"),(3,"C"),(4,"D")]:
    C(ws, r, col_i, fmt=USD, font=body_b,
      formula=f"{col_l}{R_COMP_VIS}+({col_l}{R_COMP_HOTEL}+{col_l}{R_COMP_MEAL})*{col_l}{R_COMP_DAYS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
for rr in [R_COMP_VIS, R_COMP_HOTEL, R_COMP_MEAL]: all_rows.remove(rr)
r += 2

# ── SECTION: RECOVERY & TOURISM ──
section_row(ws, r, NCOLS, "12. RECOVERY & TOURISM (OPTIONAL)"); r += 1
R_AYUR = cost_row(ws, r, "Kerala Ayurveda Retreat (5 nights)", 0, 1000, 0,
    "Panchakarma, yoga. $600-1000. Set 0 if not needed."); r += 1
R_GOA = cost_row(ws, r, "Goa Beach Recovery (5 nights)", 0, 800, 0,
    "Beachside resort + spa. $400-800."); r += 1
R_TOUR = cost_row(ws, r, "Heritage City Tour (2 days)", 0, 300, 0,
    "Taj Mahal / Jaipur / Old Delhi. $150-300."); r += 1
R_PHYSIO = cost_row(ws, r, "Private Physiotherapy (per session)", 0, 50, 0,
    "For ortho patients. $25-50/session."); r += 1
R_PHYSIO_SESS = r
lbl(ws, r, 1, "  Physio Sessions")
inp(ws, r, 2, 0, NUM); inp(ws, r, 3, 10, NUM); inp(ws, r, 4, 0, NUM)
C(ws, r, 5, fmt=NUM, formula=f"B{r}"); C(ws, r, 6, fmt=NUM, formula=f"C{r}"); C(ws, r, 7, fmt=NUM, formula=f"D{r}")
r += 1
R_PHYSIO_TOTAL = r
lbl(ws, r, 1, "  Physio Total", font=body_b)
C(ws, r, 2, fmt=USD, font=body_b, formula=f"B{R_PHYSIO}*B{R_PHYSIO_SESS}")
C(ws, r, 3, fmt=USD, font=body_b, formula=f"C{R_PHYSIO}*C{R_PHYSIO_SESS}")
C(ws, r, 4, fmt=USD, font=body_b, formula=f"D{R_PHYSIO}*D{R_PHYSIO_SESS}")
C(ws, r, 5, fmt=INR, font=body_b, formula=f"B{r}*{FX}", fill=lo_fill)
C(ws, r, 6, fmt=INR, font=body_b, formula=f"C{r}*{FX}", fill=hi_fill)
C(ws, r, 7, fmt=INR, font=body_b, formula=f"D{r}*{FX}", fill=green_fill)
all_rows.append(r)
all_rows.remove(R_PHYSIO)
r += 2

# ── SECTION: MISCELLANEOUS ──
section_row(ws, r, NCOLS, "13. MISCELLANEOUS"); r += 1
R_MISC1 = cost_row(ws, r, "Currency Exchange / ATM Fees", 5, 30, 10,
    "Budget for cash needs during stay"); r += 1
R_MISC2 = cost_row(ws, r, "Local Shopping / Personal", 0, 200, 50,
    "Pharmacy, clothing, gifts, local transport"); r += 1
R_MISC3 = cost_row(ws, r, "Contingency / Buffer", 50, 500, 100,
    "Unexpected costs — always budget 5-10% buffer"); r += 2

# ══════════════════════════════════════════════════════════════
# GRAND TOTAL
# ══════════════════════════════════════════════════════════════
r += 1
R_TOTAL = r
ws.row_dimensions[r].height = 32

# Build SUM formulas from all_rows
sum_cells_b = "+".join([f"B{rr}" for rr in all_rows])
sum_cells_c = "+".join([f"C{rr}" for rr in all_rows])
sum_cells_d = "+".join([f"D{rr}" for rr in all_rows])

ws.merge_cells(f"A{r}:A{r}")
cl = ws.cell(r, 1, "TOTAL PACKAGE COST"); cl.font = total_f; cl.fill = total_fill; cl.alignment = lft; cl.border = thin
C(ws, r, 2, fmt=USD, font=total_f, fill=total_fill, formula=sum_cells_b)
C(ws, r, 3, fmt=USD, font=total_f, fill=total_fill, formula=sum_cells_c)
C(ws, r, 4, fmt=USD, font=total_f, fill=total_fill, formula=sum_cells_d)
C(ws, r, 5, fmt=INR, font=total_f, fill=total_fill, formula=f"B{r}*{FX}")
C(ws, r, 6, fmt=INR, font=total_f, fill=total_fill, formula=f"C{r}*{FX}")
C(ws, r, 7, fmt=INR, font=total_f, fill=total_fill, formula=f"D{r}*{FX}")
C(ws, r, 8, "← YOUR PACKAGE PRICE", font=Font(name="Calibri", size=10, bold=True, color=GREEN), fill=green_fill, align=lft)
r += 2

# ── Price Range Summary ──
section_row(ws, r, NCOLS, "PACKAGE RANGE SUMMARY"); r += 1
lbl(ws, r, 1, "Minimum Package (USD)", font=green_b)
C(ws, r, 2, fmt=USD, font=green_b, fill=green_fill, formula=f"B{R_TOTAL}")
lbl(ws, r, 4, "Minimum Package (INR)", font=green_b)
C(ws, r, 5, fmt=INR, font=green_b, fill=green_fill, formula=f"E{R_TOTAL}")
r += 1
lbl(ws, r, 1, "Maximum Package (USD)", font=Font(name="Calibri", size=11, bold=True, color=RED))
C(ws, r, 2, fmt=USD, font=Font(name="Calibri", size=11, bold=True, color=RED), formula=f"C{R_TOTAL}")
lbl(ws, r, 4, "Maximum Package (INR)", font=Font(name="Calibri", size=11, bold=True, color=RED))
C(ws, r, 5, fmt=INR, font=Font(name="Calibri", size=11, bold=True, color=RED), formula=f"F{R_TOTAL}")
r += 1
lbl(ws, r, 1, "YOUR QUOTED PRICE (USD)", font=Font(name="Calibri", size=12, bold=True, color=GOLD))
C(ws, r, 2, fmt=USD, font=Font(name="Calibri", size=12, bold=True, color=GOLD), fill=green_fill, formula=f"D{R_TOTAL}")
lbl(ws, r, 4, "YOUR QUOTED PRICE (INR)", font=Font(name="Calibri", size=12, bold=True, color=GOLD))
C(ws, r, 5, fmt=INR, font=Font(name="Calibri", size=12, bold=True, color=GOLD), fill=green_fill, formula=f"G{R_TOTAL}")
r += 2

# ── Margin Calculator ──
section_row(ws, r, NCOLS, "YOUR MARGIN CALCULATOR"); r += 1
R_CLIENT_PRICE = r
lbl(ws, r, 1, "Price You Charge the Client (USD)")
inp(ws, r, 2, 5000, USD)
C(ws, r, 5, fmt=INR, formula=f"B{r}*{FX}", fill=input_fill)
C(ws, r, 8, "Enter your quoted price to the client", font=small_gray, align=lft)
r += 1
R_YOUR_COST = r
lbl(ws, r, 1, "Your Total Cost (USD)")
C(ws, r, 2, fmt=USD, formula=f"D{R_TOTAL}")
C(ws, r, 5, fmt=INR, formula=f"G{R_TOTAL}")
r += 1
R_YOUR_MARGIN = r
lbl(ws, r, 1, "Your Margin (USD)", font=green_b)
C(ws, r, 2, fmt=USD, font=green_b, fill=green_fill, formula=f"B{R_CLIENT_PRICE}-B{R_YOUR_COST}")
C(ws, r, 5, fmt=INR, font=green_b, fill=green_fill, formula=f"B{r}*{FX}")
r += 1
R_YOUR_MARGIN_PCT = r
lbl(ws, r, 1, "Margin %", font=green_b)
C(ws, r, 2, fmt=PCT, font=green_b, fill=green_fill, formula=f"B{R_YOUR_MARGIN}/B{R_CLIENT_PRICE}")
r += 2

# ── Home Country Comparison ──
section_row(ws, r, NCOLS, "SAVINGS vs HOME COUNTRY"); r += 1
R_HOME = r
lbl(ws, r, 1, "Same Treatment in Home Country (USD)")
inp(ws, r, 2, 25000, USD)
C(ws, r, 5, fmt=INR, formula=f"B{r}*{FX}", fill=input_fill)
C(ws, r, 8, "What would this cost in USA/UK/Australia?", font=small_gray, align=lft)
r += 1
lbl(ws, r, 1, "Patient Saves (USD)", font=green_b)
C(ws, r, 2, fmt=USD, font=green_b, fill=green_fill, formula=f"B{R_HOME}-B{R_CLIENT_PRICE}")
C(ws, r, 5, fmt=INR, font=green_b, fill=green_fill, formula=f"B{r}*{FX}")
r += 1
lbl(ws, r, 1, "Patient Saves (%)", font=green_b)
C(ws, r, 2, fmt=PCT, font=green_b, fill=green_fill, formula=f"(B{R_HOME}-B{R_CLIENT_PRICE})/B{R_HOME}")


# ════════════════════════════════════════════════════════════════
# SHEET 2: QUICK REFERENCE — Treatment Base Prices
# ════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("Treatment Prices")
ws2.sheet_properties.tabColor = "E74C3C"
set_widths(ws2, [28, 14, 14, 14, 14, 14, 14])

title_row(ws2, 1, 7, "TREATMENT BASE PRICES — QUICK REFERENCE")
ws2.cell(2, 1, f"INR prices = USD × ₹ rate from Package Calculator!B4").font = small_gray
ws2.merge_cells("A2:G2")
r = 3
FX2 = "'Package Calculator'!$B$4"
hdr(ws2, r, ["Treatment", "India Low (USD)", "India High (USD)", "USA (USD)", "UK (USD)", "India Low (INR)", "India High (INR)"]); r += 1

treatments = [
    ("Hair Transplant — FUE 2000", 1000, 1500, 12000, 10000),
    ("Hair Transplant — FUE 3000", 1500, 2200, 15000, 12000),
    ("Hair Transplant — DHI 3500", 2000, 3000, 18000, 14000),
    ("Hair Transplant — Mega 5000+", 2500, 4000, 22000, 16000),
    ("Dental — Single Implant", 400, 700, 5000, 3000),
    ("Dental — Veneers (per tooth)", 150, 350, 1500, 800),
    ("Dental — All-on-4", 3000, 5000, 25000, 15000),
    ("Dental — Full Mouth Rehab", 4000, 7000, 30000, 20000),
    ("Dental — Root Canal + Crown", 100, 200, 2000, 1000),
    ("Knee Replacement (single)", 4000, 6000, 35000, 20000),
    ("Knee Replacement (bilateral)", 6500, 9000, 50000, 35000),
    ("Hip Replacement", 5500, 8000, 45000, 30000),
    ("Cardiac Bypass (CABG)", 5000, 9000, 120000, 40000),
    ("Angioplasty + Stent", 2500, 4500, 30000, 15000),
    ("Heart Valve Replacement", 6000, 10000, 80000, 35000),
    ("IVF (per cycle)", 2500, 4000, 15000, 8000),
    ("Rhinoplasty", 1800, 3500, 12000, 8000),
    ("Liposuction", 1500, 3000, 10000, 7000),
    ("Tummy Tuck", 2500, 4500, 12000, 8000),
    ("Mommy Makeover (combo)", 4000, 7000, 20000, 15000),
    ("Gastric Sleeve", 3500, 5500, 20000, 12000),
    ("Gastric Bypass", 4500, 7000, 25000, 15000),
    ("LASIK (both eyes)", 500, 1000, 4000, 3000),
    ("Cataract Surgery (per eye)", 800, 1500, 5000, 3500),
    ("Spine — Disc Replacement", 5000, 8000, 50000, 30000),
    ("Spine — Fusion", 4000, 7000, 40000, 25000),
    ("Liver Transplant", 25000, 45000, 300000, 150000),
    ("Kidney Transplant", 12000, 20000, 200000, 80000),
    ("Bone Marrow Transplant", 15000, 30000, 250000, 100000),
    ("Cancer — Chemotherapy (cycle)", 500, 1500, 10000, 5000),
    ("Cancer — CyberKnife/Radiation", 3000, 6000, 40000, 20000),
    ("Executive Health Check", 300, 600, 3000, 2000),
    ("Second Opinion (remote)", 50, 150, 500, 300),
]

for t in treatments:
    lbl(ws2, r, 1, t[0])
    inp(ws2, r, 2, t[1], USD)
    inp(ws2, r, 3, t[2], USD)
    C(ws2, r, 4, t[3], fmt=USD)
    C(ws2, r, 5, t[4], fmt=USD)
    C(ws2, r, 6, fmt=INR, formula=f"B{r}*{FX2}")
    C(ws2, r, 7, fmt=INR, formula=f"C{r}*{FX2}")
    r += 1


# ── SAVE ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MedRouteIndia_Package_Calculator.xlsx")
wb.save(out)
print(f"✅ Package calculator saved: {out}")
print(f"   Sheets: {[s.title for s in wb.worksheets]}")
