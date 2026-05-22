import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


index = faiss.read_index("legal_index.faiss")
chunks = np.load("chunks.npy", allow_pickle=True)
metadata = np.load("metadata.npy", allow_pickle=True)

model = SentenceTransformer("all-mpnet-base-v2")

def retrieve(query, k=5):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    return [(chunks[i], metadata[i]) for i in I[0]]



query = "what is illegal in india?"

results = retrieve(query)

print("\n RETRIEVED RESULTS:\n")

for text, meta in results:
    print(f"{meta['act']} | {meta['section']} – {meta['heading']}")
    print(text[:300])
    print("-" * 60)
