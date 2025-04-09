# Guia Rápido - Sistema Gerenciador de Vendas

## Instruções Iniciais
- Faça o download ou clone o repositorio
```bash
    git clone https://github.com/wescley1/Mesha-Tecnologia.git
    cd Mesha-Tecnologia/gerenciador_vendas
```


- Execute o arquivo `launcher_windows.bat`, se estiver no Windows ou `launcher_linux.sh` se estiver no Linux.

---

## Visão Geral
Este projeto contém um gerenciador e um sistema web com automações integrados. Foi desenvolvido em **Python**, com execução controlada via **terminal** (usando `.bat` no Windows ou `.sh` no Linux). Algumas capacidades são:

- Cadastrar vendas  
- Monitorar alterações no banco de dados  
- Gerar relatórios  
- Enviar relatórios por e-mail

---

## Funcionalidades Principais do gerenciador

### 1. Iniciar Sistema
- Inicia dois serviços principais:
  - `app.py`: Interface web da aplicação  
    - Acesse em: [http://localhost:5000/](http://localhost:5000/)  
    - Usa templates da pasta `/templates`
  - `monitor_vendas.py`: Monitora o banco `loja.db` em tempo real  
- Caso o banco `loja.db` não exista, o sistema oferece criá-lo com `setup_banco.py`, que também adiciona produtos e uma venda fictícia.

### 2. Parar Sistema
- Encerra os serviços:
  - `app.py`
  - `monitor_vendas.py`

### 3. Executar Automação de Vendas
- Executa `automacao_vendas.py`, que simula o registro automático de vendas a partir do `vendas.json`.

### 4. Gerar Relatório e Enviar por E-mail
- Executa `gerar_relatorio.py`
- Gera um relatório em **PDF** com os dados do dia atual
- Solicita o e-mail do destinatário
- Envia o PDF por e-mail usando uma conta previamente configurada com senha de app

---

## Sobre as Automações

### Automação de Cadastro de Vendas
- Utiliza `automacao_vendas.py` para inserir dados fictícios no banco, com base no arquivo `vendas.json`.

### Monitor de Vendas
- `monitor_vendas.py` detecta automaticamente novas vendas registradas.
- Dispara ações como:
  - Simulação de envio de boleto ou chave PIX
  - Simulação de verificação de pagamento
  - Baixa automática no estoque

---

## Arquivos Importantes

- `launcher.bat` (Windows) / `launcher.sh` (Linux) — menus principais  
- `app.py` — backend da interface web  
- `monitor_vendas.py` — monitoramento em tempo real  
- `automacao_vendas.py` — simulação de vendas automáticas  
- `gerar_relatorio.py` — geração e envio de PDF  
- `setup_banco.py` — criação inicial do banco de dados  
- `requirements.txt` — dependências do projeto

---

## Requisitos

- Python 3.x
- Ambiente virtual (`venv`) com as bibliotecas:
  - `fpdf`
  - `sqlite3` (nativo)
  - `smtplib`, `email` (nativos)
  - `watchdog`
  - `selenium`
  - `flask`
- Se a pasta `venv` não existir, ela será criada automaticamente e as dependências serão instaladas.

---

## Observações
- O envio de e-mails exige uma **senha de app do Gmail**
- O e-mail do destinatário do relatório é solicitado na hora da execução

---

## Desenvolvido para o processo seletivo da Mesha Tecnologia
