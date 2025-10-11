#!/bin/bash

echo "🔧 Setting up MongoDB Replica Set for Prisma..."

echo "📋 Step 1: Stopping MongoDB service..."
sudo systemctl stop mongod

echo "📋 Step 2: Starting MongoDB with replica set configuration..."
sudo mongod --replSet rs0 --bind_ip 127.0.0.1 --port 27017 --dbpath /var/lib/mongodb --auth --fork --logpath /var/log/mongodb/mongod.log

echo "⏳ Waiting for MongoDB to start..."
sleep 5

echo "📋 Step 3: Initializing replica set..."
mongosh --eval "
rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'localhost:27017' }
  ]
})
"

echo "📋 Step 4: Creating admin user..."
mongosh --eval "
use admin
db.createUser({
  user: 'admin',
  pwd: 'Maduu219.',
  roles: ['root']
})
"

echo "✅ MongoDB Replica Set setup complete!"
echo "🔗 Connection string: mongodb://admin:Maduu219.@localhost:27017/sustainable_shopping?replicaSet=rs0"
echo ""
echo "🧪 Now let's test the connection..."

