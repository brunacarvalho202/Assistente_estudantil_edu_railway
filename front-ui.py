import streamlit as st
import requests
import os
from urllib.parse import urljoin

# Detectar se está em produção (Railway) ou local
ENV = os.environ.get("ENV", "local")

if ENV == "production":
    # Em produção (Railway), a API está no mesmo host mas porta 8000
    # Railway fornece acesso interno entre serviços
    API_BASE_URL = "http://localhost:8000"
else:
    # Em desenvolvimento local
    API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000")

API_URL = urljoin(API_BASE_URL, "/chat/")

st.set_page_config(
    page_title="Chat LLM",
    page_icon="💬",
    layout="wide",
)

st.title("💬 Seu chatbot Edu Assistant")

# Informação sobre o ambiente
col1, col2 = st.columns(2)
with col1:
    st.info(f"🌍 Ambiente: {ENV.upper()}")
with col2:
    st.info(f"🔗 API: {API_BASE_URL}")

# Input do usuário
st.markdown("---")
user_input = st.text_area(
    "Digite sua mensagem aqui:",
    height=100,
    placeholder="Escreva aqui e clique em 'Enviar'..."
)

col1, col2, col3 = st.columns(3)

with col1:
    send_button = st.button("🚀 Enviar", use_container_width=True)

with col2:
    clear_button = st.button("🗑️ Limpar", use_container_width=True)

with col3:
    st.empty()

if clear_button:
    st.session_state.messages = []
    st.rerun()

if send_button:
    if user_input.strip():
        with st.spinner("⏳ Gerando resposta..."):
            try:
                response = requests.post(
                    API_URL,
                    json={"message": user_input},
                    timeout=30
                )

                if response.status_code == 200:
                    response_data = response.json()
                    st.success("✅ Resposta recebida!")
                    st.markdown("---")
                    st.markdown(f"**Sua pergunta:** {user_input}")
                    st.markdown(f"**Resposta:** {response_data['response']}")
                else:
                    st.error(f"❌ Erro ao chamar a API (status: {response.status_code})")
                    st.error(f"Detalhes: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(
                    "❌ Não conseguiu conectar à API. "
                    f"Verifique se a API está rodando em {API_BASE_URL}"
                )
            except requests.exceptions.Timeout:
                st.error("❌ A API demorou muito tempo para responder.")
            except Exception as e:
                st.error(f"❌ Erro inesperado: {str(e)}")
    else:
        st.warning("⚠️ Por favor, digite uma mensagem antes de enviar.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 12px;'>
        Edu Assistant AI | Powered by Google Gemini
    </div>
    """,
    unsafe_allow_html=True,
)
