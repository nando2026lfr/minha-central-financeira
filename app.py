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
    .warning { color: #d29922; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- LISTA COMPLETA DE CARTÕES DE CRÉDITO ---
LISTA_CARTÕES = [
    "Cartão Itaú Black",
    "Cartão C6 Carbon",
    "Cartão Itaú Platinum",
    "Cartão Sam's Club",
    "Cartão Mercado Pago",
    "Cartão Amazon",
    "Outros Cartões"
]

# --- MEMÓRIA DA APLICAÇÃO (SESSION STATE) ---
if 'lancamentos' not in st.session_state:
    st.session_state.lancamentos = pd.DataFrame([
        {"Data": "2026-08-01", "Descrição": "Supermercado", "Valor (R$)": 350.00, "Tipo": "Saída", "Forma": "Cartão Itaú Black", "Categoria": "Alimentação"},
        {"Data": "2026-08-05", "Descrição": "Combustível", "Valor (R$)": 200.00, "Tipo": "Saída", "Forma": "Pix", "Categoria": "Transporte"},
        {"Data": "2026-08-01", "Descrição": "Adiantamento Quinzenal (1º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal"},
        {"Data": "2026-08-15", "Descrição": "Salário Quinzenal (2º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal"},
    ])

if 'despesas_fixas' not in st.session_state:
    st.session_state.despesas_fixas = pd.DataFrame([
        {"Local": "Apto", "Descrição": "Condomínio Apto", "Valor (R$)": 650.00, "Vencimento": "Dia 10", "Status": "🟢 Pago"},
        {"Local": "Apto", "Descrição": "Energia Apto", "Valor (R$)": 180.00, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},
        {"Local": "Casa", "Descrição": "IPTU Casa", "Valor (R$)": 120.00, "Vencimento": "Dia 20", "Status": "🔴 Em Aberto"},
        {"Local": "Casa", "Descrição": "Internet Casa", "Valor (R$)": 140.00, "Vencimento": "Dia 25", "Status": "🔴 Em Aberto"},
    ])

# --- NAVEGAÇÃO POR ABAS ---
st.sidebar.title("📌 Menu Principal")
aba_selecionada = st.sidebar.radio(
    "Navegue pelo App:",
    [
        "🏠 Centro de Comando", 
        "💵 Total Recebido (Mês)", 
        "🏢 Despesas Fixas (Apto / Casa)", 
        "➕ Lançar Gastos", 
        "📋 Histórico de Lançamentos"
    ]
)

# =========================================================
# ABA 1: CENTRO DE COMANDO (EDITÁVEL DIRETO NA TELA)
# =========================================================
if aba_selecionada == "🏠 Centro de Comando":
    st.title("💼 CENTRAL FINANCEIRA")
    st.caption("Ajuste os valores diretamente nas caixas abaixo:")

    df = st.session_state.lancamentos
    
    total_entradas_calc = df[df['Tipo'] == 'Entrada']['Valor (R$)'].sum()
    total_saidas_calc = df[df['Tipo'] == 'Saída']['Valor (R$)'].sum()

    # Caixas de Edição Direta na Tela Principal
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        receitas_input = st.number_input("Receitas do Mês (R$)", value=float(total_entradas_calc if total_entradas_calc > 0 else 8820.00), step=100.0)
    with c2:
        despesas_input = st.number_input("Despesas do Mês (R$)", value=float(total_saidas_calc if total_saidas_calc > 0 else 5145.60), step=100.0)
    with c3:
        saldo_editavel = st.number_input("Saldo Disponível (R$)", value=float(receitas_input - despesas_input), step=100.0)
    with c4:
        sobra_editavel = st.number_input("Sobra Prevista (R$)", value=float(receitas_input - despesas_input), step=100.0)

    st.markdown("---")

    # Caixas Editáveis de Metas e Reservas
    st.markdown("### 🎯 Metas & Reservas")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        reserva_atual = st.number_input("Reserva Atual (R$)", value=1850.00, step=100.0)
    with col_m2:
        meta_reserva = st.number_input("Meta da Reserva (R$)", value=15000.00, step=500.0)

    st.markdown("---")

    # Gráficos
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("**GASTOS POR FORMA DE PAGAMENTO / CARTÃO**")
        df_saidas = df[df['Tipo'] == 'Saída']
        if not df_saidas.empty:
            df_forma = df_saidas.groupby('Forma')['Valor (R$)'].sum().reset_index()
            fig_forma = go.Figure(data=[go.Pie(labels=df_forma['Forma'], values=df_forma['Valor (R$)'], hole=.5)])
            fig_forma.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_forma, use_container_width=True)
        else:
            st.info("Nenhum gasto registrado ainda.")

    with col_g2:
        st.markdown("**PROGRESSO DA RESERVA DE EMERGÊNCIA**")
        pct_reserva = (reserva_atual / meta_reserva) * 100 if meta_reserva > 0 else 0
        fig_reserva = go.Figure(data=[go.Pie(labels=['Atingido', 'Falta'], values=[reserva_atual, max(0.0, meta_reserva - reserva_atual)], hole=.5, marker_colors=['#d29922', '#21262d'])])
        fig_reserva.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_reserva, use_container_width=True)
        st.caption(f"Meta: R$ {meta_reserva:,.2f} ({pct_reserva:.1f}% concluído)")

# =========================================================
# ABA 2: TOTAL RECEBIDO NO MÊS
# =========================================================
elif aba_selecionada == "💵 Total Recebido (Mês)":
    st.title("💵 Total Recebido do Mês")
    st.caption("Acompanhamento dos Recebimentos Quinzenais")

    df = st.session_state.lancamentos
    df_entradas = df[df['Tipo'] == 'Entrada'].copy()
    total_recebido = df_entradas['Valor (R$)'].sum()

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown(f'<div class="card"><span class="subtext">TOTAL ACUMULADO NO MÊS</span><h2 class="positive">R$ {total_recebido:,.2f}</h2></div>', unsafe_allow_html=True)
    with col_r2:
        st.markdown(f'<div class="card"><span class="subtext">QUANTIDADE DE LANÇAMENTOS</span><h2>{len(df_entradas)} Pagamentos</h2></div>', unsafe_allow_html=True)

    st.markdown("### 📋 Detalhamento dos Recebimentos")
    st.dataframe(df_entradas[["Data", "Descrição", "Valor (R$)", "Forma"]], use_container_width=True)

# =========================================================
# ABA 3: DESPESAS FIXAS (APTO / CASA) - COM STATUS PAGO / EM ABERTO
# =========================================================
elif aba_selecionada == "🏢 Despesas Fixas (Apto / Casa)":
    st.title("🏢 Despesas Fixas (Apto & Casa)")
    st.caption("Controle de vencimentos e status de pagamento das contas recorrentes")

    df_fixas = st.session_state.despesas_fixas

    # Cálculos das Despesas Fixas
    total_fixas = df_fixas['Valor (R$)'].sum()
    total_pagas = df_fixas[df_fixas['Status'] == '🟢 Pago']['Valor (R$)'].sum()
    total_aberto = df_fixas[df_fixas['Status'] == '🔴 Em Aberto']['Valor (R$)'].sum()

    c_f1, c_f2, c_f3 = st.columns(3)
    with c_f1:
        st.markdown(f'<div class="card"><span class="subtext">TOTAL DESPESAS FIXAS</span><h2>R$ {total_fixas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c_f2:
        st.markdown(f'<div class="card"><span class="subtext">TOTAL PAGO</span><h2 class="positive">R$ {total_pagas:,.2f}</h2></div>', unsafe_allow_html=True)
    with c_f3:
        st.markdown(f'<div class="card"><span class="subtext">EM ABERTO (A PAGAR)</span><h2 class="warning">R$ {total_aberto:,.2f}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Gerenciar Status das Contas Fixas")

    # Tabela Editável para alterar o status de "🔴 Em Aberto" para "🟢 Pago"
    df_editado = st.data_editor(
        df_fixas,
        column_config={
            "Local": st.column_config.SelectboxColumn("Local", options=["Apto", "Casa", "Geral"], required=True),
            "Descrição": st.column_config.TextColumn("Descrição", required=True),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", required=True),
            "Vencimento": st.column_config.TextColumn("Vencimento (Dia/Data)", required=True),
            "Status": st.column_config.SelectboxColumn("Status de Pagamento", options=["🔴 Em Aberto", "🟢 Pago"], required=True)
        },
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state.despesas_fixas = df_editado

    st.markdown("---")
    st.markdown("### ➕ Adicionar Nova Despesa Fixa")
    with st.form("form_despesa_fixa", clear_on_submit=True):
        col_df1, col_df2 = st.columns(2)
        with col_df1:
            local_novo = st.selectbox("Local", ["Apto", "Casa", "Geral"])
            desc_nova = st.text_input("Descrição da Conta (Ex: Luz, Água, IPTU)")
            valor_novo = st.number_input("Valor Estimado (R$)", min_value=0.01, step=10.0, format="%.2f")
        with col_df2:
            venc_novo = st.text_input("Dia do Vencimento (Ex: Dia 10)")
            status_novo = st.selectbox("Status Inicial", ["🔴 Em Aberto", "🟢 Pago"])

        btn_add_fixa = st.form_submit_button("➕ Cadastrar Despesa Fixa")
        if btn_add_fixa:
            nova_fixa = {
                "Local": local_novo,
                "Descrição": desc_nova,
                "Valor (R$)": valor_novo,
                "Vencimento": venc_novo,
                "Status": status_novo
            }
            st.session_state.despesas_fixas = pd.concat([st.session_state.despesas_fixas, pd.DataFrame([nova_fixa])], ignore_index=True)
            st.success(f"Despesa fixa '{desc_nova}' adicionada com sucesso!")
            st.rerun()

# =========================================================
# ABA 4: FORMULÁRIO DE LANÇAMENTO DIÁRIO
# =========================================================
elif aba_selecionada == "➕ Lançar Gastos":
    st.title("➕ Registrar Novo Lançamento Diário")
    
    with st.form("form_lancamento", clear_on_submit=True):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            data = st.date_input("Data", datetime.now())
            descricao = st.text_input("Descrição (Ex: Feira, Mercado, Gasolina)")
            valor = st.number_input("Valor (R$)", min_value=0.01, step=5.00, format="%.2f")
        
        with col_f2:
            tipo = st.selectbox("Tipo de Lançamento", ["Saída", "Entrada"])
            
            # Opções de pagamento incluindo todos os cartões e formas de pagamento
            opcoes_pagamento = LISTA_CARTÕES + ["Débito", "Pix", "Dinheiro"]
            forma = st.selectbox("Forma de Pagamento", opcoes_pagamento)
            categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Contas Fixas", "Renda Quinzenal", "Outros"])

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
# ABA 5: HISTÓRICO COMPLETO
# =========================================================
elif aba_selecionada == "📋 Histórico de Lançamentos":
    st.title("📋 Histórico Geral de Lançamentos")
    
    df_exibicao = st.session_state.lancamentos.sort_values(by="Data", ascending=False)
    st.dataframe(df_exibicao, use_container_width=True)

    if st.button("🗑️ Limpar Todos os Lançamentos"):
        st.session_state.lancamentos = pd.DataFrame(columns=["Data", "Descrição", "Valor (R$)", "Tipo", "Forma", "Categoria"])
        st.rerun()
