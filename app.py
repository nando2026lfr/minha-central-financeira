import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Configuração da página para Celular/Desktop
st.set_page_config(page_title="Central Financeira", layout="wide", initial_sidebar_state="collapsed")

# Estilo visual escuro (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #f0f6fc; }
    .card { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 10px; }
    .subtext { color: #8b949e; font-size: 12px; }
    .positive { color: #2ea043; font-weight: bold; }
    .negative { color: #f85149; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("💼 CENTRAL FINANCEIRA")
st.caption("Agosto / 2026 — Controle & Saúde Financeira")

# --- BARRA LATERAL / CAMPOS EDITÁVEIS ---
st.sidebar.header("⚙️ Painel de Edição")
st.sidebar.markdown("Altere os dados para atualizar o dashboard:")

receita_total = st.sidebar.number_input("Receita do Mês (R$)", value=8820.00, step=100.0)
despesa_total = st.sidebar.number_input("Despesas do Mês (R$)", value=5145.60, step=100.0)
reserva_atual = st.sidebar.number_input("Reserva Atual (R$)", value=1850.00, step=100.0)
meta_reserva = st.sidebar.number_input("Meta da Reserva (R$)", value=15000.00, step=500.0)

saldo_disponivel = receita_total - despesa_total
sobra_prevista = receita_total - despesa_total

# --- 1. CARDS DE DESTAQUE ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="card">
            <span class="subtext">SALDO DISPONÍVEL</span>
            <h2 class="positive">R$ {saldo_disponivel:,.2f}</h2>
            <span class="subtext">Disponível para uso</span>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="card">
            <span class="subtext">RECEITAS DO MÊS</span>
            <h2>R$ {receita_total:,.2f}</h2>
            <span class="subtext">Recebido: R$ {receita_total*0.5:,.2f} (50%)</span>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="card">
            <span class="subtext">DESPESAS DO MÊS</span>
            <h2 class="negative">R$ {despesa_total:,.2f}</h2>
            <span class="subtext">Previsto: R$ {receita_total:,.2f} (58%)</span>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="card">
            <span class="subtext">SOBRA PREVISTA</span>
            <h2 style="color: #a371f7;">R$ {sobra_prevista:,.2f}</h2>
            <span class="subtext">Para investir ou amortizar</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- 2. GRÁFICOS DE ROSCA (CARTÕES E PATRIMÔNIO) ---
col_g1, col_g2, col_g3 = st.columns(3)

with col_g1:
    st.markdown("**UTILIZAÇÃO DOS CARTÕES**")
    fig1 = go.Figure(data=[go.Pie(
        labels=['Utilizado', 'Disponível'], 
        values=[5527.27, 40824.96], 
        hole=.6,
        marker_colors=['#1f6beb', '#21262d']
    )])
    fig1.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with col_g2:
    st.markdown("**DISTRIBUIÇÃO PATRIMONIAL**")
    fig2 = go.Figure(data=[go.Pie(
        labels=['Apartamento', 'Veículo', 'FGTS'], 
        values=[300000, 84000, 49500], 
        hole=.6,
        marker_colors=['#1f6beb', '#2ea043', '#d29922']
    )])
    fig2.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

with col_g3:
    st.markdown("**RESERVA DE EMERGÊNCIA**")
    pct_reserva = (reserva_atual / meta_reserva) * 100
    fig3 = go.Figure(data=[go.Pie(
        labels=['Atingido', 'Falta'], 
        values=[reserva_atual, meta_reserva - reserva_atual], 
        hole=.6,
        marker_colors=['#d29922', '#21262d']
    )])
    fig3.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig3, use_container_width=True)
    st.caption(f"Meta: R$ {meta_reserva:,.2f} ({pct_reserva:.1f}% concluído)")

st.markdown("---")

# --- 3. EVOLUÇÃO E RECOMENDAÇÕES ---
col_e1, col_e2 = st.columns([2, 1])

with col_e1:
    st.markdown("**EVOLUÇÃO DOS ÚLTIMOS 6 MESES**")
    meses = ['Mar/26', 'Abr/26', 'Mai/26', 'Jun/26', 'Jul/26', 'Ago/26']
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=meses, y=[375000, 390000, 410000, 420000, 428000, 433500], name='Patrimônio', line=dict(color='#2ea043', width=3)))
    fig_line.add_trace(go.Scatter(x=meses, y=[280000, 250000, 220000, 190000, 160000, 140000], name='Dívidas', line=dict(color='#f85149', width=3)))
    fig_line.update_layout(margin=dict(t=10, b=10, l=10, r=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h"))
    st.plotly_chart(fig_line, use_container_width=True)

with col_e2:
    st.markdown("**ASSISTENTE FINANCEIRO**")
    st.info("✅ Cheque especial zerado.")
    st.warning("⚠️ Priorize aportes na reserva de emergência.")
    st.success("💡 Dica: Amortizar R$ 500/mês no empréstimo Itaú economiza juros significativos.")
