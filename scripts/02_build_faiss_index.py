import json
from pathlib import Path
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Paths
CHUNKS_FILE = Path("data/chunks/chunks.jsonl")
INDEX_DIR = Path("index")
INDEX_DIR.mkdir(exist_ok=True)

FAISS_INDEX_PATH = INDEX_DIR / "faiss.index"
METADATA_PATH = INDEX_DIR / "metadata.json"

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

texts = []
metadata = []

# Read chunks
with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    for line in f:
        item = json.loads(line)
        texts.append(item["text"])
        metadata.append({
            "chunk_id": item["chunk_id"],
            "source_file": item["source_file"],
            "page": item["page"]
        })

print(f"📄 {len(texts)} chunks chargés")

# Compute embeddings
embeddings = model.encode(
    texts,
    show_progress_bar=True,
    convert_to_numpy=True,
    normalize_embeddings=True
)

dimension = embeddings.shape[1]

# Create FAISS index
index = faiss.IndexFlatIP(dimension)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, str(FAISS_INDEX_PATH))

with open(METADATA_PATH, "w", encoding="utf-8") as f:
    json.dump(metadata, f, ensure_ascii=False, indent=2)

print("✅ Index FAISS créé avec succès")
