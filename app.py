from flask import Flask, render_template, jsonify, request
from models.database_manager import DatabaseManager
from utils.sms_manager import SMSManager
from config.config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize managers
db = DatabaseManager()
sms = SMSManager()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """API endpoint for sending bulk SMS"""
    try:
        data = request.get_json()
        message = data.get('message')
        recipient_count = int(data.get('recipients', 1000))
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
            
        result = sms.send_bulk_sms(message, recipient_count)
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error sending SMS: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get SMS sending statistics"""
    try:
        stats = db.get_stats()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/phones', methods=['GET'])
def get_phones():
    """Get list of phone numbers"""
    try:
        phones = db.get_active_phones()
        return jsonify({'phones': phones})
    except Exception as e:
        logger.error(f"Error getting phones: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Ensure database is initialized
    with app.app_context():
        db.init_db()
    
    # Run the application
    app.run(debug=Config.DEBUG)