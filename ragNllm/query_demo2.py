import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load FAISS index and data
index = faiss.read_index("legal_index.faiss")
chunks = np.load("chunks.npy", allow_pickle=True)
metadata = np.load("metadata.npy", allow_pickle=True)

model = SentenceTransformer("all-mpnet-base-v2")

def retrieve(query, k=3):
    q_emb = model.encode([query])
    D, I = index.search(q_emb, k)
    return [(chunks[i], metadata[i]) for i in I[0]]

# ---------------- LAWYER MODE ----------------
def lawyer_view(query):
    print("\n👨‍⚖️ LAWYER VIEW\n")
    results = retrieve(query)

    for text, meta in results:
        print(f"Act: {meta['act']}")
        print(f"Section: {meta['section']} – {meta['heading']}")
        print("Legal Provision:")
        print(text)
        print("-" * 70)

# ---------------- CITIZEN MODE ----------------
def citizen_view(query):
    print("\n👩‍💼 CITIZEN VIEW\n")
    results = retrieve(query)

    text, meta = results[0]

    print(f"This law comes from: {meta['act']}")
    print("In simple words:")
    print(simplify(text))


# Simple rule-based simplifier (dummy but effective)
def simplify(text):
    text = text.replace("shall", "will")
    text = text.replace("hereby", "")
    text = text.replace("notwithstanding", "even if")
    return text


# ---------------- DEMO QUERY ----------------
query = "what is illegal in india?"

lawyer_view(query)
citizen_view(query)
