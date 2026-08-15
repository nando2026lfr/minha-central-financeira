import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Configuração da Página
st.set_page_config(page_title="Central Financeira", layout="wide", initial_sidebar_state="expanded")

# Estilo Visual Escuro
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    .card { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .subtext { color: #8b949e; font-size: 12px; }
    .positive { color: #2ea043; font-weight: bold; }
    .negative { color: #f85149; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- DADOS DOS CARTÕES DE CRÉDITO ---
CARTÕES_INFO = {
    "C6 Carbon": {"Fechamento": "Dia 28", "Vencimento": "Dia 05", "Limite": 23300.00},
    "Itaú Platinum": {"Fechamento": "Dia 03", "Vencimento": "Dia 11", "Limite": 15000.00},
    "Outros Cartões": {"Fechamento": "Varia", "Vencimento": "Varia", "Limite": 8052.23}
}

# --- MEMÓRIA DA APLICAÇÃO (SESSION STATE) ---
if 'lancamentos' not in st.session_state:
    st.session_state.lancamentos = pd.DataFrame([
        {"Data": "2026-08-01", "Descrição": "Supermercado", "Valor (R$)": 350.00, "Tipo": "Saída", "Forma": "Cartão C6 Carbon", "Categoria": "Alimentação"},
        {"Data": "2026-08-05", "Descrição": "Combustível", "Valor (R$)": 200.00, "Tipo": "Saída", "Forma": "Pix", "Categoria": "Transporte"},
        {"Data": "2026-08-01", "Descrição": "Adiantamento Quinzenal (1º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal"},
        {"Data": "2026-08-15", "Descrição": "Salário Quinzenal (2º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal"},
    ])

# --- NAVEGAÇÃO POR ABAS ---
st.sidebar.title("📌 Menu Principal")
aba_selecionada = st.sidebar.radio(
    "Navegue pelo App:",
    ["🏠 Centro de Comando", "💵 Total Recebido (Mês)", "➕ Lançar Gastos", "📋 Histórico de Lançamentos"]
)

# =========================================================
# ABA 1: CENTRO DE COMANDO (EDITÁVEL E COM CARTÕES)
# =========================================================
if aba_selecionada == "🏠 Centro de Comando":
    st.title("💼 CENTRAL FINANCEIRA")
    st.caption("Agosto / 2026 — Controle Editável de Caixa e Metas")

    df = st.session_state.lancamentos
    
    total_entradas = df[df['Tipo'] == 'Entrada']['Valor (R$)'].sum()
    total_saidas = df[df['Tipo'] == 'Saída']['Valor (R$)'].sum()
    saldo_disponivel = total_entradas - total_saidas

    # Edição Rápida no Centro de Comando
    with st.expander("✏️ Editar Metas e Valores Gerais do Painel"):
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            meta_reserva = st.number_input("Meta da Reserva (R$)", value=15000.00, step=500.0)
            reserva_atual = st.number_input("Reserva Atual (R$)", value=1850.00, step=100.0)
        with col_ed2:
            limite_c6 = st.number_input("Limite C6 Carbon (R$)", value=23300.00)
            limite_itau = st.number_input("Limite Itaú Platinum (R$)", value=15000.00)

    # Indicadores
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="card"><span class="subtext">SALDO DISPONÍVEL</span><h2 class="positive">R$ {saldo_disponivel:,.2f}</h2></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="card"><span class="subtext">RECEITAS DO MÊS</span><h2>R$ {total_entradas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="card"><span class="subtext">DESPESAS DO MÊS</span><h2 class="negative">R$ {total_saidas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c4:
        st.markdown(f'<div class="card"><span class="subtext">SOBRA PREVISTA</span><h2 style="color: #a371f7;">R$ {saldo_disponivel:,.2f}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")

    # Gráficos
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**GASTOS POR CARTÃO / FORMA DE PAGAMENTO**")
        df_saidas = df[df['Tipo'] == 'Saída']
        if not df_saidas.empty:
            df_forma = df_saidas.groupby('Forma')['Valor (R$)'].sum().reset_index()
            fig_forma = go.Figure(data=[go.Pie(labels=df_forma['Forma'], values=df_forma['Valor (R$)'], hole=.5)])
            fig_forma.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_forma, use_container_width=True)
        else:
            st.info("Nenhum gasto registrado ainda.")

    with col_g2:
        st.markdown("**DISTRIBUIÇÃO DA RESERVA DE EMERGÊNCIA**")
        pct_reserva = (reserva_atual / meta_reserva) * 100
        fig_reserva = go.Figure(data=[go.Pie(labels=['Atingido', 'Falta'], values=[reserva_atual, meta_reserva - reserva_atual], hole=.5, marker_colors=['#d29922', '#21262d'])])
        fig_reserva.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_reserva, use_container_width=True)
        st.caption(f"Meta: R$ {meta_reserva:,.2f} ({pct_reserva:.1f}% concluído)")

# =========================================================
# ABA 2: TOTAL RECEBIDO NO MÊS (QUINZENAL)
# =========================================================
elif aba_selecionada == "💵 Total Recebido (Mês)":
    st.title("💵 Total Recebido do Mês")
    st.caption("Acompanhamento das Entradas e Recebimentos Quinzenais")

    df = st.session_state.lancamentos
    df_entradas = df[df['Tipo'] == 'Entrada'].copy()
    
    total_recebido = df_entradas['Valor (R$)'].sum()

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f'<div class="card"><span class="subtext">TOTAL ACUMULADO NO MÊS</span><h2 class="positive">R$ {total_recebido:,.2f}</h2></div>', unsafe_allow_html=True)
    with col_r2:
        st.markdown(f'<div class="card"><span class="subtext">QTD. DE RECEBIMENTOS</span><h2>{len(df_entradas)} Pagamentos</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Detalhamento dos Recebimentos")
    st.dataframe(df_entradas[["Data", "Descrição", "Valor (R$)", "Forma"]], use_container_width=True)

# =========================================================
# ABA 3: FORMULÁRIO DE LANÇAMENTO
# =========================================================
elif aba_selecionada == "➕ Lançar Gastos":
    st.title("➕ Registrar Novo Lançamento")
    
    with st.form("form_lancamento", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            data = st.date_input("Data", datetime.now())
            descricao = st.text_input("Descrição (Ex: Feira, Mercado, Posto)")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=5.00, format="%.2f")
        
        with col_f2:
            tipo = st.selectbox("Tipo", ["Saída", "Entrada"])
            forma = st.selectbox("Forma de Pagamento", [
                "Cartão C6 Carbon", 
                "Cartão Itaú Platinum", 
                "Outros Cartões", 
                "Débito", 
                "Pix", 
                "Dinheiro"
            ])
            categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Contas Fixas", "Renda Quinzenal", "Outros"])

        # Informações do Cartão
        if "C6" in forma:
            st.info(f"💳 **C6 Carbon:** Fechamento {CARTÕES_INFO['C6 Carbon']['Fechamento']} | Vencimento {CARTÕES_INFO['C6 Carbon']['Vencimento']}")
        elif "Itaú" in forma:
            st.info(f"💳 **Itaú Platinum:** Fechamento {CARTÕES_INFO['Itaú Platinum']['Fechamento']} | Vencimento {CARTÕES_INFO['Itaú Platinum']['Vencimento']}")

        btn_salvar = st.form_submit_button("💾 Salvar Registro")

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
# ABA 4: HISTÓRICO COMPLETO
# =========================================================
elif aba_selecionada == "📋 Histórico de Lançamentos":
    st.title("📋 Histórico Geral de Lançamentos")
    
    df_exibicao = st.session_state.lancamentos.sort_values(by="Data", ascending=False)
    st.dataframe(df_exibicao, use_container_width=True)

    if st.button("🗑️ Limpar Todos os Lançamentos"):
        st.session_state.lancamentos = pd.DataFrame(columns=["Data", "Descrição", "Valor (R$)", "Tipo", "Forma", "Categoria"])
        st.rerun()
