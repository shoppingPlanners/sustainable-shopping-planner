# 🚀 Quick Start Guide

Get the Sustainable Shopping Planner integrated system up and running in minutes!

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- (Optional) Docker and Docker Compose

## Option 1: Local Development (Recommended for Development)

### Step 1: Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration (optional for basic usage)
# For basic testing, the default values will work
nano .env  # or use your favorite editor
```

### Step 3: Run All Agents

```bash
# Run all 4 agents at once
python run_all.py
```

That's it! All 4 agents are now running:
- **Brand Data Collector**: http://localhost:5001
- **Rating Calculator**: http://localhost:5002
- **User Behavior Tracker**: http://localhost:5003
- **Suggestion Agent**: http://localhost:5004

### Step 4: Test the System

Open a new terminal and try these commands:

```bash
# Check health of all agents
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health

# Scrape a brand (example)
curl -X POST http://localhost:5001/scrape \
  -H 'Content-Type: application/json' \
  -d '{"url": "http://automationpractice.pl/index.php?id_category=3&controller=category", "brand_name": "AutoPractice"}'

# Get all brands
curl http://localhost:5001/brands

# Calculate a rating
curl -X POST http://localhost:5002/calculate \
  -H 'Content-Type: application/json' \
  -d '{
    "brand_name": "AutoPractice",
    "products": [],
    "sustainability_commitments": ["We use organic materials", "Carbon neutral by 2030"],
    "certifications": ["Fair Trade", "B-Corp"]
  }'

# Track a user event
curl -X POST http://localhost:5003/track \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "user123",
    "event_type": "view",
    "product_id": "prod1",
    "category": "clothing",
    "tags": ["organic", "sustainable"]
  }'

# Get user behavior patterns
curl http://localhost:5003/behavior/patterns/user123

# Get personalized suggestions
curl http://localhost:5004/suggestions/user123

# Get trending products
curl http://localhost:5004/trending
```

## Option 2: Docker (Recommended for Production)

### Step 1: Configure Environment

```bash
cp .env.example .env
# Edit .env with your production values
```

### Step 2: Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

### Step 3: Check Status

```bash
# View logs
docker-compose logs -f

# Check running containers
docker ps

# Stop all services
docker-compose down
```

## Testing the Integrated System

### Full Workflow Example

```bash
# 1. Scrape a sustainable brand
curl -X POST http://localhost:5001/scrape \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "http://automationpractice.pl/index.php?id_category=3&controller=category",
    "brand_name": "EcoFashion"
  }'

# 2. The brand data is automatically sent to Rating Calculator
# Check the ratings
curl http://localhost:5002/ratings

# 3. Simulate user behavior
curl -X POST http://localhost:5003/track \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "alice",
    "event_type": "search",
    "category": "clothing",
    "tags": ["organic", "fair-trade"]
  }'

curl -X POST http://localhost:5003/track \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "alice",
    "event_type": "view",
    "product_id": "prod1",
    "category": "clothing",
    "tags": ["organic"]
  }'

# 4. Get personalized suggestions for Alice
curl http://localhost:5004/suggestions/alice?limit=5

# 5. Submit feedback on a suggestion
curl -X POST http://localhost:5004/feedback \
  -H 'Content-Type: application/json' \
  -d '{
    "user_id": "alice",
    "product_id": "prod1",
    "feedback_type": "clicked"
  }'
```

## Web Interface (Optional)

If you want to use the web interface:

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:3000 in your browser.

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

```bash
# Find what's using the port (example for port 5001)
lsof -i :5001

# Kill the process
kill -9 <PID>
```

Or change the ports in `.env`:

```bash
BRAND_COLLECTOR_PORT=5011
RATING_CALCULATOR_PORT=5012
USER_BEHAVIOR_PORT=5013
SUGGESTION_AGENT_PORT=5014
```

### Dependencies Not Installing

```bash
# Upgrade pip
pip install --upgrade pip

# Install with verbose output
pip install -v -r requirements.txt
```

### Agents Not Communicating

Make sure all agents are running and check the URLs in `.env`:

```bash
# Check if agents are accessible
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health
```

## Next Steps

1. **Explore the API Documentation**: Visit http://localhost:5001/docs for each agent's interactive API docs
2. **Read the Full Documentation**: Check out `README.md` for detailed information
3. **Customize Configuration**: Edit `.env` to configure agents for your needs
4. **Add Your Own Data**: Start scraping real sustainable brands
5. **Integrate with Frontend**: Connect the Next.js frontend to the agents

## Support

Need help? Check:
- `README.md` - Full documentation
- `docs/API.md` - API reference
- GitHub Issues - Report bugs or ask questions

Happy sustainable shopping! 🌱

