import time
import os
import sqlite3
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

CAMINHO_BANCO = "loja.db"

# Função de log que pode ser sobrescrita
log_callback = print

def set_log_callback(callback):
    global log_callback
    log_callback = callback

class MonitorBancoHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(CAMINHO_BANCO):
            log_callback(f"[{datetime.now().strftime('%H:%M:%S')}] Banco modificado! Executando ação...")
            efetivar_venda()
            verificar_pagamentos()

def efetivar_venda():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT id, cliente, pagamento_tipo FROM vendas where status = 'pendente' ORDER BY id")
    vendas_pendentes = cursor.fetchall()
    conn.close()
    if len(vendas_pendentes) > 0: 
        log_callback(f"Foram encontradas {len(vendas_pendentes)} vendas a serem processadas. Iniciando processamento")
        for venda in vendas_pendentes:
            log_callback(f"Venda sendo processada: {venda}")
            envio_pagamento(venda[0], venda[1], venda[2])
            registrar_pagamento_aguardando(venda[0], venda[2])
        log_callback("Todas vendas pendentes processadas")
    else:
        log_callback("Nenhuma venda pendente foi encontrada")

def envio_pagamento(venda_id, cliente, tipo='pix'):
    if tipo == 'pix':
        chave_pix = f"{random.randint(100000000000,999999999999)}@email.com"
        log_callback(f"Chave PIX enviada para {cliente}: {chave_pix}")
    else:
        codigo_boleto = f"{random.randint(10**41, 10**42 - 1)}"
        log_callback(f"Boleto enviado para {cliente}: {codigo_boleto}")

    time.sleep(2)

def registrar_pagamento_aguardando(venda_id, tipo):
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("UPDATE vendas SET status = ?, pagamento_tipo = ?, pagamento_confirmado = NULL WHERE id = ?",
                   ("Aguardando Pagamento", tipo, venda_id))
    conn.commit()
    conn.close()

def verificar_pagamentos():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()

    cursor.execute("SELECT id, cliente FROM vendas WHERE status = 'Aguardando Pagamento'")
    pendentes = cursor.fetchall()

    for venda_id, cliente in pendentes:
        foi_pago = random.choice([True, False])

        if foi_pago:
            log_callback(f"Cliente {cliente} realizou o pagamento da venda {venda_id}")
            cursor.execute("UPDATE vendas SET status = ?, pagamento_confirmado = True WHERE id = ?",
                           ("Pago", venda_id))
            cursor.execute("SELECT produto_id, quantidade FROM itens_venda WHERE venda_id = ?", (venda_id,))
            itens = cursor.fetchall()
            envio_nf()
            for produto_id, qtd in itens:
                cursor.execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?", (qtd, produto_id))
        else:
            log_callback(f"Cliente {cliente} NÃO pagou a venda {venda_id}. Mantendo como pendente.")

    conn.commit()
    conn.close()

def envio_nf():
    log_callback("Gerando e enviando nota fiscal para cliente")   

def iniciar_monitoramento():
    path = os.path.dirname(os.path.abspath(CAMINHO_BANCO))
    observer = Observer()
    event_handler = MonitorBancoHandler()
    observer.schedule(event_handler, path=path, recursive=False)

    log_callback("Monitorando alterações no banco de dados...")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    iniciar_monitoramento()
