# Items API Setup

This document explains how to set up and use the Items API that fetches data from MongoDB.

## Prerequisites

1. MongoDB running on localhost:27017
2. Python dependencies installed (`pip install -r requirements.txt`)
3. Environment variables configured

## Setup Steps

### 1. Start MongoDB
Make sure MongoDB is running on your system:
```bash
# On Ubuntu/Debian
sudo systemctl start mongod

# On macOS with Homebrew
brew services start mongodb-community

# Or run directly
mongod
```

### 2. Set Environment Variables
Create a `.env` file in the backend directory:
```bash
DATABASE_URL=mongodb://localhost:27017/sustainable-shopping-planner
```

### 3. Populate Database with Sample Data
Run the population script to add sample items:
```bash
cd backend
python populate_items.py
```

### 4. Start the Backend Server
```bash
cd backend
python -m uvicorn src.main:app --reload --port 8000
```

### 5. Start the Frontend
In a new terminal:
```bash
cd frontend
npm run dev
```

## API Endpoints

### Get All Items
```
GET http://localhost:8000/api/items
```

### Get Items by Category
```
GET http://localhost:8000/api/items?category=tops
```

### Get Specific Item
```
GET http://localhost:8000/api/items/{item_id}
```

## Testing

1. Visit `http://localhost:3002/suggestions` to see the items
2. Use the category filter to test filtering
3. Check the browser console for any errors

## Troubleshooting

- **Connection Error**: Make sure MongoDB is running and accessible
- **No Data**: Run the `populate_items.py` script to add sample data
- **CORS Issues**: The backend is configured to allow requests from `http://localhost:3002`
- **Port Conflicts**: Make sure ports 3002 (frontend) and 8000 (backend) are available
