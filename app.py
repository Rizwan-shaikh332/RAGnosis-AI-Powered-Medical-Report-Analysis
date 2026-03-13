from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-123')

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import blueprints/controllers
from src.chatbot.chat import chatbot_bp
from src.rag.retriever import rag_bp

# Register blueprints
app.register_blueprint(chatbot_bp, url_prefix='/api/chat')
app.register_blueprint(rag_bp, url_prefix='/api/rag')

@app.route('/')
def home():
    return jsonify({
        'message': 'RAGnosis API',
        'version': '1.0.0',
        'endpoints': {
            'upload': '/api/upload',
            'summarize': '/api/summarize',
            'chat': '/api/chat',
            'visualize': '/api/visualize'
        }
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)