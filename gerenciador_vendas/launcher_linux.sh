#!/bin/bash

cd "$(dirname "$0")"

# Criar venv se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar venv
source venv/bin/activate

# Instalar dependências
echo "Instalando dependências..."
pip install -r requirements.txt

while true; do
    clear
    echo "===================================="
    echo "      GERENCIADOR DE VENDAS"
    echo "===================================="
    echo "1. Iniciar Sistema"
    echo "2. Parar Sistema"
    echo "3. Executar Automacao de Vendas"
    echo "4. Gerar Relatorio e Enviar por Email"
    echo "0. Sair"
    echo "===================================="
    read -p "Escolha uma opcao: " opcao

    case $opcao in
        1)
            echo "Verificando banco de dados..."
            if [ ! -f "loja.db" ]; then
                read -p "Banco não encontrado. Deseja criar um novo? (s/n): " criar
                if [[ "$criar" == "s" || "$criar" == "S" ]]; then
                    python setup_banco.py
                else
                    echo "Operação cancelada."
                    read -p "Pressione Enter para continuar..." dummy
                    continue
                fi
            fi
            gnome-terminal -- bash -c "python app.py; exec bash"
            gnome-terminal -- bash -c "python monitor_vendas.py; exec bash"
            read -p "Serviços iniciados. Pressione Enter para continuar..." dummy
            ;;
        2)
            pkill -f app.py
            pkill -f monitor_vendas.py
            echo "Todos os processos encerrados."
            read -p "Pressione Enter para continuar..." dummy
            ;;
        3)
            python automacao_vendas.py
            read -p "Pressione Enter para continuar..." dummy
            ;;
        4)
            read -p "Digite o e-mail de destino: " email
            python gerar_relatorio.py "$email"
            read -p "Pressione Enter para continuar..." dummy
            ;;
        0)
            echo "Saindo..."
            break
            ;;
        *)
            echo "Opção inválida."
            read -p "Pressione Enter para continuar..." dummy
            ;;
    esac
done
