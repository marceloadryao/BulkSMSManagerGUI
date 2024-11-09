import sqlite3
from twilio.rest import Client

# Configuração do banco de dados
conn = sqlite3.connect('phones.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS phones (number TEXT)''')
conn.commit()

def add_phone_number(number):
    c.execute("INSERT INTO phones (number) VALUES (?)", (number,))
    conn.commit()

def get_phone_numbers(limit):
    c.execute("SELECT number FROM phones LIMIT ?", (limit,))
    return [row[0] for row in c.fetchall()]

def send_sms(message, numbers):
    # Configure as credenciais da Twilio
    account_sid = 'your_account_sid'
    auth_token = 'your_auth_token'
    client = Client(account_sid, auth_token)

    for number in numbers:
        client.messages.create(
            body=message,
            from_='+your_twilio_number',
            to=number
        )

def main():
    print("Bem-vindo ao sistema de envio de SMS!")
    
    message = input("Digite a mensagem que deseja enviar: ")
    print("Quantos números você deseja enviar a mensagem?")
    print("1. 1000")
    print("2. 5000")
    print("3. 10000")
    print("4. 20000")

    choice = int(input("Escolha uma opção (1-4): "))
    limits = {1: 1000, 2: 5000, 3: 10000, 4: 20000}
    limit = limits.get(choice, 1000)

    numbers = get_phone_numbers(limit)
    send_sms(message, numbers)
    print(f"Mensagem enviada para {len(numbers)} números.")

if __name__ == "__main__":
    main()
