def record_feedback(history, recommendation_id, feedback):
    """
    Store user feedback for a recommendation.
    feedback should be 'liked' or 'disliked'.
    """

    if feedback not in ("liked", "disliked"):
        raise ValueError(
            "Feedback must be 'liked' or 'disliked'."
        )

    updated_history = history.copy()

    updated_feedback = list(
        updated_history.get("feedback", [])
    )

    updated_feedback.append({
        "recommendation_id": recommendation_id,
        "feedback": feedback,
    })

    updated_history["feedback"] = updated_feedback

    return updated_history


def calculate_feedback_score(history, recommendation_id):
    """
    Calculate a score based on previous feedback.
    Liked = +2, Disliked = -2.
    """

    score = 0

    for item in history.get("feedback", []):
        if item.get("recommendation_id") == recommendation_id:
            if item.get("feedback") == "liked":
                score += 2
            elif item.get("feedback") == "disliked":
                score -= 2

    return score