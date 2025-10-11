#!/bin/bash

# Script to set up MongoDB as a replica set for Prisma
# This creates a single-node replica set for development

echo "Setting up MongoDB replica set..."

# Stop any existing MongoDB instance
echo "Stopping existing MongoDB..."
sudo systemctl stop mongod

# Create data directory for replica set
echo "Creating data directory..."
sudo mkdir -p /var/lib/mongodb-rs
sudo chown mongodb:mongodb /var/lib/mongodb-rs

# Create configuration file for replica set
echo "Creating replica set configuration..."
sudo tee /etc/mongod-rs.conf > /dev/null <<EOF
storage:
  dbPath: /var/lib/mongodb-rs
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod-rs.log

net:
  port: 27017
  bindIp: 127.0.0.1

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

replication:
  replSetName: rs0

security:
  authorization: disabled
EOF

# Start MongoDB with replica set configuration
echo "Starting MongoDB with replica set configuration..."
sudo mongod --config /etc/mongod-rs.conf --fork

# Wait for MongoDB to start
sleep 5

# Initialize the replica set
echo "Initializing replica set..."
mongosh --eval "
rs.initiate({
  _id: 'rs0',
  members: [
    { _id: 0, host: 'localhost:27017' }
  ]
})
"

echo "Replica set setup complete!"
echo "You can now use: mongodb://localhost:27017/sustainable_shopping?replicaSet=rs0"

