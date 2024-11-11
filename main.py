from flask import Flask, request, jsonify, render_template
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from database_manager import DatabaseManager
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
db = DatabaseManager()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class SMSManager:
    @staticmethod
    def send_bulk_sms(message, recipient_count):
        db.connect()
        try:
            phones = db.get_active_phones(limit=recipient_count)
            successful = 0
            failed = 0
            
            for phone_id, number in phones:
                try:
                    message_obj = twilio_client.messages.create(
                        body=message,
                        from_=TWILIO_PHONE_NUMBER,
                        to=number
                    )
                    
                    # Log successful message
                    db.add_message_history(
                        phone_id=phone_id,
                        message=message,
                        status='sent'
                    )
                    successful += 1
                    
                except TwilioRestException as e:
                    # Log failed message
                    db.add_message_history(
                        phone_id=phone_id,
                        message=message,
                        status=f'failed: {str(e)}'
                    )
                    failed += 1
                    
            return {
                'success': True,
                'successful': successful,
                'failed': failed,
                'total': len(phones)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
        finally:
            db.disconnect()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    if not data or 'message' not in data or 'recipients' not in data:
        return jsonify({
            'success': False,
            'error': 'Missing required fields'
        }), 400
        
    result = SMSManager.send_bulk_sms(
        message=data['message'],
        recipient_count=int(data['recipients'])
    )
    
    return jsonify(result)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db.connect()
    try:
        total_phones = len(db.get_active_phones())
        history = db.get_message_history()
        
        stats = {
            'total_phones': total_phones,
            'total_messages_sent': len(history),
            'last_message_sent': history[-1][2] if history else None
        }
        return jsonify(stats)
    finally:
        db.disconnect()

@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'success': False,
        'error': str(error)
    }), 500

if __name__ == '__main__':
    # Ensure database is initialized
    db.connect()
    db.create_tables()
    db.disconnect()
    
    # Run Flask app
    app.run(debug=True)