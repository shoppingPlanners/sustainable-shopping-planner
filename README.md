# Sustainable Shopping Planner

Welcome to the **Sustainable Shopping Planner**!  
Make smarter, greener choices for your shopping trips and reduce your environmental impact.

---

## 🌱 What is Sustainable Shopping Planner?

Sustainable Shopping Planner is an open-source project designed to help users plan shopping trips with sustainability in mind. The app suggests eco-friendly products, tracks carbon footprints, and encourages conscious consumption.

---

## 🚀 Features

### Core Features
- **🎯 Intelligent Recommendations:** Advanced AI-powered recommendation algorithm with match scoring (up to 100% accuracy)
- **🌿 Rich Sustainability Data:** Comprehensive product information with 4+ sustainability certifications per item
- **⚡ Performance Optimized:** Server-side caching with 15-minute expiration for lightning-fast responses
- **📊 Beautiful Analytics Dashboard:** Track your eco-conscious shopping journey with real-time insights
- **🎨 Modern UI/UX:** Responsive design with loading states, error handling, and smooth animations
- **👤 User Profile Management:** Personalized user dropdown with preferences and settings
- **🏷️ Smart Categorization:** 8+ product categories including activewear, footwear, and accessories
- **⭐ Rating System:** User ratings and bestseller badges for quality assurance
- **🔍 Advanced Filtering:** Budget ranges, size selection, and sustainability priority matching

### Product Database
- **18 Premium Products** across multiple sustainable brands
- Materials: Organic Cotton, Recycled Polyester, Bamboo, Hemp, Tencel, Merino Wool, Cork, Vegan Leather
- Categories: T-Shirts, Dresses, Tops, Bottoms, Outerwear, Activewear, Footwear, Accessories
- Sustainability Features: Fair Trade, GOTS Certified, Carbon Neutral, Vegan, Upcycled, Zero Waste

### Enhanced User Experience
- **Skeleton Loading States:** Professional loading animations throughout the app
- **Empty State Handling:** Helpful guidance when no matches are found
- **Error Messages:** Clear, actionable error alerts
- **Sticky Navigation:** Always-accessible navigation with active route highlighting
- **Gradient Backgrounds:** Subtle, elegant visual design
- **Badge System:** Visual indicators for bestsellers and high sustainability scores

---

## 📸 Screenshots

<!-- Add screenshots/gif demos here -->
![Screenshot 1](docs/screenshot1.png)
![Screenshot 2](docs/screenshot2.png)
![Screenshot 3](docs/screenshot3.png)

---

## 🛠️ Technologies Used

### Frontend Stack
- **Framework:** Next.js 14.2.16 (React)
- **Styling:** Tailwind CSS with custom design system
- **UI Components:** Radix UI (shadcn/ui)
- **State Management:** React Hooks
- **Icons:** Lucide React
- **Type Safety:** TypeScript

### Backend Stack
- **Framework:** FastAPI (Python)
- **Database:** MongoDB
- **ORM:** Prisma
- **Authentication:** JWT with bcrypt
- **Caching:** In-memory cache with MD5 hashing
- **Real-time:** WebSocket support

### 4-Agent AI Architecture ✨
The system uses a **multi-agent architecture** where specialized agents collaborate:
- **Agent 1 - Brand Data Collector (Port 5001):** Scrapes product data, **automatically calls Agent 2** to score each product
- **Agent 2 - Rating Calculator (Port 5002):** Calculates sustainability scores (0-100) based on materials, certifications, price fairness
- **Agent 3 - User Behavior Tracker (Port 5003):** Tracks user preferences and behavior patterns
- **Agent 4 - Suggestion Agent (Port 5004):** Orchestrates all agents for personalized recommendations

**🔗 Agent Integration:** When scraping, Agent 1 → Agent 2 (automatic scoring) → Database

**📖 See [`agents/brand_data_collector/AGENT_INTEGRATION.md`](agents/brand_data_collector/AGENT_INTEGRATION.md) for integration details**

---

## 🎯 Getting Started

### Prerequisites

- **Node.js** (v16 or higher) & npm
- **Python** (v3.9 or higher)
- **MongoDB** running locally or remotely (default: `mongodb://localhost:27017`)
- **Git** for cloning the repository

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/shoppingPlanners/sustainable-shopping-planner.git
cd sustainable-shopping-planner-2
```

2. **Install Frontend Dependencies:**
```bash
cd frontend
npm install
```

3. **Setup Backend:**
```bash
cd ../backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
prisma generate
```

4. **Setup Python Agents:**
```bash
# User Behavior Tracker
cd ../agents/user_behavior_tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Rating Calculator
cd ../rating_calculator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Suggestion Agent
cd ../suggestion_agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. **Collect Real Product Data:**

**Option A: Scrape from Real Sustainable Brands** (Recommended)
```bash
cd agents/brand_data_collector
python run_collector.py
```
This will scrape real, buyable products from **35+ sustainable fashion brands** including:
- **Major Brands**: Patagonia, Reformation, Everlane, Outerknown
- **Footwear**: Allbirds, Nisolo, Rothy's, Vivobarefoot
- **Basics**: Pact, Kotn, Mate the Label, Organic Basics, Thought Clothing
- **Activewear**: Girlfriend Collective, Tentree, prAna
- **Luxury**: Eileen Fisher, Cuyana, People Tree
- **Accessories**: ABLE, Matt & Nat, Angela Roi
- **Fair Trade**: Tradeland, SERRV, Global Goods
- **Denim**: AGOLDE, Outland Denim
- **Vegan Fashion**: Wuxly, Veerah
- **Zero Waste**: Tonlé, Christy Martin Design
- And many more!

**Option B: Use Sample Data**
```bash
cd agents/brand_data_collector
mongoimport --db sustainable_shopping --collection brands --file brand_data.json --jsonArray --drop
```

⚠️ **Note**: Web scraping should respect each site's robots.txt and terms of service. The collector is configured for educational purposes.

6. **Configure Environment Variables:**
Create a `.env` file in the `backend` directory:
```env
DATABASE_URL="mongodb://localhost:27017/sustainable_shopping"
SECRET_KEY="your-secret-key-here"
```

### Running the Application

**Option 1: Run All Services (Recommended)**
```bash
# From project root
python run_all_script.py
```

This will start:
- Frontend: http://localhost:3002
- Backend API: http://localhost:8000
- User Behavior Tracker: http://localhost:5003
- Brand Data Collector: http://localhost:5001
- Rating Calculator: http://localhost:5002
- Suggestion Agent: http://localhost:5004

**Option 2: Run Services Individually**
```bash
# Terminal 1 - Frontend
cd frontend && npm run dev

# Terminal 2 - Backend
cd backend/src && source ../.venv/bin/activate && uvicorn main:app --reload

# Terminal 3 - User Behavior Tracker
cd agents/user_behavior_tracker && source .venv/bin/activate && python run.py

# Additional terminals for other agents...
```

### First Time Setup

1. Navigate to http://localhost:3002
2. Click **"Get Started"** to create an account
3. Fill in your preferences (category, budget, sustainability priorities)
4. Click **"Find My Matches"** to see personalized recommendations
5. Explore the **Analytics** page to see your sustainability dashboard

### Testing the 4-Agent System

Run the interactive demonstration script to see the agent integration in action:

```bash
python demo_agent_flow.py
```

This will demonstrate:
- ✅ Health checks for all 4 agents
- 🏪 Brand data collection (Agent 1)
- 📊 Sustainability rating calculation (Agent 2)
- 👤 User behavior tracking (Agent 3)
- 🎯 Personalized recommendations (Agent 4)
- 🔄 Complete backend integration flow

**📖 For technical details, see [AGENT_FLOW_DOCUMENTATION.md](AGENT_FLOW_DOCUMENTATION.md)**

---

## 🎨 Recent Improvements

### v2.0 - Major System Overhaul (Latest)

#### 📦 Enhanced Product Database
- ✅ Expanded to **18 premium sustainable products** (from 7)
- ✅ Added **2 sustainable brands**: GreenThreads & EcoWear Collective
- ✅ Rich product data: ratings (4.5-4.9★), descriptions, images, certifications
- ✅ 8 product categories with diverse materials
- ✅ Bestseller flags and popularity indicators

#### 🧠 Smarter Recommendation Engine
- ✅ Upgraded scoring algorithm with **8 weighted factors**
- ✅ Budget flexibility with gradual scoring (±$5-10 tolerance)
- ✅ Multi-keyword sustainability matching
- ✅ Rating bonuses for 4.8★+ products
- ✅ Bestseller priority boost
- ✅ Detailed match reasons (e.g., "Perfect dresses match, Great value at $65")

#### 🎨 Beautiful UI Enhancements
- ✅ **Item Cards**: Sustainability badges, bestseller tags, description previews
- ✅ **Navigation**: Sticky header, active route highlighting, user profile dropdown
- ✅ **Loading States**: Professional skeleton loaders throughout
- ✅ **Error Handling**: Helpful alerts with action buttons
- ✅ **Empty States**: Guided user experience with suggestions
- ✅ **Color Coding**: Green for sustainability, amber for ratings, visual hierarchy

#### 📊 Analytics Dashboard Upgrade
- ✅ Hero section with sustainability mission statement
- ✅ 3 key metrics cards with icons and context
- ✅ Eco-awareness score with graduated levels (Excellent/Good/Fair/Developing)
- ✅ Progress bars for sustainability tags
- ✅ Insights section with motivational content
- ✅ Rank badges and achievement system

#### ⚡ Performance Optimizations
- ✅ **Server-side caching**: 15-minute expiration with MD5 cache keys
- ✅ Reduced database queries with smart caching
- ✅ Cache hit/miss logging for monitoring
- ✅ Optimized recommendation computation

#### 🔧 Technical Improvements
- ✅ TypeScript interfaces updated with new fields
- ✅ Pydantic models aligned with frontend expectations
- ✅ CORS configuration for multiple ports
- ✅ Error boundaries and try-catch blocks
- ✅ Consistent code formatting

---

## 🤝 Contributing

Contributions are welcome!  
1. Fork the repo  
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)  
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)  
4. Push to the branch (`git push origin feature/AmazingFeature`)  
5. Open a Pull Request

Check out [CONTRIBUTING.md](CONTRIBUTING.md) for more details.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more information.

---

## 💬 Contact

Questions, ideas, or feedback?  
Open an issue or reach out via [Discussions](https://github.com/shoppingPlanners/sustainable-shopping-planner/discussions).

---

## 🌟 Support & Star

If you find this project useful, please give it a ⭐️!  
Your support helps us continue building awesome sustainable tools.
