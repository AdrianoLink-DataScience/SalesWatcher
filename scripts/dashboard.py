import streamlit as st
import pandas as pd
import sqlite3
import os

# Configuração da Página (Ícone e Título)
st.set_page_config(page_title="SalesWatcher Dashboard", page_icon="📈", layout="wide")

# --- FUNÇÃO PARA CARREGAR DADOS ---
# Usar @st.cache_data faz o dashboard ficar super rápido, pois não relê o banco a cada clique
@st.cache_data
def load_data():
    # Caminho do banco (Blindado para Nuvem)
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(pasta_atual, "..", "db", "vendas.db")
    
    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM vendas"
        df = pd.read_sql(query, conn)
        conn.close()
        
        # Garante que a coluna 'data' seja reconhecida como data
        df['data'] = pd.to_datetime(df['data'])
        return df
    except Exception as e:
        st.error(f"Erro ao conectar: {e}")
        return pd.DataFrame()

# Carrega os dados
df = load_data()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("🔍 Filtros")
st.sidebar.markdown("Use as opções abaixo para filtrar os resultados.")

# Filtro de Loja
if not df.empty:
    lojas_disponiveis = df['loja'].unique()
    lojas_selecionadas = st.sidebar.multiselect("Selecione a Loja:", lojas_disponiveis, default=lojas_disponiveis)
    
    # Filtro de Produto
    produtos_disponiveis = df['produto'].unique()
    produtos_selecionados = st.sidebar.multiselect("Selecione o Produto:", produtos_disponiveis, default=produtos_disponiveis)

    # Aplica os filtros no DataFrame
    df_filtrado = df[
        (df['loja'].isin(lojas_selecionadas)) & 
        (df['produto'].isin(produtos_selecionados))
    ]
else:
    df_filtrado = df

# --- CORPO DO DASHBOARD ---
st.title("📊 SalesWatcher: Visão Estratégica")
st.markdown("Monitoramento de vendas e performance em tempo real.")
st.markdown("---")

if df_filtrado.empty:
    st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
else:
    # 1. KPIs (Indicadores Principais)
    total_vendas = df_filtrado['valor_total'].sum()
    qtd_total = df_filtrado['quantidade'].sum()
    ticket_medio = total_vendas / qtd_total if qtd_total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Receita Total", f"R$ {total_vendas:,.2f}")
    col2.metric("📦 Total de Itens", f"{qtd_total}")
    col3.metric("🏷️ Ticket Médio", f"R$ {ticket_medio:,.2f}")
    
    st.markdown("---")

    # 2. Gráficos em Abas (Melhor organização)
    aba1, aba2, aba3 = st.tabs(["📈 Evolução Temporal", "🏪 Por Loja", "🛍️ Por Produto"])

    with aba1:
        st.subheader("Evolução das Vendas (Dia a Dia)")
        # Agrupa por data para o gráfico de linha
        vendas_tempo = df_filtrado.groupby('data')['valor_total'].sum()
        st.line_chart(vendas_tempo, color="#00FF00") # Linha verde neon (se o tema permitir)

    with aba2:
        st.subheader("Performance por Loja")
        vendas_loja = df_filtrado.groupby("loja")["valor_total"].sum().sort_values(ascending=True)
        st.bar_chart(vendas_loja) # Streamlit ajusta a cor automática

    with aba3:
        st.subheader("Produtos Mais Vendidos (Qtd)")
        vendas_produto = df_filtrado.groupby("produto")["quantidade"].sum().sort_values(ascending=True)
        st.bar_chart(vendas_produto)

    # 3. Tabela de Dados Detalhada
    st.markdown("---")
    with st.expander("🔎 Ver Base de Dados Detalhada"):
        st.dataframe(
            df_filtrado[['data', 'loja', 'produto', 'quantidade', 'valor_total']].sort_values(by='data', ascending=False),
            use_container_width=True,
            hide_index=True
        )

    # Botão de Atualizar
    if st.sidebar.button("🔄 Atualizar Dados"):
        st.cache_data.clear() # Limpa o cache para forçar releitura do banco
        st.rerun()
