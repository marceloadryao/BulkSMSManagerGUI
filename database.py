import sqlite3

# Conectar ao banco de dados (ou criar, se não existir)
conn = sqlite3.connect('bulk_sms_manager.db')

# Criar um cursor
cursor = conn.cursor()

# Criar uma tabela
cursor.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY,
    recipient TEXT NOT NULL,
    message TEXT NOT NULL,
    status TEXT NOT NULL
)
''')

# Salvar (commit) as mudanças
conn.commit()

# Fechar a conexão
conn.close()