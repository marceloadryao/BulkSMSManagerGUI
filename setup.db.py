import sqlite3
import random
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='phones.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.conn:
            self.conn.close()

    def create_tables(self):
        self.connect()
        # Tabela com mais informações úteis
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS phones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                number TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP,
                last_message_sent TIMESTAMP
            )
        ''')
        
        # Tabela para histórico de mensagens
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_id INTEGER,
                message TEXT,
                sent_at TIMESTAMP,
                status TEXT,
                FOREIGN KEY (phone_id) REFERENCES phones (id)
            )
        ''')
        self.conn.commit()

    def generate_random_phone_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(8)])

    def add_phone_number(self, number):
        self.cursor.execute(
            "INSERT INTO phones (number, created_at) VALUES (?, ?)",
            (number, datetime.now())
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_message_history(self, phone_id, message, status='sent'):
        self.cursor.execute(
            "INSERT INTO message_history (phone_id, message, sent_at, status) VALUES (?, ?, ?, ?)",
            (phone_id, message, datetime.now(), status)
        )
        self.conn.commit()

    def get_active_phones(self, limit=None):
        query = "SELECT id, number FROM phones WHERE status = 'active'"
        if limit:
            query += f" LIMIT {limit}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_phone_status(self, phone_id, status):
        self.cursor.execute(
            "UPDATE phones SET status = ? WHERE id = ?",
            (status, phone_id)
        )
        self.conn.commit()

    def get_message_history(self, phone_id=None):
        if phone_id:
            self.cursor.execute(
                """
                SELECT p.number, m.message, m.sent_at, m.status 
                FROM message_history m 
                JOIN phones p ON m.phone_id = p.id 
                WHERE p.id = ?
                """, 
                (phone_id,)
            )
        else:
            self.cursor.execute(
                """
                SELECT p.number, m.message, m.sent_at, m.status 
                FROM message_history m 
                JOIN phones p ON m.phone_id = p.id
                """
            )
        return self.cursor.fetchall()

def initialize_database():
    db = DatabaseManager()
    db.connect()
    db.create_tables()
    
    # Adicionar números de exemplo
    for _ in range(50):
        number = db.generate_random_phone_number()
        db.add_phone_number(number)
    
    print("Banco de dados inicializado com 50 números aleatórios")
    db.disconnect()

if __name__ == "__main__":
    initialize_database()