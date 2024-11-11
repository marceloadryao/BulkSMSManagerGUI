from flask import Flask, render_template, jsonify, request
from models.database_manager import DatabaseManager # type: ignore
from utils.sms_manager import SMSManager # type: ignore
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sms_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = DatabaseManager(app)
sms = SMSManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    result = sms.send_bulk_sms(
        message=data['message'],
        recipient_count=data['recipients']
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)