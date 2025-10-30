# Sustainable Shopping Planner

Welcome to the **Sustainable Shopping Planner**—an AI-powered platform to help you make smarter, greener shopping choices. This system combines advanced recommendation logic, real-time analytics, and robust data collection to guide users toward more eco-friendly purchases.

---

## 🏗️ Architecture Overview

![System Architecture](docs/system_architecture.drawio.png)

- **Frontend (Next.js)**: Modern React UI for user interaction.
- **Backend (FastAPI + MongoDB)**: Central API for products, recommendations, and preferences.
- **All components are orchestrated via `run_all_script.py` for instant startup!**

---

## 🤖 4-Agent AI System

A core innovation of this project is its **multi-agent architecture**, where specialized agents independently handle domain intelligence and work together for powerful, AI-driven, eco-conscious recommendations.

### 1. Brand Data Collector (Port 5001)
- **Purpose:** Scrapes product/brand data from 35+ sustainable labels (e.g., Patagonia, Reformation, Allbirds).
- **Features:**
  - Configurable for new brands (domain-specific selectors in `config.py`)
  - Eco keyword detection in materials & descriptions
  - Direct database integration (MongoDB)
  - Exports to JSON for backup
- **Endpoints:**
  - `GET /` – Health check
  - `GET /brands` – List all scraped brand data
  - `Run via:` `agents/brand_data_collector/app.py` (Flask)
- **Extensible:** Add/modify brands by editing `websites.txt` and selectors in `config.py`.

### 2. Rating Calculator (Port 5002)
- **Purpose:** Assigns granular sustainability scores to each product, factoring in materials, certifications, price fairness, and more. Supports eco-label parsing via NLP.
- **Features:**
  - Machine learning/NLP rating engine (`rating_engine.py`)
  - Multi-factor scoring (certifications, material, energy, price, etc.)
  - API-based, integrates with collector and suggestion agent
  - **Endpoints:** `/` (health), `/rate` (calculate scores)
  - `Run via:` `agents/rating_calculator/app.py` (FastAPI)

### 3. User Behavior Tracker (Port 5003)
- **Purpose:** Tracks, analyzes, and summarizes user interactions for hyper-personalized experiences and advanced analytics.
- **Features:**
  - Real-time tracking: page views, searches, add-to-cart, purchases, preferences
  - Segmenting via clustering & AI (can use OpenAI for semantic analysis)
  - Insightful dashboards: engagement, sustainability focus, price sensitivity
  - Consent management and GDPR compliance
- **APIs:**
  - `POST /track` (track events)
  - `GET /behavior/insights/{user_id}` (personalized insights)
  - `GET /analytics/platform` (global metrics)
  - `Run via:` `agents/user_behavior_tracker/run.py`

### 4. Suggestion Agent (Port 5004)
- **Purpose:** Orchestrates the overall recommendation—merges behavior analytics, item database, sustainability scoring and delivers top personalized matches (with explanations).
- **Features:**
  - Composes inputs from all agents
  - Leverages LLMs for natural-language explanations (optional OpenAI integration)
  - Real-time endpoint for tailored recommendations
  - **Endpoints:** `POST /recommend` (input: user ID/preferences → output: best product matches w/ match reasons)
  - `Run via:` `agents/suggestion_agent/agent4_suggestion.py`

---
## 🌟 Features

**For Users:**
- 🌱 _AI-powered personalized recommendations_
- 📊 _Beautiful analytics dashboard to track your impact_
- 🛒 _Eco-product catalog with detailed certifications & sustainability metrics_
- 🎯 _Smart forms for budget, preferred materials, and categories_
- ⭐️ _Bestseller and rating badges_
- 🧩 _Advanced filtering: size, price, sustainability focus, etc._

**For Developers/Researchers:**
- 🔄 _Modular 4-agent architecture_
- 🔎 _Real-time tracking & AI-based user analysis_
- 🛠️ _Rich product database scraped from real sustainable brands_
- ⚙️ _Easy extension, custom brand/site scraping_

---

## 🖥️ Technology Stack

- **Frontend:** Next.js (React), Tailwind CSS, Radix UI (shadcn/ui), TypeScript
- **Backend:** FastAPI (Python), MongoDB, Prisma ORM, JWT Auth
- **AI/Agents:** Python (Flask/FastAPI), OpenAI (optional), multi-process via Python
- **DevOps:** Start ALL services in one command with `run_all_script.py`

---

## 🚀 Quick Start

> **No more juggling multiple terminal tabs! Launch the entire stack at once:**

```bash
python run_all_script.py
```

This launches:
- Frontend on http://localhost:3002
- Backend API on http://localhost:8000
- Brand Data Collector Agent on http://localhost:5001
- Rating Calculator Agent on http://localhost:5002
- User Behavior Tracker on http://localhost:5003
- Suggestion Agent on http://localhost:5004

> _See the output for live status and logs. Press **Ctrl+C** in the terminal to stop all services gracefully._

### 1. Prerequisites
- **Node.js v16+**, **npm**
- **Python 3.9+**
- **MongoDB** (default: `mongodb://localhost:27017`)
- (Optional) **OpenAI API Key** for advanced analytics

### 2. Environment Variables
Set up the backend `.env`:
```env
DATABASE_URL="mongodb://localhost:27017/sustainable_shopping"
SECRET_KEY="your-secret-key-here"
```
_See also `/agents/user_behavior_tracker/env.example` if needed._

### 3. (Optional) Data Collection
To scrape new products:
```bash
cd agents/brand_data_collector
python run_collector.py
```
Or import with sample data:
```bash
mongoimport --db sustainable_shopping --collection brands --file brand_data.json --jsonArray --drop
```

---

## 🧩 Subsystems in Detail

### Frontend (`frontend/`)
- Powered by Next.js + Tailwind
- Modern UI, responsive, beautiful dashboards, advanced filtering (category, price, rating, sustainability)
- State managed via React hooks, profile, registration, live analytics

### Backend (`backend/`)
- FastAPI w/ JWT authentication
- Serves Product, Preferences & Recommendation APIs
- MongoDB and Prisma ORM for fast queries
- Endpoints:
  - `/api/items` Get/filter all items
  - `/api/preferences/save` Save user shopping preferences
  - `/api/preferences/recommendations` Personalized recommendations
  - `/api/preferences/recent` Fetch last saved preferences

### Agents (`agents/`)
- **Brand Data Collector**: Scrapes >35 brands, exports to DB/JSON
- **Rating Calculator**: Assigns eco-scores using machine learning/NLP
- **User Behavior Tracker**: Real-time user event capture & AI analytics
- **Suggestion Agent**: Fuses all inputs for best-match suggestions
- _All are started from `run_all_script.py`_

---

## 📸 Screenshots
- ![Screenshot 1](docs/screenshot1.png)
- ![Screenshot 2](docs/screenshot2.png)
- ![Screenshot 3](docs/screenshot3.png)

---

## 🤝 Contributing
We welcome contributions!
1. Fork & clone this repo
2. Create a feature branch (`git checkout -b feature/YourFeatureName`)
3. Make commits/changes
4. Push and open a Pull Request

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines.

---
## 👥 Authors

| Name  | GitHub |
|------|--------|
| **KUMARI M. A. D. N.** | [nadee2k](https://github.com/nadee2k) |
| **KAPUWELLA K. G. N. D.** |  [NipunDemintha](https://github.com/NipunDemintha) |
| **VITHANA Y. S. D.** | [diw-666](https://github.com/diw-666) |
| **AYYASH M. R. Y.** |  [yahiyaiyash](https://github.com/yahiyaiyash) |


---

## 💬 Contact & Support
Questions or feedback?
- Open an issue on GitHub
- Start a discussion at [Discussions](https://github.com/shoppingPlanners/sustainable-shopping-planner/discussions)

**If you find this project useful, give it a ⭐️! Your support helps build a more sustainable future.**
