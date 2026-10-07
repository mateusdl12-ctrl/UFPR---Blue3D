import streamlit as st
import os
import importlib.util
from models.pedido_venda import adicionar_pedido_venda
import urllib.parse
import datetime
import os as _os
import socket
import time
from streamlit_extras.stylable_container import stylable_container
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
import tempfile
import requests

# Google Sheets integração
try:
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
except ImportError:
    gspread = None
    ServiceAccountCredentials = None

def enviar_pedido_google_sheets(dados):
    if not gspread or not ServiceAccountCredentials:
        return False, "Bibliotecas gspread/oauth2client não disponíveis."
    try:
        nome_planilha = "Pedidos_Blus3D"
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds_dict = None
        try:
            if "gcp_service_account" in st.secrets:
                creds_dict = dict(st.secrets["gcp_service_account"])
        except Exception:
            pass
        if not creds_dict and _os.path.exists("clayto3d-3063b97a968d.json"):
            import json
            with open("clayto3d-3063b97a968d.json", "r") as f:
                creds_dict = json.load(f)

        if not creds_dict:
            return False, "Credenciais do Google Sheets não encontradas."

        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open(nome_planilha).sheet1
        sheet.append_row(dados)
        return True, None
    except Exception as e:
        return False, str(e)


# Detecta ambiente público automaticamente
def is_public_env():
    host = socket.gethostname().lower()
    if "streamlit" in host or "cloud" in host:
        return True
    if os.environ.get("BLUS3D_PUBLIC", "0") == "1":
        return True
    return False

IS_PUBLIC = True # Mantido como estava no seu código

# Função para decidir se usa lista fixa ou banco
def listar_filamentos():
    filamentos_publicos_path = _os.path.join(_os.path.dirname(__file__), "filamentos_publicos.py")
    if _os.path.exists(filamentos_publicos_path):
        spec = importlib.util.spec_from_file_location("filamentos_publicos", filamentos_publicos_path)
        filamentos_publicos = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(filamentos_publicos)
        return getattr(filamentos_publicos, "FILAMENTOS_PUBLICOS", [])
    else:
        from models.filamento import listar_filamentos as lf
        return lf()

# Função para upload no Google Drive

def upload_to_drive(file_buffer, filename, folder_id, creds_dict):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file_buffer.getbuffer())
        temp_path = tmp.name
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(temp_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file_id = file.get('id')
    service.permissions().create(fileId=file_id, body={'role': 'reader', 'type': 'anyone'}).execute()
    link = f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"
    return link

def pagina_calculadora_cliente():
    st.title("Simule seu Orçamento 3D")
    st.write("Preencha os dados abaixo para estimar o valor da sua impressão 3D.")
    st.info("O valor apresentado é uma estimativa. O valor final pode variar após análise do projeto.")

    # Botão estilizado para MakerWorld
    st.markdown('''
        <div style='text-align:center; margin: 2rem 0;'>
            <a href="https://makerworld.com/pt" target="_blank" style="background: linear-gradient(90deg, #0088ff 0%, #00d4ff 100%); color: white; border: none; border-radius: 8px; padding: 1rem 2.5rem; font-size: 1.3rem; font-weight: bold; box-shadow: 0 0 16px #0088ff88; text-decoration: none; display: inline-block;">
                <img src="https://makerworld.com/favicon.ico" width="32" style="vertical-align:middle; margin-right:0.7rem;"> Explorar modelos 3D em MakerWorld
            </a>
        </div>
    ''', unsafe_allow_html=True)

    # (Removido campo de input e prévia de imagem do modelo MakerWorld)

    if 'orcamento' not in st.session_state:
        st.session_state.orcamento = None
    if 'whatsapp_link' not in st.session_state:
        st.session_state.whatsapp_link = None
    if 'orcamento_registrado' not in st.session_state:
        st.session_state.orcamento_registrado = False
    if 'filamentos_lista' not in st.session_state:
        st.session_state.filamentos_lista = []
    if 'orcamento_enviado' not in st.session_state:
        st.session_state.orcamento_enviado = False

    # Nome e WhatsApp lado a lado (Campos Obrigatórios)
    col1, col2 = st.columns([1, 1])
    with col1:
        nome_cliente = st.text_input("Seu nome*", placeholder="Nome completo")
    with col2:
        telefone_cliente = st.text_input("Seu WhatsApp (Número)*", placeholder="(apenas números)")

    # Tutorial para obter tempo de impressão e peso no MakerWorld (com imagem)
    with st.expander("💡 Como obter Tempo de Impressão e Peso no MakerWorld?"):
        st.markdown("""
        Para ter uma estimativa precisa, você precisa informar o **Tempo de Impressão** e o **Peso Total** da peça.
        Essas informações estão disponíveis na página de cada modelo no site [MakerWorld](https://makerworld.com/pt), conforme imagem abaixo.
        """)
        tuto_img_path = None
        for cand in ["TUTO2.png", "tuto.png", _os.path.join(_os.path.dirname(__file__), "..", "TUTO2.png"), _os.path.join(_os.path.dirname(__file__), "..", "tuto.png")]:
            if _os.path.exists(cand):
                tuto_img_path = cand
                break
        if tuto_img_path:
            st.image(tuto_img_path, caption="Clique no perfil de impressão para ver os detalhes")
        

    # Nome da peça, tempo de impressão, peso total e link lado a lado
    col3, col4, col5, col6 = st.columns([1, 0.7, 0.7, 2])
    with col3:
        nome_peca = st.text_input("Nome da Peça (opcional)", placeholder="Ex: Suporte de celular")
    with col4:
        tempo_impressao = st.number_input("Tempo (h)*", min_value=0.0, step=0.1)
    with col5:
        peso_total = st.number_input("Peso total (g)*", min_value=0.0, step=1.0)
    with col6:
        link_extra = st.text_input(
            "Link do arquivo de impressão (opcional)",
            placeholder="https://makerworld.com"
        )
    
    # Campo para observação
    observacao_cor = st.text_input("Cor desejada (se a peça for de uma cor só)", placeholder="Ex: Preto, Branco, Vermelho translúcido")

    # Garante que anexos_info sempre existe
    anexos_info = []
    if link_extra:
        anexos_info.append(f"Link: {link_extra}")

    # Botão Calcular Orçamento
    calcular = st.button("Calcular orçamento")

    if calcular:
        if not nome_cliente or not nome_cliente.strip():
            st.warning("Por favor, preencha o seu Nome para prosseguir.")
        elif not telefone_cliente or not telefone_cliente.strip():
            st.warning("Por favor, preencha o seu WhatsApp (Número) para prosseguir.")
        elif not tempo_impressao or tempo_impressao <= 0:
            st.warning("Por favor, preencha o Tempo de Impressão da peça (maior que zero).")
        elif not peso_total or peso_total <= 0:
            st.warning("Por favor, preencha o Peso Total da peça (maior que zero).")
        else:
            custo_hora = 2.0
            margem = 1.5
            preco_kg = 100.0  # Preço fixo do filamento
            preco_custo_filamentos = preco_kg * (peso_total / 1000)
            preco_custo = custo_hora * tempo_impressao + preco_custo_filamentos
            preco_venda = preco_custo * margem

            st.session_state.orcamento = {
                'nome_cliente': nome_cliente,
                'telefone_cliente': telefone_cliente,
                'nome_peca': nome_peca,
                'tempo_impressao': tempo_impressao,
                'peso_total': peso_total,
                'preco_venda': preco_venda,
                'custo_hora': custo_hora,
                'margem': margem,
                'anexos': anexos_info,
                'observacao_cor': observacao_cor
            }
            st.session_state.whatsapp_link_gerado = None
            st.session_state.orcamento_registrado = False

    if st.session_state.orcamento:
        preco_venda = st.session_state.orcamento['preco_venda']
        valor_formatado = f"{preco_venda:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        st.markdown(f"""
    <div style='background: #23243a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 0 16px #7c3aed44;'>
        <h3 style='text-align:center; margin-bottom:1.2rem;'>Resumo do Orçamento</h3>
        <table style='width:100%; font-size:1.1rem; color:#fff;'>
            <tr><td><b>Nome:</b></td><td>{st.session_state.orcamento['nome_cliente']}</td></tr>
            <tr><td><b>WhatsApp:</b></td><td>{st.session_state.orcamento['telefone_cliente']}</td></tr>
            <tr><td><b>Peça:</b></td><td>{st.session_state.orcamento.get('nome_peca', '-')}</td></tr>
            <tr><td><b>Tempo de Impressão:</b></td><td>{st.session_state.orcamento.get('tempo_impressao', '-')} horas</td></tr>
            <tr><td><b>Peso Total:</b></td><td>{st.session_state.orcamento.get('peso_total', '-')}g</td></tr>
            <tr><td><b>Cor Desejada:</b></td><td>{st.session_state.orcamento.get('observacao_cor', '-') or '-'}</td></tr> <tr><td><b>Valor estimado:</b></td><td style='font-size:1.3rem; color:#ff4ecd;'><b>R$ {valor_formatado}</b></td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
        st.caption("Este valor é uma estimativa. O valor final pode variar após análise do projeto.")

        # Gere o link do WhatsApp para +55 41 9570-2837
        numero_whatsapp = "554195702837"
        mensagem = f"""Olá! Gostaria de solicitar um orçamento para impressão 3D:\n\nNome: {st.session_state.orcamento['nome_cliente']}\nWhatsApp: {st.session_state.orcamento['telefone_cliente']}\nPeça: {st.session_state.orcamento['nome_peca'] or '-'}\nTempo de impressão: {st.session_state.orcamento['tempo_impressao']} horas\nPeso total: {st.session_state.orcamento['peso_total']}g\n"""
        if st.session_state.orcamento.get('observacao_cor'):
            mensagem += f"Cor Desejada: {st.session_state.orcamento['observacao_cor']}\n"
        mensagem += f"Valor estimado: R$ {valor_formatado}"
        if st.session_state.orcamento['anexos']:
            mensagem += "\nAnexos: " + "; ".join(st.session_state.orcamento['anexos'])
        mensagem += "\n\nAguardo retorno!"
        mensagem_url = urllib.parse.quote(mensagem)
        st.session_state.whatsapp_link = f"https://wa.me/{numero_whatsapp}?text={mensagem_url}"

        if st.session_state.orcamento:
            if not st.session_state.orcamento_enviado:
                if st.button("Registrar orçamento na fila", key="btn_solicitar_orcamento_whatsapp"):
                    with st.spinner("Registrando orçamento..."):
                        # 1. Salva no banco de dados local (impressao3d.db)
                        try:
                            observacao_db = f"Nome: {st.session_state.orcamento['nome_cliente']} | WhatsApp: {st.session_state.orcamento['telefone_cliente']}"
                            if st.session_state.orcamento.get('observacao_cor'):
                                observacao_db += f" | Cor: {st.session_state.orcamento['observacao_cor']}"
                            if st.session_state.orcamento['anexos']:
                                observacao_db += " | " + "; ".join(st.session_state.orcamento['anexos'])

                            adicionar_pedido_venda(
                                id_cliente=None,
                                nome_peca=st.session_state.orcamento['nome_peca'] or '-',
                                tempo_impressao_horas=st.session_state.orcamento['tempo_impressao'],
                                custo_impressao_hora=st.session_state.orcamento['custo_hora'],
                                filamentos_utilizados=[],
                                preco_arquivo=0.0,
                                margem_lucro_percentual=st.session_state.orcamento['margem'],
                                data_venda=str(datetime.date.today()),
                                status="Orçamento Solicitado",
                                observacao=observacao_db
                            )
                        except Exception as e_db:
                            print(f"Aviso ao registrar no banco local: {e_db}")

                        # 2. Tenta enviar para o Google Sheets se disponível
                        try:
                            dados = [
                                str(datetime.date.today()),
                                "Orçamento Solicitado",
                                st.session_state.orcamento['nome_peca'] or '-',
                                st.session_state.orcamento['tempo_impressao'],
                                f"R$ {valor_formatado}",
                                st.session_state.orcamento['nome_cliente'],
                                st.session_state.orcamento['telefone_cliente'],
                                next((a.replace('Link: ', '') for a in st.session_state.orcamento['anexos'] if a.startswith('Link:')), ''),
                                st.session_state.orcamento.get('observacao_cor', '')
                            ]
                            enviar_pedido_google_sheets(dados)
                        except Exception as e_sheets:
                            pass

                        # Finaliza e libera o botão do WhatsApp
                        st.session_state.orcamento_enviado = True
                        st.session_state.orcamento_registrado = True
                        st.success("Orçamento registrado na fila com sucesso! Agora clique abaixo para enviar pelo WhatsApp.")

            if st.session_state.orcamento_enviado and st.session_state.whatsapp_link:
                st.markdown(f'''
    <div style="display: flex; justify-content: center; margin: 1.5rem 0;">
        <a href="{st.session_state.whatsapp_link}" target="_blank" style="text-decoration: none;">
            <button style="
                background: linear-gradient(90deg, #ff4ecd 0%, #7c3aed 100%);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 1rem 2.5rem;
                font-size: 1.3rem;
                font-weight: bold;
                box-shadow: 0 0 16px #ff4ecd88;
                cursor:pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.7rem;
                width: fit-content;
                ">
                <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" width="32" style="vertical-align:middle;"> Enviar pelo WhatsApp
            </button>
        </a>
    </div>
''', unsafe_allow_html=True)

    # Limpa orçamento se qualquer campo relevante mudar
    if (
        st.session_state.get('orcamento') and (
            st.session_state.orcamento.get('nome_cliente') != nome_cliente or
            st.session_state.orcamento.get('telefone_cliente') != telefone_cliente or
            st.session_state.orcamento.get('nome_peca') != nome_peca or
            st.session_state.orcamento.get('tempo_impressao') != tempo_impressao or
            st.session_state.orcamento.get('peso_total') != peso_total or
            st.session_state.orcamento.get('anexos') != anexos_info or
            st.session_state.orcamento.get('observacao_cor') != observacao_cor
        )
    ):
        st.session_state.orcamento = None
        st.session_state.orcamento_enviado = False
