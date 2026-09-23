def explain_recommendation(
    item,
    emotional_state,
    preferences=None,
    history=None,
):
    """
    Explain why a recommendation was suggested
    using the available recommendation signals.
    """

    preferences = preferences or []
    history = history or {}

    reasons = []

    current_emotion = str(
        emotional_state.get("dominant_emotion", "")
    ).lower()

    intensity = str(
        emotional_state.get("intensity_level", "")
    ).lower()

    item_emotions = {
        str(emotion).lower()
        for emotion in item.get("emotions", [])
    }

    item_intensities = {
        str(level).lower()
        for level in item.get("intensity_levels", [])
    }

    # Reason 1: Current emotion match
    if current_emotion and current_emotion in item_emotions:
        reasons.append(
            f"It matches the detected emotion: {current_emotion}."
        )

    # Reason 2: Intensity match
    if intensity and intensity in item_intensities:
        reasons.append(
            f"It is listed for {intensity} intensity."
        )

    # Reason 3: Preference match
    if item.get("category") in preferences:
        reasons.append(
            f"It matches your selected preference: "
            f"{item.get('category')}."
        )

    # Reason 4: Previously liked recommendation
    if item.get("id") in history.get("liked", []):
        reasons.append(
            "You previously liked this recommendation."
        )

    # Reason 5: Feedback history
    feedback_records = history.get("feedback", [])

    liked_before = any(
        record.get("recommendation_id") == item.get("id")
        and record.get("feedback") == "liked"
        for record in feedback_records
    )

    disliked_before = any(
        record.get("recommendation_id") == item.get("id")
        and record.get("feedback") == "disliked"
        for record in feedback_records
    )

    if liked_before:
        reasons.append(
            "Your previous feedback on this item was positive."
        )

    if disliked_before:
        reasons.append(
            "Your previous feedback on this item was negative."
        )

    # Fallback if no specific reason matched
    if not reasons:
        reasons.append(
            "This item was included by the recommendation "
            "system based on its available rules and scores."
        )

    return reasons