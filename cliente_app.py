import streamlit as st
import os
from database import init_db
from ui.calculadora_cliente import pagina_calculadora_cliente

st.set_page_config(
    page_title="Blus3D - Orçamento de Impressão 3D",
    page_icon="🖨️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inicializa banco de dados
init_db()

# Estilos da página do cliente (sem sidebar e com tema Blus3D)
st.markdown("""<style>
/* Ocultar barra lateral completamente e botoes de controle */
[data-testid="stSidebar"], [data-testid="collapsedControl"] {
    display: none !important;
}

/* Centralizar e limitar largura para leitura confortavel */
.block-container {
    max-width: 950px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Logo centralizada */
[data-testid="stImage"] img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    max-width: 180px;
    border-radius: 16px;
    box-shadow: 0 0 24px #0088ff88;
    margin-bottom: 1.5rem;
}

/* Efeito neon para titulos */
.stApp h1, .stApp h2, .stApp h3 {
    background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 8px #0088ff88;
}

/* Botoes estilizados */
.stButton > button {
    background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%) !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 0 8px #0088ff88;
    font-weight: bold;
}
</style>""", unsafe_allow_html=True)

# Logo da Blus3D no topo
col_l, col_center, col_r = st.columns([1, 1, 1])
with col_center:
    if os.path.exists("Logo.png"):
        st.image("Logo.png", use_container_width=True)
    elif os.path.exists("logo.png"):
        st.image("logo.png", use_container_width=True)

# Exibe exclusivamente a calculadora do cliente
pagina_calculadora_cliente()
