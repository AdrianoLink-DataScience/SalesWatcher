import csv
import random
import datetime
import os

# Gera um nome de arquivo único baseado no tempo, ex: vendas_2023-10-27_1530.csv
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"../data_raw/vendas_{timestamp}.csv"

produtos = ["Notebook", "Mouse", "Teclado", "Monitor", "Cadeira"]
lojas = ["SP_Capital", "RJ_Centro", "MG_BeloHorizonte", "SC_Blumenau"]

print(f"Gerando arquivo: {filename}")

with open(filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["data", "loja", "produto", "quantidade", "valor_unitario"])
    
    # Gera entre 5 e 20 vendas aleatórias
    for _ in range(random.randint(5, 20)):
        data = datetime.date.today()
        loja = random.choice(lojas)
        produto = random.choice(produtos)
        qtd = random.randint(1, 5)
        valor = random.randint(50, 5000)
        writer.writerow([data, loja, produto, qtd, valor])

print("Arquivo gerado com sucesso.")
