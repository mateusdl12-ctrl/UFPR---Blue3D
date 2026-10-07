import streamlit as st
from database import init_db
from ui.clientes import pagina_clientes
from ui.filamentos import pagina_filamentos
from ui.pedidos_compra import pagina_pedidos_compra
from ui.estoque import pagina_estoque
from ui.pedidos_venda import pagina_pedidos_venda
from ui.calculadora import pagina_calculadora
from ui.calculadora_cliente import pagina_calculadora_cliente
from ui.relatorios import pagina_relatorios

init_db()

# CSS customizado para tema azul, mas sidebar com fundo preto igual ao fundo principal
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
}
</style>""", unsafe_allow_html=True)

with st.sidebar:
    st.image("logo.png", use_container_width=True)
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