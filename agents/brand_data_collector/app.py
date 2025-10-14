# Flask app for brand data collector
from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv
from pymongo import MongoClient

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# Load root .env so DATABASE_URL is available even when cwd is this agent dir
load_dotenv(os.path.join(ROOT_DIR, ".env"))
load_dotenv()  # also load local .env if present

app = Flask(__name__)


def get_mongo():
    url = os.getenv('DATABASE_URL', 'mongodb://localhost:27017/sustainable-shopping-planner')
    client = MongoClient(url)
    db = client.get_default_database()
    return client, db


@app.route('/')
def home():
    return 'Brand Data Collector Running'


@app.route('/health')
def health():
    try:
        client, db = get_mongo()
        db.command('ping')
        client.close()
        return jsonify({
            'status': 'healthy'
        })
    except Exception as e:
        return jsonify({'status': 'degraded', 'error': str(e)}), 500


@app.route('/brands')
def list_brands():
    try:
        client, db = get_mongo()
        limit = int(request.args.get('limit', '100'))
        docs = list(db.brands.find({}, {"_id": 0}).limit(limit))
        client.close()
        return jsonify({'brands': docs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=5001)
