from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_vector_store():
    docs = []
    doc_titles = []
    for idx, filename in enumerate(os.listdir('data')):
        with open(f'data/{filename}', 'r', encoding='utf-8') as file:
            content = file.read()
            docs.append(content)
            doc_titles.append(filename.replace('.txt', ''))

    embeddings = model.encode(docs)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))

    return (index, docs), doc_titles

def retrieve_context(query, vector_store, doc_titles, top_k=3):
    index, docs = vector_store
    query_vector = model.encode([query])
    distances, indices = index.search(query_vector, top_k)
    retrieved_docs = [docs[i] for i in indices[0]]
    sources = [doc_titles[i] for i in indices[0]]
    return retrieved_docs, sources

