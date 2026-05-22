import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

index = faiss.read_index("legal_index.faiss")
chunks = np.load("chunks.npy", allow_pickle=True)
metadata = np.load("metadata.npy", allow_pickle=True)

embed_model = SentenceTransformer("all-mpnet-base-v2")


def retrieve(query, k=3):
    q_emb = embed_model.encode([query])
    D, I = index.search(q_emb, k)

    results = []
    for rank, (idx, distance) in enumerate(zip(I[0], D[0]), start=1):

        similarity = 1 / (1 + distance)

        results.append({
            "rank": rank,
            "distance": float(distance),
            "similarity": float(similarity),
            "text": chunks[idx],
            "meta": metadata[idx]
        })

    return results


def find_similar_cases(case_text, k=3):
    q_emb = embed_model.encode([case_text])
    D, I = index.search(q_emb, k)

    results = []
    for rank, (idx, distance) in enumerate(zip(I[0], D[0]), start=1):

        similarity = 1 / (1 + distance)

        results.append({
            "rank": rank,
            "distance": float(distance),
            "similarity": float(similarity),
            "text": chunks[idx],
            "meta": metadata[idx]
        })

    return results