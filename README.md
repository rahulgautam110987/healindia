# BharatHeals — Medical Tourism Platform for Australian Patients

A premium, full-stack medical tourism platform connecting Australian (and international) patients with India's finest JCI-accredited hospitals. Features hair transplant, dental treatment, cardiac surgery, orthopedics, IVF, and 10+ specialties.

## Quick Start

```bash
npm install
npm start
```

Open **http://localhost:3000** in your browser.

## Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Homepage | Hero, trust bar, consultation CTA, cost comparison (AUD), mini calculator, 10 specialties, hair & dental deep-dives, doctor profiles, before/after gallery, hospitals, process, testimonials, Australia logistics, FAQ accordion, WhatsApp widget |
| `/calculator.html` | Cost Calculator | Interactive savings calculator with AUD/USD/GBP support + full comparison table for 14 procedures |
| `/doctors.html` | Doctor Directory | 9 specialist profiles with credentials, stats, and consultation booking |
| `/faq.html` | FAQ | 18+ questions organised by category — safety, costs, insurance, travel, treatments |

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/consultations` | Book a free consultation |
| `POST` | `/api/contact` | Quick contact form |
| `POST` | `/api/newsletter` | Subscribe to newsletter |
| `GET`  | `/api/treatments` | All treatment prices (AU/US/UK/India) |
| `GET`  | `/api/treatments/:id` | Single treatment details |
| `GET`  | `/api/calculator?treatment=X&currency=aud` | Calculate savings |
| `GET`  | `/api/doctors` | All doctor profiles |
| `GET`  | `/api/doctors/:id` | Single doctor profile |

### Admin

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET`  | `/api/admin/consultations` | All consultation bookings |
| `GET`  | `/api/admin/contacts` | All contact submissions |
| `GET`  | `/api/admin/stats` | Dashboard stats |

## Project Structure

```
BharatHeals/
├── server.js              # Express backend + API routes + pricing data
├── db.js                  # SQLite database setup
├── package.json
├── data/                  # Auto-created on first run
│   └── bharatheals.db
├── public/
│   ├── index.html         # Homepage (Australia-focused)
│   ├── calculator.html    # Cost calculator page
│   ├── doctors.html       # Doctor directory
│   ├── faq.html           # FAQ page
│   ├── css/
│   │   └── style.css      # Shared styles
│   └── js/
│       └── app.js         # Shared JavaScript
└── README.md
```

## Key Features

**Australia-Targeted:**
- AUD pricing throughout
- Flight info from Sydney, Melbourne, Brisbane, Perth
- Medicare/private insurance guidance
- Tax deduction information
- Australian patient testimonials
- Australian phone number + WhatsApp support
- e-Medical Visa guide for Australians

**Medical Services:**
- 10+ specialties (Hair Transplant & Dental highlighted)
- Detailed pricing packages in AUD
- Before/after gallery
- 9 doctor profiles with credentials
- 6 partner hospital profiles
- Interactive cost calculator (AUD/USD/GBP)

**Conversion:**
- Free consultation modal on every page
- WhatsApp floating widget
- Multiple CTAs throughout
- FAQ addressing key objections
- Trust bar with media logos
- 5-step process visualization

**Technical:**
- Express.js + SQLite backend
- Rate-limited APIs
- Security headers (Helmet)
- Mobile-responsive design
- Intersection Observer animations
- Zero build step — vanilla HTML/CSS/JS

## Environment

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT`   | `3000`  | Server port |
