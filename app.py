import streamlit as st
import plotly.graph_objects as go

# Configuração para adaptar à tela do celular
st.set_page_config(page_title="Central Financeira", layout="wide", initial_sidebar_state="collapsed")

# Estilo escuro
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: white; }
    div[data-testid="stMetricValue"] { color: #2ea043; }
    </style>
    """, unsafe_allow_html=True)

st.title("💰 Central Financeira")

# Entradas de dados interativas
st.subheader("⚙️ Lançamentos Rápido")
col1, col2 = st.columns(2)
with col1:
    receita = st.number_input("Receitas do Mês (R$)", value=8820.00, step=100.0)
with col2:
    despesa = st.number_input("Despesas do Mês (R$)", value=5145.60, step=50.0)

saldo = receita - despesa

# Cards Principais
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Saldo Disponível", f"R$ {saldo:,.2f}")
c2.metric("Receita Total", f"R$ {receita:,.2f}")
c3.metric("Despesa Total", f"R$ {despesa:,.2f}")

# Gráfico de Distribuição
st.markdown("---")
fig = go.Figure(data=[go.Pie(
    labels=['Receitas', 'Despesas'], 
    values=[receita, despesa], 
    hole=.5,
    marker_colors=['#2ea043', '#f85149']
)])
fig.update_layout(
    title="Resumo Financeiro", 
    template="plotly_dark",
    paper_bgcolor='#0d1117',
    plot_bgcolor='#0d1117'
)
st.plotly_chart(fig, use_container_width=True)
