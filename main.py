import re

def validate_phone_number(number):
    # Basic phone number validation pattern
    pattern = re.compile(r'^\+?1?\d{9,15}$')
    return bool(pattern.match(number))

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