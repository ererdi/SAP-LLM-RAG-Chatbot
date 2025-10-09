# -*- coding: utf-8 -*-
"""
SAP Hata Çözüm Asistanı (On-Prem LLM + RAG)
Intel CPU veya küçük modeller için optimize edilmiş versiyon.
"""

import streamlit as st
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate

# --- Sabitler ---
PERSIST_DIR = "db"


# --- UI ---
st.set_page_config(
    page_title="SAP Hata Çözüm Asistanı",
    page_icon="🧩",
    layout="wide"
)
st.title("🧩 SAP Hata Çözüm Asistanı")

MODEL_OPTIONS = ["qwen2:0.5b", "phi3:mini", "mistral:7b"]

SELECTED_MODEL = st.sidebar.selectbox("LLM Modeli Seç", MODEL_OPTIONS, index=0)
TEMPERATURE = st.sidebar.slider("Yaratıcılık (temperature)", 0.0, 1.0, 0.2, 0.1)


# --- Model önbelleğe alma (cache) ---
@st.cache_resource
def load_model(selected_model_name, model_temp):

    """Ollama modelini belleğe yükler ve cache'te saklar."""
    return ChatOllama(
    model=selected_model_name,
    temperature=model_temp,
    base_url="http://127.0.0.1:11434"
)



# Model yalnızca ilk çalıştırmada yüklenir, sonra bellekte tutulur
LLM = load_model(SELECTED_MODEL, TEMPERATURE)


# --- Embedding & Vector DB ---
EMBEDDINGS = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
VECTOR_DB = Chroma(persist_directory=PERSIST_DIR, embedding_function=EMBEDDINGS)
RETRIEVER = VECTOR_DB.as_retriever(search_kwargs={"k": 4})


# --- Prompt ---
SYSTEM_PROMPT = """\
Aşağıdaki bağlam SAP hata kodu çözümlerinden derlenmiştir.
Yalnızca bu bağlama dayanarak Türkçe yanıt ver.

Kurallar:
- En fazla 250 kelime.
- Numara verilmiş adımlar sun (1., 2., 3., ...).
- Bağlam yetersizse “Yeterli bağlam yok, lütfen ek detay verin (modül, tcode, işlem adımı).” de.
- Uydurma yapma; emin olmadığın noktaları açıkça belirt.

--- BAĞLAM BAŞLANGIÇ ---
{context}
--- BAĞLAM BİTİŞ ---

Soru: {question}
"""

PROMPT = ChatPromptTemplate.from_template(SYSTEM_PROMPT)


def trim_to_words(text: str, limit: int = 250) -> str:
    """Yanıtı maksimum kelime sayısına kısaltır."""
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]) + " ..."


# --- Form ---
with st.form("qa"):
    user_question = st.text_input(
        "Sorunuzu yazın (örn. 'VP199 hatası çözümü nedir?')"
    )
    submitted = st.form_submit_button("Yanıtla")

if submitted and user_question.strip():
    with st.spinner("Getiriliyor…"):
        docs = RETRIEVER.invoke(user_question)
        context_blocks = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "?")
            code = doc.metadata.get("code", "")
            title = doc.metadata.get("title", "")
            page_text = doc.page_content
            block = (
                f"[{i}] Kaynak: {source} | Kod: {code} | Başlık: {title}\n{page_text}"
            )
            context_blocks.append(block)

        full_context = "\n\n".join(context_blocks)
        final_prompt = PROMPT.format(context=full_context, question=user_question)
        answer_raw = LLM.invoke(final_prompt)
        answer = trim_to_words(answer_raw.content, 250)

    st.subheader("Yanıt")
    st.write(answer)

    st.divider()
    st.subheader("Kaynak Parçaları")
    for i, doc in enumerate(docs, start=1):
        code = doc.metadata.get("code", "")
        title = doc.metadata.get("title", "")
        link = doc.metadata.get("link", "")
        st.markdown(f"**[{i}] {code} – {title}**")
        if link:
            st.markdown(f"[Kaynak bağlantı]({link})")
        preview = doc.page_content[:900]
        if len(doc.page_content) > 900:
            preview += "..."
        st.caption(preview)
