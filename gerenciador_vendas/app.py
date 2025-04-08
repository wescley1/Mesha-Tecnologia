from flask import Flask, render_template, request, redirect, flash, redirect, url_for
import sqlite3
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import os


app = Flask(__name__)

########################
#####configura logs#####
#########################
if not os.path.exists('logs'):
    os.makedirs('logs')


log_formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)

log_file = 'logs/app.log'

file_handler = RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Adiciona ao logger da aplicação Flask
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


######################################
###### define funções e rotas#########
#####################################

def conectar_banco():
    app.logger.info(f'Iniciando conexão com o banco')
    return sqlite3.connect('loja.db')

def buscar_produtos():
    conn = conectar_banco()
    cursor = conn.cursor()
    app.logger.info(f'Buscando produtos no banco de dados')
    cursor.execute("SELECT id, nome FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return produtos

@app.route('/')
def home():
    app.logger.info(f'Acessando home')
    return render_template('home.html')


@app.route('/nova-venda', methods=['GET', 'POST'])
def nova_venda():
    if request.method == 'POST':
        cliente = request.form['cliente']
        data = request.form['data']
        produtos = request.form.getlist('produto')
        quantidades = request.form.getlist('quantidade')
        pagamento_tipo = request.form.get('pagamento_tipo')

        app.logger.info(f'Nova venda obtida da aplicação. Cliente: {cliente}')

        conn = conectar_banco()
        cursor = conn.cursor()

        total = 0

        # Calcular total
        for i, prod_id in enumerate(produtos):
            cursor.execute("SELECT preco FROM produtos WHERE id = ?", (prod_id,))
            preco = cursor.fetchone()[0]
            total += preco * int(quantidades[i]) 
        app.logger.info(f'Valor total da venda: {total}')
        app.logger.info(f'Tipo de pagamento da venda: {pagamento_tipo}')
        app.logger.info(f'Inserindo novas vendas nas tabelas')
        
        # Inserir na tabela vendas
        status = 'pendente'
        sql = f"""
    INSERT INTO vendas (cliente, data, total, status, pagamento_tipo)
    VALUES ('{cliente}', '{data}', {total}, '{status}', '{pagamento_tipo}')
"""
        app.logger.info(f'Query de insert: {sql}')
        cursor.execute(sql)
        venda_id = cursor.lastrowid

        # Inserir na tabela itens_venda
        for i, prod_id in enumerate(produtos):
            cursor.execute("SELECT preco FROM produtos WHERE id = ?", (prod_id,))
            preco = cursor.fetchone()[0]
            cursor.execute(
                "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (venda_id, prod_id, int(quantidades[i]), preco)
            )

        conn.commit()
        app.logger.info(f'Informações adicionadas com sucesso. Fechando conexão com banco.')
        conn.close()
        return redirect('/nova-venda')  # Você pode mudar pra outra rota depois

    produtos = buscar_produtos()
    # from datetime import datetime  # já deve estar no topo

    data_hoje = datetime.utcnow().strftime('%Y-%m-%d')
    return render_template('nova_venda.html', produtos=produtos, data_hoje=data_hoje)

@app.route('/vendas')
def listar_vendas():
    conn = conectar_banco()
    app.logger.info(f'Buscando informações de vendas')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT vendas.id, vendas.cliente, vendas.data, vendas.total, COUNT(itens_venda.id)
        FROM vendas
        LEFT JOIN itens_venda ON vendas.id = itens_venda.venda_id
        GROUP BY vendas.id
        ORDER BY vendas.data DESC
    """)
    vendas = cursor.fetchall()
    conn.close()

    return render_template('listar_vendas.html', vendas=vendas)

@app.route('/vendas/<int:venda_id>')
def detalhes_venda(venda_id):
    conn = conectar_banco()
    app.logger.info(f'Buscando detalhes da venda de id {venda_id}')
    cursor = conn.cursor()

    # Busca a venda
    cursor.execute("""
        SELECT id, cliente, data, total, pagamento_tipo
        FROM vendas
        WHERE id = ?
    """, (venda_id,))
    venda = cursor.fetchone()

    # Busca os itens da venda com os nomes dos produtos
    cursor.execute("""
        SELECT produtos.nome, itens_venda.quantidade, itens_venda.preco_unitario
        FROM itens_venda
        JOIN produtos ON produtos.id = itens_venda.produto_id
        WHERE itens_venda.venda_id = ?
    """, (venda_id,))
    itens = cursor.fetchall()

    conn.close()

    return render_template('detalhes_venda.html', venda=venda, itens=itens)

@app.route('/vendas/<int:venda_id>/editar', methods=['GET', 'POST'])
def editar_venda(venda_id):
    conn = conectar_banco()
    app.logger.info(f'Editando informações da venda {venda_id}')
    cursor = conn.cursor()

    if request.method == 'POST':
        # Atualiza o cliente
        cliente = request.form['cliente']
        cursor.execute("UPDATE vendas SET cliente = ? WHERE id = ?", (cliente, venda_id))

        # Remove os itens antigos
        cursor.execute("DELETE FROM itens_venda WHERE venda_id = ?", (venda_id,))

        total = 0
        produtos = cursor.execute("SELECT id, nome FROM produtos").fetchall()

        for produto in produtos:
            pid = produto[0]
            qtd = request.form.get(f'quantidade_{pid}')
            if qtd and int(qtd) > 0:
                preco = cursor.execute("SELECT preco FROM produtos WHERE id = ?", (pid,)).fetchone()[0]
                subtotal = int(qtd) * preco
                total += subtotal
                cursor.execute(
                    "INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                    (venda_id, pid, int(qtd), preco)
                )

        # Atualiza o total
        cursor.execute("UPDATE vendas SET total = ? WHERE id = ?", (total, venda_id))

        conn.commit()
        conn.close()
        return redirect('/vendas')

    # Para método GET, carrega dados da venda
    venda = cursor.execute("SELECT cliente FROM vendas WHERE id = ?", (venda_id,)).fetchone()
    itens = cursor.execute("SELECT produto_id, quantidade FROM itens_venda WHERE venda_id = ?", (venda_id,)).fetchall()
    produtos = cursor.execute("SELECT id, nome FROM produtos").fetchall()

    # Converte itens para dicionário {produto_id: quantidade}
    itens_dict = {pid: qtd for pid, qtd in itens}

    conn.close()

    return render_template('editar_venda.html', venda_id=venda_id, cliente=venda[0], produtos=produtos, itens=itens_dict)

@app.route('/vendas/<int:venda_id>/excluir', methods=['GET', 'POST'])
def excluir_venda(venda_id):
    conn = conectar_banco()
    app.logger.info(f'Excluindo venda {venda_id}')
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("DELETE FROM itens_venda WHERE venda_id = ?", (venda_id,))
        cursor.execute("DELETE FROM vendas WHERE id = ?", (venda_id,))
        conn.commit()
        conn.close()
        return redirect('/vendas')

    venda = cursor.execute("SELECT cliente FROM vendas WHERE id = ?", (venda_id,)).fetchone()
    conn.close()
    return render_template('excluir_venda.html', venda_id=venda_id, cliente=venda[0])

@app.route('/relatorio')
def relatorio():
    conn = conectar_banco()
    cursor = conn.cursor()

    vendas = cursor.execute("SELECT id, cliente, data, total FROM vendas ORDER BY data DESC").fetchall()

    relatorio_vendas = []
    for venda in vendas:
        venda_id, cliente, data, total = venda
        itens = cursor.execute('''
            SELECT p.nome, iv.quantidade, iv.preco_unitario
            FROM itens_venda iv
            JOIN produtos p ON iv.produto_id = p.id
            WHERE iv.venda_id = ?
        ''', (venda_id,)).fetchall()

        itens_formatados = [
            {
                'nome': item[0],
                'quantidade': item[1],
                'preco': item[2],
                'subtotal': item[1] * item[2]
            }
            for item in itens
        ]

        relatorio_vendas.append({
            'id': venda_id,
            'cliente': cliente,
            'data': data,
            'total': total,
            'itens': itens_formatados
        })

    conn.close()
    return render_template('relatorio.html', vendas=relatorio_vendas)




if __name__ == '__main__':
    app.run(debug=True)

