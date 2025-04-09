import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Caminho do WebDriver (ajuste se necessário)
#driver = webdriver.Chrome()

# Carrega as vendas do JSON
with open('vendas.json', 'r', encoding='utf-8') as f:
    vendas = json.load(f)

for venda in vendas:
    driver.get('http://localhost:5000/nova-venda')  # Rota local do app Flask

    time.sleep(1)

    # Preenche o nome do cliente
    input_cliente = driver.find_element(By.NAME, 'cliente')
    input_cliente.send_keys(venda['cliente'])
    
    # Preenche a data
    driver.find_element(By.NAME, 'data').clear()
    driver.find_element(By.NAME, 'data').send_keys(venda['data'])
    
    # Seleciona o tipo de pagamento
    pagamento_select = Select(driver.find_element(By.NAME, 'pagamento_tipo'))
    pagamento_select.select_by_value(venda['pagamento_tipo'])

    # Para cada produto da venda
    for i, item in enumerate(venda['produtos']):
        if i > 0:
            # Clica no botão para adicionar mais um produto
            driver.find_element(By.XPATH, '/html/body/div[2]/form/button[1]').click()
            time.sleep(0.3)

        # Localiza os campos de produto e quantidade
        select_produto = Select(driver.find_element(By.XPATH, f'/html/body/div[2]/form/div/div[{i+1}]/select'))
        select_produto.select_by_value(str(item['produto_id']))

        input_qtd = driver.find_element(By.XPATH, f'/html/body/div[2]/form/div/div[{i+1}]/input')
        input_qtd.clear()
        input_qtd.send_keys(str(item['quantidade']))

    time.sleep(0.5)

    # Clica no botão de salvar
    driver.find_element(By.XPATH, '//button[text()="Salvar"]').click()
    time.sleep(1)

print("Todas as vendas foram simuladas com sucesso!")
driver.quit()
