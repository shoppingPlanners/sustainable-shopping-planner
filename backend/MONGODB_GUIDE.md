# 🍃 MongoDB Setup Guide for Sustainable Shopping Planner

This guide covers MongoDB setup, configuration, and usage for the Sustainable Shopping Planner backend.

## 📋 Overview

The system uses MongoDB as the primary database with the following collections:
- **products** - Product catalog with sustainability features
- **reviews** - Customer reviews and ratings
- **ai_ratings** - AI-calculated ratings and analysis
- **users** - User accounts and authentication

## 🚀 Quick Setup

### 1. Install MongoDB

#### Ubuntu/Debian
```bash
# Import MongoDB public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Add MongoDB repository
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org
```

#### macOS
```bash
# Install using Homebrew
brew tap mongodb/brew
brew install mongodb-community
```

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run the installer and follow the setup wizard
3. Add MongoDB to your PATH

#### Docker (Recommended)
```bash
# Run MongoDB in Docker container
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -v mongodb_data:/data/db \
  mongo:latest

# Or with authentication
docker run -d \
  --name mongodb \
  -p 27017:27017 \
  -e MONGO_INITDB_ROOT_USERNAME=admin \
  -e MONGO_INITDB_ROOT_PASSWORD=password \
  -v mongodb_data:/data/db \
  mongo:latest
```

### 2. Start MongoDB

#### Service (Linux/macOS)
```bash
# Start MongoDB service
sudo systemctl start mongod

# Enable auto-start
sudo systemctl enable mongod

# Check status
sudo systemctl status mongod
```

#### Manual Start
```bash
# Create data directory
sudo mkdir -p /data/db
sudo chown -R $USER /data/db

# Start MongoDB
mongod --dbpath /data/db
```

### 3. Setup Database

```bash
cd backend
python mongodb_setup.py
```

This script will:
- Create the `sustainable_shopping` database
- Create collections with validation schemas
- Set up indexes for optimal performance
- Configure data validation rules

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sustainable_shopping

# For MongoDB with authentication
MONGODB_URL=mongodb://username:password@localhost:27017

# For MongoDB Atlas (cloud)
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/sustainable_shopping
```

### Connection Options

```python
# Local MongoDB
MONGODB_URL = "mongodb://localhost:27017"

# MongoDB with authentication
MONGODB_URL = "mongodb://username:password@localhost:27017"

# MongoDB Atlas (cloud)
MONGODB_URL = "mongodb+srv://username:password@cluster.mongodb.net"

# MongoDB with SSL
MONGODB_URL = "mongodb://username:password@localhost:27017/?ssl=true"
```

## 📊 Database Schema

### Products Collection
```javascript
{
  _id: ObjectId,
  name: String,
  brand: String,
  category: String,
  price: Number,
  description: String,
  sustainability_features: [String],
  image: String,
  created_at: Date,
  updated_at: Date
}
```

### Reviews Collection
```javascript
{
  _id: ObjectId,
  product_id: String,
  user_id: String,
  rating: Number (1-5),
  text: String,
  date: Date,
  created_at: Date
}
```

### AI Ratings Collection
```javascript
{
  _id: ObjectId,
  product_id: String,
  ai_rating: Number (1.0-5.0),
  sentiment_score: Number (-1.0 to 1.0),
  sustainability_score: Number (0.0-1.0),
  confidence: Number (0.0-1.0),
  breakdown: Object,
  timestamp: Date,
  created_at: Date,
  updated_at: Date
}
```

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String (unique),
  username: String (unique),
  hashed_password: String,
  is_active: Boolean,
  created_at: Date,
  updated_at: Date
}
```

## 🔍 Indexes

The system creates the following indexes for optimal performance:

### Products
- `name` (text search)
- `brand` (lookup)
- `category` (filtering)
- `price` (sorting)

### Reviews
- `product_id` (product reviews)
- `user_id` (user reviews)
- `rating` (rating analysis)
- `date` (chronological)
- `product_id + rating` (compound)

### AI Ratings
- `product_id` (product ratings)
- `ai_rating` (rating sorting)
- `timestamp` (chronological)

### Users
- `email` (unique, authentication)
- `username` (unique, authentication)

## 🛠️ Database Operations

### Using MongoDB Shell

```bash
# Connect to MongoDB
mongo

# Switch to database
use sustainable_shopping

# View collections
show collections

# View documents
db.products.find()
db.reviews.find()
db.ai_ratings.find()

# Count documents
db.products.countDocuments()
db.reviews.countDocuments()

# Query examples
db.products.find({category: "clothing"})
db.reviews.find({rating: {$gte: 4}})
db.ai_ratings.find({ai_rating: {$gte: 4.0}})
```

### Using Python (Motor)

```python
from motor.motor_asyncio import AsyncIOMotorClient

# Connect to MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.sustainable_shopping

# Query products
products = await db.products.find({"category": "clothing"}).to_list(10)

# Insert document
await db.products.insert_one({
    "name": "Eco T-Shirt",
    "brand": "GreenWear",
    "category": "clothing",
    "price": 29.99
})

# Update document
await db.products.update_one(
    {"_id": product_id},
    {"$set": {"price": 24.99}}
)
```

## 🔒 Security

### Authentication

```bash
# Enable authentication
mongod --auth

# Create admin user
mongo
use admin
db.createUser({
  user: "admin",
  pwd: "password",
  roles: ["userAdminAnyDatabase", "dbAdminAnyDatabase", "readWriteAnyDatabase"]
})

# Create application user
use sustainable_shopping
db.createUser({
  user: "app_user",
  pwd: "app_password",
  roles: ["readWrite"]
})
```

### Network Security

```bash
# Bind to specific IP
mongod --bind_ip 127.0.0.1

# Enable SSL
mongod --sslMode requireSSL --sslPEMKeyFile /path/to/cert.pem
```

### Data Validation

The system includes JSON Schema validation:

```javascript
// Products validation
{
  $jsonSchema: {
    bsonType: "object",
    required: ["name", "brand", "category", "price", "description"],
    properties: {
      name: {bsonType: "string"},
      price: {bsonType: "double", minimum: 0},
      rating: {bsonType: "int", minimum: 1, maximum: 5}
    }
  }
}
```

## 📈 Performance Optimization

### Indexing Strategy

```javascript
// Create compound indexes
db.reviews.createIndex({product_id: 1, rating: 1})
db.reviews.createIndex({user_id: 1, date: -1})

// Create text indexes for search
db.products.createIndex({name: "text", description: "text"})

// Create partial indexes
db.reviews.createIndex({rating: 1}, {partialFilterExpression: {rating: {$gte: 4}}})
```

### Query Optimization

```javascript
// Use projection to limit fields
db.products.find({}, {name: 1, price: 1, _id: 0})

// Use limit and skip for pagination
db.products.find().skip(20).limit(10)

// Use aggregation for complex queries
db.reviews.aggregate([
  {$match: {product_id: "123"}},
  {$group: {_id: "$rating", count: {$sum: 1}}},
  {$sort: {_id: 1}}
])
```

## 🧪 Testing

### Connection Test

```bash
# Test MongoDB connection
mongo --eval "db.adminCommand('ping')"
```

### Data Validation Test

```python
# Test data insertion
from database import Product

product = Product(
    name="Test Product",
    brand="Test Brand",
    category="clothing",
    price=29.99,
    description="Test description"
)

await product.insert()
```

### Performance Test

```python
# Test query performance
import time

start_time = time.time()
products = await Product.find_all().to_list()
end_time = time.time()

print(f"Query took {end_time - start_time:.2f} seconds")
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Connection Refused
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Check port
netstat -tulpn | grep 27017
```

#### 2. Authentication Failed
```bash
# Check user credentials
mongo -u username -p password --authenticationDatabase admin
```

#### 3. Database Not Found
```bash
# List databases
mongo --eval "db.adminCommand('listDatabases')"

# Create database
mongo
use sustainable_shopping
db.createCollection("products")
```

#### 4. Index Creation Failed
```bash
# Check existing indexes
db.products.getIndexes()

# Drop and recreate
db.products.dropIndex("index_name")
```

### Monitoring

```bash
# Check MongoDB status
mongo --eval "db.serverStatus()"

# Check database stats
mongo --eval "db.stats()"

# Check collection stats
mongo --eval "db.products.stats()"
```

## 🚀 Production Deployment

### MongoDB Atlas (Cloud)

1. Create account at [mongodb.com/atlas](https://www.mongodb.com/atlas)
2. Create cluster
3. Get connection string
4. Update environment variables

### Self-Hosted

```bash
# Production configuration
mongod --config /etc/mongod.conf

# With replica set
mongod --replSet rs0 --port 27017
```

### Docker Compose

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:latest
    container_name: mongodb
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
```

## 📚 Additional Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Motor Documentation](https://motor.readthedocs.io/)
- [Beanie Documentation](https://beanie-odm.dev/)
- [MongoDB Atlas](https://www.mongodb.com/atlas)

---

**Happy Sustainable Shopping with MongoDB! 🍃**
