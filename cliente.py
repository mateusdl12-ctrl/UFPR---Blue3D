import streamlit as st
from ui.calculadora_cliente import pagina_calculadora_cliente

st.set_page_config(
    page_title="Orçamento Blus3D",
    page_icon="logo.png",
    layout="wide"
)

# Neon nos títulos
st.markdown('''
    <style>
    .stApp h1, .stApp h2, .stApp h3 {
        background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 8px #0088ff88;
    }
    </style>
''', unsafe_allow_html=True)

# Logo na lateral (sidebar)
with st.sidebar:
    st.image("logo.png", use_container_width=True)

# Título centralizado
st.markdown("<h1 style='text-align:center; margin-top:0;'>Orçamento Blus3D</h1>", unsafe_allow_html=True)

pagina_calculadora_cliente()