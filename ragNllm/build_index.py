import json, os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

DATA_DIR = "data/acts_json"

chunks = []
metadata = []
def extract_text(obj):
   
    collected = ""

    if isinstance(obj, str):
        collected += obj + " "

    elif isinstance(obj, dict):
        if "text" in obj:
            collected += obj["text"] + " "
        if "contains" in obj:
            for v in obj["contains"].values():
                collected += extract_text(v)

    return collected

print(" Reading legal JSON files...")

for file in os.listdir(DATA_DIR):
    if not file.endswith(".json"):
        continue

    file_path = os.path.join(DATA_DIR, file)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            act = json.load(f)
    except Exception as e:
        print(f"Failed to read {file}: {e}")
        continue

    if not isinstance(act, dict):
        print(f" Skipping file (not a JSON object): {file}")
        continue

    act_title = act.get("Act Title", "Unknown Act")

   
    chapters = act.get("Chapters")

    
    if chapters:
        chapter_items = chapters.values()
    else:
        sections = act.get("Sections") or act.get("sections")
        if not sections:
            print(f" Skipping file (no Chapters or Sections): {file}")
            continue

        
        chapter_items = [{
            "Name": "NO CHAPTER",
            "Sections": sections
        }]

    for chapter in chapter_items:
        chapter_name = chapter.get("Name", "Unknown Chapter")
        sections = chapter.get("Sections", {})

        if not sections:
            continue

        for sec_id, section in sections.items():
            heading = section.get("heading", "")

            text = f"{sec_id} {heading}\n"

         
            for para in section.get("paragraphs", {}).values():
                text += extract_text(para)
            text = text.strip()

            if len(text) < 80:
                continue

            chunks.append(text)
            metadata.append({
                "source_file": file,
                "act": act_title,
                "chapter": chapter_name,
                "section": sec_id,
                "heading": heading
            })

print(f" Total chunks created: {len(chunks)}")

if not chunks:
    raise ValueError("No valid chunks found. Check dataset structure.")

print(" Creating embeddings...")
model = SentenceTransformer("all-mpnet-base-v2")
embeddings = model.encode(chunks, show_progress_bar=True)

print(" Building FAISS index...")
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(np.array(embeddings))

faiss.write_index(index, "legal_index.faiss")
np.save("chunks.npy", np.array(chunks, dtype=object))
np.save("metadata.npy", np.array(metadata, dtype=object))

print(" Knowledge base built successfully")
