import ollama
import streamlit as st

st.set_page_config(
    page_title="Chat MedGemma Local", page_icon="🩺", layout="centered"
)

st.title("🩺 Assistente Local com MedGemma")
st.caption(
    "Ambiente de estudo focado em suporte clínico e termos médicos (Rodando local via Ollama)"
)

# Inicializa o histórico de mensagens na sessão do Streamlit
if "messages" not in st.session_state:
  st.session_state["messages"] = []

# Exibe as mensagens anteriores na tela ao recarregar
for message in st.session_state["messages"]:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

# Caixa de input para o usuário digitar a pergunta
if prompt := st.chat_input(
    "Digite sua dúvida clínica ou caso de estudo..."
):
  # Adiciona a mensagem do usuário ao histórico
  st.session_state["messages"].append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  # Gera a resposta do modelo via Ollama mantendo o contexto da conversa
  with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    try:
      # Envia o histórico completo para o modelo manter o contexto do chat
      stream = ollama.chat(
          model="medgemma:4b", messages=st.session_state["messages"], stream=True
      )

      for chunk in stream:
        content = chunk["message"]["content"]
        full_response += content
        message_placeholder.markdown(full_response + "▌")

      message_placeholder.markdown(full_response)

    except Exception as e:
      full_response = f"Erro ao comunicar com o Ollama: {e}"
      message_placeholder.error(full_response)

  # Adiciona a resposta do assistente ao histórico
  st.session_state["messages"].append(
      {"role": "assistant", "content": full_response}
  )