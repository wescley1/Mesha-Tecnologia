Guia Rápido - Sistema Gerenciador de Vendas
---------------------------------------------
Visão Geral
-Para iniciar, clone o repositorio utilizando 
git clone https://github.com/wescley1/Mesha-Tecnologia.git

Funcionalidades Principais

1. Iniciar Sistema
- Inicia dois serviços principais:
  - app.py: Interface web do sistema de vendas.
    - Uma vez iniciado, a interface da aplicação web pode ser acessada em http://localhost:5000/
    - Faz uso dos templates que estão na pasta /templates para gerar as informações das páginas web.

  - monitor_vendas.py: Serviço de monitoramento do banco de dados.
- O sistema verifica se o banco loja.db existe. Se não existir, pergunta se deseja criá-lo automaticamente com o script setup_banco.py. O scrip setup_banco.py adiciona informações de alguns produtos e de uma venda.

2. Parar Sistema
- Encerra os serviços que foram iniciados:
  - Finaliza o processo da aplicação web (app.py).
  - Finaliza o monitor de vendas (monitor_vendas.py).

3. Executar Automação de Vendas
- Executa o script automacao_vendas.py, responsável por simular o registro automático de vendas no sistema com dados fictícios.
- Demonstra 

4. Gerar Relatório e Enviar por E-mail
- Executa o script gerar_relatorio.py.
- Gera um relatório em PDF com os dados de vendas do dia atual.
- Pergunta qual e-mail deve receber o relatório.
- Envia o relatório por e-mail usando uma conta previamente configurada com senha de app.

-------------------------------------------------------------------
Sobre as Automações

Automação de Cadastro de Vendas
- O script automacao_vendas.py insere dados no banco loja.db, a partir das informações contidas no arquivo vendas.json. 

Monitor de Vendas
- O script monitor_vendas.py monitora constantemente o banco de dados para identificar e processar a novas vendas registradas, sendo usado para disparar funcionalidades automáticas como, gerar um boleto ou br_code pix ficticio, verificar se houve pagamento e dar baixa em estoque.

Arquivos Importantes
- launcher.bat (Windows) ou launcher.sh (Linux): Menu principal de execução.
- app.py: Backend web para cadastro e listagem de vendas.
- monitor_vendas.py: Serviço que monitora o banco em tempo real.
- automacao_vendas.py: Simulador de vendas.
- gerar_relatorio.py: Gera e envia relatório em PDF.
- setup_banco.py: Cria o banco de dados inicial.
- requirements.txt: Possui as bibliotecas python necessárias para funcionamento das aplicações.

Requisitos
- Python 3.x
- Ambiente virtual (venv) com as bibliotecas:
  - fpdf
  - sqlite3 
  - smtplib, email
  - watchdog
  - selenium
  - flask
- Note que caso não exista uma pasta \venv na raiz do projeto, ela será criada e as dependências serão instaladas 

Observações
- O envio de e-mails usa uma senha de app do Gmail.
- O destinatário do relatório é solicitado na hora da execução.