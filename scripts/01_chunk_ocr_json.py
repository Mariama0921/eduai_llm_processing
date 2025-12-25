import json
import os
import re
from pathlib import Path

# Paths
OCR_DIR = Path("data/ocr_json")
OUTPUT_DIR = Path("data/chunks")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "chunks.jsonl"

# Chunk parameters
CHUNK_SIZE = 500   # characters
CHUNK_OVERLAP = 50

def clean_markdown(text: str) -> str:
    # Remove image markdown ![...](...)
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
    # Normalize spaces
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()

def split_text(text, chunk_size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
        if start < 0:
            start = 0
    return chunks

with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
    for json_file in OCR_DIR.glob("*.json"):
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        pages = data.get("pages", [])
        for page in pages:
            page_index = page.get("index")
            markdown = page.get("markdown", "")
            cleaned_text = clean_markdown(markdown)

            if not cleaned_text:
                continue

            chunks = split_text(cleaned_text, CHUNK_SIZE, CHUNK_OVERLAP)

            for i, chunk in enumerate(chunks):
                record = {
                    "chunk_id": f"{json_file.stem}_page{page_index}_chunk{i}",
                    "text": chunk,
                    "source_file": json_file.name,
                    "page": page_index
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")

print("✅ Chunking terminé avec succès")
