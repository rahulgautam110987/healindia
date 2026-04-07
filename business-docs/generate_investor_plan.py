#!/usr/bin/env python3
"""
BharatHeals — Investor-Grade Business Plan (Excel)
All numbers are FORMULA-BASED. Change any yellow input cell and everything recalculates.
Dual currency: USD + INR.
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os, string

wb = openpyxl.Workbook()

# ── Styles ──
NAVY = "0A1628"
GOLD = "C6A35B"
WHITE = "FFFFFF"
CREAM = "FFF9E6"       # Yellow tint for editable cells
INPUT_BG = "FFF2CC"     # Strong yellow for input cells
LIGHT = "F5F5F5"
GREEN_BG = "E8F5E9"
GREEN = "1B7A3D"
RED = "C0392B"
BLUE = "2471A3"
MID_GRAY = "D9D9D9"

title_font = Font(name="Calibri", size=14, bold=True, color=WHITE)
h2_font = Font(name="Calibri", size=12, bold=True, color=NAVY)
header_font = Font(name="Calibri", size=10, bold=True, color=WHITE)
sub_font = Font(name="Calibri", size=10, bold=True, color=NAVY)
body = Font(name="Calibri", size=10, color="333333")
body_b = Font(name="Calibri", size=10, bold=True, color="333333")
gold_b = Font(name="Calibri", size=10, bold=True, color=GOLD)
green_b = Font(name="Calibri", size=10, bold=True, color=GREEN)
red_b = Font(name="Calibri", size=10, bold=True, color=RED)
blue_b = Font(name="Calibri", size=10, bold=True, color=BLUE)
input_font = Font(name="Calibri", size=10, bold=True, color=NAVY)
pct_font = Font(name="Calibri", size=10, color="333333")

navy_fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
gold_fill = PatternFill(start_color=GOLD, end_color=GOLD, fill_type="solid")
input_fill = PatternFill(start_color=INPUT_BG, end_color=INPUT_BG, fill_type="solid")
light_fill = PatternFill(start_color=LIGHT, end_color=LIGHT, fill_type="solid")
green_fill = PatternFill(start_color=GREEN_BG, end_color=GREEN_BG, fill_type="solid")
white_fill = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")

thin = Border(
    left=Side("thin", MID_GRAY), right=Side("thin", MID_GRAY),
    top=Side("thin", MID_GRAY), bottom=Side("thin", MID_GRAY))
ctr = Alignment(horizontal="center", vertical="center", wrap_text=True)
lft = Alignment(horizontal="left", vertical="center", wrap_text=True)
rgt = Alignment(horizontal="right", vertical="center")

USD = '#,##0'
USD2 = '#,##0.00'
INR = '[$₹-4009] #,##0'
INR_L = '[$₹-4009] #,##,##0'  # Lakhs style
PCT = '0.0%'
PCT0 = '0%'
NUM = '#,##0'
X_FMT = '0.0"x"'


def title_row(ws, r, ncols, txt):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
    c = ws.cell(r, 1, txt); c.font = title_font; c.fill = navy_fill; c.alignment = lft
    ws.row_dimensions[r].height = 30

def section_row(ws, r, ncols, txt):
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=ncols)
    c = ws.cell(r, 1, txt); c.font = h2_font; c.fill = light_fill; c.alignment = lft
    ws.row_dimensions[r].height = 24

def hdr(ws, r, vals, fill=gold_fill):
    for i, v in enumerate(vals, 1):
        c = ws.cell(r, i, v); c.font = header_font; c.fill = fill; c.alignment = ctr; c.border = thin
    ws.row_dimensions[r].height = 24

def cell(ws, r, c, val=None, fmt=None, font=body, fill=None, align=rgt, formula=None):
    cl = ws.cell(r, c)
    if formula:
        cl.value = formula
    elif val is not None:
        cl.value = val
    cl.font = font; cl.border = thin; cl.alignment = align
    if fill: cl.fill = fill
    if fmt: cl.number_format = fmt
    return cl

def input_cell(ws, r, c, val, fmt=None):
    """Yellow highlighted editable input cell"""
    return cell(ws, r, c, val=val, fmt=fmt, font=input_font, fill=input_fill)

def label_cell(ws, r, c, txt, font=body, indent=0):
    cl = ws.cell(r, c, ("  " * indent) + txt)
    cl.font = font; cl.border = thin; cl.alignment = lft
    return cl

def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w

# Helper: cell reference on another sheet
def ref(sheet, r, c):
    col = get_column_letter(c)
    return f"'{sheet}'!{col}{r}"

# ════════════════════════════════════════════════════════════════
# SHEET 1: ASSUMPTIONS & INPUTS (the control panel)
# ════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "Assumptions"
ws.sheet_properties.tabColor = GOLD
set_widths(ws, [38, 16, 16, 16, 16, 16, 16, 30])

title_row(ws, 1, 8, "BHARATHEALS — KEY ASSUMPTIONS & INPUTS")
ws.cell(2, 1, "⚠️  YELLOW CELLS = EDITABLE INPUTS. Change any yellow cell and all sheets recalculate.").font = Font(name="Calibri", size=9, bold=True, color=RED)
ws.merge_cells("A2:H2")

# -- Currency --
r = 4
section_row(ws, r, 8, "CURRENCY"); r += 1
label_cell(ws, r, 1, "USD to INR Exchange Rate"); input_cell(ws, r, 2, 83, NUM)
A_FX = f"Assumptions!B{r}"; r += 2  # row 5 => B5

# -- Patient Volume --
section_row(ws, r, 8, "PATIENT VOLUME"); r += 1
hdr(ws, r, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "", "Notes"]); r += 1
R_PAT = r  # row 9
label_cell(ws, r, 1, "New Patients")
input_cell(ws, r, 2, 800, NUM)
input_cell(ws, r, 3, 1800, NUM)
input_cell(ws, r, 4, 3500, NUM)
input_cell(ws, r, 5, 6000, NUM)
input_cell(ws, r, 6, 10000, NUM)
cell(ws, r, 8, "Editable — change patient targets", font=Font(name="Calibri", size=9, italic=True, color="999999"))
r += 1
R_GR = r
label_cell(ws, r, 1, "YoY Growth Rate")
cell(ws, r, 2, "-", font=body)
for c in range(3, 7):
    cell(ws, r, c, fmt=PCT, formula=f"({get_column_letter(c)}{R_PAT}/{get_column_letter(c-1)}{R_PAT})-1")
r += 2

# -- Pricing --
section_row(ws, r, 8, "PRICING & REVENUE DRIVERS"); r += 1
hdr(ws, r, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "", "Notes"]); r += 1
R_ATV = r
label_cell(ws, r, 1, "Avg Treatment Value (USD)")
for i, v in enumerate([7500, 7800, 8000, 8200, 8500]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_COMM = r - 1 + 1  # next row
label_cell(ws, R_COMM, 1, "Hospital Commission Rate")
for i, v in enumerate([0.175, 0.175, 0.175, 0.175, 0.175]):
    input_cell(ws, R_COMM, i+2, v, PCT)
r = R_COMM + 1

R_PKG_RATE = r
label_cell(ws, r, 1, "Package Attach Rate (% patients)")
for i, v in enumerate([0.55, 0.60, 0.65, 0.70, 0.72]):
    input_cell(ws, r, i+2, v, PCT); r += 1

R_PKG_REV = r
label_cell(ws, r, 1, "Avg Package Revenue (USD)")
for i, v in enumerate([600, 650, 700, 750, 800]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_TELE_RATE = r
label_cell(ws, r, 1, "Telemedicine Attach Rate")
for i, v in enumerate([0.40, 0.50, 0.60, 0.65, 0.70]):
    input_cell(ws, r, i+2, v, PCT); r += 1

R_TELE_REV = r
label_cell(ws, r, 1, "Avg Telemedicine Revenue (USD)")
for i, v in enumerate([100, 120, 140, 150, 160]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_ANC_REV = r
label_cell(ws, r, 1, "Avg Ancillary Revenue (insurance, tourism)")
for i, v in enumerate([50, 60, 70, 80, 90]):
    input_cell(ws, r, i+2, v, USD); r += 2

# -- Costs --
section_row(ws, r, 8, "COST ASSUMPTIONS"); r += 1
hdr(ws, r, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "", "Notes"]); r += 1

R_CAC = r
label_cell(ws, r, 1, "Customer Acquisition Cost (USD)")
for i, v in enumerate([225, 190, 155, 135, 120]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_ONBOARD = r
label_cell(ws, r, 1, "Onboarding Cost per Patient (USD)")
for i, v in enumerate([50, 45, 40, 35, 30]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_OPS = r
label_cell(ws, r, 1, "Operations/Coordination per Patient (USD)")
for i, v in enumerate([120, 110, 100, 90, 80]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_TECH_PAT = r
label_cell(ws, r, 1, "Technology Cost per Patient (USD)")
for i, v in enumerate([30, 25, 20, 15, 12]):
    input_cell(ws, r, i+2, v, USD); r += 2

# -- Team --
section_row(ws, r, 8, "TEAM & SALARIES"); r += 1
hdr(ws, r, ["Role", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Avg CTC (USD)", "Avg CTC (INR)"]); r += 1

R_TEAM_START = r
team_roles = [
    ("Founders / Leadership", [2,2,3,4,5], 60000),
    ("Medical Consultants", [2,4,6,8,12], 18000),
    ("Care Coordinators", [1,3,5,8,12], 12000),
    ("Tech / AI Engineers", [2,3,4,5,6], 30000),
    ("Digital Marketing", [1,2,3,4,5], 15000),
    ("Content & SEO", [0,1,2,2,3], 12000),
    ("Finance & Ops", [0,1,1,2,2], 15000),
]
for role, counts, ctc in team_roles:
    label_cell(ws, r, 1, role)
    for i, c in enumerate(counts):
        input_cell(ws, r, i+2, c, NUM)
    input_cell(ws, r, 7, ctc, USD)
    cell(ws, r, 8, fmt=INR, formula=f"G{r}*{A_FX}")
    r += 1
R_TEAM_END = r - 1

# Total headcount
R_HC = r
label_cell(ws, r, 1, "Total Headcount", font=body_b)
for c in range(2, 7):
    cell(ws, r, c, fmt=NUM, font=body_b, formula=f"SUM({get_column_letter(c)}{R_TEAM_START}:{get_column_letter(c)}{R_TEAM_END})")
r += 1

# Total salary cost
R_SAL = r
label_cell(ws, r, 1, "Total Salary Cost (USD)", font=body_b)
for c in range(2, 7):
    cell(ws, r, c, fmt=USD, font=body_b,
         formula=f"SUMPRODUCT({get_column_letter(c)}{R_TEAM_START}:{get_column_letter(c)}{R_TEAM_END},$G${R_TEAM_START}:$G${R_TEAM_END})")
r += 1
R_SAL_INR = r
label_cell(ws, r, 1, "Total Salary Cost (INR)", font=body_b)
for c in range(2, 7):
    cell(ws, r, c, fmt=INR, font=body_b, formula=f"{get_column_letter(c)}{R_SAL}*{A_FX}")
r += 2

# -- Fixed Costs --
section_row(ws, r, 8, "OTHER FIXED COSTS (USD / year)"); r += 1
hdr(ws, r, ["Item", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "", ""]); r += 1
R_OFFICE = r
label_cell(ws, r, 1, "Office & Admin")
for i, v in enumerate([60000, 90000, 130000, 180000, 250000]):
    input_cell(ws, r, i+2, v, USD); r += 1
R_LEGAL = r
label_cell(ws, r, 1, "Legal & Compliance")
for i, v in enumerate([20000, 30000, 50000, 70000, 90000]):
    input_cell(ws, r, i+2, v, USD); r += 1
R_MISC = r
label_cell(ws, r, 1, "Miscellaneous / Contingency")
for i, v in enumerate([30000, 40000, 60000, 80000, 100000]):
    input_cell(ws, r, i+2, v, USD); r += 1

R_TAX = r
label_cell(ws, r, 1, "Corporate Tax Rate")
input_cell(ws, r, 2, 0.25, PCT)
cell(ws, r, 8, "Section 115BAA — 25% for new companies", font=Font(name="Calibri", size=9, italic=True, color="999999"))
r += 1
R_DISC = r
label_cell(ws, r, 1, "Discount Rate (for DCF)")
input_cell(ws, r, 2, 0.20, PCT)

LAST_ASSUM = r

# ════════════════════════════════════════════════════════════════
# SHEET 2: 5-YEAR P&L (USD)
# ════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("P&L (USD)")
ws2.sheet_properties.tabColor = NAVY
set_widths(ws2, [38, 16, 16, 16, 16, 16])

title_row(ws2, 1, 6, "PROFIT & LOSS STATEMENT — USD")
r = 3
hdr(ws2, r, ["", "Year 1 (2026)", "Year 2 (2027)", "Year 3 (2028)", "Year 4 (2029)", "Year 5 (2030)"]); r += 1

# -- Revenue --
section_row(ws2, r, 6, "REVENUE"); r += 1

# Patients
R2_PAT = r
label_cell(ws2, r, 1, "Patients")
for c in range(2, 7):
    cell(ws2, r, c, fmt=NUM, formula=f"Assumptions!{get_column_letter(c)}{R_PAT}")
r += 1

# Gross Treatment Volume
R2_GTV = r
label_cell(ws2, r, 1, "Gross Treatment Volume (GTV)")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_ATV}")
r += 1

# Hospital Commission
R2_COMM = r
label_cell(ws2, r, 1, "  Hospital Commission Revenue")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_GTV}*Assumptions!{get_column_letter(c)}{R_COMM}")
r += 1

# Package Revenue
R2_PKG = r
label_cell(ws2, r, 1, "  Package Revenue")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD,
         formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_PKG_RATE}*Assumptions!{get_column_letter(c)}{R_PKG_REV}")
r += 1

# Telemedicine Revenue
R2_TELE = r
label_cell(ws2, r, 1, "  Telemedicine Revenue")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD,
         formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_TELE_RATE}*Assumptions!{get_column_letter(c)}{R_TELE_REV}")
r += 1

# Ancillary Revenue
R2_ANC = r
label_cell(ws2, r, 1, "  Ancillary Revenue (insurance, tourism)")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_ANC_REV}")
r += 1

# TOTAL REVENUE
R2_REV = r
label_cell(ws2, r, 1, "TOTAL REVENUE", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=body_b, fill=green_fill,
         formula=f"SUM({get_column_letter(c)}{R2_COMM}:{get_column_letter(c)}{R2_ANC})")
r += 1

# Revenue Growth
R2_REV_GR = r
label_cell(ws2, r, 1, "  Revenue Growth YoY")
cell(ws2, r, 2, "-", font=body)
for c in range(3, 7):
    cell(ws2, r, c, fmt=PCT, formula=f"({get_column_letter(c)}{R2_REV}/{get_column_letter(c-1)}{R2_REV})-1")
r += 2

# -- COGS --
section_row(ws2, r, 6, "COST OF REVENUE (VARIABLE)"); r += 1
R2_CAC_TOT = r
label_cell(ws2, r, 1, "  Marketing & Acquisition (CAC × Patients)")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_CAC}")
r += 1

R2_ONBOARD_TOT = r
label_cell(ws2, r, 1, "  Onboarding Cost")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_ONBOARD}")
r += 1

R2_OPS_TOT = r
label_cell(ws2, r, 1, "  Operations & Coordination")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_OPS}")
r += 1

R2_TECH_TOT = r
label_cell(ws2, r, 1, "  Technology (per patient)")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_PAT}*Assumptions!{get_column_letter(c)}{R_TECH_PAT}")
r += 1

R2_COGS = r
label_cell(ws2, r, 1, "TOTAL VARIABLE COSTS", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=body_b,
         formula=f"SUM({get_column_letter(c)}{R2_CAC_TOT}:{get_column_letter(c)}{R2_TECH_TOT})")
r += 1

R2_GP = r
label_cell(ws2, r, 1, "GROSS PROFIT", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=green_b, fill=green_fill,
         formula=f"{get_column_letter(c)}{R2_REV}-{get_column_letter(c)}{R2_COGS}")
r += 1

R2_GPM = r
label_cell(ws2, r, 1, "  Gross Margin %")
for c in range(2, 7):
    cell(ws2, r, c, fmt=PCT, formula=f"{get_column_letter(c)}{R2_GP}/{get_column_letter(c)}{R2_REV}")
r += 2

# -- OpEx --
section_row(ws2, r, 6, "OPERATING EXPENSES (FIXED)"); r += 1
R2_SAL = r
label_cell(ws2, r, 1, "  Salaries & Benefits")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_SAL}")
r += 1

R2_OFFICE = r
label_cell(ws2, r, 1, "  Office & Admin")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_OFFICE}")
r += 1

R2_LEGAL = r
label_cell(ws2, r, 1, "  Legal & Compliance")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_LEGAL}")
r += 1

R2_MISC = r
label_cell(ws2, r, 1, "  Miscellaneous / Contingency")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_MISC}")
r += 1

R2_OPEX = r
label_cell(ws2, r, 1, "TOTAL OPERATING EXPENSES", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=body_b,
         formula=f"SUM({get_column_letter(c)}{R2_SAL}:{get_column_letter(c)}{R2_MISC})")
r += 2

# -- EBITDA --
R2_EBITDA = r
label_cell(ws2, r, 1, "EBITDA", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=green_b, fill=green_fill,
         formula=f"{get_column_letter(c)}{R2_GP}-{get_column_letter(c)}{R2_OPEX}")
r += 1

R2_EBITDA_M = r
label_cell(ws2, r, 1, "  EBITDA Margin %")
for c in range(2, 7):
    cell(ws2, r, c, fmt=PCT, formula=f"{get_column_letter(c)}{R2_EBITDA}/{get_column_letter(c)}{R2_REV}")
r += 2

# -- Tax & Net Profit --
R2_TAX = r
label_cell(ws2, r, 1, "  Tax (@ rate from Assumptions)")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"IF({get_column_letter(c)}{R2_EBITDA}>0,{get_column_letter(c)}{R2_EBITDA}*Assumptions!$B${R_TAX},0)")
r += 1

R2_NP = r
label_cell(ws2, r, 1, "NET PROFIT", font=body_b)
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, font=green_b, fill=green_fill,
         formula=f"{get_column_letter(c)}{R2_EBITDA}-{get_column_letter(c)}{R2_TAX}")
r += 1

R2_NPM = r
label_cell(ws2, r, 1, "  Net Profit Margin %")
for c in range(2, 7):
    cell(ws2, r, c, fmt=PCT, formula=f"{get_column_letter(c)}{R2_NP}/{get_column_letter(c)}{R2_REV}")
r += 2

# -- Cumulative --
R2_CUM = r
label_cell(ws2, r, 1, "Cumulative Net Profit", font=body_b)
cell(ws2, r, 2, fmt=USD, font=body_b, formula=f"B{R2_NP}")
for c in range(3, 7):
    cell(ws2, r, c, fmt=USD, font=body_b, formula=f"{get_column_letter(c-1)}{R2_CUM}+{get_column_letter(c)}{R2_NP}")
r += 1

# Revenue per patient
R2_RPP = r
label_cell(ws2, r, 1, "Revenue per Patient")
for c in range(2, 7):
    cell(ws2, r, c, fmt=USD, formula=f"{get_column_letter(c)}{R2_REV}/{get_column_letter(c)}{R2_PAT}")


# ════════════════════════════════════════════════════════════════
# SHEET 3: P&L (INR) — All formulas = USD sheet × FX rate
# ════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("P&L (INR)")
ws3.sheet_properties.tabColor = "E67E22"
set_widths(ws3, [38, 18, 18, 18, 18, 18])

title_row(ws3, 1, 6, "PROFIT & LOSS STATEMENT — INR (₹)")
ws3.cell(2, 1, f"All values = USD P&L × Exchange Rate (₹ from Assumptions!B5)").font = Font(name="Calibri", size=9, italic=True, color="999999")
ws3.merge_cells("A2:F2")
r = 3
hdr(ws3, r, ["", "Year 1 (₹)", "Year 2 (₹)", "Year 3 (₹)", "Year 4 (₹)", "Year 5 (₹)"]); r += 1

inr_rows = [
    ("REVENUE", None),
    ("Patients", R2_PAT, NUM),
    ("Gross Treatment Volume", R2_GTV),
    ("  Hospital Commission", R2_COMM),
    ("  Package Revenue", R2_PKG),
    ("  Telemedicine Revenue", R2_TELE),
    ("  Ancillary Revenue", R2_ANC),
    ("TOTAL REVENUE", R2_REV),
    ("  Revenue Growth YoY", R2_REV_GR, PCT),
    ("", None),
    ("COST OF REVENUE", None),
    ("  Marketing & Acquisition", R2_CAC_TOT),
    ("  Onboarding Cost", R2_ONBOARD_TOT),
    ("  Operations & Coordination", R2_OPS_TOT),
    ("  Technology", R2_TECH_TOT),
    ("TOTAL VARIABLE COSTS", R2_COGS),
    ("GROSS PROFIT", R2_GP),
    ("  Gross Margin %", R2_GPM, PCT),
    ("", None),
    ("OPERATING EXPENSES", None),
    ("  Salaries & Benefits", R2_SAL),
    ("  Office & Admin", R2_OFFICE),
    ("  Legal & Compliance", R2_LEGAL),
    ("  Miscellaneous", R2_MISC),
    ("TOTAL OPEX", R2_OPEX),
    ("", None),
    ("EBITDA", R2_EBITDA),
    ("  EBITDA Margin %", R2_EBITDA_M, PCT),
    ("  Tax", R2_TAX),
    ("NET PROFIT", R2_NP),
    ("  Net Margin %", R2_NPM, PCT),
    ("Cumulative Net Profit", R2_CUM),
]

for item in inr_rows:
    if len(item) == 2 and item[1] is None:
        if item[0]:
            section_row(ws3, r, 6, item[0])
        r += 1; continue
    lbl = item[0]
    src_row = item[1]
    fmt_override = item[2] if len(item) > 2 else None
    is_bold = lbl.isupper() or lbl.startswith("TOTAL") or lbl.startswith("NET") or lbl.startswith("Cumulative") or lbl == "EBITDA"
    f = body_b if is_bold else body
    label_cell(ws3, r, 1, lbl, font=f)
    for c in range(2, 7):
        col = get_column_letter(c)
        if fmt_override == NUM:
            cell(ws3, r, c, fmt=NUM, font=f, formula=f"'P&L (USD)'!{col}{src_row}")
        elif fmt_override == PCT:
            cell(ws3, r, c, fmt=PCT, font=f, formula=f"'P&L (USD)'!{col}{src_row}")
        else:
            fl = green_fill if is_bold else None
            ff = green_b if is_bold else f
            cell(ws3, r, c, fmt=INR, font=ff, fill=fl, formula=f"'P&L (USD)'!{col}{src_row}*{A_FX}")
    r += 1


# ════════════════════════════════════════════════════════════════
# SHEET 4: UNIT ECONOMICS
# ════════════════════════════════════════════════════════════════
ws4 = wb.create_sheet("Unit Economics")
ws4.sheet_properties.tabColor = "27AE60"
set_widths(ws4, [38, 16, 16, 16, 16, 16, 16, 16])

title_row(ws4, 1, 8, "UNIT ECONOMICS — PER PATIENT")
r = 3
hdr(ws4, r, ["Metric", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "INR (Y1)", "INR (Y5)"]); r += 1

ue_items = [
    ("REVENUE PER PATIENT", True),
    ("  Commission Revenue", f"'P&L (USD)'!{{c}}{R2_COMM}/'P&L (USD)'!{{c}}{R2_PAT}"),
    ("  Package Revenue", f"'P&L (USD)'!{{c}}{R2_PKG}/'P&L (USD)'!{{c}}{R2_PAT}"),
    ("  Telemedicine Revenue", f"'P&L (USD)'!{{c}}{R2_TELE}/'P&L (USD)'!{{c}}{R2_PAT}"),
    ("  Ancillary Revenue", f"'P&L (USD)'!{{c}}{R2_ANC}/'P&L (USD)'!{{c}}{R2_PAT}"),
    ("Total Revenue / Patient", f"'P&L (USD)'!{{c}}{R2_REV}/'P&L (USD)'!{{c}}{R2_PAT}", True),
    ("", None),
    ("COST PER PATIENT", True),
    ("  Customer Acquisition", f"Assumptions!{{c}}{R_CAC}"),
    ("  Onboarding", f"Assumptions!{{c}}{R_ONBOARD}"),
    ("  Operations", f"Assumptions!{{c}}{R_OPS}"),
    ("  Technology", f"Assumptions!{{c}}{R_TECH_PAT}"),
    ("Total Cost / Patient", f"'P&L (USD)'!{{c}}{R2_COGS}/'P&L (USD)'!{{c}}{R2_PAT}", True),
    ("", None),
    ("PROFIT PER PATIENT", True),
    ("Gross Profit / Patient", f"('P&L (USD)'!{{c}}{R2_REV}-'P&L (USD)'!{{c}}{R2_COGS})/'P&L (USD)'!{{c}}{R2_PAT}", True),
]

for item in ue_items:
    if len(item) >= 2 and item[1] is None:
        r += 1; continue
    if len(item) >= 2 and item[1] is True:
        section_row(ws4, r, 8, item[0]); r += 1; continue
    lbl = item[0]
    formula_tpl = item[1]
    is_bold = len(item) > 2 and item[2]
    f = body_b if is_bold else body
    fl = green_fill if is_bold and "Profit" in lbl else None
    label_cell(ws4, r, 1, lbl, font=f)
    for c_i in range(2, 7):
        col = get_column_letter(c_i)
        formula = formula_tpl.replace("{c}", col)
        cell(ws4, r, c_i, fmt=USD, font=f, fill=fl, formula=formula)
    # INR columns for Y1 and Y5
    cell(ws4, r, 7, fmt=INR, font=f, formula=f"B{r}*{A_FX}")
    cell(ws4, r, 8, fmt=INR, font=f, formula=f"F{r}*{A_FX}")
    r += 1

# LTV and LTV:CAC
r += 1
section_row(ws4, r, 8, "LIFETIME VALUE & EFFICIENCY"); r += 1
R4_LTV_MULT = r
label_cell(ws4, r, 1, "Repeat / Referral Multiplier")
input_cell(ws4, r, 2, 1.5, '0.0"x"')
cell(ws4, r, 8, "Avg patient generates 1.5x value (repeat + referrals)", font=Font(name="Calibri", size=9, italic=True, color="999999"))
r += 1

R4_LTV = r
label_cell(ws4, r, 1, "Lifetime Value (LTV)", font=body_b)
for c in range(2, 7):
    col = get_column_letter(c)
    # LTV = Revenue per patient * multiplier
    cell(ws4, r, c, fmt=USD, font=green_b, fill=green_fill,
         formula=f"('P&L (USD)'!{col}{R2_REV}/'P&L (USD)'!{col}{R2_PAT})*$B${R4_LTV_MULT}")
r += 1

R4_LTVCAC = r
label_cell(ws4, r, 1, "LTV : CAC Ratio", font=body_b)
for c in range(2, 7):
    col = get_column_letter(c)
    cell(ws4, r, c, fmt=X_FMT, font=green_b, fill=green_fill,
         formula=f"{col}{R4_LTV}/Assumptions!{col}{R_CAC}")
r += 1

R4_PAYBACK = r
label_cell(ws4, r, 1, "CAC Payback (months)", font=body_b)
for c in range(2, 7):
    col = get_column_letter(c)
    cell(ws4, r, c, fmt='0.0',  font=body_b,
         formula=f"Assumptions!{col}{R_CAC}/('P&L (USD)'!{col}{R2_REV}/'P&L (USD)'!{col}{R2_PAT}/12)")


# ════════════════════════════════════════════════════════════════
# SHEET 5: TREATMENT MIX
# ════════════════════════════════════════════════════════════════
ws5 = wb.create_sheet("Treatment Mix")
ws5.sheet_properties.tabColor = "E74C3C"
set_widths(ws5, [26, 14, 14, 14, 14, 14, 14, 14])

title_row(ws5, 1, 8, "TREATMENT MIX, PRICING & SAVINGS")
r = 3
hdr(ws5, r, ["Treatment", "India (USD)", "USA (USD)", "UK (USD)", "Savings %", "Volume Mix", "Commission", "India (INR)"]); r += 1

treatments = [
    ("Hair Transplant (FUE 3000)", 1800, 15000, 12000, 0.25),
    ("Dental Implants (Full Mouth)", 4200, 25000, 18000, 0.18),
    ("Dental Veneers (10 teeth)", 2500, 15000, 10000, 0.06),
    ("Knee Replacement", 7000, 50000, 35000, 0.10),
    ("Hip Replacement", 6500, 45000, 30000, 0.06),
    ("Cardiac Bypass (CABG)", 7500, 120000, 40000, 0.05),
    ("IVF (per cycle)", 3200, 15000, 8000, 0.08),
    ("Cosmetic Surgery", 2800, 12000, 8000, 0.06),
    ("Bariatric Surgery", 4500, 25000, 15000, 0.04),
    ("LASIK (both eyes)", 800, 4000, 3000, 0.03),
    ("Spine Surgery", 5000, 50000, 25000, 0.03),
    ("Cancer Treatment (avg)", 8000, 80000, 40000, 0.03),
    ("Liver Transplant", 35000, 300000, 150000, 0.02),
    ("Surrogacy (Altruistic)", 15000, 150000, 120000, 0.01),
]
R5_START = r
for t in treatments:
    label_cell(ws5, r, 1, t[0])
    input_cell(ws5, r, 2, t[1], USD)   # India price
    input_cell(ws5, r, 3, t[2], USD)   # USA
    input_cell(ws5, r, 4, t[3], USD)   # UK
    cell(ws5, r, 5, fmt=PCT, formula=f"1-(B{r}/C{r})")  # Savings vs USA
    input_cell(ws5, r, 6, t[4], PCT)   # Volume Mix
    cell(ws5, r, 7, fmt=USD, formula=f"B{r}*0.175")      # Commission
    cell(ws5, r, 8, fmt=INR, formula=f"B{r}*{A_FX}")     # INR
    r += 1
R5_END = r - 1

# Weighted avg
label_cell(ws5, r, 1, "Weighted Avg Treatment Value", font=body_b)
cell(ws5, r, 2, fmt=USD, font=body_b, fill=green_fill,
     formula=f"SUMPRODUCT(B{R5_START}:B{R5_END},F{R5_START}:F{R5_END})")
cell(ws5, r, 5, fmt=PCT, font=body_b,
     formula=f"SUMPRODUCT((1-B{R5_START}:B{R5_END}/C{R5_START}:C{R5_END}),F{R5_START}:F{R5_END})")
cell(ws5, r, 6, fmt=PCT, font=body_b, formula=f"SUM(F{R5_START}:F{R5_END})")
cell(ws5, r, 7, fmt=USD, font=body_b, fill=green_fill,
     formula=f"SUMPRODUCT(B{R5_START}:B{R5_END},F{R5_START}:F{R5_END})*0.175")
cell(ws5, r, 8, fmt=INR, font=body_b, formula=f"B{r}*{A_FX}")


# ════════════════════════════════════════════════════════════════
# SHEET 6: MARKETING & CAC DETAIL
# ════════════════════════════════════════════════════════════════
ws6 = wb.create_sheet("Marketing & CAC")
ws6.sheet_properties.tabColor = "16A085"
set_widths(ws6, [28, 14, 14, 14, 14, 14, 28])

title_row(ws6, 1, 7, "MARKETING SPEND & CAC DETAIL")
r = 3
hdr(ws6, r, ["Channel", "% Budget", "CAC (USD)", "Conv. Rate", "Y1 Spend", "Y5 Spend", "Notes"]); r += 1

channels = [
    ("Google Ads (Search)", 0.35, 200, 0.035, "Treatment + country KWs"),
    ("Meta (FB + Instagram)", 0.20, 150, 0.020, "Video testimonials"),
    ("SEO & Content", 0.15, 80, 0.045, "Blog, comparisons, AI tools"),
    ("YouTube Content", 0.10, 180, 0.018, "Hospital tours, patient stories"),
    ("Referral Program", 0.10, 50, 0.12, "$200 credit per referral"),
    ("Aggregators", 0.05, 250, 0.05, "WhatClinic, Bookimed"),
    ("Clinic Partnerships", 0.05, 120, 0.08, "UK/UAE clinic referrals"),
]
R6_START = r
# Total mkt spend Y1 = Patients * CAC (from Assumptions)
# We'll compute total marketing budget as patients * CAC
for ch in channels:
    label_cell(ws6, r, 1, ch[0])
    input_cell(ws6, r, 2, ch[1], PCT)
    input_cell(ws6, r, 3, ch[2], USD)
    input_cell(ws6, r, 4, ch[3], PCT)
    # Y1 spend = % budget * total_mkt_Y1; total_mkt_Y1 = patients_Y1 * CAC_Y1
    cell(ws6, r, 5, fmt=USD, formula=f"B{r}*(Assumptions!B{R_PAT}*Assumptions!B{R_CAC})")
    cell(ws6, r, 6, fmt=USD, formula=f"B{r}*(Assumptions!F{R_PAT}*Assumptions!F{R_CAC})")
    cell(ws6, r, 7, ch[4], font=Font(name="Calibri", size=9, color="999999"))
    r += 1
R6_END = r - 1

label_cell(ws6, r, 1, "TOTAL", font=body_b)
cell(ws6, r, 2, fmt=PCT, font=body_b, formula=f"SUM(B{R6_START}:B{R6_END})")
cell(ws6, r, 5, fmt=USD, font=body_b, fill=green_fill, formula=f"SUM(E{R6_START}:E{R6_END})")
cell(ws6, r, 6, fmt=USD, font=body_b, fill=green_fill, formula=f"SUM(F{R6_START}:F{R6_END})")
r += 2

# CAC trajectory
section_row(ws6, r, 7, "BLENDED CAC TRAJECTORY"); r += 1
hdr(ws6, r, ["Metric", "Y1", "Y2", "Y3", "Y4", "Y5", ""]); r += 1
label_cell(ws6, r, 1, "Blended CAC (USD)")
for c in range(2, 7):
    cell(ws6, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_CAC}")
r += 1
label_cell(ws6, r, 1, "Blended CAC (INR)")
for c in range(2, 7):
    cell(ws6, r, c, fmt=INR, formula=f"Assumptions!{get_column_letter(c)}{R_CAC}*{A_FX}")
r += 1
label_cell(ws6, r, 1, "Total Mkt Spend (USD)")
for c in range(2, 7):
    cell(ws6, r, c, fmt=USD, formula=f"Assumptions!{get_column_letter(c)}{R_PAT}*Assumptions!{get_column_letter(c)}{R_CAC}")
r += 1
label_cell(ws6, r, 1, "Total Mkt Spend (INR)")
for c in range(2, 7):
    cell(ws6, r, c, fmt=INR, formula=f"Assumptions!{get_column_letter(c)}{R_PAT}*Assumptions!{get_column_letter(c)}{R_CAC}*{A_FX}")


# ════════════════════════════════════════════════════════════════
# SHEET 7: FUNDING & USE OF FUNDS
# ════════════════════════════════════════════════════════════════
ws7 = wb.create_sheet("Funding")
ws7.sheet_properties.tabColor = "8E44AD"
set_widths(ws7, [35, 18, 18, 18, 40])

title_row(ws7, 1, 5, "FUNDING REQUIREMENT & USE OF FUNDS")
r = 3
section_row(ws7, r, 5, "FUNDING ASK"); r += 1
hdr(ws7, r, ["Item", "USD", "INR (₹)", "% of Round", "Purpose"]); r += 1

R7_TOTAL = None
fund_items = [
    ("Technology & AI Platform", 500000, 0.25, "AI chatbot, website, mobile app, telemedicine integration"),
    ("Marketing & Growth", 600000, 0.30, "Google, Meta, YouTube, SEO — patient acquisition across 15+ countries"),
    ("Team Hiring (12 months)", 400000, 0.20, "Medical consultants, coordinators, engineers, marketing"),
    ("Hospital Network Expansion", 200000, 0.10, "Onboard 20+ new hospitals in Tier-2 cities"),
    ("Working Capital", 200000, 0.10, "Ops buffer, insurance deposits, office setup"),
    ("Legal & Compliance", 100000, 0.05, "IP protection, medical tourism licensing, data privacy (DPDP Act)"),
]
R7_START = r
for f_item in fund_items:
    label_cell(ws7, r, 1, f_item[0])
    input_cell(ws7, r, 2, f_item[1], USD)
    cell(ws7, r, 3, fmt=INR, formula=f"B{r}*{A_FX}")
    cell(ws7, r, 4, fmt=PCT, formula=f"B{r}/B{R7_START + len(fund_items)}")
    cell(ws7, r, 5, f_item[3], font=Font(name="Calibri", size=9, color="666666"))
    r += 1
R7_END = r - 1

R7_TOTAL_R = r
label_cell(ws7, r, 1, "TOTAL FUNDING ASK", font=body_b)
cell(ws7, r, 2, fmt=USD, font=body_b, fill=green_fill, formula=f"SUM(B{R7_START}:B{R7_END})")
cell(ws7, r, 3, fmt=INR, font=body_b, fill=green_fill, formula=f"B{r}*{A_FX}")
cell(ws7, r, 4, fmt=PCT, font=body_b, formula=f"SUM(D{R7_START}:D{R7_END})")
r += 3

# Milestones
section_row(ws7, r, 5, "MILESTONES WITH THIS FUNDING"); r += 1
milestones = [
    ("6 Months", "Platform v2 live, 10 new hospital partners, 300 patients served"),
    ("12 Months", "Mobile app launched, 800+ patients, $1.5M revenue run-rate"),
    ("18 Months", "Breakeven achieved, 25+ hospitals, Africa market entry"),
    ("24 Months", "Series A ready, 3,500+ patients, $7M+ revenue"),
]
for m in milestones:
    label_cell(ws7, r, 1, m[0], font=body_b)
    ws7.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
    cell(ws7, r, 2, m[1], font=body, align=lft)
    r += 1


# ════════════════════════════════════════════════════════════════
# SHEET 8: VALUATION & INVESTOR RETURNS
# ════════════════════════════════════════════════════════════════
ws8 = wb.create_sheet("Valuation & Returns")
ws8.sheet_properties.tabColor = "2C3E50"
set_widths(ws8, [38, 18, 18, 18, 18, 18])

title_row(ws8, 1, 6, "VALUATION & INVESTOR RETURNS")
r = 3

section_row(ws8, r, 6, "VALUATION INPUTS"); r += 1
R8_PREMONEY = r
label_cell(ws8, r, 1, "Pre-Money Valuation (USD)")
input_cell(ws8, r, 2, 8000000, USD)
cell(ws8, r, 3, fmt=INR, formula=f"B{r}*{A_FX}")
cell(ws8, r, 4, "(INR)", font=Font(name="Calibri", size=9, color="999999"))
r += 1

R8_RAISE = r
label_cell(ws8, r, 1, "Funding Raised (USD)")
cell(ws8, r, 2, fmt=USD, formula=f"Funding!B{R7_TOTAL_R}")
cell(ws8, r, 3, fmt=INR, formula=f"B{r}*{A_FX}")
r += 1

R8_POST = r
label_cell(ws8, r, 1, "Post-Money Valuation", font=body_b)
cell(ws8, r, 2, fmt=USD, font=body_b, fill=green_fill, formula=f"B{R8_PREMONEY}+B{R8_RAISE}")
cell(ws8, r, 3, fmt=INR, font=body_b, fill=green_fill, formula=f"B{r}*{A_FX}")
r += 1

R8_DILUTION = r
label_cell(ws8, r, 1, "Investor Ownership %")
cell(ws8, r, 2, fmt=PCT, font=body_b, formula=f"B{R8_RAISE}/B{R8_POST}")
r += 2

# Revenue multiple valuation
section_row(ws8, r, 6, "EXIT VALUATION (Revenue Multiple Method)"); r += 1
hdr(ws8, r, ["Metric", "Year 3", "Year 4", "Year 5", "", ""]); r += 1

R8_YREV = r
label_cell(ws8, r, 1, "Annual Revenue (USD)")
cell(ws8, r, 2, fmt=USD, formula=f"'P&L (USD)'!D{R2_REV}")
cell(ws8, r, 3, fmt=USD, formula=f"'P&L (USD)'!E{R2_REV}")
cell(ws8, r, 4, fmt=USD, formula=f"'P&L (USD)'!F{R2_REV}")
r += 1

R8_MULT = r
label_cell(ws8, r, 1, "Revenue Multiple (HealthTech SaaS-like)")
input_cell(ws8, r, 2, 8, '0"x"')
input_cell(ws8, r, 3, 7, '0"x"')
input_cell(ws8, r, 4, 6, '0"x"')
cell(ws8, r, 5, "Adjust based on market comps", font=Font(name="Calibri", size=9, italic=True, color="999999"))
r += 1

R8_EXIT_VAL = r
label_cell(ws8, r, 1, "Exit Valuation (USD)", font=body_b)
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=USD, font=green_b, fill=green_fill, formula=f"{col}{R8_YREV}*{col}{R8_MULT}")
r += 1

R8_EXIT_INR = r
label_cell(ws8, r, 1, "Exit Valuation (INR)", font=body_b)
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=INR, font=body_b, formula=f"{col}{R8_EXIT_VAL}*{A_FX}")
r += 2

# Investor returns
section_row(ws8, r, 6, "INVESTOR RETURNS"); r += 1
hdr(ws8, r, ["Metric", "Year 3 Exit", "Year 4 Exit", "Year 5 Exit", "", ""]); r += 1

R8_INV_SHARE = r
label_cell(ws8, r, 1, "Investor Share of Exit")
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=USD, font=body_b, formula=f"{col}{R8_EXIT_VAL}*B{R8_DILUTION}")
r += 1

R8_ROI = r
label_cell(ws8, r, 1, "Return on Investment (ROI)")
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=X_FMT, font=green_b, fill=green_fill,
         formula=f"{col}{R8_INV_SHARE}/B{R8_RAISE}")
r += 1

R8_IRR_LABEL = r
label_cell(ws8, r, 1, "Multiple on Invested Capital (MOIC)")
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=X_FMT, font=green_b, fill=green_fill,
         formula=f"{col}{R8_INV_SHARE}/B{R8_RAISE}")
r += 1

label_cell(ws8, r, 1, "Investor Profit (USD)")
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=USD, font=green_b, fill=green_fill,
         formula=f"{col}{R8_INV_SHARE}-B{R8_RAISE}")
r += 1
label_cell(ws8, r, 1, "Investor Profit (INR)")
for c_i in range(2, 5):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=INR, font=green_b, fill=green_fill,
         formula=f"({col}{R8_INV_SHARE}-B{R8_RAISE})*{A_FX}")
r += 2

# DCF
section_row(ws8, r, 6, "DCF VALUATION (Net Profit based)"); r += 1
hdr(ws8, r, ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]); r += 1

R8_DCF_NP = r
label_cell(ws8, r, 1, "Net Profit (USD)")
for c_i in range(2, 7):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=USD, formula=f"'P&L (USD)'!{col}{R2_NP}")
r += 1

R8_DCF_DISC = r
label_cell(ws8, r, 1, "Discount Factor")
for c_i in range(2, 7):
    yr = c_i - 1
    cell(ws8, r, c_i, fmt='0.000', formula=f"1/(1+Assumptions!$B${R_DISC})^{yr}")
r += 1

R8_DCF_PV = r
label_cell(ws8, r, 1, "Present Value of Cash Flow")
for c_i in range(2, 7):
    col = get_column_letter(c_i)
    cell(ws8, r, c_i, fmt=USD, formula=f"{col}{R8_DCF_NP}*{col}{R8_DCF_DISC}")
r += 1

R8_TV = r
label_cell(ws8, r, 1, "Terminal Value (10x Y5 Profit)")
input_cell(ws8, r, 2, 10, '0"x"')
cell(ws8, r, 3, "multiplier", font=Font(name="Calibri", size=9, color="999999"))
cell(ws8, r, 6, fmt=USD, formula=f"F{R8_DCF_NP}*B{R8_TV}")
r += 1

R8_TV_PV = r
label_cell(ws8, r, 1, "PV of Terminal Value")
cell(ws8, r, 6, fmt=USD, formula=f"F{R8_TV}*F{R8_DCF_DISC}")
r += 1

R8_DCF_TOTAL = r
label_cell(ws8, r, 1, "DCF Enterprise Value (USD)", font=body_b)
cell(ws8, r, 2, fmt=USD, font=green_b, fill=green_fill,
     formula=f"SUM(B{R8_DCF_PV}:F{R8_DCF_PV})+F{R8_TV_PV}")
r += 1
label_cell(ws8, r, 1, "DCF Enterprise Value (INR)", font=body_b)
cell(ws8, r, 2, fmt=INR, font=green_b, fill=green_fill, formula=f"B{R8_DCF_TOTAL}*{A_FX}")


# ════════════════════════════════════════════════════════════════
# SHEET 9: RISK ANALYSIS
# ════════════════════════════════════════════════════════════════
ws9 = wb.create_sheet("Risks")
ws9.sheet_properties.tabColor = "C0392B"
set_widths(ws9, [28, 50, 12, 12, 50])

title_row(ws9, 1, 5, "RISK ANALYSIS & MITIGATION")
r = 3
hdr(ws9, r, ["Risk", "Description", "Likelihood", "Impact", "Mitigation"]); r += 1

risks = [
    ("Regulatory Change", "India tightens medical tourism visa/regulations", "Low", "High", "Legal counsel on retainer; diversify source markets; lobby via FICCI"),
    ("Hospital Quality", "Partner hospital has a safety incident", "Low", "Critical", "JCI/NABH-only policy; quarterly audits; immediate delisting; malpractice insurance"),
    ("Competition", "Large players (Bookimed, Practo) enter aggressively", "Medium", "Medium", "AI technology moat; concierge quality; deep hospital relationships; brand"),
    ("Currency Risk", "INR appreciation makes India less price-competitive", "Medium", "Low", "USD pricing; currency hedging; Tier-2 city expansion for lower costs"),
    ("Negative PR", "Dissatisfied patient goes viral on social media", "Medium", "High", "24/7 patient support; <4h complaint SLA; PR response playbook; insurance"),
    ("AI Liability", "AI chatbot gives incorrect medical info", "Low", "High", "Medical disclaimers on all AI responses; human-in-the-loop; liability insurance"),
    ("Slow Onboarding", "Top hospitals resist partnership", "Medium", "Medium", "Start with 2-3 flagships; prove volume; offer analytics; no upfront cost"),
    ("Geopolitical", "Travel advisories affect source markets", "Low", "Medium", "50+ countries diversification; no market >20% of revenue"),
    ("Key Man Risk", "Founder departure or illness", "Low", "High", "Vesting schedules; 2+ co-founders; strong #2 in each function"),
    ("Data Privacy", "Patient data breach (DPDP Act, GDPR)", "Low", "Critical", "ISO 27001 compliance; encrypted storage; annual pen testing; DPO appointed"),
]
for rk in risks:
    label_cell(ws9, r, 1, rk[0])
    cell(ws9, r, 2, rk[1], font=body, align=lft)
    cell(ws9, r, 3, rk[2], font=body, align=ctr)
    sev_font = red_b if rk[3] in ("High", "Critical") else body
    cell(ws9, r, 4, rk[3], font=sev_font, align=ctr)
    cell(ws9, r, 5, rk[4], font=body, align=lft)
    r += 1


# ── SAVE ──
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "BharatHeals_Investor_Business_Plan.xlsx")
wb.save(out)
print(f"✅ Investor business plan saved: {out}")
print(f"   Sheets: {[s.title for s in wb.worksheets]}")
print(f"   All formulas reference Assumptions sheet — change yellow cells to recalculate everything.")
