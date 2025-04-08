@echo off
cd /d "%~dp0"

:: Verificar se venv existe
IF NOT EXIST "venv\" (
    echo Criando ambiente virtual...
    python -m venv venv
)

:: Ativar venv
call venv\Scripts\activate

:: Instalar dependências se necessário
echo Instalando dependências...
pip install -r requirements.txt

:MENU
cls
echo ====================================
echo       GERENCIADOR DE VENDAS
echo ====================================
echo 1. Iniciar Sistema
echo 2. Parar Sistema
echo 3. Executar Automacao de Vendas
echo 4. Gerar Relatorio e Enviar por Email
echo 0. Sair
echo ====================================
set /p op=Escolha uma opcao: 

if "%op%"=="1" goto INICIAR
if "%op%"=="2" goto PARAR
if "%op%"=="3" goto VENDAS
if "%op%"=="4" goto RELATORIO
if "%op%"=="0" exit
goto MENU

:INICIAR
echo Verificando banco de dados...
if exist "loja.db" (
    goto INICIAR_SISTEMA
)

:: Se não existe, pergunta se quer criar
echo Banco de dados nao encontrado.
set /p criar_banco=Deseja criar um novo banco? (s/n): 
if /i "%criar_banco%"=="s" (
    python setup_banco.py
    goto INICIAR_SISTEMA
) else (
    echo Operacao cancelada.
    pause
    goto MENU
)

:INICIAR_SISTEMA
start cmd /k python app.py
start cmd /k python monitor_vendas.py
pause
goto MENU

:PARAR
taskkill /im python.exe /f >nul 2>nul
echo Todos os processos Python foram encerrados.
pause
goto MENU

:VENDAS
python automacao_vendas.py
pause
goto MENU

:RELATORIO
set /p email_destino=Digite o email destino: 
python gerar_relatorio.py "%email_destino%"
pause
goto MENU
