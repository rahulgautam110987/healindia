const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const path = require('path');
const { v4: uuidv4 } = require('uuid');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { getDb } = require('./db');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'medrouteindia_secret_2026_change_in_production';

app.use(helmet({ contentSecurityPolicy: false, crossOriginEmbedderPolicy: false }));
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public'), {
  etag: false,
  setHeaders: function(res, filePath) {
    if (filePath.endsWith('.js') || filePath.endsWith('.css')) {
      res.set('Cache-Control', 'no-cache, no-store, must-revalidate');
      res.set('Pragma', 'no-cache');
      res.set('Expires', '0');
    }
  }
}));

const apiLimiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 100, standardHeaders: true, legacyHeaders: false, message: { success: false, error: 'Too many requests.' } });
app.use('/api/', apiLimiter);

// ==================== DATA ====================

const CONSULTANTS = [
  { id: 'sarah-mitchell', name: 'Sarah Mitchell', title: 'Senior Medical Tourism Consultant', specialties: ['Hair Transplant', 'Cosmetic Surgery'], experience: '8 years', bio: 'Former hospital nurse turned medical tourism expert. Has helped 2,000+ international patients plan their medical journey to India.', languages: ['English'], rating: 4.9, reviews: 342 },
  { id: 'james-wong', name: 'James Wong', title: 'International Patient Coordinator', specialties: ['Dental Implants', 'IVF', 'Fertility Law'], experience: '6 years', bio: 'Healthcare management graduate. Specialises in fertility tourism and complex dental cases for patients worldwide.', languages: ['English', 'Mandarin', 'Arabic'], rating: 4.8, reviews: 278 },
  { id: 'priya-nair', name: 'Dr. Priya Nair', title: 'Medical Advisor & Care Coordinator', specialties: ['IVF', 'Surrogacy Law', 'Cosmetic Surgery'], experience: '12 years', bio: 'MBBS with Masters in Healthcare Administration. Previously at Apollo Hospitals international desk. Deep knowledge of Indian healthcare system and Surrogacy (Regulation) Act, 2021.', languages: ['English', 'Hindi', 'Arabic', 'Malayalam'], rating: 4.9, reviews: 456 },
  { id: 'david-chen', name: 'David Chen', title: 'Travel & Logistics Coordinator', specialties: ['Hair Transplant', 'Dental Implants'], experience: '5 years', bio: 'Former airline travel coordinator. Expert in medical visa processing and travel planning for patients from 50+ countries.', languages: ['English', 'Cantonese'], rating: 4.7, reviews: 189 },
];

const TREATMENTS = {
  'hair-transplant': {
    id: 'hair-transplant', name: 'Hair Transplant Surgery', rating: 4.8, icon: '💇', category: 'Hair',
    description: 'Restore natural hair growth using advanced FUE, FUT, DHI, and Sapphire techniques by globally trained trichologists.',
    types: ['FUE (Follicular Unit Extraction)', 'FUT (Strip Method)', 'DHI (Direct Hair Implantation)', 'Beard / Eyebrow Transplants', 'Scalp Micropigmentation', 'PRP & Stem Cell Therapy'],
    prices: { australia: 16000, usa: 15000, uk: 12000, thailand: 5000, turkey: 3500, singapore: 8000, malaysia: 4000, india: 1500 },
    stay: '3-5 days', recovery: '7-10 days',
    packages: [
      { name: 'FUE — 2000 Grafts', detail: 'Hairline restoration', price: 1200 },
      { name: 'FUE — 3000 Grafts', detail: 'Crown + hairline', price: 1500 },
      { name: 'DHI — 3500 Grafts', detail: 'Premium pen technique', price: 2200 },
      { name: 'Mega Session — 5000+', detail: 'Full coverage', price: 3000 },
    ],
  },
  'dental-implants': {
    id: 'dental-implants', name: 'Dental Implants', rating: 4.7, icon: '🦷', category: 'Dental',
    description: 'World-class dental care from implants to full smile makeovers using Nobel Biocare, Straumann, and Ivoclar materials.',
    types: ['Single Dental Implant', 'All-on-4 Full Arch', 'Porcelain Veneers', 'Full Mouth Rehabilitation', 'Root Canal + Crown', 'Teeth Whitening & Aligners'],
    prices: { australia: 5500, usa: 5000, uk: 3500, thailand: 1800, turkey: 1200, singapore: 3000, malaysia: 1500, india: 500 },
    stay: '5-7 days', recovery: '3-5 days',
    packages: [
      { name: 'Single Implant + Crown', detail: 'Titanium + porcelain', price: 500 },
      { name: 'Porcelain Veneers (per tooth)', detail: 'E-max / Zirconia', price: 250 },
      { name: 'All-on-4 Implants', detail: 'Full arch restoration', price: 3500 },
      { name: 'Full Mouth Rehab', detail: 'Complete smile makeover', price: 5000 },
    ],
  },
  'cosmetic-surgery': {
    id: 'cosmetic-surgery', name: 'Cosmetic Surgery', rating: 4.8, icon: '✨', category: 'Cosmetic',
    description: 'From subtle enhancements to full transformations — rhinoplasty, liposuction, facelifts, breast procedures, and more.',
    types: ['Rhinoplasty (Nose Job)', 'Liposuction', 'Facelift & Neck Lift', 'Breast Augmentation / Reduction', 'Tummy Tuck (Abdominoplasty)', 'Botox & Fillers'],
    prices: { australia: 12000, usa: 10000, uk: 8000, thailand: 4000, turkey: 3000, singapore: 7000, malaysia: 3500, india: 2500 },
    stay: '7-14 days', recovery: '14-21 days',
    packages: [
      { name: 'Rhinoplasty', detail: 'Nose reshaping', price: 2500 },
      { name: 'Liposuction (single area)', detail: 'Body contouring', price: 1800 },
      { name: 'Breast Augmentation', detail: 'Silicone/saline implants', price: 3000 },
      { name: 'Full Mommy Makeover', detail: 'Tummy tuck + breast + lipo', price: 5500 },
    ],
  },
  'ivf': {
    id: 'ivf', name: 'IVF (In-Vitro Fertilization)', rating: 4.9, icon: '👶', category: 'Fertility',
    description: 'Advanced reproductive medicine including IVF, ICSI, egg freezing, genetic screening, and donor programs at world-class fertility centres.',
    types: ['IVF with Own Eggs', 'IVF with Donor Eggs', 'ICSI Treatment', 'Egg / Embryo Freezing', 'Genetic Testing (PGT)', 'Fertility Assessments'],
    prices: { australia: 12000, usa: 15000, uk: 8000, thailand: 5000, turkey: 4000, singapore: 10000, malaysia: 5000, india: 2500 },
    stay: '15-20 days', recovery: '2-3 days',
    packages: [
      { name: 'Basic IVF Cycle', detail: 'Stimulation to transfer', price: 2500 },
      { name: 'IVF + ICSI', detail: 'For male factor infertility', price: 3200 },
      { name: 'IVF + Donor Eggs', detail: 'Screened donor program', price: 4500 },
      { name: 'IVF + PGT Testing', detail: 'Genetic screening included', price: 4000 },
    ],
  },
  'surrogacy': {
    id: 'surrogacy', name: 'Surrogacy (Altruistic)', rating: 4.8, icon: '🤱', category: 'Fertility',
    description: 'Altruistic surrogacy for eligible Indian citizens under the Surrogacy (Regulation) Act, 2021. Commercial surrogacy is banned in India. Foreign nationals are NOT eligible. MedRouteIndia provides legal guidance, clinic coordination, and medical support for compliant surrogacy journeys.',
    legalNotice: 'IMPORTANT: Under the Surrogacy (Regulation) Act, 2021 — (1) Only altruistic surrogacy is legal. (2) Only Indian married couples (F:23-50, M:26-55) or Indian widows/divorcees (35-45) are eligible. (3) Foreign nationals, NRIs, PIOs, and OCIs cannot commission surrogacy in India. (4) The surrogate must be a close relative, married, aged 25-35, with at least one child. (5) Maximum 3 attempts per surrogate, once-in-lifetime. (6) 36-month insurance mandatory for surrogate.',
    types: ['Eligibility Assessment & Legal Consultation', 'National Surrogacy Board Application', 'Registered Clinic Coordination', 'IVF + Gestational Embryo Transfer', 'Surrogate Health Monitoring & Prenatal Care', 'Delivery Coordination & Parentage Documentation', '36-Month Surrogate Insurance', 'Post-Birth Legal Formalities'],
    prices: { australia: null, usa: null, uk: null, thailand: null, turkey: null, singapore: null, malaysia: null, india: null },
    priceNote: 'Surrogacy in India is altruistic only — no commercial pricing. Medical procedure costs (IVF, prenatal care, delivery) apply separately. Contact us for a detailed assessment.',
    stay: 'Multiple visits over 12-15 months', recovery: 'N/A',
    eligibility: {
      intendingCouple: 'Indian citizens, legally married, Female 23-50 yrs, Male 26-55 yrs, no surviving child, medical indication certified by District Medical Board',
      intendingWoman: 'Indian widow or divorcee, 35-45 yrs (2023 amendment), donor gametes permitted',
      surrogateMother: 'Married woman, 25-35 yrs, close relative, at least one child, once-in-lifetime, max 3 attempts, not genetically related to child',
      notEligible: 'Foreign nationals, NRIs, PIOs, OCIs, unmarried singles, same-sex couples, live-in partners'
    },
    packages: [
      { name: 'Legal Consultation & Eligibility Assessment', detail: 'Full legal review under Surrogacy Act 2021', price: 500 },
      { name: 'Complete Medical Coordination', detail: 'IVF, prenatal monitoring, delivery (medical costs only)', price: 8000 },
      { name: 'End-to-End Legal + Medical Support', detail: 'Board application, legal docs, clinic, insurance, delivery', price: 12000 },
    ],
  },
  'bariatric-surgery': {
    id: 'bariatric-surgery', name: 'Bariatric Surgery', rating: 4.7, icon: '⚖️', category: 'Weight Loss',
    description: 'Gastric bypass, sleeve gastrectomy, and mini-gastric bypass performed by experienced bariatric surgeons at JCI-accredited hospitals.',
    types: ['Gastric Sleeve', 'Roux-en-Y Gastric Bypass', 'Mini Gastric Bypass', 'Gastric Balloon', 'Revision Surgery'],
    prices: { australia: 20000, usa: 25000, uk: 15000, thailand: 8000, turkey: 5500, singapore: 12000, malaysia: 6000, india: 3500 },
    stay: '5-7 days', recovery: '14-21 days',
    packages: [
      { name: 'Gastric Sleeve', detail: 'Laparoscopic, JCI hospital, 5 nights', price: 3500 },
      { name: 'Roux-en-Y Bypass', detail: 'Full package with dietitian', price: 5000 },
      { name: 'Mini Gastric Bypass', detail: 'Less invasive, shorter stay', price: 4200 },
      { name: 'Gastric Balloon', detail: 'Non-surgical, outpatient', price: 2000 },
    ],
  },
  'lasik-eye': {
    id: 'lasik-eye', name: 'LASIK & Eye Care', rating: 4.8, icon: '👁️', category: 'Ophthalmology',
    description: 'Advanced vision correction with bladeless LASIK, SMILE, PRK, and cataract surgery using premium lenses at India\'s top eye hospitals.',
    types: ['Bladeless LASIK', 'SMILE Surgery', 'PRK', 'ICL (Implantable Lens)', 'Cataract Surgery', 'Retina Treatment'],
    prices: { australia: 5000, usa: 4000, uk: 3500, thailand: 2000, turkey: 1500, singapore: 3500, malaysia: 1800, india: 800 },
    stay: '2-3 days', recovery: '3-5 days',
    packages: [
      { name: 'LASIK (both eyes)', detail: 'Bladeless, Zeiss/Alcon laser', price: 800 },
      { name: 'SMILE Surgery (both eyes)', detail: 'Minimally invasive', price: 1200 },
      { name: 'Cataract Surgery (per eye)', detail: 'Premium IOL, phaco', price: 1500 },
      { name: 'ICL Implant (both eyes)', detail: 'For high prescriptions', price: 2500 },
    ],
  },
  'spine-neuro': {
    id: 'spine-neuro', name: 'Spine & Neurosurgery', rating: 4.8, icon: '🧠', category: 'Neurology',
    description: 'Minimally invasive spine surgery, disc replacement, brain tumour excision, and deep brain stimulation by India\'s top neurosurgeons.',
    types: ['Spinal Fusion', 'Disc Replacement', 'Minimally Invasive Spine Surgery', 'Brain Tumour Excision', 'Deep Brain Stimulation', 'Epilepsy Surgery'],
    prices: { australia: 40000, usa: 50000, uk: 30000, thailand: 15000, turkey: 10000, singapore: 25000, malaysia: 12000, india: 5000 },
    stay: '7-14 days', recovery: '30-90 days',
    packages: [
      { name: 'Spinal Fusion (single level)', detail: 'Robotic-assisted, JCI hospital', price: 5000 },
      { name: 'Disc Replacement', detail: 'Artificial disc, faster recovery', price: 6500 },
      { name: 'Brain Tumour Excision', detail: 'Neuro-navigation guided', price: 8000 },
      { name: 'Deep Brain Stimulation', detail: 'For Parkinson\'s/movement disorders', price: 12000 },
    ],
  },
  'cancer-treatment': {
    id: 'cancer-treatment', name: 'Cancer Treatment', rating: 4.9, icon: '🎗️', category: 'Oncology',
    description: 'Comprehensive oncology — chemotherapy, immunotherapy, CyberKnife, proton therapy, and surgical oncology at NCCN-aligned cancer centres.',
    types: ['Chemotherapy', 'Immunotherapy', 'CyberKnife / Gamma Knife', 'Proton Beam Therapy', 'Surgical Oncology', 'Bone Marrow Transplant'],
    prices: { australia: 50000, usa: 80000, uk: 40000, thailand: 18000, turkey: 12000, singapore: 35000, malaysia: 15000, india: 3000 },
    stay: 'Varies (7-90 days)', recovery: 'Varies',
    packages: [
      { name: 'CyberKnife Treatment', detail: 'Non-invasive radiation, outpatient', price: 3000 },
      { name: 'Chemotherapy (per cycle)', detail: 'International-protocol drugs', price: 800 },
      { name: 'Immunotherapy (per cycle)', detail: 'Keytruda/Opdivo equivalent', price: 2000 },
      { name: 'Bone Marrow Transplant', detail: 'Allogeneic/autologous, full package', price: 25000 },
    ],
  },
  'organ-transplant': {
    id: 'organ-transplant', name: 'Organ Transplant', rating: 4.9, icon: '🫀', category: 'Transplant',
    description: 'Kidney, liver, and heart transplants with world-class post-operative care. India is a global leader in living-donor transplants.',
    types: ['Kidney Transplant', 'Liver Transplant', 'Heart Transplant', 'Cornea Transplant', 'Bone Marrow Transplant'],
    prices: { australia: 80000, usa: 120000, uk: 70000, thailand: 35000, turkey: 25000, singapore: 60000, malaysia: 30000, india: 12000 },
    stay: '21-45 days', recovery: '60-90 days',
    packages: [
      { name: 'Kidney Transplant', detail: 'Living donor, full workup', price: 12000 },
      { name: 'Liver Transplant', detail: 'Living donor, ICU + ward', price: 28000 },
      { name: 'Heart Transplant', detail: 'Full cardiac ICU package', price: 40000 },
      { name: 'Cornea Transplant', detail: 'Donor cornea, outpatient', price: 2500 },
    ],
  },
  'executive-health-check': {
    id: 'executive-health-check', name: 'Executive Health Check', rating: 4.7, icon: '🩺', category: 'Preventive',
    description: 'Comprehensive full-body screening — cardiac, cancer markers, hormonal, genetic — at premium hospitals. Same-day reports.',
    types: ['Basic Health Screen', 'Advanced Cardiac Screen', 'Cancer Marker Panel', 'Full Body MRI', 'Genetic Health Assessment', 'Women\'s / Men\'s Wellness'],
    prices: { australia: 2500, usa: 3000, uk: 2000, thailand: 800, turkey: 600, singapore: 1500, malaysia: 500, india: 450 },
    stay: '1-2 days', recovery: 'None',
    packages: [
      { name: 'Essential Health Screen', detail: '70+ tests, cardiac, diabetes, thyroid', price: 250 },
      { name: 'Executive Full Body', detail: '150+ tests, MRI, echo, stress test', price: 450 },
      { name: 'Platinum Genetic Screen', detail: 'Full body + genetic markers + cancer', price: 900 },
      { name: 'Couples Fertility Check', detail: 'Comprehensive fertility workup', price: 350 },
    ],
  },
  'ayurveda-wellness': {
    id: 'ayurveda-wellness', name: 'Ayurveda & Wellness', rating: 4.6, icon: '🧘', category: 'Wellness',
    description: 'Authentic Panchakarma, yoga retreats, rejuvenation programs, and integrative medicine at Kerala\'s top wellness centres.',
    types: ['Panchakarma Detox', 'Yoga & Meditation Retreat', 'Rejuvenation Therapy', 'Stress Management', 'Weight Management', 'Joint & Spine Therapy'],
    prices: { australia: 5000, usa: 6000, uk: 4000, thailand: 2500, turkey: null, singapore: 3500, malaysia: 2000, india: 1200 },
    stay: '14-28 days', recovery: 'Ongoing wellness',
    packages: [
      { name: 'Panchakarma (14 days)', detail: 'Traditional detox, Kerala resort', price: 1200 },
      { name: 'Yoga Retreat (21 days)', detail: 'Rishikesh/Kerala, certified instructors', price: 1800 },
      { name: 'Rejuvenation (28 days)', detail: 'Full Rasayana program', price: 2500 },
      { name: 'Joint Therapy (14 days)', detail: 'Ayurvedic + physio for arthritis', price: 1500 },
    ],
  },
  'second-opinion': {
    id: 'second-opinion', name: 'Second Opinion', rating: 4.8, icon: '📋', category: 'Consultation',
    description: 'Get a verified second opinion from India\'s top specialists via telemedicine. Full medical record review and written report.',
    types: ['Oncology Second Opinion', 'Cardiac Second Opinion', 'Orthopaedic Second Opinion', 'Neurology Second Opinion', 'General Second Opinion'],
    prices: { australia: 500, usa: 600, uk: 400, thailand: 200, turkey: 150, singapore: 350, malaysia: 180, india: 99 },
    stay: 'Remote / Telemedicine', recovery: 'N/A',
    packages: [
      { name: 'Standard Second Opinion', detail: 'Record review + written report', price: 99 },
      { name: 'Specialist Video Consult', detail: '30-min video with top specialist', price: 150 },
      { name: 'Comprehensive Review', detail: 'Multi-specialist panel + report', price: 250 },
    ],
  },
};

const COUNTRY_FLAGS = {
  australia: '🇦🇺', usa: '🇺🇸', uk: '🇬🇧', thailand: '🇹🇭', turkey: '🇹🇷', singapore: '🇸🇬', malaysia: '🇲🇾', india: '🇮🇳'
};

const DOCTORS = [
  // Hair Transplant (4)
  { id: 'dr-gaurang-krishna', name: 'Dr. Gaurang Krishna', specialty: 'Hair Transplant', experience: 20, hospital: 'MedLinks, New Delhi & Gurgaon', credentials: ['MBBS (Mumbai), MD Dermatology (AIIMS)', 'Inventor of PERFECT-i Hair Transplant Technique', 'Honoured at British Parliament, House of Commons'], website: 'https://medlinkshairtransplants.com', photo: '/images/doctors/dr-gaurang-krishna.png' },
  { id: 'dr-pradeep-sethi', name: 'Dr. Pradeep Sethi', specialty: 'Hair Transplant', experience: 20, hospital: 'Eugenix Hair Sciences, Delhi', credentials: ['MBBS, MD Dermatology (AIIMS)', 'ISHRS Fellow — Pioneer of DHT Technique', '4,500+ hair transplant surgeries'], website: 'https://eugenix.in' },
  { id: 'dr-abhishek-pilani', name: 'Dr. Abhishek Pilani', specialty: 'Hair Transplant', experience: 15, hospital: 'Assure Clinic, Mumbai', credentials: ['MBBS, MS, MCh', 'ISHRS Member, DHA Licensed', '20,000+ successful hair transplants'], website: 'https://assureclinic.com' },
  // Dental (3)
  { id: 'dr-vikas-gowd', name: 'Prof. Dr. Vikas Gowd', specialty: 'Dental Implantology', experience: 25, hospital: "Dr. Gowds' Dental Hospitals, Hyderabad", credentials: ['MDS, FICD, FICOI, DICOI', 'Pioneer of Immediate Implant Technique', '15,000+ dental implants placed'], website: 'https://drgowds.com' },
  { id: 'dr-aman-ahuja', name: 'Dr. Aman Ahuja', specialty: 'Dental Implantology', experience: 15, hospital: 'Cosmodent India, Gurugram', credentials: ['BDS, MDS — Gold Medalist', 'Fellowship in Advanced Implantology (NYU)', 'Zygomatic Implants & Full Mouth Rehabilitation Specialist'], website: 'https://cosmodentindia.com' },
  { id: 'dr-priyank-sethi', name: 'Dr. Priyank Sethi', specialty: 'Cosmetic Dentistry & Implants', experience: 20, hospital: 'The Dental House, Delhi', credentials: ['BDS, MDS, PhD Dental Sciences', 'Certified in Digital Smile Design', 'Awarded Best Dentist in India — 1,000+ global patients'], website: 'https://priyanksethi.com' },
  // IVF (3)
  { id: 'dr-hrishikesh-pai', name: 'Dr. Hrishikesh Pai', specialty: 'Fertility & IVF', experience: 35, hospital: 'Bloom IVF Group, Mumbai & Delhi', credentials: ['MBBS, MD (OB-GYN)', 'Former President — FOGSI & ISAR', '7 IVF centres across India, 35+ years experience'], website: 'https://drhrishikeshpai.com' },
  { id: 'dr-mona-dahiya', name: 'Dr. Mona Dahiya', specialty: 'Fertility & IVF', experience: 25, hospital: 'Little Angel IVF, Noida', credentials: ['MBBS, MD, DNB (OB-GYN)', '25,000+ couples helped, 90%+ success rate', '100+ publications, 50+ awards including Times Now Excellence Award'], website: 'https://drmonadahiya.com' },
  { id: 'dr-gautam-daftary', name: 'Dr. Gautam Daftary', specialty: 'Fertility & IVF', experience: 20, hospital: 'Aksigen IVF, Mumbai', credentials: ['MBBS, MD (OB-GYN), DNB', 'National Fertility Awards 2026 — IVF Clinic of the Year', 'Pioneer of ROOTS 360 Fertility Framework'], website: 'https://aksigenivf.com' },
];

// ==================== AUTH MIDDLEWARE ====================

function authMiddleware(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (!token) return res.status(401).json({ success: false, error: 'Authentication required.' });
  try {
    req.user = jwt.verify(token, JWT_SECRET);
    next();
  } catch { return res.status(401).json({ success: false, error: 'Invalid or expired token.' }); }
}

function optionalAuth(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  if (token) { try { req.user = jwt.verify(token, JWT_SECRET); } catch {} }
  next();
}

// ==================== AUTH ROUTES ====================

app.post('/api/auth/register', (req, res) => {
  try {
    const { name, email, password, phone, country } = req.body;
    if (!name || !email || !password) return res.status(400).json({ success: false, error: 'Name, email, and password are required.' });
    if (password.length < 6) return res.status(400).json({ success: false, error: 'Password must be at least 6 characters.' });
    if (!isValidEmail(email)) return res.status(400).json({ success: false, error: 'Invalid email address.' });

    const db = getDb();
    const existing = db.prepare('SELECT id FROM users WHERE email = ?').get(email);
    if (existing) return res.status(409).json({ success: false, error: 'An account with this email already exists.' });

    const id = uuidv4();
    const hashedPassword = bcrypt.hashSync(password, 10);
    db.prepare('INSERT INTO users (id, name, email, password, phone, country, auth_provider) VALUES (?, ?, ?, ?, ?, ?, ?)').run(id, name, email, hashedPassword, phone || null, country || null, 'email');

    const token = jwt.sign({ id, name, email }, JWT_SECRET, { expiresIn: '7d' });
    res.status(201).json({ success: true, message: 'Account created successfully!', token, user: { id, name, email, country: country || null } });
  } catch (err) {
    console.error('Register error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong.' });
  }
});

app.post('/api/auth/login', (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) return res.status(400).json({ success: false, error: 'Email and password required.' });

    const db = getDb();
    const user = db.prepare('SELECT * FROM users WHERE email = ?').get(email);
    if (!user) return res.status(401).json({ success: false, error: 'Invalid email or password.' });
    if (!bcrypt.compareSync(password, user.password)) return res.status(401).json({ success: false, error: 'Invalid email or password.' });

    const token = jwt.sign({ id: user.id, name: user.name, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, token, user: { id: user.id, name: user.name, email: user.email, country: user.country } });
  } catch (err) {
    console.error('Login error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong.' });
  }
});

// Social login: verify token with provider, create/find user, return JWT
app.post('/api/auth/social', async (req, res) => {
  try {
    const { provider, token, id_token } = req.body;
    console.log(`[Social Auth] Provider: ${provider}, has token: ${!!token}, has id_token: ${!!id_token}`);
    if (!provider || (!token && !id_token)) return res.status(400).json({ success: false, error: 'Provider and token required.' });

    let profile = null;

    if (provider === 'google') {
      let gData;
      if (id_token) {
        console.log('[Social Auth] Verifying Google id_token...');
        const gRes = await fetch('https://oauth2.googleapis.com/tokeninfo?id_token=' + id_token);
        console.log('[Social Auth] Google tokeninfo status:', gRes.status);
        if (!gRes.ok) return res.status(401).json({ success: false, error: 'Invalid Google token.' });
        gData = await gRes.json();
        profile = { id: gData.sub, name: gData.name, email: gData.email, avatar: gData.picture };
      } else if (token) {
        console.log('[Social Auth] Verifying Google access_token via userinfo...');
        const gRes = await fetch('https://www.googleapis.com/oauth2/v3/userinfo', { headers: { Authorization: 'Bearer ' + token } });
        console.log('[Social Auth] Google userinfo status:', gRes.status);
        if (!gRes.ok) {
          const errText = await gRes.text();
          console.error('[Social Auth] Google userinfo error:', errText);
          return res.status(401).json({ success: false, error: 'Invalid Google access token.' });
        }
        gData = await gRes.json();
        console.log('[Social Auth] Got user:', gData.name, gData.email);
        profile = { id: gData.sub, name: gData.name, email: gData.email, avatar: gData.picture };
      } else {
        return res.status(400).json({ success: false, error: 'Google token required.' });
      }
    } else if (provider === 'facebook' || provider === 'instagram') {
      const fbRes = await fetch('https://graph.facebook.com/me?fields=id,name,email,picture.type(large)&access_token=' + token);
      if (!fbRes.ok) return res.status(401).json({ success: false, error: 'Invalid Facebook token.' });
      const fbData = await fbRes.json();
      profile = { id: fbData.id, name: fbData.name, email: fbData.email, avatar: fbData.picture?.data?.url };
    } else {
      return res.status(400).json({ success: false, error: 'Unsupported provider.' });
    }

    if (!profile || !profile.email) return res.status(401).json({ success: false, error: 'Could not retrieve email from provider.' });

    const db = getDb();
    let user = db.prepare('SELECT * FROM users WHERE email = ?').get(profile.email);

    if (!user) {
      const id = uuidv4();
      db.prepare('INSERT INTO users (id, name, email, password, auth_provider, provider_id, avatar) VALUES (?, ?, ?, ?, ?, ?, ?)').run(id, profile.name, profile.email, null, provider, profile.id, profile.avatar || null);
      user = { id, name: profile.name, email: profile.email, country: null, auth_provider: provider, avatar: profile.avatar };
    } else if (!user.auth_provider || user.auth_provider === 'email') {
      db.prepare('UPDATE users SET auth_provider = ?, provider_id = ?, avatar = ? WHERE id = ?').run(provider, profile.id, profile.avatar || null, user.id);
      user.auth_provider = provider;
      user.avatar = profile.avatar;
    }

    const jwtToken = jwt.sign({ id: user.id, name: user.name, email: user.email }, JWT_SECRET, { expiresIn: '7d' });
    res.json({ success: true, token: jwtToken, user: { id: user.id, name: user.name, email: user.email, country: user.country, avatar: user.avatar, provider } });
  } catch (err) {
    console.error('Social auth error:', err);
    res.status(500).json({ success: false, error: 'Social login failed. Please try again.' });
  }
});

app.get('/api/auth/me', authMiddleware, (req, res) => {
  const db = getDb();
  const user = db.prepare('SELECT id, name, email, phone, country, created_at FROM users WHERE id = ?').get(req.user.id);
  if (!user) return res.status(404).json({ success: false, error: 'User not found.' });
  res.json({ success: true, user });
});

// ==================== CONSULTATIONS ====================

app.post('/api/consultations', (req, res) => {
  try {
    const { name, email, phone, country, treatment, message, preferred_date, consultant } = req.body;
    if (!name || !email) return res.status(400).json({ success: false, error: 'Name and email required.' });
    if (!isValidEmail(email)) return res.status(400).json({ success: false, error: 'Invalid email.' });

    const db = getDb();
    const id = uuidv4();
    db.prepare('INSERT INTO consultations (id, name, email, phone, country, treatment, message, preferred_date, consultant) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)').run(id, name, email, phone || null, country || null, treatment || null, message || null, preferred_date || null, consultant || null);

    res.status(201).json({ success: true, message: 'Consultation booked! Our team will contact you within 24 hours.', booking_id: id });
  } catch (err) {
    console.error('Consultation error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong.' });
  }
});

app.post('/api/contact', (req, res) => {
  try {
    const { name, email, country, treatment } = req.body;
    if (!name || !email) return res.status(400).json({ success: false, error: 'Name and email required.' });
    const db = getDb();
    db.prepare('INSERT INTO contact_submissions (id, name, email, country, treatment) VALUES (?, ?, ?, ?, ?)').run(uuidv4(), name, email, country || null, treatment || null);
    res.status(201).json({ success: true, message: 'Thank you! We will send you a treatment plan within 24 hours.' });
  } catch (err) { res.status(500).json({ success: false, error: 'Something went wrong.' }); }
});

app.post('/api/newsletter', (req, res) => {
  try {
    const { email } = req.body;
    if (!email || !isValidEmail(email)) return res.status(400).json({ success: false, error: 'Valid email required.' });
    const db = getDb();
    const existing = db.prepare('SELECT id FROM newsletter_subscribers WHERE email = ?').get(email);
    if (existing) return res.json({ success: true, message: 'Already subscribed!' });
    db.prepare('INSERT INTO newsletter_subscribers (id, email) VALUES (?, ?)').run(uuidv4(), email);
    res.status(201).json({ success: true, message: 'Subscribed!' });
  } catch (err) { res.status(500).json({ success: false, error: 'Something went wrong.' }); }
});

// ==================== TREATMENTS & COMPARE ====================

app.get('/api/treatments', (req, res) => { res.json({ success: true, data: TREATMENTS }); });
app.get('/api/treatments/:id', (req, res) => {
  const t = TREATMENTS[req.params.id];
  if (!t) return res.status(404).json({ success: false, error: 'Treatment not found.' });
  res.json({ success: true, data: t });
});

app.get('/api/compare', (req, res) => {
  const { treatment } = req.query;
  if (!treatment || !TREATMENTS[treatment]) return res.status(400).json({ success: false, error: 'Valid treatment required.' });
  const t = TREATMENTS[treatment];
  const indiaPrice = t.prices.india;
  const comparison = Object.entries(t.prices).filter(([, v]) => v !== null).map(([country, price]) => ({
    country, flag: COUNTRY_FLAGS[country] || '', price, currency: 'USD',
    savings: (country !== 'india' && indiaPrice != null) ? Math.round(((price - indiaPrice) / price) * 100) : 0,
  })).sort((a, b) => b.price - a.price);
  res.json({ success: true, treatment: t.name, data: comparison, indiaPrice: t.prices.india, packages: t.packages });
});

// ==================== DOCTORS & CONSULTANTS ====================

app.get('/api/doctors', (req, res) => res.json({ success: true, data: DOCTORS }));
app.get('/api/consultants', (req, res) => res.json({ success: true, data: CONSULTANTS }));
app.get('/api/consultants/:id', (req, res) => {
  const c = CONSULTANTS.find(x => x.id === req.params.id);
  if (!c) return res.status(404).json({ success: false, error: 'Consultant not found.' });
  res.json({ success: true, data: c });
});

// ==================== AI CHAT ====================

app.post('/api/chat', optionalAuth, (req, res) => {
  try {
    const { session_id, message, context } = req.body;
    if (!message) return res.status(400).json({ success: false, error: 'Message required.' });

    const lowerMsg = message.toLowerCase();
    let reply = '';
    let suggestions = [];
    let planData = null;

    if (!context || !context.step) {
      if (lowerMsg.includes('hair') || lowerMsg.includes('bald') || lowerMsg.includes('transplant')) {
        reply = "Great! You're interested in **Hair Transplant** treatment. India is the world's top destination for hair restoration — saving up to 90% vs typical prices.\n\nTo create your personalised plan, I need a few details:\n\n**What type of hair loss are you experiencing?**";
        suggestions = ['Receding hairline', 'Thinning crown', 'Full baldness (Norwood 5-7)', 'Beard/eyebrow transplant'];
      } else if (lowerMsg.includes('dental') || lowerMsg.includes('teeth') || lowerMsg.includes('implant') || lowerMsg.includes('veneer')) {
        reply = "Wonderful! **Dental treatment** in India uses the same premium materials (Nobel Biocare, Straumann) as top clinics worldwide — at 90% less.\n\nTo build your plan:\n\n**What dental treatment are you looking for?**";
        suggestions = ['Single/multiple implants', 'Veneers or smile makeover', 'Full mouth rehabilitation', 'Root canal or crowns'];
      } else if (lowerMsg.includes('cosmetic') || lowerMsg.includes('plastic') || lowerMsg.includes('nose') || lowerMsg.includes('lipo') || lowerMsg.includes('breast') || lowerMsg.includes('facelift')) {
        reply = "Excellent choice! **Cosmetic surgery** in India is performed by internationally trained plastic surgeons at JCI-accredited hospitals.\n\n**What procedure interests you?**";
        suggestions = ['Rhinoplasty (nose)', 'Liposuction', 'Breast augmentation/reduction', 'Facelift / tummy tuck'];
      } else if (lowerMsg.includes('ivf') || lowerMsg.includes('fertility') || lowerMsg.includes('conceive') || lowerMsg.includes('baby')) {
        reply = "I understand. **IVF treatment** in India has excellent success rates (55-65%) at world-class fertility centres, at a fraction of typical costs.\n\n**Can you tell me more about your situation?**";
        suggestions = ['First time trying IVF', 'Failed IVF cycles elsewhere', 'Need donor eggs/sperm', 'Want genetic testing (PGT)'];
      } else if (lowerMsg.includes('surrogacy') || lowerMsg.includes('surrogate')) {
        reply = "**Important Legal Notice:** Under the **Surrogacy (Regulation) Act, 2021**, only **altruistic surrogacy** is legal in India. Commercial surrogacy is banned.\n\n**Who is eligible?**\n- Indian married couples (F: 23-50, M: 26-55) with medical indication and no surviving child\n- Indian widows/divorcees (35-45 yrs) — per 2023 amendment\n\n**NOT eligible:** Foreign nationals, NRIs, PIOs, OCIs, unmarried singles, same-sex couples.\n\nMedRouteIndia provides **legal consultation, eligibility assessment, registered clinic coordination, and medical support** for eligible Indian citizens.\n\n**How can I help you?**";
        suggestions = ['Am I eligible? (Indian citizen)', 'Explain the legal process', 'What does it cost? (medical expenses)', 'Book surrogacy legal consultation'];
      } else {
        reply = "Welcome to **MedRouteIndia**! 🏥 I'm your AI medical tourism assistant.\n\nI can help you explore treatments, compare costs, and create a personalised travel plan. **What treatment are you interested in?**";
        suggestions = ['Hair Transplant', 'Dental Implants', 'Cosmetic Surgery', 'IVF Treatment', 'Surrogacy Law'];
      }
    } else if (context.step === 'details') {
      reply = "Thanks for sharing that! Now, to create your approximate plan:\n\n**What's your preferred timeline for treatment?**";
      suggestions = ['Within 1 month', '1-3 months', '3-6 months', 'Flexible / no rush'];
    } else if (context.step === 'timeline') {
      reply = "Great! And one last question:\n\n**What's your approximate budget (in USD)?**";
      suggestions = ['Under $3,000', '$3,000 - $8,000', '$8,000 - $15,000', '$15,000+', 'Need cost estimate first'];
    } else if (context.step === 'budget') {
      const treatment = context.treatment || 'Hair Transplant';
      const treatmentKey = Object.keys(TREATMENTS).find(k => TREATMENTS[k].name.toLowerCase().includes(treatment.toLowerCase())) || 'hair-transplant';
      const t = TREATMENTS[treatmentKey];

      const indiaPrice = t.prices.india || 0;
      const usaPrice = t.prices.usa || 0;
      planData = {
        treatment: t.name,
        estimatedCost: indiaPrice ? ('$' + (t.packages[1]?.price || indiaPrice).toLocaleString()) : 'Contact for assessment',
        homeCost: usaPrice ? ('$' + usaPrice.toLocaleString()) : 'N/A',
        savings: (usaPrice && indiaPrice) ? (Math.round(((usaPrice - indiaPrice) / usaPrice) * 100) + '%') : 'N/A',
        duration: t.stay,
        recovery: t.recovery,
        hospital: DOCTORS.find(d => d.specialty.toLowerCase().includes(t.category.toLowerCase()))?.hospital || 'Apollo Hospitals, Delhi',
        doctor: DOCTORS.find(d => d.specialty.toLowerCase().includes(t.category.toLowerCase()))?.name || 'To be assigned',
        timeline: context.timeline || '1-3 months',
        steps: [
          { day: 'Pre-Trip', task: 'Free video consultation with specialist', detail: 'Share medical reports, discuss treatment plan' },
          { day: 'Week Before', task: 'Visa & travel arrangements', detail: 'e-Medical visa, flights, hotel booking' },
          { day: 'Day 1', task: 'Arrive in India', detail: 'Airport pickup, hotel check-in, rest' },
          { day: 'Day 2', task: 'Hospital consultation', detail: 'In-person assessment, final treatment plan, pre-op tests' },
          { day: 'Day 3-' + (parseInt(t.stay) || 5), task: 'Treatment / Procedure', detail: 'Procedure at JCI-accredited hospital with dedicated care coordinator' },
          { day: 'Post-Treatment', task: 'Recovery period', detail: t.recovery + ' recovery, daily check-ups, medication' },
          { day: 'Before Departure', task: 'Final check-up', detail: 'Clearance from doctor, medical reports, prescriptions' },
          { day: 'Back Home', task: 'Telemedicine follow-up', detail: '12 months of video follow-up with your Indian specialist' },
        ],
        consultant: CONSULTANTS.find(c => c.specialties.some(s => s.toLowerCase().includes(t.category.toLowerCase())))?.name || 'Sarah Mitchell',
      };

      reply = `Here's your **approximate treatment plan**:\n\n🏥 **Treatment:** ${planData.treatment}\n💰 **Estimated Cost in India:** ${planData.estimatedCost}\n🌍 **Same Abroad:** ${planData.homeCost}\n📊 **You Save:** ${planData.savings}\n🏨 **Recommended Hospital:** ${planData.hospital}\n👨‍⚕️ **Recommended Doctor:** ${planData.doctor}\n📅 **Stay Duration:** ${planData.duration}\n🔄 **Recovery:** ${planData.recovery}\n\n✅ This plan includes consultation, procedure, hospital stay, airport transfers, and post-op care.\n\n📄 **You can download this plan as a PDF** using the button below.\n\n*For a more accurate and personalised plan, we recommend booking a free consultation with **${planData.consultant}**, our specialist consultant.*`;
      suggestions = ['Download PDF Plan', 'Book Consultant: ' + planData.consultant, 'Compare costs with other countries', 'Start over'];
    } else {
      reply = "I'm here to help! What would you like to know about medical treatment in India?";
      suggestions = ['Hair Transplant', 'Dental Implants', 'Cosmetic Surgery', 'IVF Treatment', 'Surrogacy Law'];
    }

    const sessionId = session_id || uuidv4();
    if (planData) {
      const db = getDb();
      try {
        db.prepare('INSERT OR REPLACE INTO chat_sessions (id, user_id, treatment, messages, plan_generated, plan_data, updated_at) VALUES (?, ?, ?, ?, 1, ?, datetime("now"))').run(sessionId, req.user?.id || null, context?.treatment || null, '[]', JSON.stringify(planData));
      } catch {}
    }

    res.json({ success: true, session_id: sessionId, reply, suggestions, plan: planData });
  } catch (err) {
    console.error('Chat error:', err);
    res.status(500).json({ success: false, error: 'Chat service error.' });
  }
});

// ==================== JOURNEY PLANNER ====================

app.post('/api/journey/plan', (req, res) => {
  try {
    const { name, email, treatment, country, budget, travel_date } = req.body;
    if (!name || !email || !treatment) return res.status(400).json({ success: false, error: 'Name, email, and treatment required.' });

    const treatmentKey = Object.keys(TREATMENTS).find(k => TREATMENTS[k].name.toLowerCase().includes(treatment.toLowerCase())) || Object.keys(TREATMENTS)[0];
    const t = TREATMENTS[treatmentKey];

    const planData = {
      treatment: t.name,
      estimatedCost: t.prices.india,
      auCost: t.prices.australia,
      savings: Math.round(((t.prices.australia - t.prices.india) / t.prices.australia) * 100),
      stay: t.stay,
      recovery: t.recovery,
      packages: t.packages,
      hospital: DOCTORS.find(d => d.specialty.toLowerCase().includes(t.category.toLowerCase()))?.hospital || 'Apollo Hospitals',
      doctor: DOCTORS.find(d => d.specialty.toLowerCase().includes(t.category.toLowerCase()))?.name || 'To be assigned',
      consultant: CONSULTANTS.find(c => c.specialties.some(s => s.toLowerCase().includes(t.category.toLowerCase())))?.name || CONSULTANTS[0].name,
    };

    const db = getDb();
    const id = uuidv4();
    db.prepare('INSERT INTO journey_plans (id, name, email, treatment, country, budget, travel_date, plan_data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)').run(id, name, email, treatment, country || 'Australia', budget || null, travel_date || null, JSON.stringify(planData));

    res.status(201).json({ success: true, plan_id: id, plan: planData });
  } catch (err) {
    console.error('Journey error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong.' });
  }
});

app.get('/api/journey/:id', (req, res) => {
  const db = getDb();
  const plan = db.prepare('SELECT * FROM journey_plans WHERE id = ?').get(req.params.id);
  if (!plan) return res.status(404).json({ success: false, error: 'Plan not found.' });
  res.json({ success: true, data: { ...plan, plan_data: JSON.parse(plan.plan_data || '{}') } });
});

// ==================== ADMIN ====================

app.get('/api/admin/consultations', (req, res) => { try { res.json({ success: true, data: getDb().prepare('SELECT * FROM consultations ORDER BY created_at DESC').all() }); } catch { res.status(500).json({ success: false }); } });
app.get('/api/admin/contacts', (req, res) => { try { res.json({ success: true, data: getDb().prepare('SELECT * FROM contact_submissions ORDER BY created_at DESC').all() }); } catch { res.status(500).json({ success: false }); } });
app.get('/api/admin/stats', (req, res) => {
  try {
    const db = getDb();
    res.json({ success: true, data: {
      totalConsultations: db.prepare('SELECT COUNT(*) as c FROM consultations').get().c,
      totalContacts: db.prepare('SELECT COUNT(*) as c FROM contact_submissions').get().c,
      totalUsers: db.prepare('SELECT COUNT(*) as c FROM users').get().c,
      totalSubscribers: db.prepare('SELECT COUNT(*) as c FROM newsletter_subscribers').get().c,
      topTreatments: db.prepare('SELECT treatment, COUNT(*) as count FROM consultations WHERE treatment IS NOT NULL GROUP BY treatment ORDER BY count DESC LIMIT 5').all(),
    }});
  } catch { res.status(500).json({ success: false }); }
});

// ==================== CLAUDE AI AGENT ====================

const CLAUDE_BASE_URL = process.env.CLAUDE_BASE_URL || 'https://anthropic.prod.ai-gateway.quantumblack.com/3500a962-bc81-4f66-9c11-80e340a37bfc';
const CLAUDE_API_KEY = process.env.CLAUDE_API_KEY || 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJkaGk3OW9NajBaMThTVEktci1FbGZYUnF6STJrXzhrbWZXSHVWaVZFd19BIn0.eyJleHAiOjE3NzUzOTk0NjgsImlhdCI6MTc3NTM2MzUyMSwiYXV0aF90aW1lIjoxNzc1MzYzNTIwLCJqdGkiOiI3Y2MwYzg0NC1lM2RlLTQ5NWQtOTYxZS1kN2I1ZDQwMGRmYzIiLCJpc3MiOiJodHRwczovL2F1dGgubWNraW5zZXkuaWQvYXV0aC9yZWFsbXMvciIsImF1ZCI6ImJjZDIzNzI4LTNkMjctNDQ3Yy1hMGE5LWVhY2FmMzkzYTZmNSIsInN1YiI6ImI0NDRiYmViLTM2MTctNGNlNy05ZGQyLWRhMmVjYTU0OTI1NyIsInR5cCI6IklEIiwiYXpwIjoiYmNkMjM3MjgtM2QyNy00NDdjLWEwYTktZWFjYWYzOTNhNmY1Iiwic2Vzc2lvbl9zdGF0ZSI6Ijk4MTMwNWZiLTAwZjMtNGQyNi04NzM0LTY1N2Q5NTY2OGNkNSIsImF0X2hhc2giOiI2eGtuVWs3T0w0OGdmX01pd2hENVdRIiwibmFtZSI6IlJhaHVsIEdhdXRhbSIsImdpdmVuX25hbWUiOiJSYWh1bCIsImZhbWlseV9uYW1lIjoiR2F1dGFtIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiZjQzNDNkYzc1NmM1ZWUxMCIsImVtYWlsIjoiUmFodWxfR2F1dGFtQG1ja2luc2V5LmNvbSIsImFjciI6IjEiLCJzaWQiOiI5ODEzMDVmYi0wMGYzLTRkMjYtODczNC02NTdkOTU2NjhjZDUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZm1ubyI6IjMyODc1MCIsImdyb3VwcyI6WyI2ZmE3Nzc5MC0wY2RlLTQzY2EtOGRjYS02YTM0OWU5YjRlMTQiLCI3MDdkZTUwMy00MmUwLTQ5N2YtYmE3YS1kZmQzZmM2NDUzMDQiLCJBbGwgRmlybSBVc2VycyIsIjM1MDBhOTYyLWJjODEtNGY2Ni05YzExLTgwZTM0MGEzN2JmYyIsIjc0ZWFiYWQxLWQ4M2EtNDJhMy05MjFjLTA3ZGQ4NDgxNzI3OCJdfQ.IpRvmAG-MxW8QirLjnfPiMaaTmNeNF2FgmebtcEsL4PhMrfd04Sk8GoFH5gvGVBT59eYMv0Fh6E3QohNF-PjHSM1Cnq-RHvIQLnlHNl2p6XOur8n4qu7ujOEjEK8dYLw-Y4pnX1j-WOEtXS5BtIv4KnaKooQ26WtkUh67MMKeIB-YyRARdKLFGIBEBcEjfUutZY2L7njGnX4S4KTn_utYymA2Jd3GPEzea9aioTIpyzrys2ClLhq9jNFlKcDqy9wgYwyHWT1ufpyNSgNc5VWlkXUZnrh9cj4eZmezyUEGTu3V-6AAV5YGz6fXHRZjfExnby_wQxffWBbzLYxCMYlqg';
const CLAUDE_MODEL = 'claude-haiku-4-5-20251001';

const AI_SYSTEM_PROMPT = `You are MedRouteIndia' world-class AI medical tourism consultant. You help international patients from around the world explore and plan medical treatment in India. Do NOT assume the patient is from any specific country — ask where they are from if needed.

YOUR KNOWLEDGE BASE:

TREATMENTS & PRICING (USD equivalents):
1. Hair Transplant Surgery ⭐ 4.8
   - India: $1,200–3,000 | Typical home country: $12,000–16,000
   - Types: FUE, FUT, DHI, Sapphire, Beard/Eyebrow, PRP
   - Packages: FUE 2000 grafts $1,200 | FUE 3000 $1,500 | DHI 3500 $2,200 | Mega 5000+ $3,000
   - Stay: 3-5 days | Recovery: 7-10 days
   - Recommended Doctors:
     • Dr. Gaurang Krishna — MedLinks, New Delhi & Gurgaon (MD AIIMS, Inventor of PERFECT-i Technique, Honoured at British Parliament)
     • Dr. Pradeep Sethi — Eugenix Hair Sciences, Delhi (ISHRS Fellow, Pioneer of DHT Technique, 4,500+ surgeries)
     • Dr. Abhishek Pilani — Assure Clinic, Mumbai (20,000+ transplants, patented UFME & DSHI techniques)

2. Dental Implants ⭐ 4.7
   - India: $250–5,000 | Typical home country: $3,500–5,500
   - Types: Single implant, All-on-4, Veneers, Full mouth rehab, Root canal, Whitening
   - Packages: Single implant $500 | Veneers/tooth $250 | All-on-4 $3,500 | Full mouth $5,000
   - Stay: 5-7 days | Recovery: 3-5 days
   - Recommended Doctors:
     • Prof. Dr. Vikas Gowd — Dr. Gowds' Dental Hospitals, Hyderabad (Pioneer of Immediate Implant Technique, 15,000+ implants)
     • Dr. Aman Ahuja — Cosmodent India, Gurugram (NYU Fellowship, Gold Medalist, Zygomatic Implant specialist)
     • Dr. Priyank Sethi — The Dental House, Delhi (BDS, MDS, PhD, Awarded Best Dentist in India)

3. Cosmetic Surgery ⭐ 4.8
   - India: $1,800–5,500 | Typical home country: $8,000–12,000
   - Types: Rhinoplasty, Liposuction, Facelift, Breast aug/reduction, Tummy tuck, Botox
   - Packages: Rhinoplasty $2,500 | Lipo $1,800 | Breast aug $3,000 | Mommy makeover $5,500
   - Stay: 7-14 days | Recovery: 14-21 days
   - Recommended Hospital: Fortis Mumbai

4. IVF (In-Vitro Fertilization) ⭐ 4.9
   - India: $2,500–4,500 | Typical home country: $8,000–15,000
   - Types: IVF own eggs, Donor eggs, ICSI, Egg freezing, PGT, Fertility assessment
   - Packages: Basic IVF $2,500 | IVF+ICSI $3,200 | Donor eggs $4,500 | IVF+PGT $4,000
   - Stay: 15-20 days | Recovery: 2-3 days
   - Recommended Doctors:
     • Dr. Hrishikesh Pai — Bloom IVF Group, Mumbai & Delhi (35+ yrs, Former President FOGSI & ISAR, 7 IVF centres)
     • Dr. Mona Dahiya — Little Angel IVF, Noida (25+ yrs, 25,000+ couples, 90%+ success rate)
     • Dr. Gautam Daftary — Aksigen IVF, Mumbai (National Fertility Awards 2026 winner, ROOTS 360 framework)

5. Surrogacy (Altruistic — Regulation Act 2021) ⭐ 4.8
   CRITICAL LEGAL NOTICE — Surrogacy (Regulation) Act, 2021:
   - ONLY altruistic surrogacy is legal in India. Commercial surrogacy is BANNED.
   - ELIGIBLE: Indian married couples (F:23-50, M:26-55, no surviving child, medical indication) OR Indian widows/divorcees (35-45 yrs, per 2023 amendment)
   - NOT ELIGIBLE: Foreign nationals, NRIs, PIOs, OCIs, unmarried singles, same-sex couples, live-in partners
   - Surrogate must be: close relative, married, 25-35 yrs, has own child, max once in lifetime, max 3 attempts
   - 36-month insurance for surrogate mandatory. National Surrogacy Board approval required.
   - Types: Eligibility assessment, Board application, Registered clinic coordination, IVF + embryo transfer, Prenatal monitoring, Delivery + parentage docs
   - Packages: Legal consultation $500 | Medical coordination (IVF, prenatal, delivery) $8,000 | End-to-end legal+medical $12,000
   - Stay: Multiple visits over 12-15 months
   - ALWAYS state the legal restrictions when discussing surrogacy. If the user is not an Indian citizen, clearly inform them surrogacy is not available to them in India.

IMPORTANT: When mentioning hospitals and doctors, ALWAYS say "We recommend" — never present them as the only option.

YOUR CONSULTANTS (for booking):
- Sarah Mitchell — Senior Consultant (Hair Transplant, Cosmetic Surgery) — 4.9⭐, 342 reviews
- James Wong — Patient Coordinator (Dental, IVF, Fertility Law) — 4.8⭐, 278 reviews
- Dr. Priya Nair — Medical Advisor (IVF, Surrogacy Law, Cosmetic) — 4.9⭐, 456 reviews
- David Chen — Travel & Logistics (Hair, Dental) — 4.7⭐, 189 reviews

PARTNER HOSPITALS: Eugenix Hair Sciences (Delhi), Assure Clinic (Mumbai), SM Hair Transplant (Delhi/Gurgaon), Dr. Gowds' Dental (Hyderabad), Cosmodent India (Gurugram), The Dental House (Delhi), Bloom IVF (Mumbai, Delhi), Little Angel IVF (Noida), Aksigen IVF (Mumbai), Apollo (Delhi, Chennai), Fortis (Gurugram, Mumbai), Medanta (Gurugram), Max (Delhi)

TRAVEL LOGISTICS:
- India is well-connected: direct flights from Dubai (3.5h), Riyadh (4h), London (8.5h), New York (15h), Sydney (12h), Singapore (5.5h)
- Visa: e-Medical visa, apply online, approved in 72 hours, 60 days, triple entry
- All hospitals have English-speaking staff; Arabic interpreters available at major hospitals
- Comprehensive medical travel insurance recommended
- Airport pickup, hotel, transfers all included in packages

OUR PATIENTS COME FROM: Saudi Arabia, UAE, UK, USA, Australia, Kuwait, Oman, Nigeria, Kenya, Bangladesh, Iraq, Afghanistan, and 50+ other countries.

IMPORTANT BEHAVIOR RULES:
1. Be warm, empathetic, professional. Use a conversational tone.
2. Quote prices in USD ($) by default. If the patient mentions their country, you may also mention their local currency.
3. NEVER assume the patient is from a specific country. If you need to compare costs, compare India vs "typical home country" or ask where they are from.
4. When discussing costs, show savings percentage vs typical international prices.
5. Ask clarifying questions to understand the patient's needs before recommending.
6. After gathering enough information (treatment type, specific procedure, timeline preference), generate a TREATMENT PLAN.
7. When you generate a treatment plan, you MUST include a JSON block wrapped exactly like this:
   <<<PLAN_JSON>>>
   {
     "treatment":"...",
     "procedure":"Detailed procedure description",
     "estimatedCost":"$X,XXX",
     "homeCost":"$XX,XXX",
     "savings":"XX%",
     "savingsAmount":"$XX,XXX",
     "hospital":"Full hospital name (recommended)",
     "hospitalCity":"Delhi/Mumbai/Bangalore/etc",
     "hospitalAddress":"Full address of hospital",
     "hospitalAccreditation":"JCI / NABH accredited",
     "doctor":"Dr. Full Name (recommended)",
     "doctorCredentials":"Degree, Fellowship, XX years exp, specialty",
     "doctorExperience":"XX,XXX+ procedures performed",
     "stay":"X-X days in India",
     "recovery":"X-X days post-procedure",
     "consultant":"Name — Title",
     "consultantPhone":"+91 98XXX XXXXX",
     "consultantEmail":"name@medrouteindia.com",
     "travel":{
       "flightEstimate":"$XXX-$XXX round trip",
       "flightDuration":"Xh direct / Xh with 1 stop",
       "nearestAirport":"Indira Gandhi International (DEL) / Chhatrapati Shivaji (BOM) / etc",
       "airportDistance":"XX km from hospital, ~XX min by car",
       "bestAirlines":"Emirates, Qatar Airways, Singapore Airlines, IndiGo, Air India",
       "visa":"e-Medical Visa — apply online at indianvisaonline.gov.in",
       "visaCost":"$25 USD",
       "visaProcessing":"72 hours approval, 60-day validity, triple entry",
       "visaDocuments":"Passport, hospital invitation letter (we provide), photo, travel itinerary",
       "insurance":"Comprehensive medical travel insurance $50-150",
       "insuranceTip":"Get a policy covering medical evacuation & treatment complications"
     },
     "accommodation":[
       {"type":"Budget","name":"3-star hotel / guest house near hospital","cost":"$20-35/night","totalStay":"$XXX-$XXX","notes":"Clean rooms, AC, Wi-Fi, hot water, walking distance to hospital","examples":"Hotel Ibis, OYO Rooms, Treebo"},
       {"type":"Mid-Range","name":"4-star hotel / serviced apartment","cost":"$50-80/night","totalStay":"$XXX-$XXX","notes":"Swimming pool, restaurant, room service, laundry, gym, 10 min from hospital","examples":"Lemon Tree, Holiday Inn, Novotel"},
       {"type":"Premium","name":"5-star luxury hotel / hospital suite","cost":"$120-250/night","totalStay":"$XXX-$XXX","notes":"Luxury recovery, personal concierge, spa, gourmet dining, private transfers","examples":"Taj, Oberoi, ITC Hotels, Leela Palace"}
     ],
     "foodGuide":{
       "hospitalFood":"Most hospitals provide meals ($5-10/day) — Indian, Continental & Middle Eastern options",
       "streetFood":"$2-5/meal — Samosa, Dosa, Chaat, Biryani (safe at popular stalls)",
       "midRange":"$8-15/meal — Restaurants like Saravana Bhavan, Barbeque Nation, local favorites",
       "fineDining":"$20-40/meal — Hotel restaurants, international cuisine, rooftop dining",
       "dietaryNote":"Vegetarian food widely available. Halal options at most restaurants. Western food at all major hotels.",
       "waterTip":"Always drink bottled/filtered water. Brands: Bisleri, Kinley, Aquafina ($0.30/bottle)"
     },
     "dailyCosts":{
       "food":"$10-25/day (street food to restaurants)",
       "localTransport":"$5-15/day (Uber/Ola rides, very affordable)",
       "sim":"$3-5 for 30-day prepaid data SIM (Airtel/Jio, 2GB/day + calls)",
       "laundry":"$3-5/load (hotel laundry or local service)",
       "misc":"$5-10/day (tips, bottled water, snacks, toiletries)",
       "totalDaily":"$25-60/day depending on lifestyle"
     },
     "totalEstimate":{
       "budget":"$X,XXX - $X,XXX",
       "budgetBreakdown":"Treatment $X,XXX + Flights $XXX + Hotel $XXX + Food $XXX + Transport $XXX",
       "midRange":"$X,XXX - $X,XXX",
       "midRangeBreakdown":"Treatment $X,XXX + Flights $XXX + Hotel $XXX + Food $XXX + Transport $XXX",
       "premium":"$X,XXX - $X,XXX",
       "premiumBreakdown":"Treatment $X,XXX + Flights $XXX + Hotel $XXX + Food $XXX + Transport $XXX"
     },
     "cityGuide":{
       "city":"Delhi / Mumbai / Bangalore",
       "weather":"Current season weather & what to expect",
       "bestTime":"Oct-Mar (pleasant), avoid Jun-Sep (monsoon)",
       "language":"Hindi & English widely spoken. Hospital staff fluent in English.",
       "currency":"Indian Rupee (INR). 1 USD ≈ 83 INR. Cards accepted everywhere. ATMs widely available.",
       "timezone":"IST (UTC+5:30)",
       "electricity":"230V, Type C/D plugs — bring universal adapter",
       "safety":"India is generally safe for medical tourists. Hospitals are in well-developed areas.",
       "emergencyNumbers":"Ambulance: 102/108, Police: 100, MedRouteIndia 24/7: +91 99999 99999"
     },
     "packingChecklist":[
       "Valid passport (6+ months validity)",
       "e-Medical Visa printout",
       "Medical reports, scans & prescriptions",
       "Travel insurance documents",
       "Comfortable loose clothing for recovery",
       "Universal power adapter (Type C/D)",
       "Prescription medications in original packaging",
       "Copy of hospital invitation letter",
       "Sunscreen, hat & comfortable walking shoes",
       "Small cash in USD (for airport exchange)"
     ],
     "inclusions":["Airport pickup & drop in AC vehicle","Dedicated English-speaking care coordinator","All hospital, surgeon & anesthesia fees","Post-op medications & dressings","24/7 WhatsApp support during entire trip","12-month telemedicine follow-up with your surgeon","Hospital invitation letter for visa","Local SIM card on arrival","Translation services if needed"],
     "optionalExtras":[
       {"item":"Recovery holiday in Goa/Kerala","cost":"$500-1,500","desc":"Beach resort or Ayurvedic retreat for peaceful recovery"},
       {"item":"Ayurvedic wellness package","cost":"$200-500","desc":"Traditional therapies, yoga sessions, meditation"},
       {"item":"Companion sightseeing tours","cost":"$100-300","desc":"Taj Mahal, local markets, cultural tours for family"},
       {"item":"Extended stay serviced apartment","cost":"$400-800/month","desc":"Full kitchen, living room, ideal for long recovery"},
       {"item":"Physiotherapy / rehab sessions","cost":"$15-30/session","desc":"Professional post-op rehabilitation if needed"},
       {"item":"Dental/health checkup add-on","cost":"$50-200","desc":"Full body checkup or dental cleaning while in India"}
     ],
     "steps":[
       {"phase":"Week -4","task":"Free Video Consultation","detail":"Discuss your case with our medical team. Share reports & scans. Get personalised treatment plan & cost estimate."},
       {"phase":"Week -3","task":"Confirm & Book","detail":"Choose your hospital & doctor. Pay refundable booking deposit. Receive hospital invitation letter for visa."},
       {"phase":"Week -2","task":"Visa & Travel Prep","detail":"Apply for e-Medical Visa online ($25, 72hr approval). Book flights. Arrange travel insurance. Pack using our checklist."},
       {"phase":"Day 1","task":"Arrival in India","detail":"Airport pickup by our coordinator. Transfer to hotel. Receive local SIM card. Rest and acclimatize."},
       {"phase":"Day 2","task":"Hospital Visit & Pre-Op","detail":"Meet your surgeon face-to-face. Pre-operative tests & assessments. Final treatment plan confirmation."},
       {"phase":"Day 3","task":"Procedure Day","detail":"Treatment performed at the hospital. Our coordinator stays with you throughout. Family updated in real-time."},
       {"phase":"Day 4-X","task":"Recovery & Follow-Up","detail":"Post-op care at hospital/hotel. Daily check-ins with doctor. Medication management. Light sightseeing when cleared."},
       {"phase":"Departure","task":"Fly Home","detail":"Final check-up with surgeon. Discharge summary & medication pack. Airport transfer. 12-month follow-up plan starts."}
     ],
     "importantNotes":[
       "All prices are estimates in USD — final quote after video consultation with surgeon",
       "Hospital and doctor assignment confirmed after reviewing your medical reports",
       "e-Medical Visa allows triple entry — you can leave India and return if needed",
       "Companion visa available for one family member/caretaker at no additional cost",
       "Most hospitals accept international credit/debit cards, wire transfers & cash",
       "Post-treatment: 12 months of free telemedicine follow-up included",
       "If complications arise during stay, all corrective treatment is covered under package",
       "We provide 24/7 emergency contact throughout your stay in India"
     ]
   }
   <<<END_PLAN>>>
   This JSON will generate a comprehensive 6-8 page PDF travel & treatment guide. Calculate all costs realistically. For totalEstimate, add treatment + flights + accommodation (based on stay duration) + food + transport. Give specific examples, real hotel names, real airline names. Make the plan feel like a premium travel agency document.
8. After showing a plan, suggest: "You can download this as a comprehensive PDF travel & treatment plan, or book a free consultation with [consultant name] for a personalised assessment."
9. Keep responses concise but informative. Use markdown formatting (bold, lists, line breaks).
10. If asked about something outside medical tourism, politely redirect.
11. For surrogacy, ALWAYS clearly state: (a) Only altruistic surrogacy is legal in India under the Surrogacy (Regulation) Act, 2021. (b) Only Indian citizens are eligible — foreign nationals, NRIs, PIOs, OCIs cannot commission surrogacy. (c) If the user is not an Indian citizen, politely inform them surrogacy is not available to them in India and suggest they explore IVF or other fertility treatments instead. (d) Never quote commercial surrogacy prices. (e) Explain eligibility criteria (couple: F 23-50, M 26-55, married, no surviving child, medical indication; single: widow/divorcee 35-45). (f) Mention surrogate requirements (close relative, married, 25-35, own child, once in lifetime).`;

const aiChatLimiter = rateLimit({ windowMs: 60 * 1000, max: 20, message: { success: false, error: 'Too many requests. Please wait a moment.' } });

app.post('/api/ai-agent', aiChatLimiter, async (req, res) => {
  try {
    const { messages } = req.body;
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ success: false, error: 'Messages array required.' });
    }

    const claudeMessages = messages.map(m => ({
      role: m.role === 'assistant' ? 'assistant' : 'user',
      content: m.content,
    }));

    const response = await fetch(CLAUDE_BASE_URL + '/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: CLAUDE_MODEL,
        max_tokens: 2048,
        system: AI_SYSTEM_PROMPT,
        messages: claudeMessages,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error('Claude API error:', response.status, errText);
      return res.status(502).json({ success: false, error: 'AI service temporarily unavailable. Please try again.' });
    }

    const data = await response.json();
    const reply = data.content?.[0]?.text || 'I apologize, I could not generate a response. Please try again.';

    let planData = null;
    const planMatch = reply.match(/<<<PLAN_JSON>>>\s*([\s\S]*?)\s*<<<END_PLAN>>>/);
    if (planMatch) {
      try { planData = JSON.parse(planMatch[1].trim()); } catch (e) { console.error('Plan parse error:', e); }
    }

    const cleanReply = reply.replace(/<<<PLAN_JSON>>>[\s\S]*?<<<END_PLAN>>>/, '').trim();

    res.json({ success: true, reply: cleanReply, plan: planData });
  } catch (err) {
    console.error('AI Agent error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong with the AI service.' });
  }
});

app.post('/api/ai-agent/stream', aiChatLimiter, async (req, res) => {
  try {
    const { messages } = req.body;
    if (!messages || !Array.isArray(messages) || messages.length === 0) {
      return res.status(400).json({ success: false, error: 'Messages array required.' });
    }

    const claudeMessages = messages.map(m => ({
      role: m.role === 'assistant' ? 'assistant' : 'user',
      content: m.content,
    }));

    const response = await fetch(CLAUDE_BASE_URL + '/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': CLAUDE_API_KEY,
        'anthropic-version': '2023-06-01',
      },
      body: JSON.stringify({
        model: CLAUDE_MODEL,
        max_tokens: 2048,
        stream: true,
        system: AI_SYSTEM_PROMPT,
        messages: claudeMessages,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      console.error('Claude stream error:', response.status, errText);
      return res.status(502).json({ success: false, error: 'AI service temporarily unavailable.' });
    }

    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.setHeader('X-Accel-Buffering', 'no');

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let aborted = false;

    req.on('close', () => { aborted = true; reader.cancel(); });

    (async () => {
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done || aborted) break;
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop() || '';

          for (const line of lines) {
            if (!line.startsWith('data: ')) continue;
            const payload = line.slice(6).trim();
            if (payload === '[DONE]') { res.write('data: [DONE]\n\n'); continue; }
            try {
              const event = JSON.parse(payload);
              if (event.type === 'content_block_delta' && event.delta?.text) {
                res.write(`data: ${JSON.stringify({ text: event.delta.text })}\n\n`);
              } else if (event.type === 'message_stop') {
                res.write('data: [DONE]\n\n');
              }
            } catch {}
          }
        }
      } catch (err) {
        if (!aborted) console.error('Stream read error:', err);
      }
      if (!aborted) { res.write('data: [DONE]\n\n'); res.end(); }
    })();
  } catch (err) {
    console.error('AI Stream error:', err);
    res.status(500).json({ success: false, error: 'Something went wrong.' });
  }
});

// ==================== PAGES ====================

const pages = ['calculator', 'doctors', 'faq', 'compare-cost', 'plan-journey', 'chat', 'login', 'about', 'team', 'build-package', 'dashboard', 'meet-your-doctor'];
pages.forEach(p => app.get('/' + p, (req, res) => res.sendFile(path.join(__dirname, 'public', p + '.html'))));
app.get('*', (req, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));

function isValidEmail(e) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e); }

app.listen(PORT, () => {
  console.log(`\n  ✦ MedRouteIndia running at http://localhost:${PORT}`);
  console.log(`  ✦ Pages: / | /compare-cost | /plan-journey | /chat | /login | /doctors | /faq`);
  console.log(`  ✦ API: /api/auth | /api/treatments | /api/compare | /api/chat | /api/journey\n`);
});
