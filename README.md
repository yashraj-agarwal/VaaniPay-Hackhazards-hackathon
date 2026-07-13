<img width="4320" height="1440" alt="hh26 main poster 2 with sponsors 3x1 (4320 x 1440 px) (2)" src="https://github.com/user-attachments/assets/c698b2cd-da84-4cb0-9276-125c6a7244aa" />

# 🚀 VaaniPay

> Voice-First IVR Financial Inclusion Platform for feature phones — Bridging the digital divide for 350M+ Indians.

---

## 📌 Problem & Domain

While India's digital payment ecosystem (UPI) processes over 10 billion transactions monthly, a stark digital divide remains. Over **350 million Indians**—predominantly in rural areas, comprising gig workers, farmers, and the elderly—lack smartphones, internet access, or the digital literacy required to use app-based banking. Existing USSD solutions (*99#) are text-heavy, suffer from high session drop rates, and are inaccessible to the visually impaired or illiterate. VaaniPay bridges this gap by bringing state-of-the-art AI financial services to the one piece of infrastructure they already have and know how to use: the basic telephone.

**Themes Selected (at least one):**
- [ ] Human Experience & Productivity  
- [ ] Climate & Sustainability Systems  
- [ ] HealthTech & Bio Platforms  
- [x] Learning & Knowledge Systems  
- [x] Work, Finance & Digital Economy  
- [ ] Infrastructure, Mobility & Smart Systems  
- [x] Trust, Identity & Security  
- [ ] Media, Social & Interactive Platforms  
- [x] Public Systems, Governance and Civic Tech  
- [ ] Developer Tools & Software Infrastructure  

---

## 🎯 Objective

VaaniPay completely removes the hardware, internet, and literacy barriers from modern banking. By dialing a single toll-free number, users can speak naturally in their native language to access payments, credit, insurance, and savings entirely through an AI-powered voice interface. 

- **Target Users:** Daily wage earners, small-holder farmers, rural communities, visually impaired individuals, and the 65% of rural India still relying on feature phones.
- **Pain Point:** Total exclusion from digital finance, inability to build a formal credit history, and friction in using text-based USSD menus.
- **The Value:** Frictionless, native-language financial access with sub-2-second latency. We convert voice to intent and process transactions securely, enabling "New to Credit" (NTC) users to build a formal financial footprint simply by making phone calls.

---

## 🧠 Team & Approach

### Team Name:  
`Legion`

### Team Members:  
- Yash Raj Agarwal 

### Your Approach:
- **Why we chose this problem:** Financial inclusion shouldn't demand a hardware upgrade. We believe technology should meet users where they already are.
- **Key challenges addressed:** Processing highly compressed, lossy 8KHz PSTN telephony audio. We engineered a robust pipeline that translates poor-quality audio across 9 distinct Indian languages into actionable financial intents with 94%+ accuracy. We also tackled the challenge of maintaining secure, stateful multi-turn IVR sessions without a visual UI.
- **Pivots & Breakthroughs:** Initially, generic STT models failed on telephony audio. We pivoted to Sarvam AI's specialized Indic models, drastically improving our Word Error Rate (WER). Furthermore, to ensure the AI Financial Mentor didn't trigger Twilio's 15-second timeout, we integrated Groq's LPU inference, achieving blazing fast ~800ms response times for the LLM.

---

## 🛠️ Tech Stack

### Core Technologies Used:
- **Frontend:** React Native (Expo) Web Dashboard — *Renders real-time transaction updates via polling for merchant and family visibility.*
- **Backend:** Python (Flask) — *Handles high-concurrency webhook parallelization for Twilio IVR routing.*
- **Database:** Neo4j AuraDB (Graph Database) & JSON Fallback — *Models users and transactions as nodes/edges to calculate trust-based credit scores.*
- **APIs:** Twilio (IVR/Telephony), Sarvam AI (Indic STT/TTS pipeline), Groq (LLaMA 3 inference for Financial Mentor).
- **Hosting:** Render (API & Worker environments).

### Additional Technologies Used (Optional):
- [x] AI / ML  
- [ ] Web3 / Blockchain  
- [ ] Cyber Security 
- [ ] Cloud  

---

## 🏆 Sponsored Track (Optional)

Select if your project participates in any track:

- [x] **Expo Track** – Built using Expo  
- [x] **Neo4j Track** – Uses AuraDB as primary database  
- [ ] **Base44 Track** – Prototype/Final Product built using Base44  

> _We utilized **Neo4j AuraDB** to transcend traditional relational data limits. By storing users as nodes and transactions as edges, our behavioral credit scoring engine can traverse 2nd and 3rd-degree network connections. It analyzes transaction frequency and node centrality to instantly generate a trust-based credit score for unbanked users. The **Expo** companion app serves as a real-time web dashboard for merchants or literate family members to instantly verify transactions initiated over the PSTN network._

---

## ✨ Key Features

- ✅ **Voice-Driven UPI Payments:** Send money securely by just speaking over a basic phone call. Bypasses the need for internet or UPI apps.
- ✅ **Graph-Based Behavioral Credit Scoring:** Analyzes transaction history using Neo4j to generate a 300-900 score for unbanked users, enabling access to micro-loans.
- ✅ **Hyper-Localized Support (9 Languages):** Full localized STT & TTS pipeline via Sarvam AI, natively supporting Hindi, Tamil, Telugu, Kannada, Malayalam, Marathi, Bengali, Gujarati, and English—covering ~90% of India's population.
- ✅ **AI Financial Mentor (Sub-2s Latency):** Ask complex financial questions (e.g., "How do I save for a tractor?") in your native language and get contextual LLM-generated advice spoken back to you instantly, powered by Groq.
- ✅ **Real-Time Web Dashboard:** A premium Expo-built companion app that updates instantly when a phone transaction occurs, bringing visibility to offline payments.
- ✅ **Robust Telephony Security:** Includes 3-attempt mPIN lockouts and strict session state management to prevent brute-force attacks on financial data.

---

## 📽️ Demo & Deliverables

- **Demo Video Link (Mandatory):** https://youtu.be/4mincKwHNKM  
- **Deployment Link (Recommended):** [Insert Link Here] 
- **Pitch Deck / PPT (Optional):** https://pdflink.to/vaanipay/  

---

## ✅ Tasks & Bonus Checklist

- [x] All team members completed the mandatory social task  
- [x] Bonus Task 1 – Badge sharing  
- [x] Bonus Task 2 – Blog/article  

---

## 🧪 How to Run the Project

### Requirements:
- Python 3.11+
- Node.js 18+ (for Expo frontend)
- API Keys: Twilio, Sarvam AI, Groq, Neo4j

### Local Setup:
```bash
# 1. Clone & Install Backend
git clone https://github.com/yashraj-agarwal/VaaniPay-Hackhazards-hackathon
cd VaaniPay-Hackhazards-hackathon
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# 2. Setup Environment Variables
copy .env.example .env
# Edit .env with your keys and your active ngrok URL

# 3. Generate Audio Prompts (~260 localized IVR files)
python download_audios.py

# 4. Start Flask Server
python app.py

# 5. Start Expo Dashboard (in a new terminal)
cd expo-app
npm install
npm start
```

---

## 🧬 Future Scope

- 📈 **NPCI *99# USSD Bridge:** Direct infrastructure integration with NPCI to execute real banking ledger movements without intermediary wallets.
- 🛡️ **Voice Biometrics (V-CIP):** Implementing continuous voice authentication to replace DTMF mPINs entirely, making the system 100% hands-free.
- 🌐 **Pan-India Coverage:** Expanding the Sarvam AI pipeline to support all 22 scheduled Indian languages and over 100 dialects.
- 🏦 **NBFC API Integration:** Connecting our graph-based credit scoring directly to Non-Banking Financial Companies for instant loan disbursements.

---

## 📎 Resources / Credits

- **Sarvam AI:** For incredibly fast and accurate Indic speech models that made interacting over 8KHz audio possible.
- **Twilio:** For the robust telephony and IVR webhook infrastructure.
- **Neo4j:** For the graph database powering our NTC credit scoring algorithms.
- **Groq:** For lightning-fast LLaMA 3 inference, keeping our AI Mentor responses strictly under the IVR timeout thresholds.

---

## 🏁 Final Words

Building VaaniPay was an incredibly rewarding journey. It challenged us to think outside the paradigm of sleek mobile UI/UX and instead focus on raw accessibility and infrastructure. Integrating cutting-edge AI with legacy PSTN telephony showed us that the most impactful technology often doesn't need a screen. Huge shout-out to the HackHazards '26 team for an amazing, inspiring event!
