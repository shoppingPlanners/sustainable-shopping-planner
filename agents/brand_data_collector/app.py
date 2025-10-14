# Flask app for brand data collector
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return 'Brand Data Collector Running'

if __name__ == '__main__':
    app.run(port=5001)
