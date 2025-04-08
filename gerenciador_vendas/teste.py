# -*- coding: utf-8 -*-
"""
Created on Mon Apr  7 12:50:54 2025

@author: wescl
"""

import time
import os
import sqlite3
import random
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

CAMINHO_BANCO = "loja.db"  # Ajuste se seu arquivo estiver em outro lugar


def acao_apos_venda():
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas ORDER BY id DESC LIMIT 1")
    nova_venda = cursor.fetchone()
    vendas = cursor.fetchall()
    print(nova_venda[0])
    conn.close()
    print(f"📦 Última venda: {nova_venda}")

def simular_envio_pagamento(venda_id, cliente, tipo='pix'):
    if tipo == 'pix':
        chave_pix = f"{random.randint(100000000000,999999999999)}@email.com"
        print(f"🔔 Chave PIX enviada para {cliente}: {chave_pix}")
    else:
        codigo_boleto = f"{random.randint(100000000000000000000000000000000000000000, 999999999999999999999999999999999999999999)}"
        print(f"🔔 Boleto enviado para {cliente}: {codigo_boleto}")

    # Simula tempo de espera até o pagamento (em segundos)
    time.sleep(2)



if __name__ == "__main__":
    path = os.path.dirname(os.path.abspath(CAMINHO_BANCO))    
    #acao_apos_venda()
    
    conn = sqlite3.connect(CAMINHO_BANCO)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas where status = 'pendente' ORDER BY id")        
    vendas = cursor.fetchall()    
    for venda in vendas:
        print(f"Ultima venda: {venda}")
    conn.close()
    

    #print("🔍 Monitorando alterações no banco de dados...")
    #observer.start()

    #try:
    #    while True:
    #        time.sleep(1)
    #except KeyboardInterrupt:
    #    observer.stop()

    #observer.join()
