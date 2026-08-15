import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro Pessoal",
    page_icon="📊",
    layout="wide"
)

# Estilização CSS customizada
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel Financeiro Pessoal")

# --- DADOS CONSOLIDADOS ---
RECEITA_MENSAL = 8820.00  # 2x de R$ 4.410,00
META_RESERVA = 15000.00

# Despesas Fixas Mapeadas
despesas_fixas_data = {
    "Categoria": ["Moradia (Apto e Casa)", "Serviços e Rotina"],
    "Valor": [1024.90, 2195.26]
}
df_fixas = pd.DataFrame(despesas_fixas_data)
total_despesas_fixas = df_fixas["Valor"].sum()

# Faturas de Cartões de Crédito (7 cartões mapeados)
cartoes_data = {
    "Cartão": ["Cartão 1", "Cartão 2", "Cartão 3", "Cartão 4", "Cartão 5", "Cartão 6", "Cartão 7"],
    "Valor Fatura": [850.00, 620.00, 710.00, 450.00, 530.00, 380.00, 375.75]
}
df_cartoes = pd.DataFrame(cartoes_data)
total_cartoes = df_cartoes["Valor Fatura"].sum()

# Totais do Mês
total_despesas = total_despesas_fixas + total_cartoes
saldo_livre = RECEITA_MENSAL - total_despesas

# --- MÉTRICAS DE TOPO ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Receita Mensal", f"R$ {RECEITA_MENSAL:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Despesas Fixas", f"R$ {total_despesas_fixas:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Faturas de Cartões", f"R$ {total_cartoes:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
col4.metric("Saldo Livre Estimado", f"R$ {saldo_livre:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

st.divider()

# --- META DE RESERVA DE EMERGÊNCIA ---
st.subheader("🎯 Meta de Reserva Financeira")
reserva_atual = st.number_input(
    "Valor atual acumulado na reserva (R$):", 
    min_value=0.0, 
    value=5000.00, 
    step=500.00
)
progresso_reserva = min(reserva_atual / META_RESERVA, 1.0)

st.progress(progresso_reserva)
st.caption(f"Progresso: **{progresso_reserva*100:.1f}%** de R$ {META_RESERVA:,.2f} atingidos.")

st.divider()

# --- ANÁLISE GRÁFICA ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Detalhamento de Cartões de Crédito")
    fig_cartoes = px.bar(
        df_cartoes,
        x="Cartão",
        y="Valor Fatura",
        text_auto=".2f",
        color="Cartão",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_cartoes.update_layout(showlegend=False, yaxis_title="R$")
    st.plotly_chart(fig_cartoes, use_container_width=True)

with col_graf2:
    st.subheader("Distribuição de Despesas Fixas")
    fig_fixas = px.pie(
        df_fixas,
        names="Categoria",
        values="Valor",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    st.plotly_chart(fig_fixas, use_container_width=True)

# --- TABELAS DETALHADAS ---
st.divider()
st.subheader("📋 Resumo dos Cartões")
st.dataframe(df_cartoes, use_container_width=True)
