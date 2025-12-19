import streamlit as st
import pandas as pd
import sqlite3

# Configuração da Página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

st.title("📊 SalesWatcher: Monitoramento de Vendas")

# 1. Conectar ao Banco de Dados
# Nota: Como vamos rodar de dentro de 'scripts', o banco está em '../db'
db_path = "../db/vendas.db"
conn = sqlite3.connect(db_path)

# 2. Carregar os dados para um DataFrame do Pandas
query = "SELECT * FROM vendas"
df = pd.read_sql(query, conn)

# Fechar conexão (boa prática)
conn.close()

# Se o banco estiver vazio, avisa
if df.empty:
    st.warning("Nenhum dado encontrado no banco de dados.")
else:
    # 3. Métricas Principais (KPIs)
    col1, col2, col3 = st.columns(3)
    
    total_vendas = df['valor_total'].sum()
    qtd_total = df['quantidade'].sum()
    ticket_medio = total_vendas / qtd_total if qtd_total > 0 else 0

    col1.metric("Receita Total", f"R$ {total_vendas:,.2f}")
    col2.metric("Total de Itens Vendidos", qtd_total)
    col3.metric("Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.markdown("---")

    # 4. Gráficos
    col_graf1, col_graf2 = st.columns(2)

    with col_graf1:
        st.subheader("Vendas por Loja")
        # Agrupa por loja e soma o total
        vendas_por_loja = df.groupby("loja")["valor_total"].sum().sort_values(ascending=False)
        st.bar_chart(vendas_por_loja)

    with col_graf2:
        st.subheader("Vendas por Produto")
        vendas_por_produto = df.groupby("produto")["quantidade"].sum().sort_values(ascending=False)
        st.bar_chart(vendas_por_produto)

    # 5. Tabela de Dados Recentes
    st.subheader("Últimas Vendas Processadas")
    st.dataframe(df.tail(10))

    # Botão para atualizar (simples refresh)
    if st.button("Atualizar Dados"):
        st.rerun()
