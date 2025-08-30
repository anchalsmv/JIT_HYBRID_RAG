
import streamlit as st
from hybrid_retriever import HybridRetriever

# --- Config ---
ES_ENDPOINT = "add elastic cloud eendpoint url"
ES_API_KEY = "add elastic cloud api key"

# --- Initialize retriever ---
retriever = HybridRetriever(ES_ENDPOINT, ES_API_KEY)

# --- Streamlit UI ---
st.title(" Hybrid Search Chatbot (Elastic + FAISS)")

query = st.text_input("Enter your question:")

if st.button("Search") and query:
    results = retriever.search(query, top_k=3)

    st.subheader("ElasticSearch Results")
    for r in results["elasticsearch"]:
        st.write("•", r)

    st.subheader("FAISS Results")
    for r in results["faiss"]:
        st.write("•", r)
