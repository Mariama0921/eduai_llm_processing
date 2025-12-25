import faiss
import json
import os
from sentence_transformers import SentenceTransformer
from mistralai import Mistral

# ========================
# CONFIGURATION
# ========================
FAISS_INDEX_PATH = "index/faiss.index"   
CHUNKS_PATH = "data/chunks/chunks.jsonl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "mistral-large-latest"
TOP_K = 5

# ========================
# CHARGEMENT
# ========================
print(" Chargement des modèles et données...")

# Embeddings
embedder = SentenceTransformer(EMBEDDING_MODEL)

# Index FAISS
index = faiss.read_index(FAISS_INDEX_PATH)

# Chunks JSONL
chunks = []
with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            chunks.append(json.loads(line))

print(f" {len(chunks)} chunks chargés")

# Client Mistral (NOUVELLE API)
client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

# ========================
# BOUCLE RAG
# ========================
while True:
    query = input("\n Que veux-tu savoir ? (ou 'exit') : ")
    if query.lower() == "exit":
        break

    # Embedding de la question
    q_embedding = embedder.encode([query])

    # Recherche FAISS
    distances, indices = index.search(q_embedding, TOP_K)

    context = "\n\n".join(chunks[i]["text"] for i in indices[0])

    messages = [
        {
            "role": "system",
            "content": (
                "Tu es un assistant pédagogique spécialisé dans l'analyse de documents OCR. "
                "Réponds uniquement à partir du contexte fourni. "
                "Si l'information n'est pas présente, dis-le clairement."
            )
        },
        {
            "role": "user",
            "content": f"Contexte :\n{context}\n\nQuestion :\n{query}"
        }
    ]

    response = client.chat.complete(
        model=LLM_MODEL,
        messages=messages,
        temperature=0.2
    )

    print("\n Réponse :")
    print(response.choices[0].message.content)
