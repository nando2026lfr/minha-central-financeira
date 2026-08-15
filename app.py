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

# --- DADOS DETALHADOS REAIS (SESSION STATE) ---
if 'lancamentos' not in st.session_state:
    st.session_state.lancamentos = pd.DataFrame([
        # Receitas Quinzenais
        {"Data": "2026-08-01", "Descrição": "Adiantamento Quinzenal (1º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal", "Status": "🟢 Pago"},
        {"Data": "2026-08-15", "Descrição": "Salário Quinzenal (2º Pagamento)", "Valor (R$)": 4410.00, "Tipo": "Entrada", "Forma": "Pix", "Categoria": "Renda Quinzenal", "Status": "🟢 Pago"},
        
        # Faturas dos Cartões de Crédito
        {"Data": "2026-08-10", "Descrição": "Fatura Itaú Black", "Valor (R$)": 850.00, "Tipo": "Saída", "Forma": "Cartão Itaú Black", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Fatura C6 Carbon", "Valor (R$)": 620.00, "Tipo": "Saída", "Forma": "Cartão C6 Carbon", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Fatura Itaú Platinum", "Valor (R$)": 710.00, "Tipo": "Saída", "Forma": "Cartão Itaú Platinum", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Fatura Sam's Club", "Valor (R$)": 450.00, "Tipo": "Saída", "Forma": "Cartão Sam's Club", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Fatura Mercado Pago", "Valor (R$)": 530.00, "Tipo": "Saída", "Forma": "Cartão Mercado Pago", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Fatura Amazon", "Valor (R$)": 380.00, "Tipo": "Saída", "Forma": "Cartão Amazon", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"},
        {"Data": "2026-08-10", "Descrição": "Outros Cartões", "Valor (R$)": 375.75, "Tipo": "Saída", "Forma": "Outros Cartões", "Categoria": "Cartão de Crédito", "Status": "🔴 Em Aberto"}
    ])

if 'despesas_fixas' not in st.session_state:
    st.session_state.despesas_fixas = pd.DataFrame([
        # Apartamento
        {"Local": "Apto", "Descrição": "Condomínio Apto", "Valor (R$)": 429.00, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Apto", "Descrição": "Seguro Apto", "Valor (R$)": 104.77, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Apto", "Descrição": "Internet Apto", "Valor (R$)": 99.90, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},
        {"Local": "Apto", "Descrição": "Energia Apto", "Valor (R$)": 72.00, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},
        {"Local": "Apto", "Descrição": "IPTU Apto", "Valor (R$)": 33.33, "Vencimento": "Dia 20", "Status": "🔴 Em Aberto"},

        # Casa
        {"Local": "Casa", "Descrição": "Internet Casa", "Valor (R$)": 99.90, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Casa", "Descrição": "Energia Casa", "Valor (R$)": 96.00, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},
        {"Local": "Casa", "Descrição": "Água Casa", "Valor (R$)": 90.00, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},

        # Compromissos e Contas Fixas Gerais
        {"Local": "Geral", "Descrição": "Curso de Inglês", "Valor (R$)": 293.40, "Vencimento": "Dia 05", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Seguro Carro", "Valor (R$)": 231.80, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "CREA", "Valor (R$)": 118.00, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Plano Funerário", "Valor (R$)": 92.26, "Vencimento": "Dia 10", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Vivo (Telefonia)", "Valor (R$)": 86.00, "Vencimento": "Dia 15", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Netflix", "Valor (R$)": 59.90, "Vencimento": "Dia 20", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Amazon Prime", "Valor (R$)": 13.90, "Vencimento": "Dia 20", "Status": "🔴 Em Aberto"},

        # Estimativas Mensais de Rotina
        {"Local": "Geral", "Descrição": "Mercado (Estimado)", "Valor (R$)": 1000.00, "Vencimento": "Mensal", "Status": "🔴 Em Aberto"},
        {"Local": "Geral", "Descrição": "Lazer (Estimado)", "Valor (R$)": 300.00, "Vencimento": "Mensal", "Status": "🔴 Em Aberto"}
    ])

# --- HISTÓRICO EXATO DE PARCELAS DETALHADAS ---
if 'parcelados' not in st.session_state:
    st.session_state.parcelados = pd.DataFrame([
        # C6 Carbon
        {"Item / Compra": "Pneus", "Cartão": "Cartão C6 Carbon", "Valor Parcela (R$)": 165.80, "Parcela Atual": 8, "Total Parcelas": 10, "Mês Término": "10/2026"},
        {"Item / Compra": "Despesas CNPJ", "Cartão": "Cartão C6 Carbon", "Valor Parcela (R$)": 825.48, "Parcela Atual": 2, "Total Parcelas": 12, "Mês Término": "06/2027"},

        # Itaú Black
        {"Item / Compra": "Seguro Jeep", "Cartão": "Cartão Itaú Black", "Valor Parcela (R$)": 231.80, "Parcela Atual": 6, "Total Parcelas": 10, "Mês Término": "12/2026"},

        # Mercado Pago
        {"Item / Compra": "Compra MP #1", "Cartão": "Cartão Mercado Pago", "Valor Parcela (R$)": 141.61, "Parcela Atual": 6, "Total Parcelas": 18, "Mês Término": "08/2027"},
        {"Item / Compra": "Compra MP #2", "Cartão": "Cartão Mercado Pago", "Valor Parcela (R$)": 121.37, "Parcela Atual": 13, "Total Parcelas": 18, "Mês Término": "01/2027"},
        {"Item / Compra": "Compra MP #3", "Cartão": "Cartão Mercado Pago", "Valor Parcela (R$)": 85.66, "Parcela Atual": 14, "Total Parcelas": 21, "Mês Término": "03/2027"}
    ])

# --- NAVEGAÇÃO POR ABAS ---
st.sidebar.title("📌 Menu Principal")
aba_selecionada = st.sidebar.radio(
    "Navegue pelo App:",
    [
        "🏠 Centro de Comando", 
        "💵 Total Recebido (Mês)", 
        "🏢 Despesas Fixas (Apto / Casa)", 
        "💳 Compras Parceladas",
        "➕ Lançar Gastos", 
        "📋 Histórico de Lançamentos"
    ]
)

# =========================================================
# ABA 1: CENTRO DE COMANDO
# =========================================================
if aba_selecionada == "🏠 Centro de Comando":
    st.title("💼 CENTRAL FINANCEIRA")
    st.caption("Ajuste os valores diretamente nas caixas abaixo:")

    df = st.session_state.lancamentos
    df_fixas = st.session_state.despesas_fixas
    
    total_entradas_calc = df[df['Tipo'] == 'Entrada']['Valor (R$)'].sum()
    total_saidas_calc = df[df['Tipo'] == 'Saída']['Valor (R$)'].sum() + df_fixas['Valor (R$)'].sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        receitas_input = st.number_input("Receitas do Mês (R$)", value=float(total_entradas_calc), step=100.0)
    with c2:
        despesas_input = st.number_input("Despesas do Mês (R$)", value=float(total_saidas_calc), step=100.0)
    with c3:
        saldo_editavel = st.number_input("Saldo Disponível (R$)", value=float(receitas_input - despesas_input), step=100.0)
    with c4:
        sobra_editavel = st.number_input("Sobra Prevista (R$)", value=float(receitas_input - despesas_input), step=100.0)

    st.markdown("---")

    st.markdown("### 🎯 Metas & Reservas")
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        reserva_atual = st.number_input("Reserva Atual (R$)", value=5000.00, step=100.0)
    with col_m2:
        meta_reserva = st.number_input("Meta da Reserva (R$)", value=15000.00, step=500.0)

    st.markdown("---")

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
    st.caption("Acompanhamento dos Recebimentos Quinzenais (2x de R$ 4.410,00)")

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
# ABA 3: DESPESAS FIXAS (APTO / CASA / GERAL)
# =========================================================
elif aba_selecionada == "🏢 Despesas Fixas (Apto / Casa)":
    st.title("🏢 Despesas Fixas (Apto, Casa & Geral)")
    st.caption("Controle individualizado de vencimentos e status de pagamento das contas recorrentes")

    df_fixas = st.session_state.despesas_fixas

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
            desc_nova = st.text_input("Descrição da Conta")
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
# ABA 4: COMPRAS PARCELADAS DOS CARTÕES DETALHADAS
# =========================================================
elif aba_selecionada == "💳 Compras Parceladas":
    st.title("💳 Acompanhamento de Parcelados por Cartão")
    st.caption("Visão individualizada de cada compra parcelada, com cálculo de término e valor restante")

    df_p = st.session_state.parcelados

    # Cálculos dinâmicos
    if not df_p.empty:
        df_p["Faltam (Parcelas)"] = df_p["Total Parcelas"] - df_p["Parcela Atual"]
        df_p["Saldo Restante (R$)"] = df_p["Faltam (Parcelas)"] * df_p["Valor Parcela (R$)"]
        total_comprometido = df_p["Saldo Restante (R$)"].sum()
        total_parcela_mes = df_p["Valor Parcela (R$)"].sum()
    else:
        total_comprometido = 0.0
        total_parcela_mes = 0.0

    cp1, cp2 = st.columns(2)
    with cp1:
        st.markdown(f'<div class="card"><span class="subtext">TOTAL MENSAL EM PARCELAS</span><h2>R$ {total_parcela_mes:,.2f}</h2></div>', unsafe_allow_html=True)
    with cp2:
        st.markdown(f'<div class="card"><span class="subtext">SALDO DEVEDOR TOTAL A QUITAR</span><h2 class="warning">R$ {total_comprometido:,.2f}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📋 Tabela de Compras Parceladas")

    df_p_editado = st.data_editor(
        df_p,
        column_config={
            "Item / Compra": st.column_config.TextColumn("Item / Compra", required=True),
            "Cartão": st.column_config.SelectboxColumn("Cartão", options=LISTA_CARTÕES, required=True),
            "Valor Parcela (R$)": st.column_config.NumberColumn("Valor Parcela (R$)", format="R$ %.2f", required=True),
            "Parcela Atual": st.column_config.NumberColumn("Parcela Atual", min_value=1, required=True),
            "Total Parcelas": st.column_config.NumberColumn("Total Parcelas", min_value=1, required=True),
            "Mês Término": st.column_config.TextColumn("Mês/Ano Término", required=True),
            "Faltam (Parcelas)": st.column_config.NumberColumn("Faltam", disabled=True),
            "Saldo Restante (R$)": st.column_config.NumberColumn("Saldo Restante", format="R$ %.2f", disabled=True)
        },
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state.parcelados = df_p_editado

    st.markdown("---")
    st.markdown("### ➕ Cadastrar Nova Compra Parcelada")
    with st.form("form_parcelado", clear_on_submit=True):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            item_p = st.text_input("Descrição do Item (Ex: Celular, Pneu, Ferramenta)")
            cartao_p = st.selectbox("Cartão Utilizado", LISTA_CARTÕES)
            valor_p = st.number_input("Valor da Parcela (R$)", min_value=0.01, step=10.0, format="%.2f")
        with col_p2:
            atual_p = st.number_input("Parcela Atual", min_value=1, value=1, step=1)
            total_p = st.number_input("Total de Parcelas", min_value=1, value=12, step=1)
            termino_p = st.text_input("Mês/Ano Término (Ex: 12/2026)")

        btn_add_p = st.form_submit_button("➕ Salvar Parcelamento")
        if btn_add_p:
            novo_p = {
                "Item / Compra": item_p,
                "Cartão": cartao_p,
                "Valor Parcela (R$)": valor_p,
                "Parcela Atual": atual_p,
                "Total Parcelas": total_p,
                "Mês Término": termino_p
            }
            st.session_state.parcelados = pd.concat([st.session_state.parcelados, pd.DataFrame([novo_p])], ignore_index=True)
            st.success(f"Parcelamento '{item_p}' salvo com sucesso!")
            st.rerun()

# =========================================================
# ABA 5: FORMULÁRIO DE LANÇAMENTO DIÁRIO
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
            opcoes_pagamento = LISTA_CARTÕES + ["Débito", "Pix", "Dinheiro"]
            forma = st.selectbox("Forma de Pagamento", opcoes_pagamento)
            categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Moradia", "Lazer", "Contas Fixas", "Renda Quinzenal", "Cartão de Crédito", "Outros"])
            status_lanc = st.selectbox("Status", ["🔴 Em Aberto", "🟢 Pago"])

        btn_salvar = st.form_submit_button("💾 Salvar Registro")

        if btn_salvar:
            novo_item = {
                "Data": str(data),
                "Descrição": descricao,
                "Valor (R$)": valor,
                "Tipo": tipo,
                "Forma": forma,
                "Categoria": categoria,
                "Status": status_lanc
            }
            st.session_state.lancamentos = pd.concat([st.session_state.lancamentos, pd.DataFrame([novo_item])], ignore_index=True)
            st.success(f"Lançamento '{descricao}' de R$ {valor:.2f} registrado com sucesso!")

# =========================================================
# ABA 6: HISTÓRICO COMPLETO
# =========================================================
elif aba_selecionada == "📋 Histórico de Lançamentos":
    st.title("📋 Histórico Geral de Lançamentos & Cartões")
    st.caption("Altere o status das faturas dos cartões de 🔴 Em Aberto para 🟢 Pago diretamente na tabela abaixo:")

    df_hist = st.session_state.lancamentos.sort_values(by="Data", ascending=False)
    
    df_hist_editado = st.data_editor(
        df_hist,
        column_config={
            "Data": st.column_config.TextColumn("Data", required=True),
            "Descrição": st.column_config.TextColumn("Descrição", required=True),
            "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f", required=True),
            "Tipo": st.column_config.SelectboxColumn("Tipo", options=["Entrada", "Saída"], required=True),
            "Forma": st.column_config.SelectboxColumn("Forma de Pagamento / Cartão", options=LISTA_CARTÕES + ["Débito", "Pix", "Dinheiro"], required=True),
            "Categoria": st.column_config.TextColumn("Categoria"),
            "Status": st.column_config.SelectboxColumn("Status", options=["🔴 Em Aberto", "🟢 Pago"], required=True)
        },
        num_rows="dynamic",
        use_container_width=True
    )

    st.session_state.lancamentos = df_hist_editado

    if st.button("🗑️ Limpar Todos os Lançamentos"):
        st.session_state.lancamentos = pd.DataFrame(columns=["Data", "Descrição", "Valor (R$)", "Tipo", "Forma", "Categoria", "Status"])
        st.rerun()
