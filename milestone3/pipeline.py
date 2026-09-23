from milestone3.hybrid.engine import (
    generate_hybrid_recommendations,
)
from milestone3.explainability.explainer import (
    explain_recommendation,
)


def generate_explained_recommendations(
    emotional_state,
    preferences=None,
    history=None,
    top_n=3,
):
    """
    Generate recommendations and explain why
    each item was suggested.
    """

    preferences = preferences or []
    history = history or {}

    recommendations = generate_hybrid_recommendations(
        emotional_state=emotional_state,
        preferences=preferences,
        history=history,
        top_n=top_n,
    )

    for item in recommendations:
        item["explanation"] = explain_recommendation(
            item=item,
            emotional_state=emotional_state,
            preferences=preferences,
            history=history,
        )

    return recommendations