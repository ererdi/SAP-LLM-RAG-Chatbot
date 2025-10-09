# ingest.py
import os
import pandas as pd
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

DATA_XLSX = "data/sap_errors.xlsx"
PERSIST_DIR = "db"

def load_rows_as_docs():
    if not os.path.exists(DATA_XLSX):
        raise FileNotFoundError("data/sap_errors.xlsx bulunamadı.")
    df = pd.read_excel(DATA_XLSX)

    docs = []
    for _, r in df.iterrows():
        content = (
            f"SAP Hata Kodu: {r.get('code','')}\n"
            f"Başlık: {r.get('title','')}\n"
            f"Bağlam: {r.get('context','')}\n"
            f"Çözüm Adımları:\n{r.get('solution','')}\n"
        )
        meta = {
            "source": "sap_errors.xlsx",
            "code": r.get("code",""),
            "title": r.get("title",""),
            "link": r.get("source_link","")
        }
        docs.append(Document(page_content=content, metadata=meta))
    return docs

def main():
    print("→ Excel okunuyor…")
    base_docs = load_rows_as_docs()
    print(f"Toplam satır: {len(base_docs)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=120)
    chunks = splitter.split_documents(base_docs)
    print(f"Parça (chunk) sayısı: {len(chunks)}")

    embeddings = SentenceTransformerEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
    )
    db.persist()
    print(f"✅ Vektör veritabanı hazır: {PERSIST_DIR}")

if __name__ == "__main__":
    main()
