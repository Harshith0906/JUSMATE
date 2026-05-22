import time
import json
from retriever import find_similar_cases

# Load test queries
with open("evaluation_queries.json", "r") as f:
    test_cases = json.load(f)

total = len(test_cases)
correct_top3 = 0
total_time = 0

for case in test_cases:
    query = case["query"]
    expected = case["expected_keywords"]

    start = time.time()
    results = find_similar_cases(query, k=5)
    end = time.time()

    total_time += (end - start)

    acts_returned = [r["meta"]["act"] for r in results]

    # Check if any expected keyword appears
    if any(any(exp.lower() in act.lower() for act in acts_returned) for exp in expected):
        correct_top3 += 1
    print("Query:", query)
    print("Expected:", expected)
    print("Returned:", acts_returned)
    print("Matched?:", any(exp.lower() in act.lower() for exp in expected for act in acts_returned))
    print("------")

accuracy = (correct_top3 / total) * 100
avg_time = total_time / total

print("Total Queries:", total)
print("Top-3 Accuracy:", accuracy, "%")
print("Average Retrieval Time:", avg_time, "seconds")