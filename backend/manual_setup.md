# MongoDB Replica Set Setup Guide

## Option 1: MongoDB Atlas (Recommended - Easiest)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a new cluster (free tier available)
4. Get your connection string
5. Update your `.env` file:
   ```
   DATABASE_URL="mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/sustainable_shopping?retryWrites=true&w=majority"
   ```

## Option 2: Local MongoDB Replica Set

### Step 1: Stop MongoDB
```bash
sudo systemctl stop mongod
```

### Step 2: Start MongoDB with replica set configuration
```bash
sudo mongod --replSet rs0 --bind_ip 127.0.0.1 --port 27017 --dbpath /var/lib/mongodb --fork --logpath /var/log/mongodb/mongod.log
```

### Step 3: Initialize the replica set
```bash
mongosh
```
Then in the MongoDB shell:
```javascript
rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'localhost:27017' }
  ]
})
```

### Step 4: Update your .env file
```bash
DATABASE_URL="mongodb://localhost:27017/sustainable_shopping?replicaSet=rs0"
```

### Step 5: Test the connection
```bash
cd backend && python -c "
import asyncio
from src.database import db

async def test():
    await db.connect()
    users = await db.user.find_many()
    print(f'Found {len(users)} users')
    await db.disconnect()

asyncio.run(test())
"
```

## Option 3: Use Docker (Alternative)

Create a `docker-compose.yml`:
```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    container_name: mongodb-rs
    restart: always
    ports:
      - "27017:27017"
    command: mongod --replSet rs0 --bind_ip_all
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

Run with:
```bash
docker-compose up -d
```

Then initialize replica set:
```bash
docker exec -it mongodb-rs mongosh --eval "rs.initiate()"
```

