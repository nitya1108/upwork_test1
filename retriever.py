from sentence_transformers import SentenceTransformer
import faiss
import os

model = SentenceTransformer('all-MiniLM-L6-v2')  # Embedding model

# Load documents from data folder
data_dir = "data"
documents = []
doc_ids = []

for filename in os.listdir(data_dir):
    if filename.endswith(".txt"):
        with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
            doc_ids.append(filename)

# Generate embeddings for all documents
doc_embeddings = model.encode(documents, show_progress_bar=True)

# Create FAISS index
dimension = doc_embeddings.shape[1]  # Get embedding size
index = faiss.IndexFlatL2(dimension)  # L2 distance index
index.add(doc_embeddings)  # Add document vectors to FAISS index

# Function to get top 3 similar documents based on query
def get_top_documents(query, k=3):
    query_embedding = model.encode([query])  # Embed the query
    distances, indices = index.search(query_embedding, k)  # Search top k

    top_docs = []
    sources = []
    for idx in indices[0]:
        top_docs.append(documents[idx])
        sources.append(doc_ids[idx])

    return top_docs, sources
