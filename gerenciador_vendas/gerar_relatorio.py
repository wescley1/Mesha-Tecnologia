from fpdf import FPDF
import sqlite3
from datetime import datetime, timedelta, date
import smtplib
from email.message import EmailMessage
import os
import sys


CAMINHO_BANCO = "loja.db"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "Relatório de Vendas do Dia", ln=1, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Data: {date.today().strftime('%d/%m/%Y')}", ln=1, align="C")
        self.ln(5)

    def add_summary(self, total_vendas, total_itens, total_valor):
        self.set_font("Arial", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8,
            f"Resumo do dia:\n"
            f"- Total de vendas: {total_vendas}\n"
            f"- Total de itens vendidos: {total_itens}\n"
            f"- Valor total arrecadado: R$ {total_valor:.2f}\n"
        )
        self.ln(5)

    def table_header(self):
        self.set_font("Arial", "B", 11)
        self.set_fill_color(200, 220, 255)
        headers = ["Cliente", "Data", "Produto", "Qtd", "Preço Unit", "Pagamento"]
        widths = [35, 25, 40, 15, 30, 35]

        for i in range(len(headers)):
            self.cell(widths[i], 10, headers[i], 1, 0, "C", fill=True)
        self.ln()

    def add_row(self, row):
        self.set_font("Arial", "", 10)
        widths = [35, 25, 40, 15, 30, 35]
        for i, col in enumerate(row):
            self.cell(widths[i], 9, str(col), 1, 0, "C")
        self.ln()       
        
def enviar_email_com_pdf(destinatario, caminho_pdf):
    # Configurações do remetente
    remetente = "wescleydesenvolvimento@gmail.com"
    senha_app = "nfpd qjtj regi gplr"

    # Criando a mensagem
    msg = EmailMessage()
    msg['Subject'] = 'Relatório de Vendas - Dia Anterior'
    msg['From'] = remetente
    msg['To'] = destinatario
    msg.set_content('Olá,\n\nSegue em anexo o relatório de vendas do dia anterior.')

    # Anexar o PDF
    with open(caminho_pdf, 'rb') as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(caminho_pdf))

    # Enviar o e-mail via Gmail
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(remetente, senha_app)
        smtp.send_message(msg)

    print("E-mail enviado com sucesso!")



# === BUSCAR OS DADOS === #
conn = sqlite3.connect(CAMINHO_BANCO)
cursor = conn.cursor()
hoje = date.today().isoformat()
# ontem = (datetime.now() - timedelta(days=1)).date().isoformat()

cursor.execute("""
    SELECT v.cliente, v.data, p.nome, i.quantidade, i.preco_unitario, v.pagamento_tipo
    FROM vendas v
    JOIN itens_venda i ON v.id = i.venda_id
    JOIN produtos p ON i.produto_id = p.id
    WHERE v.data = ?
""", (hoje,))
vendas = cursor.fetchall()
conn.close()

# === CALCULAR O RESUMO === #
total_vendas = len(set((v[0], v[1]) for v in vendas))  # cliente + data únicos
total_itens = sum(v[3] for v in vendas)
total_valor = sum(v[3] * v[4] for v in vendas)

# === CRIAR O PDF === #
pdf = PDF()
pdf.add_page()
pdf.add_summary(total_vendas, total_itens, total_valor)
pdf.table_header()

for venda in vendas:
    row = (
        venda[0],  # cliente
        venda[1],
        venda[2],
        str(venda[3]),
        f"R$ {venda[4]:.2f}",
        venda[5].capitalize(),
    )
    pdf.add_row(row)

# === SALVAR PDF === #
filename = f"relatorio_{date.today().isoformat()}.pdf"
pdf.output(filename)
print(f"PDF gerado: {filename}")
# Verifica se o destinatário foi passado
if len(sys.argv) < 2:
    print("Uso: python gerar_relatorio.py <email_destinatario>")
    sys.exit(1)

destinatario = sys.argv[1]

enviar_email_com_pdf(destinatario, filename)

print(f"E-mail enviado com sucesso: {filename}")
