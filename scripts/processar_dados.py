import sys
import sqlite3
import csv
import os

# O script precisa receber o arquivo como argumento
if len(sys.argv) < 2:
    print("Erro: Informe o arquivo CSV.")
    sys.exit(1)

arquivo_csv = sys.argv[1]
db_path = "../db/vendas.db"

print(f"--> Python: Lendo {arquivo_csv} e salvando no Banco de Dados...")

try:
    # 1. Conectar ao Banco (se não existir, ele cria sozinho)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. Criar a tabela se ela ainda não existir
    # Isso garante que o script rode na primeira vez sem erro
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data DATE,
            loja TEXT,
            produto TEXT,
            quantidade INTEGER,
            valor_unitario REAL,
            valor_total REAL
        )
    ''')

    # 3. Ler o CSV e Inserir no Banco
    with open(arquivo_csv, 'r') as file:
        reader = csv.DictReader(file) # Lê usando o cabeçalho como chave
        
        for row in reader:
            # Pequeno cálculo extra: Total = Qtd * Valor
            total = int(row['quantidade']) * float(row['valor_unitario'])
            
            cursor.execute('''
                INSERT INTO vendas (data, loja, produto, quantidade, valor_unitario, valor_total)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (row['data'], row['loja'], row['produto'], row['quantidade'], row['valor_unitario'], total))

    # 4. Salvar as alterações (Commit)
    conn.commit()
    print("--> Python: Dados inseridos com sucesso!")
    conn.close()

except Exception as e:
    print(f"--> Python ERRO: {e}")
    sys.exit(1) # Sai com erro para o Shell Script saber
