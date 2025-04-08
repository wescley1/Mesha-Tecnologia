import sqlite3
from datetime import datetime

# Conecta ao banco de dados (ou cria se não existir)
conn = sqlite3.connect('loja.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL,
    estoque INTEGER DEFAULT 0
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT NOT NULL,
    pagamento_tipo TEXT DEFAULT 'pix',
    pagamento_confirmado BOOLEAN DEFAULT False,
    data TEXT NOT NULL,
    total REAL NOT NULL,               
    status TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS itens_venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    venda_id INTEGER NOT NULL,
    produto_id INTEGER NOT NULL,
    quantidade INTEGER NOT NULL,
    preco_unitario REAL NOT NULL,
    FOREIGN KEY (venda_id) REFERENCES vendas(id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id)
)
''')

# Popula produtos se estiver vazio
cursor.execute('SELECT COUNT(*) FROM produtos')
if cursor.fetchone()[0] == 0:
    produtos = [
        ('Mouse Gamer', 150.0, 100),
        ('Teclado Mecânico', 250.0, 50),
        ('Monitor 24"', 900.0, 20),
        ('Webcam HD', 120.0, 35),
        ('Headset', 200.0, 40)
    ]
    cursor.executemany('INSERT INTO produtos (nome, preco, estoque) VALUES (?, ?, ?)', produtos)
    print("🟢 Produtos inseridos com sucesso.")

# Inserir uma venda de teste
cursor.execute('SELECT COUNT(*) FROM vendas')
if cursor.fetchone()[0] == 0:
    # Dados da venda
    cliente = "João da Silva"
    data = datetime.now().isoformat()
    status = "pendente"
    
    # Itens da venda: (produto_id, quantidade)
    itens = [
        (1, 2),  # 2 x Mouse Gamer
        (2, 1),  # 1 x Teclado Mecânico
    ]

    # Calcula total e insere venda
    total = 0.0
    for produto_id, quantidade in itens:
        cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
        preco_unit = cursor.fetchone()[0]
        total += preco_unit * quantidade

    cursor.execute('INSERT INTO vendas (cliente, data, total, status) VALUES (?, ?, ?, ?)',
                   (cliente, data, total, status))
    venda_id = cursor.lastrowid

    # Insere itens da venda
    for produto_id, quantidade in itens:
        cursor.execute('SELECT preco FROM produtos WHERE id = ?', (produto_id,))
        preco_unit = cursor.fetchone()[0]
        cursor.execute('''
            INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario)
            VALUES (?, ?, ?, ?)
        ''', (venda_id, produto_id, quantidade, preco_unit))

    print("🟢 Venda de teste inserida com sucesso.")

# Salva e fecha conexão
conn.commit()
conn.close()
