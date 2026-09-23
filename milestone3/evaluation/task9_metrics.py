import json
import math
import time
from pathlib import Path

from milestone3.recommendation.pipeline import (
    get_ranked_recommendations,
)
from milestone3.recommendation.recommendation_data import (
    RECOMMENDATIONS,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CASES_FILE = PROJECT_ROOT / "milestone3" / "data" / "task9_cases.json"


def precision_at_k(ranked_ids, relevant_ids, k):
    top_k = ranked_ids[:k]

    if not top_k:
        return 0.0

    hits = sum(item_id in relevant_ids for item_id in top_k)
    return hits / len(top_k)


def recall_at_k(ranked_ids, relevant_ids, k):
    if not relevant_ids:
        return 0.0

    hits = sum(
        item_id in relevant_ids
        for item_id in ranked_ids[:k]
    )
    return hits / len(relevant_ids)


def f1_score(precision, recall):
    if precision + recall == 0:
        return 0.0

    return 2 * precision * recall / (precision + recall)


def ndcg_at_k(ranked_ids, relevant_ids, k):
    dcg = 0.0

    for index, item_id in enumerate(ranked_ids[:k]):
        if item_id in relevant_ids:
            dcg += 1 / math.log2(index + 2)

    ideal_hits = min(len(relevant_ids), k)
    ideal_dcg = sum(
        1 / math.log2(index + 2)
        for index in range(ideal_hits)
    )

    if ideal_dcg == 0:
        return 0.0

    return dcg / ideal_dcg


def recommendation_diversity(ranked_ids):
    items_by_id = {
        item["id"]: item
        for item in RECOMMENDATIONS
    }

    categories = {
        items_by_id[item_id]["category"]
        for item_id in ranked_ids
        if item_id in items_by_id
    }

    if not ranked_ids:
        return 0.0

    return len(categories) / len(ranked_ids)


def evaluate_case(case, k=3):
    emotional_state = {
        "dominant_emotion": case["emotion"],
        "intensity_level": case["intensity"],
    }

    preferences = case.get("preferences", [])
    relevant_ids = set(case["relevant_ids"])

    # Baseline: original recommendation dataset order
    baseline_ids = [
        item["id"]
        for item in RECOMMENDATIONS
    ][:k]

    # Advanced: existing personalized + hybrid + ranking pipeline
    start_time = time.perf_counter()

    advanced_results = get_ranked_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history={},
        top_n=k,
    )

    response_time_ms = (
        time.perf_counter() - start_time
    ) * 1000

    advanced_ids = [
        item["id"]
        for item in advanced_results
    ]

    def calculate_metrics(ids):
        precision = precision_at_k(
            ids, relevant_ids, k
        )
        recall = recall_at_k(
            ids, relevant_ids, k
        )

        return {
            "precision_at_k": precision,
            "recall_at_k": recall,
            "f1_at_k": f1_score(
                precision, recall
            ),
            "ndcg_at_k": ndcg_at_k(
                ids, relevant_ids, k
            ),
            "diversity": recommendation_diversity(
                ids
            ),
        }

    return {
        "case": case["name"],
        "baseline_ids": baseline_ids,
        "advanced_ids": advanced_ids,
        "baseline": calculate_metrics(
            baseline_ids
        ),
        "advanced": calculate_metrics(
            advanced_ids
        ),
        "response_time_ms": round(
            response_time_ms, 3
        ),
    }


def main():
    with CASES_FILE.open(
        "r", encoding="utf-8"
    ) as file:
        cases = json.load(file)

    all_results = []

    for case in cases:
        result = evaluate_case(case)
        all_results.append(result)

        print(f"\n=== {result['case']} ===")
        print("Baseline IDs:", result["baseline_ids"])
        print("Advanced IDs:", result["advanced_ids"])
        print("Baseline metrics:", result["baseline"])
        print("Advanced metrics:", result["advanced"])
        print(
            "Response time (ms):",
            result["response_time_ms"],
        )

    metric_names = [
        "precision_at_k",
        "recall_at_k",
        "f1_at_k",
        "ndcg_at_k",
        "diversity",
    ]

    print("\n=== AVERAGE METRICS ===")

    for metric in metric_names:
        baseline_average = sum(
            result["baseline"][metric]
            for result in all_results
        ) / len(all_results)

        advanced_average = sum(
            result["advanced"][metric]
            for result in all_results
        ) / len(all_results)

        print(
            f"{metric}: "
            f"baseline={baseline_average:.3f}, "
            f"advanced={advanced_average:.3f}"
        )

    average_response_time = sum(
        result["response_time_ms"]
        for result in all_results
    ) / len(all_results)

    print(
        "Average response time (ms):",
        round(average_response_time, 3),
    )

    print(
        "\nNote: These relevance labels are "
        "manually defined test labels, not real user ratings."
    )


if __name__ == "__main__":
    main()