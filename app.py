import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Dashboard Financeiro",
    page_icon="💰",
    layout="wide"
)

# Estilização personaliza com CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("💰 Painel Financeiro Pessoal")

# Dados de exemplo para inicialização
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame({
        "Data": ["2026-08-01", "2026-08-05", "2026-08-10"],
        "Categoria": ["Moradia", "Alimentação", "Transporte"],
        "Descrição": ["Aluguel", "Supermercado", "Combustível"],
        "Valor": [1500.0, 450.0, 200.0],
        "Tipo": ["Despesa", "Despesa", "Despesa"]
    })

# Menu Lateral (Sidebar)
st.sidebar.header("Novo Lançamento")
com_data = st.sidebar.date_input("Data")
com_cat = st.sidebar.selectbox("Categoria", ["Moradia", "Alimentação", "Transporte", "Lazer", "Receita", "Outros"])
com_desc = st.sidebar.text_input("Descrição")
com_val = st.sidebar.number_input("Valor (R$)", min_value=0.0, format="%.2f")
com_tipo = st.sidebar.radio("Tipo", ["Despesa", "Receita"])

if st.sidebar.button("Adicionar Lançamento"):
    novo_dado = pd.DataFrame({
        "Data": [str(com_data)],
        "Categoria": [com_cat],
        "Descrição": [com_desc],
        "Valor": [com_val],
        "Tipo": [com_tipo]
    })
    st.session_state.df = pd.concat([st.session_state.df, novo_dado], ignore_index=True)
    st.sidebar.success("Lançamento adicionado com sucesso!")

# Métricas Principais
total_receita = st.session_state.df[st.session_state.df["Tipo"] == "Receita"]["Valor"].sum()
total_despesa = st.session_state.df[st.session_state.df["Tipo"] == "Despesa"]["Valor"].sum()
saldo = total_receita - total_despesa

col1, col2, col3 = st.columns(3)
col1.metric("Receita Total", f"R$ {total_receita:,.2f}")
col2.metric("Despesa Total", f"R$ {total_despesa:,.2f}")
col3.metric("Saldo Atual", f"R$ {saldo:,.2f}")

st.divider()

# Gráficos
col_graf1, col_graf2 = st.columns(2)

df_despesas = st.session_state.df[st.session_state.df["Tipo"] == "Despesa"]

with col_graf1:
    st.subheader("Despesas por Categoria")
    if not df_despesas.empty:
        fig_cat = px.pie(
            df_despesas, 
            names="Categoria", 
            values="Valor", 
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("Nenhuma despesa registrada.")

with col_graf2:
    st.subheader("Histórico de Lançamentos")
    st.dataframe(st.session_state.df, use_container_width=True)
