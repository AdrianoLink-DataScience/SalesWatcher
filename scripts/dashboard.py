import streamlit as st
import pandas as pd
import sqlite3
import os
import altair as alt  # Importando a biblioteca de gráficos avançados

# Configuração da Página
st.set_page_config(page_title="SalesWatcher Dashboard", page_icon="📊", layout="wide")

# --- FUNÇÃO PARA CARREGAR DADOS ---
@st.cache_data
def load_data():
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(pasta_atual, "..", "db", "vendas.db")
    
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM vendas"
        df = pd.read_sql(query, conn)
        conn.close()
        df['data'] = pd.to_datetime(df['data'])
        return df
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return pd.DataFrame()

df = load_data()

# --- BARRA LATERAL ---
st.sidebar.header("🔍 Filtros Avançados")

if not df.empty:
    lojas = df['loja'].unique()
    sel_lojas = st.sidebar.multiselect("Lojas:", lojas, default=lojas)
    
    produtos = df['produto'].unique()
    sel_produtos = st.sidebar.multiselect("Produtos:", produtos, default=produtos)

    df_filtrado = df[
        (df['loja'].isin(sel_lojas)) & 
        (df['produto'].isin(sel_produtos))
    ]
else:
    df_filtrado = df

# --- DASHBOARD ---
st.title("📊 SalesWatcher: Analytics")
st.markdown("---")

if df_filtrado.empty:
    st.warning("Nenhum dado disponível com os filtros atuais.")
else:
    # 1. KPIs
    total = df_filtrado['valor_total'].sum()
    qtd = df_filtrado['quantidade'].sum()
    ticket = total / qtd if qtd > 0 else 0
    
    c1, c2, c3 = st.columns(3)
    c1.metric("💰 Receita Total", f"R$ {total:,.2f}")
    c2.metric("📦 Volume de Vendas", f"{qtd}")
    c3.metric("🏷️ Ticket Médio", f"R$ {ticket:,.2f}")
    
    st.markdown("---")

    # 2. Gráficos Customizados com Altair
    aba1, aba2, aba3 = st.tabs(["📈 Tendência", "🏪 Performance Lojas", "🛍️ Top Produtos"])

    with aba1:
        st.subheader("Evolução Diária")
        dados_tempo = df_filtrado.groupby('data')['valor_total'].sum().reset_index()
        
        # Gráfico de Linha com Pontos
        grafico_tempo = alt.Chart(dados_tempo).mark_line(point=True).encode(
            x=alt.X('data', title='Data', axis=alt.Axis(format='%d/%m')),
            y=alt.Y('valor_total', title='Receita (R$)'),
            tooltip=['data', 'valor_total']
        ).properties(height=400)
        
        st.altair_chart(grafico_tempo, use_container_width=True)

    with aba2:
        st.subheader("Receita por Loja")
        dados_loja = df_filtrado.groupby('loja')['valor_total'].sum().reset_index()
        
        # Gráfico de Barras com Rótulo a 45 graus
        grafico_loja = alt.Chart(dados_loja).mark_bar().encode(
            x=alt.X('loja', title='Loja', axis=alt.Axis(labelAngle=-45)), # <--- A MÁGICA AQUI
            y=alt.Y('valor_total', title='Receita Total'),
            color='loja',
            tooltip=['loja', 'valor_total']
        ).properties(height=400)
        
        st.altair_chart(grafico_loja, use_container_width=True)

    with aba3:
        st.subheader("Mix de Produtos (Qtd)")
        dados_prod = df_filtrado.groupby('produto')['quantidade'].sum().reset_index()
        
        grafico_prod = alt.Chart(dados_prod).mark_bar().encode(
            x=alt.X('produto', title='Produto', sort='-y', axis=alt.Axis(labelAngle=-45)), # Ordenado do maior para o menor
            y=alt.Y('quantidade', title='Qtd Vendida'),
            color=alt.value('#FF4B4B'), # Cor personalizada (vermelho Streamlit)
            tooltip=['produto', 'quantidade']
        ).properties(height=400)
        
        st.altair_chart(grafico_prod, use_container_width=True)

    # 3. Botão de Refresh
    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear()
        st.rerun()
