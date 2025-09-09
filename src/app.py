import os
import sys

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

try:
    from app import app
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port, debug=False)
except:
    from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    def home():
        return "Yamama AI Assistant"
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 10000))
        app.run(host='0.0.0.0', port=port, debug=False)
