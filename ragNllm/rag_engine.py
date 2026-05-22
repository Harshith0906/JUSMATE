# from retriever import retrieve
# from prompts import build_prompt
# from model_loader import generate

# def rag_answer(query, role):
#     results = retrieve(query, k=3)

#     context = "\n\n".join([r["text"][:1500] for r in results])

#     prompt = build_prompt(context, query, role)

#     answer = generate(prompt)

#     return {
#         "answer": answer,
#         "sources": results
#     }

# from retriever import find_similar_cases
# from model_loader import generate

# def analyze_case_similarity(case_text, role):
#     results = find_similar_cases(case_text, k=3)

#     combined_sections = ""

#     for item in results:
#         combined_sections += f"""
# Rank {item['rank']}:
# Act: {item['meta']['act']}
# Section: {item['meta']['section']} – {item['meta']['heading']}
# Provision:
# {item['text'][:1200]}

# --------------------------------
# """

#     if role == "lawyer":
#         instruction = """
# You are an Indian legal research assistant.
# For each ranked section, explain briefly (2-3 lines) why it is relevant to the case.
# Use legal terminology.
# Respond in structured format .
# """
#     else:
#         instruction = """
# You are a legal assistant for a citizen.
# For each ranked section, explain briefly (2-3 lines) how it relates to the case.
# Use simple language.
# """

#     prompt = f"""
# {instruction}

# Case Facts:
# {case_text}

# Legal Provisions:
# {combined_sections}

# Response:
# """

#     explanation = generate(prompt)

#     return {
#         "analysis": explanation,
#         "retrieved_sections": results
#     }


# def filter_relevant_sections(case_text, retrieved_sections):
    
#     combined = ""
    
#     for idx, item in enumerate(retrieved_sections):
#         combined += f"""
# Option {idx+1}:
# Act: {item['meta']['act']}
# Section: {item['meta']['section']}
# Provision:
# {item['text'][:800]}
# --------------------------------
# """

#     prompt = f"""
# You are a legal expert.

# Case Facts:
# {case_text}

# Below are retrieved legal provisions.

# Identify which options are directly applicable to the case.
# Return only the option numbers that are truly relevant.
# If none are relevant, say NONE.

# {combined}

# Relevant Option Numbers:
# """

#     response = generate(prompt)

#     return response


from retriever import retrieve, find_similar_cases
from prompts import build_prompt
from model_loader import generate


# 🔴 1. Detect non-legal / small talk queries
def is_non_legal_query(query):
    smalltalk = ["hi", "hello", "hey", "thanks", "thank you", "bye"]

    query_clean = query.lower().strip()

    # exact match OR too short query
    if query_clean in smalltalk or len(query_clean.split()) <= 2:
        return True

    return False


# 🔵 2. Main RAG Answer Function
def rag_answer(query, role):

    # 🔴 Step 1: Handle non-legal queries
    if is_non_legal_query(query):
        return {
            "answer": "Hello! I am JusMate, your legal assistant. Please ask a legal question related to Indian law.",
            "sources": []
        }

    # 🔵 Step 2: Retrieve relevant chunks
    results = retrieve(query, k=3)

    # 🔴 Step 3: Relevance check (IMPORTANT)
    # If similarity not added yet, replace with distance logic
    top_result = results[0]

    similarity = top_result.get("similarity")

    # fallback if similarity not present (use distance)
    if similarity is None:
        distance = top_result.get("distance", 1)
        similarity = 1 / (1 + distance)

    # if similarity < 0.5:
    #     return {
    #         "answer": "The query does not appear to relate to Indian law. Please ask a relevant legal question.",
    #         "sources": []
    #     }

    # 🔵 Step 4: Build context
    context = "\n\n".join([r["text"][:1500] for r in results])

    # 🔵 Step 5: Generate answer
    prompt = build_prompt(context, query, role)
    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": results
    }


# 🔵 3. Case Similarity Analysis
def analyze_case_similarity(case_text, role):
    results = find_similar_cases(case_text, k=3)

    combined_sections = ""

    for item in results:
        combined_sections += f"""
Rank {item['rank']}:
Act: {item['meta']['act']}
Section: {item['meta']['section']} – {item['meta']['heading']}
Provision:
{item['text'][:1200]}

--------------------------------
"""

    if role == "lawyer":
        instruction = """
You are an Indian legal research assistant.
For each ranked section, explain briefly (2-3 lines) why it is relevant to the case.
Use legal terminology.
Respond in structured format.
"""
    else:
        instruction = """
You are a legal assistant for a citizen.
For each ranked section, explain briefly (2-3 lines) how it relates to the case.
Use simple language.
"""

    prompt = f"""
{instruction}

Case Facts:
{case_text}

Legal Provisions:
{combined_sections}

Response:
"""

    explanation = generate(prompt)

    return {
        "analysis": explanation,
        "retrieved_sections": results
    }


# 🔵 4. Filter Relevant Sections (Optional Boost)
def filter_relevant_sections(case_text, retrieved_sections):

    combined = ""

    for idx, item in enumerate(retrieved_sections):
        combined += f"""
Option {idx+1}:
Act: {item['meta']['act']}
Section: {item['meta']['section']}
Provision:
{item['text'][:800]}
--------------------------------
"""

    prompt = f"""
You are a legal expert.

Case Facts:
{case_text}

Below are retrieved legal provisions.

Identify which options are directly applicable to the case.
Return only the option numbers that are truly relevant.
If none are relevant, say NONE.

{combined}

Relevant Option Numbers:
"""

    response = generate(prompt)

    return response