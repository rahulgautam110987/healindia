#!/usr/bin/env python3
"""Generate BharatHeals Business Plan Excel workbook with multiple sheets."""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.utils import get_column_letter
import os

wb = openpyxl.Workbook()

# ── Style definitions ──
NAVY = "0A1628"
GOLD = "C6A35B"
WHITE = "FFFFFF"
CREAM = "F9F6F0"
LIGHT_GRAY = "F2F2F2"
MID_GRAY = "D9D9D9"
GREEN = "27AE60"
RED = "E74C3C"

title_font = Font(name="Calibri", size=16, bold=True, color=WHITE)
header_font = Font(name="Calibri", size=11, bold=True, color=WHITE)
subheader_font = Font(name="Calibri", size=11, bold=True, color=NAVY)
body_font = Font(name="Calibri", size=10, color="333333")
gold_font = Font(name="Calibri", size=11, bold=True, color=GOLD)
money_font = Font(name="Calibri", size=10, color="333333")

navy_fill = PatternFill(start_color=NAVY, end_color=NAVY, fill_type="solid")
gold_fill = PatternFill(start_color=GOLD, end_color=GOLD, fill_type="solid")
cream_fill = PatternFill(start_color=CREAM, end_color=CREAM, fill_type="solid")
light_fill = PatternFill(start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid")
green_fill = PatternFill(start_color="E8F5E9", end_color="E8F5E9", fill_type="solid")
white_fill = PatternFill(start_color=WHITE, end_color=WHITE, fill_type="solid")

thin_border = Border(
    left=Side(style="thin", color=MID_GRAY),
    right=Side(style="thin", color=MID_GRAY),
    top=Side(style="thin", color=MID_GRAY),
    bottom=Side(style="thin", color=MID_GRAY),
)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left_wrap = Alignment(horizontal="left", vertical="center", wrap_text=True)
right_align = Alignment(horizontal="right", vertical="center")

USD = '#,##0'
USD_DEC = '#,##0.00'
PCT = '0.0%'
NUM = '#,##0'


def style_title_row(ws, row, cols, text):
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)
    c = ws.cell(row=row, column=1, value=text)
    c.font = title_font
    c.fill = navy_fill
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[row].height = 36


def style_header_row(ws, row, headers, fill=gold_fill):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = header_font
        c.fill = fill
        c.alignment = center
        c.border = thin_border
    ws.row_dimensions[row].height = 28


def style_data_row(ws, row, values, formats=None, alt=False):
    fill = cream_fill if alt else white_fill
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.font = body_font
        c.fill = fill
        c.border = thin_border
        c.alignment = left_wrap if i == 1 else right_align
        if formats and i - 1 < len(formats) and formats[i - 1]:
            c.number_format = formats[i - 1]


def auto_width(ws, cols, min_w=12, max_w=40):
    for i in range(1, cols + 1):
        ws.column_dimensions[get_column_letter(i)].width = min(max(min_w, 16), max_w)


# ════════════════════════════════════════════════════
# SHEET 1: EXECUTIVE SUMMARY
# ════════════════════════════════════════════════════
ws = wb.active
ws.title = "Executive Summary"
ws.sheet_properties.tabColor = NAVY
cols = 5
auto_width(ws, cols, 18, 50)
ws.column_dimensions["A"].width = 28
ws.column_dimensions["B"].width = 55

style_title_row(ws, 1, cols, "BHARATHEALS — BUSINESS PLAN 2026-2030")
ws.merge_cells("A2:B2")
ws.cell(row=2, column=1, value="Premium Global Medical Tourism Platform").font = gold_font

r = 4
sections = [
    ("Company", "BharatHeals Pvt. Ltd."),
    ("Founded", "2019"),
    ("Headquarters", "New Delhi, India"),
    ("Website", "www.bharatheals.com"),
    ("Industry", "Medical Tourism / HealthTech"),
    ("", ""),
    ("MISSION", "Make world-class medical treatment hassle-free and affordable for everyone, regardless of geography or budget."),
    ("VISION", "Become the most trusted global platform for medical tourism, serving 100,000+ patients by 2030."),
    ("", ""),
    ("PROBLEM", "Patients outside India pay 3-10x more for the same quality treatment. They face language barriers, unknown hospitals, complex visa processes, and no trusted coordination."),
    ("SOLUTION", "A single, end-to-end platform that handles everything: AI-powered treatment planning, hospital matching, doctor selection, visa, flights, accommodation, on-ground coordination, and post-op follow-up."),
    ("", ""),
    ("TARGET MARKET", "International patients from 50+ countries seeking affordable, high-quality treatment in India. Primary: Middle East, UK, USA, Australia, Africa."),
    ("REVENUE MODEL", "Commission from partner hospitals (15-20% of treatment value) + Premium concierge packages + Telemedicine subscriptions."),
    ("", ""),
    ("KEY METRICS (2026)", ""),
    ("  Patients Served", "10,000+ cumulative"),
    ("  Countries", "50+"),
    ("  Partner Hospitals", "44 JCI/NABH accredited"),
    ("  Patient Satisfaction", "97%"),
    ("  Average Savings", "60-90% vs home country"),
    ("  Total Patient Savings", "$120M+"),
    ("", ""),
    ("FUNDING ASK", "$2M Seed Round for technology, marketing, and hospital network expansion across Tier-2 Indian cities and new source markets (Africa, CIS, Latin America)."),
]
for label, val in sections:
    ws.cell(row=r, column=1, value=label).font = subheader_font if label.isupper() else body_font
    ws.cell(row=r, column=2, value=val).font = body_font
    ws.cell(row=r, column=2).alignment = left_wrap
    r += 1


# ════════════════════════════════════════════════════
# SHEET 2: MARKET OPPORTUNITY
# ════════════════════════════════════════════════════
ws2 = wb.create_sheet("Market Opportunity")
ws2.sheet_properties.tabColor = GOLD
cols = 4
auto_width(ws2, cols, 20, 45)
ws2.column_dimensions["A"].width = 35

style_title_row(ws2, 1, cols, "MARKET OPPORTUNITY")

r = 3
ws2.cell(row=r, column=1, value="GLOBAL MEDICAL TOURISM MARKET").font = subheader_font
r += 1
mkt_data = [
    ["Metric", "Value", "Source", "Year"],
    ["Global Market Size", "$88 Billion", "Grand View Research", "2025"],
    ["Projected Market Size", "$210 Billion", "Allied Market Research", "2030"],
    ["CAGR", "19.1%", "Grand View Research", "2025-30"],
    ["India's Share", "$9 Billion", "FICCI / CII", "2025"],
    ["India Projected Share", "$28 Billion", "NITI Aayog Target", "2030"],
    ["Patients Visiting India Annually", "2.0 Million", "Ministry of Tourism", "2025"],
    ["India CAGR (Medical Tourism)", "22.5%", "IBEF", "2025-30"],
]
style_header_row(ws2, r, mkt_data[0])
r += 1
for i, row_data in enumerate(mkt_data[1:]):
    style_data_row(ws2, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws2.cell(row=r, column=1, value="WHY INDIA WINS").font = subheader_font
r += 1
why_data = [
    ["Factor", "India", "Thailand", "Turkey"],
    ["Cost vs USA/UK", "60-90% lower", "50-75% lower", "50-70% lower"],
    ["JCI Hospitals", "44", "67", "35"],
    ["English Proficiency", "High (official language)", "Low-Medium", "Low"],
    ["Visa for Medical Travel", "e-Medical Visa (72h)", "Visa on arrival", "e-Visa"],
    ["Specialty Strength", "Cardiac, Ortho, Fertility, Hair, Dental", "Cosmetic, Dental", "Hair, Cosmetic"],
    ["Top Hospital Brands", "Apollo, Fortis, Medanta, Max", "Bumrungrad", "Memorial, Acibadem"],
    ["Doctor Training", "AIIMS, Mayo, Cleveland Clinic, Johns Hopkins alumni", "Mixed", "Mixed"],
    ["Annual Med Tourists", "2.0M", "2.5M", "1.2M"],
]
style_header_row(ws2, r, why_data[0])
r += 1
for i, row_data in enumerate(why_data[1:]):
    style_data_row(ws2, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws2.cell(row=r, column=1, value="TARGET SEGMENTS (by Country)").font = subheader_font
r += 1
seg_data = [
    ["Region", "Key Countries", "Primary Treatments", "Avg. Spend / Patient"],
    ["Middle East", "Saudi Arabia, UAE, Kuwait, Oman, Qatar", "Cardiac, Ortho, Cosmetic, Fertility", "$8,000 - $25,000"],
    ["UK & Europe", "UK, Germany, Ireland", "Ortho (hip/knee), Dental, Hair", "$5,000 - $15,000"],
    ["North America", "USA, Canada", "Dental, IVF, Cosmetic, Cardiac", "$6,000 - $30,000"],
    ["Australia & NZ", "Australia, New Zealand", "Hair, Dental, Ortho, Cosmetic", "$4,000 - $12,000"],
    ["Africa", "Nigeria, Kenya, Ethiopia, Tanzania", "Cardiac, Oncology, Neuro, Transplant", "$5,000 - $20,000"],
    ["CIS / Central Asia", "Uzbekistan, Kazakhstan, Russia", "Oncology, Cardiac, Fertility", "$5,000 - $18,000"],
]
style_header_row(ws2, r, seg_data[0])
r += 1
for i, row_data in enumerate(seg_data[1:]):
    style_data_row(ws2, r, row_data, alt=i % 2 == 0)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 3: REVENUE MODEL & UNIT ECONOMICS
# ════════════════════════════════════════════════════
ws3 = wb.create_sheet("Revenue Model")
ws3.sheet_properties.tabColor = "27AE60"
cols = 5
auto_width(ws3, cols, 18, 45)
ws3.column_dimensions["A"].width = 40

style_title_row(ws3, 1, cols, "REVENUE MODEL & UNIT ECONOMICS")

r = 3
ws3.cell(row=r, column=1, value="REVENUE STREAMS").font = subheader_font
r += 1
rev_streams = [
    ["Revenue Stream", "Description", "% of Revenue", "Avg. per Patient", "Margin"],
    ["Hospital Commission", "15-20% commission on treatment value from partner hospitals", "65%", "$1,200", "~95%"],
    ["Premium Packages", "Comfort / Platinum / Royal concierge tiers (hotel, transfers, coordinator)", "20%", "$600", "~50%"],
    ["Telemedicine Follow-up", "Post-treatment telemedicine subscription (3-12 months)", "8%", "$150", "~80%"],
    ["AI Treatment Plans", "Premium AI-generated detailed plans with PDF (future monetisation)", "3%", "$50", "~90%"],
    ["Insurance Referrals", "Referral commission from travel insurance partners", "2%", "$30", "~100%"],
    ["Recovery Tourism", "Commission from wellness resorts (Kerala, Goa, Rajasthan)", "2%", "$40", "~90%"],
]
style_header_row(ws3, r, rev_streams[0])
r += 1
for i, row_data in enumerate(rev_streams[1:]):
    style_data_row(ws3, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws3.cell(row=r, column=1, value="UNIT ECONOMICS (per patient)").font = subheader_font
r += 1
unit_data = [
    ["Metric", "Value", "Notes"],
    ["Average Treatment Value (ATV)", "$7,500", "Blended across all treatments"],
    ["Hospital Commission (17.5%)", "$1,313", "Primary revenue driver"],
    ["Package Revenue", "$600", "60% of patients take Platinum+"],
    ["Telemedicine + Ancillary", "$220", "Follow-up + insurance + tourism"],
    ["Total Revenue per Patient", "$2,133", ""],
    ["", "", ""],
    ["Customer Acquisition Cost (CAC)", "$180", "Digital marketing + referrals"],
    ["Onboarding Cost", "$50", "Consultation + coordinator time"],
    ["Operations / Coordination", "$120", "Visa, travel, on-ground support"],
    ["Technology Cost (AI, Platform)", "$25", "Amortised per patient"],
    ["Total Cost per Patient", "$375", ""],
    ["", "", ""],
    ["Gross Profit per Patient", "$1,758", ""],
    ["Gross Margin", "82.4%", ""],
    ["LTV (Lifetime Value)", "$3,200", "1.5x repeat / referral multiplier"],
    ["LTV : CAC Ratio", "17.8x", "Excellent — target >3x"],
]
style_header_row(ws3, r, unit_data[0])
r += 1
for i, row_data in enumerate(unit_data[1:]):
    style_data_row(ws3, r, row_data, alt=i % 2 == 0)
    if row_data[0] in ("Gross Profit per Patient", "LTV : CAC Ratio"):
        for col in range(1, 4):
            ws3.cell(row=r, column=col).fill = green_fill
            ws3.cell(row=r, column=col).font = Font(name="Calibri", size=10, bold=True, color=GREEN)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 4: 5-YEAR FINANCIAL PROJECTIONS
# ════════════════════════════════════════════════════
ws4 = wb.create_sheet("Financial Projections")
ws4.sheet_properties.tabColor = "2980B9"
cols = 7
auto_width(ws4, cols, 16, 45)
ws4.column_dimensions["A"].width = 35

style_title_row(ws4, 1, cols, "5-YEAR FINANCIAL PROJECTIONS (USD)")

r = 3
ws4.cell(row=r, column=1, value="PATIENT VOLUME & REVENUE").font = subheader_font
r += 1
proj_headers = ["Metric", "Year 1 (2026)", "Year 2 (2027)", "Year 3 (2028)", "Year 4 (2029)", "Year 5 (2030)"]
style_header_row(ws4, r, proj_headers)
r += 1

projections = [
    ["New Patients", 800, 1800, 3500, 6000, 10000],
    ["Growth Rate (YoY)", "-", "125%", "94%", "71%", "67%"],
    ["Avg Treatment Value (ATV)", 7500, 7800, 8000, 8200, 8500],
    ["Gross Treatment Volume (GTV)", 6000000, 14040000, 28000000, 49200000, 85000000],
    ["", "", "", "", "", ""],
    ["Hospital Commission Revenue", 1050000, 2457000, 4900000, 8610000, 14875000],
    ["Package Revenue", 384000, 900000, 1820000, 3240000, 5600000],
    ["Telemedicine + Ancillary", 136000, 324000, 665000, 1200000, 2100000],
    ["Total Revenue", 1570000, 3681000, 7385000, 13050000, 22575000],
    ["", "", "", "", "", ""],
    ["COGS (Hospital Ops)", 157000, 331000, 590000, 914000, 1355000],
    ["Gross Profit", 1413000, 3350000, 6795000, 12136000, 21220000],
    ["Gross Margin", "90.0%", "91.0%", "92.0%", "93.0%", "93.8%"],
    ["", "", "", "", "", ""],
    ["Marketing & Sales", 470000, 920000, 1477000, 2088000, 2710000],
    ["Technology & AI", 280000, 400000, 550000, 700000, 900000],
    ["Team & Salaries", 350000, 600000, 1050000, 1700000, 2500000],
    ["Office & Admin", 80000, 120000, 180000, 250000, 350000],
    ["Total Operating Expenses", 1180000, 2040000, 3257000, 4738000, 6460000],
    ["", "", "", "", "", ""],
    ["EBITDA", 233000, 1310000, 3538000, 7398000, 14760000],
    ["EBITDA Margin", "14.8%", "35.6%", "47.9%", "56.7%", "65.4%"],
    ["Net Profit (est. after tax)", 175000, 983000, 2654000, 5549000, 11070000],
]
fmts = [None, USD, USD, USD, USD, USD]
for i, row_data in enumerate(projections):
    style_data_row(ws4, r, row_data, formats=fmts, alt=i % 2 == 0)
    if row_data[0] in ("Total Revenue", "Gross Profit", "EBITDA", "Net Profit (est. after tax)"):
        for col in range(1, 8):
            ws4.cell(row=r, column=col).font = Font(name="Calibri", size=10, bold=True, color="333333")
    if row_data[0] in ("EBITDA", "Net Profit (est. after tax)"):
        for col in range(1, 8):
            ws4.cell(row=r, column=col).fill = green_fill
    r += 1

r += 2
ws4.cell(row=r, column=1, value="KEY ASSUMPTIONS").font = subheader_font
r += 1
assumptions = [
    "Patient growth driven by digital marketing (Google, Meta) + referral program + hospital partnerships",
    "ATV increases modestly (2-4% YoY) as mix shifts toward higher-value treatments (cardiac, oncology, transplant)",
    "Hospital commission rate: 15-20% blended (17.5% average), standard in medical tourism industry",
    "CAC decreases from $225 (Y1) to $120 (Y5) as brand recognition and organic/referral traffic increases",
    "Team scales from 8 (Y1) to 45 (Y5) — consultants, coordinators, tech, marketing",
    "Technology investment includes AI infrastructure, platform development, and mobile app",
    "Tax rate assumed at 25% (Indian corporate tax for new companies under Section 115BAA)",
]
for a in assumptions:
    ws4.cell(row=r, column=1, value=f"• {a}").font = body_font
    ws4.merge_cells(start_row=r, start_column=1, end_row=r, end_column=7)
    ws4.cell(row=r, column=1).alignment = left_wrap
    r += 1


# ════════════════════════════════════════════════════
# SHEET 5: TREATMENT PRICING & MARGINS
# ════════════════════════════════════════════════════
ws5 = wb.create_sheet("Treatment Pricing")
ws5.sheet_properties.tabColor = "E74C3C"
cols = 7
auto_width(ws5, cols, 16, 40)
ws5.column_dimensions["A"].width = 28

style_title_row(ws5, 1, cols, "TREATMENT PRICING, SAVINGS & COMMISSION")

r = 3
treat_headers = ["Treatment", "India Price (USD)", "USA Price", "UK Price", "Savings %", "Commission (17.5%)", "Patient Volume Mix"]
style_header_row(ws5, r, treat_headers)
r += 1

treatments = [
    ["Hair Transplant (FUE 3000)", 1800, 15000, 12000, "85-88%", 315, "25%"],
    ["Dental Implants (Full Mouth)", 4200, 25000, 18000, "77-83%", 735, "18%"],
    ["Dental Veneers (10 teeth)", 2500, 15000, 10000, "75-83%", 438, "8%"],
    ["Knee Replacement (Bilateral)", 7000, 50000, 35000, "80-86%", 1225, "10%"],
    ["Hip Replacement", 6500, 45000, 30000, "78-86%", 1138, "7%"],
    ["Cardiac Bypass (CABG)", 7500, 120000, 40000, "81-94%", 1313, "5%"],
    ["IVF (per cycle)", 3200, 15000, 8000, "60-79%", 560, "8%"],
    ["Cosmetic Surgery (Rhinoplasty)", 2800, 12000, 8000, "65-77%", 490, "6%"],
    ["Bariatric Surgery", 4500, 25000, 15000, "70-82%", 788, "4%"],
    ["LASIK (both eyes)", 800, 4000, 3000, "73-80%", 140, "3%"],
    ["Cancer Treatment (avg)", 8000, 80000, 40000, "80-90%", 1400, "3%"],
    ["Liver Transplant", 35000, 300000, 150000, "77-88%", 6125, "2%"],
    ["Surrogacy (Altruistic — Medical)", 15000, 150000, 120000, "88-90%", 2625, "1%"],
]
fmts = [None, USD, USD, USD, None, USD, None]
for i, row_data in enumerate(treatments):
    style_data_row(ws5, r, row_data, formats=fmts, alt=i % 2 == 0)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 6: HOSPITAL PARTNERSHIP MODEL
# ════════════════════════════════════════════════════
ws6 = wb.create_sheet("Hospital Partnership")
ws6.sheet_properties.tabColor = "8E44AD"
cols = 4
auto_width(ws6, cols, 18, 50)
ws6.column_dimensions["A"].width = 35
ws6.column_dimensions["B"].width = 55

style_title_row(ws6, 1, cols, "HOSPITAL & DOCTOR PARTNERSHIP MODEL")

r = 3
ws6.cell(row=r, column=1, value="WHAT WE OFFER HOSPITALS").font = subheader_font
r += 1
offers = [
    ["Benefit", "Details"],
    ["Steady International Patient Flow", "We bring pre-qualified patients from 50+ countries. Hospitals get incremental revenue with zero marketing spend."],
    ["Complete Patient Coordination", "We handle visa, travel, accommodation, airport pickup, translation, insurance — hospitals focus on treatment."],
    ["Digital Marketing & Lead Gen", "Our website, AI agent, Google/Meta campaigns, and SEO drive high-intent patient enquiries directly to your hospital."],
    ["Quality Assurance & Feedback", "Post-treatment surveys, NPS tracking, and public reviews build your hospital's international reputation."],
    ["Technology Integration", "Our AI platform pre-screens patients, collects medical records digitally, and facilitates telemedicine pre-consultations."],
    ["No Upfront Cost", "Zero joining fee. We earn only when a patient completes treatment at your hospital."],
]
style_header_row(ws6, r, offers[0])
r += 1
for i, row_data in enumerate(offers[1:]):
    style_data_row(ws6, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws6.cell(row=r, column=1, value="COMMISSION STRUCTURE").font = subheader_font
r += 1
comm = [
    ["Tier", "Annual Patients Referred", "Commission Rate", "Payment Terms"],
    ["Standard", "1-50 patients/year", "20%", "Net 30 after discharge"],
    ["Gold", "51-150 patients/year", "17.5%", "Net 30 after discharge"],
    ["Platinum", "151-400 patients/year", "15%", "Net 15 after discharge"],
    ["Strategic", "400+ patients/year", "12-15% (negotiable)", "Net 15 + quarterly bonus"],
]
style_header_row(ws6, r, comm[0])
r += 1
for i, row_data in enumerate(comm[1:]):
    style_data_row(ws6, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws6.cell(row=r, column=1, value="CURRENT PARTNER HOSPITALS").font = subheader_font
r += 1
hospitals = [
    ["Hospital", "Cities", "Accreditation", "Key Specialties"],
    ["Apollo Hospitals", "Chennai, Delhi, Hyderabad, Mumbai", "JCI, NABH", "Cardiac, Oncology, Ortho, Transplant"],
    ["Fortis Healthcare", "Gurugram, Bangalore, Mumbai", "JCI, NABH", "Cardiac, Neuro, Ortho, Fertility"],
    ["Medanta — The Medicity", "Gurugram, Lucknow", "JCI, NABH", "Cardiac (founded by ex-Harvard surgeon), Oncology"],
    ["Max Healthcare", "Delhi, Noida, Mohali", "JCI, NABH", "Robotic Surgery, Cardiac, Neuro"],
    ["Kokilaben Ambani Hospital", "Mumbai", "JCI, NABH", "CyberKnife, Oncology, Neuro"],
    ["Manipal Hospitals", "Bangalore, Delhi, Kolkata", "NABH", "Research, Stem Cell, Bone Marrow"],
]
style_header_row(ws6, r, hospitals[0])
r += 1
for i, row_data in enumerate(hospitals[1:]):
    style_data_row(ws6, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
ws6.cell(row=r, column=1, value="DOCTOR ONBOARDING BENEFITS").font = subheader_font
r += 1
doc_benefits = [
    ["Benefit", "Details"],
    ["International Patient Access", "Treat patients from USA, UK, Middle East, Australia — expand your practice beyond domestic market."],
    ["Zero Marketing Cost", "We promote your profile, credentials, and reviews on our platform. Patients find you, not the other way around."],
    ["Telemedicine Revenue", "Earn from pre-consultation video calls and post-treatment follow-ups — billable telemedicine sessions."],
    ["Professional Profile Page", "Dedicated doctor page with your photo, credentials, specialties, reviews, and booking button."],
    ["Reputation Building", "International patient reviews build your Google profile and medical tourism reputation globally."],
    ["Flexible Scheduling", "You control your availability. We work around your calendar — no disruption to your existing practice."],
]
style_header_row(ws6, r, doc_benefits[0])
r += 1
for i, row_data in enumerate(doc_benefits[1:]):
    style_data_row(ws6, r, row_data, alt=i % 2 == 0)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 7: TEAM & HIRING PLAN
# ════════════════════════════════════════════════════
ws7 = wb.create_sheet("Team & Hiring")
ws7.sheet_properties.tabColor = "F39C12"
cols = 7
auto_width(ws7, cols, 14, 35)
ws7.column_dimensions["A"].width = 30

style_title_row(ws7, 1, cols, "TEAM & HIRING ROADMAP")

r = 3
team_headers = ["Role", "Y1 (2026)", "Y2 (2027)", "Y3 (2028)", "Y4 (2029)", "Y5 (2030)", "Avg. CTC (USD)"]
style_header_row(ws7, r, team_headers)
r += 1

team_plan = [
    ["Founders / Leadership", 2, 2, 3, 4, 5, 60000],
    ["Medical Consultants", 2, 4, 6, 8, 12, 18000],
    ["Care Coordinators (on-ground)", 1, 3, 5, 8, 12, 12000],
    ["Tech / AI Engineers", 2, 3, 4, 5, 6, 30000],
    ["Digital Marketing", 1, 2, 3, 4, 5, 15000],
    ["Content & SEO", 0, 1, 2, 2, 3, 12000],
    ["Finance & Ops", 0, 1, 1, 2, 2, 15000],
    ["", "", "", "", "", "", ""],
    ["Total Headcount", 8, 16, 24, 33, 45, ""],
    ["Total Salary Cost (USD)", 252000, 480000, 840000, 1320000, 2040000, ""],
]
fmts = [None, NUM, NUM, NUM, NUM, NUM, USD]
for i, row_data in enumerate(team_plan):
    style_data_row(ws7, r, row_data, formats=fmts, alt=i % 2 == 0)
    if row_data[0] in ("Total Headcount", "Total Salary Cost (USD)"):
        for col in range(1, 8):
            ws7.cell(row=r, column=col).font = Font(name="Calibri", size=10, bold=True)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 8: MARKETING & CAC
# ════════════════════════════════════════════════════
ws8 = wb.create_sheet("Marketing & CAC")
ws8.sheet_properties.tabColor = "16A085"
cols = 7
auto_width(ws8, cols, 16, 40)
ws8.column_dimensions["A"].width = 30

style_title_row(ws8, 1, cols, "MARKETING STRATEGY & CUSTOMER ACQUISITION")

r = 3
ws8.cell(row=r, column=1, value="CHANNEL MIX & CAC").font = subheader_font
r += 1
mkt_headers = ["Channel", "% of Budget", "CAC", "Conversion Rate", "Monthly Spend (Y1)", "Key Tactic", "Scalability"]
style_header_row(ws8, r, mkt_headers)
r += 1

channels = [
    ["Google Ads (Search)", "35%", "$200", "3.5%", "$13,700", "Treatment + country keywords", "High"],
    ["Meta Ads (FB + Instagram)", "20%", "$150", "2.0%", "$7,800", "Testimonial videos, before/after", "High"],
    ["SEO & Content Marketing", "15%", "$80", "4.5%", "$5,900", "Blog, comparison guides, AI tools", "Very High"],
    ["YouTube Pre-roll + Content", "10%", "$180", "1.8%", "$3,900", "Patient stories, hospital tours", "High"],
    ["Referral Program", "10%", "$50", "12%", "$3,900", "$200 credit per referral", "Very High"],
    ["Medical Tourism Aggregators", "5%", "$250", "5.0%", "$2,000", "Listings on WhatClinic, Bookimed", "Medium"],
    ["Partnerships (Clinics Abroad)", "5%", "$120", "8.0%", "$2,000", "UK/UAE clinic tie-ups for referrals", "High"],
]
for i, row_data in enumerate(channels):
    style_data_row(ws8, r, row_data, alt=i % 2 == 0)
    r += 1

r += 2
cac_proj = [
    ["Year", "Total Mkt Spend", "New Patients", "Blended CAC", "Organic %"],
    ["2026", "$470,000", "800", "$225", "15%"],
    ["2027", "$920,000", "1,800", "$190", "25%"],
    ["2028", "$1,477,000", "3,500", "$155", "35%"],
    ["2029", "$2,088,000", "6,000", "$135", "42%"],
    ["2030", "$2,710,000", "10,000", "$120", "50%"],
]
ws8.cell(row=r, column=1, value="CAC TRAJECTORY (decreasing with scale)").font = subheader_font
r += 1
style_header_row(ws8, r, cac_proj[0])
r += 1
for i, row_data in enumerate(cac_proj[1:]):
    style_data_row(ws8, r, row_data, alt=i % 2 == 0)
    r += 1


# ════════════════════════════════════════════════════
# SHEET 9: RISK ANALYSIS
# ════════════════════════════════════════════════════
ws9 = wb.create_sheet("Risk Analysis")
ws9.sheet_properties.tabColor = "C0392B"
cols = 4
auto_width(ws9, cols, 20, 50)
ws9.column_dimensions["A"].width = 30
ws9.column_dimensions["B"].width = 50
ws9.column_dimensions["C"].width = 15
ws9.column_dimensions["D"].width = 50

style_title_row(ws9, 1, cols, "RISK ANALYSIS & MITIGATION")

r = 3
risk_headers = ["Risk", "Description", "Severity", "Mitigation"]
style_header_row(ws9, r, risk_headers)
r += 1

risks = [
    ["Regulatory Changes", "India tightens medical tourism regulations or visa policies", "Medium", "Maintain legal counsel, diversify source markets, lobby via FICCI Medical Tourism Council"],
    ["Hospital Quality Incident", "A partner hospital has a quality failure or patient safety issue", "High", "Strict JCI/NABH-only policy, quarterly audits, immediate delisting protocol, malpractice insurance"],
    ["Currency Fluctuation", "INR appreciation makes India less competitive vs Thailand/Turkey", "Low", "Price in USD, hedge currency risk, diversify to lower-cost Tier-2 cities"],
    ["Competition", "Larger players (Bookimed, Medical Departures) enter India aggressively", "Medium", "Differentiate via AI technology, concierge quality, and deep hospital relationships"],
    ["Negative Reviews / PR", "A dissatisfied patient goes viral on social media", "Medium", "24/7 patient support, proactive follow-up, complaint resolution SLA (<4 hours), PR response playbook"],
    ["Technology Failure", "AI chatbot gives incorrect medical advice", "High", "AI responses always include medical disclaimer, human-in-the-loop review, liability insurance"],
    ["Slow Hospital Onboarding", "Top hospitals resist partnership or demand exclusivity", "Medium", "Start with 2-3 flagship hospitals, prove patient volume, then expand. Offer data & analytics."],
    ["Geopolitical Risk", "Conflict or travel advisories affect source markets", "Low", "Diversified across 50+ countries — no single market >20% of revenue"],
]
for i, row_data in enumerate(risks):
    style_data_row(ws9, r, row_data, alt=i % 2 == 0)
    r += 1


# ── Save ──
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "BharatHeals_Business_Plan_2026.xlsx")
wb.save(output_path)
print(f"✅ Business plan saved to: {output_path}")
