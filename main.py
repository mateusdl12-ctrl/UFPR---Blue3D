import streamlit as st
import os
from database import init_db
from ui.clientes import pagina_clientes
from ui.filamentos import pagina_filamentos
from ui.pedidos_compra import pagina_pedidos_compra
from ui.estoque import pagina_estoque
from ui.pedidos_venda import pagina_pedidos_venda
from ui.calculadora import pagina_calculadora
from ui.calculadora_cliente import pagina_calculadora_cliente
from ui.relatorios import pagina_relatorios

st.set_page_config(
    page_title="Blus3D - Painel Administrativo",
    page_icon="🔐",
    layout="wide"
)

init_db()

# Senha configurada
SENHA_ADMIN = st.secrets.get("ADMIN_PASSWORD", "25021510") if hasattr(st, "secrets") else "25021510"

# Controle de sessão
if "admin_autenticado" not in st.session_state:
    st.session_state.admin_autenticado = False

# Estilos CSS
st.markdown("""<style>
/* Sidebar fundo preto */
[data-testid="stSidebar"] > div:first-child {
    background: #181c23 !important;
    color: white !important;
}
/* Logo centralizada e redonda */
[data-testid="stSidebar"] img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 80%;
    max-width: 180px;
    border-radius: 16px;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
    box-shadow: 0 0 24px #0088ff88;
}
/* Nome da empresa estilizado */
.blus3d-title {
    text-align: center;
    font-size: 2rem;
    font-weight: bold;
    background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1.5rem;
    margin-top: 0.2rem;
    letter-spacing: 2px;
    text-shadow: 0 0 8px #0088ff88;
}
/* Neon effect for headers */
.stApp h1, .stApp h2, .stApp h3 {
    background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 8px #0088ff88;
}
/* Neon effect for buttons */
.stButton > button {
    background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 0 8px #0088ff88;
    font-weight: bold;
}
</style>""", unsafe_allow_html=True)

# Tela de Login (se não autenticado)
if not st.session_state.admin_autenticado:
    # Esconde a barra lateral na tela de login
    st.markdown("""<style>
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {
        display: none !important;
    }
    </style>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.write("")
        st.write("")
        if os.path.exists("Logo.png"):
            st.image("Logo.png", width=180)
        elif os.path.exists("logo.png"):
            st.image("logo.png", width=180)
        
        st.markdown("<h2 style='text-align: center; margin-top: 1rem;'>Painel Administrativo</h2>", unsafe_allow_html=True)
        st.write("<p style='text-align: center; color: #8892b0;'>Acesso restrito Blus3D. Digite sua senha numérica para continuar.</p>", unsafe_allow_html=True)
        
        with st.form("form_login_admin"):
            senha_digitada = st.text_input("Senha de Administrador", type="password", placeholder="Digite a senha")
            btn_entrar = st.form_submit_button("Entrar no Painel", use_container_width=True)

            if btn_entrar:
                if str(senha_digitada).strip() == str(SENHA_ADMIN):
                    st.session_state.admin_autenticado = True
                    st.success("Acesso liberado com sucesso!")
                    st.rerun()
                else:
                    st.error("Senha incorreta. Tente novamente.")
    st.stop()

# Área Administrativa (Usuário Autenticado)
with st.sidebar:
    if os.path.exists("Logo.png"):
        st.image("Logo.png")
    elif os.path.exists("logo.png"):
        st.image("logo.png")
    
    st.markdown("<div style='text-align: center; color: #00d4ff; font-weight: bold; margin-bottom: 1rem;'>🔒 ADM Conectado</div>", unsafe_allow_html=True)
    
    pagina = st.radio("Menu", [
        "Dashboard",
        "Clientes",
        "Filamentos",
        "Pedidos de Compra",
        "Estoque",
        "Pedidos de Venda",
        "Calculadora de Orçamento (Admin)",
        "Calculadora de Orçamento (Cliente)",
        "Relatórios"
    ])
    
    st.write("---")
    if st.button("🚪 Sair do ADM", use_container_width=True):
        st.session_state.admin_autenticado = False
        st.rerun()

if pagina == "Dashboard":
    st.title("Bem-vindo à Blus3D!")
    st.write("Selecione uma opção no menu ao lado para começar.")
elif pagina == "Clientes":
    pagina_clientes()
elif pagina == "Filamentos":
    pagina_filamentos()
elif pagina == "Pedidos de Compra":
    pagina_pedidos_compra()
elif pagina == "Estoque":
    pagina_estoque()
elif pagina == "Pedidos de Venda":
    pagina_pedidos_venda()
elif pagina == "Calculadora de Orçamento (Admin)":
    pagina_calculadora()
elif pagina == "Calculadora de Orçamento (Cliente)":
    pagina_calculadora_cliente()
elif pagina == "Relatórios":
    pagina_relatorios()