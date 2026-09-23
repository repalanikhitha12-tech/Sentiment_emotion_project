
from milestone3.feedback.feedback_learner import (
    record_feedback,
    calculate_feedback_score,
)


def evaluate_feedback(feedback_records):
    """
    Evaluate recommendation feedback.

    Acceptance rate = liked / total feedback * 100
    """

    history = {"feedback": list(feedback_records)}

    total = len(feedback_records)
    liked = sum(
        item.get("feedback") == "liked"
        for item in feedback_records
    )
    disliked = sum(
        item.get("feedback") == "disliked"
        for item in feedback_records
    )

    acceptance_rate = (
        (liked / total) * 100
        if total > 0
        else 0.0
    )

    scores = {}

    for item in feedback_records:
        recommendation_id = item.get(
            "recommendation_id"
        )

        if recommendation_id:
            scores[recommendation_id] = (
                calculate_feedback_score(
                    history,
                    recommendation_id,
                )
            )

    return {
        "total_feedback": total,
        "liked": liked,
        "disliked": disliked,
        "acceptance_rate_percent": round(
            acceptance_rate, 2
        ),
        "feedback_scores": scores,
    }


def main():
    # Sample test feedback (not real user data)
    sample_feedback = [
        {
            "recommendation_id": "calm_music",
            "feedback": "liked",
        },
        {
            "recommendation_id": "journal",
            "feedback": "disliked",
        },
        {
            "recommendation_id": "calm_music",
            "feedback": "liked",
        },
        {
            "recommendation_id": "take_a_break",
            "feedback": "disliked",
        },
    ]

    results = evaluate_feedback(sample_feedback)

    print("=== Feedback Evaluation ===")
    print("Total feedback:", results["total_feedback"])
    print("Liked:", results["liked"])
    print("Disliked:", results["disliked"])
    print(
        "Acceptance rate:",
        f"{results['acceptance_rate_percent']}%",
    )
    print("Feedback scores:", results["feedback_scores"])


if __name__ == "__main__":
    main()