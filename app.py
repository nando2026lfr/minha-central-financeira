import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração inicial
st.set_page_config(page_title="Central Financeira", layout="wide", initial_sidebar_state="expanded")

# Estilo visual escuro
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    .card { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .subtext { color: #8b949e; font-size: 12px; }
    .positive { color: #2ea043; font-weight: bold; }
    .negative { color: #f85149; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- SISTEMA DE MEMÓRIA DE DADOS (SESSION STATE) ---
if 'lancamentos' not in st.session_state:
    # Dados de exemplo pré-carregados
    st.session_state.lancamentos = pd.DataFrame([
        {"Data": "2026-08-01", "Descrição": "Supermercado", "Valor (R$)": 350.00, "Tipo": "Saída", "Forma": "Cartão de Crédito", "Categoria": "Alimentação"},
        {"Data": "2026-08-05", "Descrição": "Combustível", "Valor (R$)": 200.00, "Tipo": "Saída", "Forma": "Pix", "Categoria": "Transporte"},
        {"Data": "2026-08-15", "Descrição": "Adiantamento Salarial / Quinzena", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda"},
    ])

# --- NAVEGAÇÃO POR ABAS NA BARRA LATERAL ---
st.sidebar.title("📌 Menu Principal")
aba_selecionada = st.sidebar.radio(
    "Navegue pelo App:",
    ["🏠 Centro de Comando", "➕ Lançar Gastos", "📋 Histórico de Lançamentos"]
)

# =========================================================
# ABA 1: CENTRO DE COMANDO (DASHBOARD)
# =========================================================
if aba_selecionada == "🏠 Centro de Comando":
    st.title("💼 CENTRAL FINANCEIRA")
    st.caption("Visão Geral & Indicadores da Quinzena / Mês")

    df = st.session_state.lancamentos
    
    total_entradas = df[df['Tipo'] == 'Entrada']['Valor (R$)'].sum()
    total_saidas = df[df['Tipo'] == 'Saída']['Valor (R$)'].sum()
    saldo_atual = total_entradas - total_saidas

    # Cards Principais
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="card"><span class="subtext">SALDO ATUAL</span><h2 class="positive">R$ {saldo_atual:,.2f}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card"><span class="subtext">ENTRADAS</span><h2>R$ {total_entradas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card"><span class="subtext">SAÍDAS (GASTOS)</span><h2 class="negative">R$ {total_saidas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="card"><span class="subtext">SOBRA PREVISTA</span><h2 style="color: #a371f7;">R$ {saldo_atual:,.2f}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Gráfico de Gastos por Forma de Pagamento
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**GASTOS POR FORMA DE PAGAMENTO**")
        df_saidas = df[df['Tipo'] == 'Saída']
        if not df_saidas.empty:
            df_forma = df_saidas.groupby('Forma')['Valor (R$)'].sum().reset_index()
            fig_forma = go.Figure(data=[go.Pie(labels=df_forma['Forma'], values=df_forma['Valor (R$)'], hole=.5)])
            fig_forma.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_forma, use_container_width=True)
        else:
            st.info("Nenhum gasto registrado ainda.")

    with col_g2:
        st.markdown("**GASTOS POR CATEGORIA**")
        if not df_saidas.empty:
            df_cat = df_saidas.groupby('Categoria')['Valor (R$)'].sum().reset_index()
            fig_cat = go.Figure(data=[go.Pie(labels=df_cat['Categoria'], values=df_cat['Valor (R$)'], hole=.5)])
            fig_cat.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Nenhuma categoria registrada ainda.")

# =========================================================
# ABA 2: FORMULÁRIO DE LANÇAMENTO RÁPIDO
# =========================================================
elif aba_selecionada == "➕ Lançar Gastos":
    st.title("➕ Registrar Novo Lançamento")
    st.caption("Preencha os dados abaixo para registrar um gasto ou entrada:")

    with st.form("form_lancamento", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            data = st.date_input("Data do Lançamento", datetime.now())
            descricao = st.text_input("Descrição (Ex: Feira, Gasolina, Lanche)")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=5.00, format="%.2f")
        
        with col_f2:
            tipo = st.selectbox("Tipo de Movimentação", ["Saída", "Entrada"])
            forma = st.selectbox("Forma de Pagamento / Origem", ["Cartão de Crédito", "Débito", "Pix", "Dinheiro"])
            categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Contas Fixas", "Outros", "Renda"])

        btn_salvar = st.form_submit_button("💾 Salvar Lançamento")

        if btn_salvar:
            novo_item = {
                "Data": str(data),
                "Descrição": descricao,
                "Valor (R$)": valor,
                "Tipo": tipo,
                "Forma": forma,
                "Categoria": categoria
            }
            st.session_state.lancamentos = pd.concat([st.session_state.lancamentos, pd.DataFrame([novo_item])], ignore_index=True)
            st.success(f"Lançamento '{descricao}' de R$ {valor:.2f} registrado com sucesso!")

# =========================================================
# ABA 3: HISTÓRICO DE LANÇAMENTOS
# =========================================================
elif aba_selecionada == "📋 Histórico de Lançamentos":
    st.title("📋 Histórico Completo de Lançamentos")
    st.caption("Confira todos os registros da quinzena/mês:")

    df_exibicao = st.session_state.lancamentos.sort_values(by="Data", ascending=False)
    st.dataframe(df_exibicao, use_container_width=True)

    if st.button("🗑️ Limpar Todos os Dados"):
        st.session_state.lancamentos = pd.DataFrame(columns=["Data", "Descrição", "Valor (R$)", "Tipo", "Forma", "Categoria"])
        st.rerun()
