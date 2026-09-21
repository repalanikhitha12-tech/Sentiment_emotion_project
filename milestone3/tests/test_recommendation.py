import unittest

from milestone3.recommendation.personalized import (
    generate_recommendations,
)


class TestPersonalizedRecommendations(unittest.TestCase):

    def test_returns_recommendations(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_recommendations(state)
        self.assertGreater(len(results), 0)

    def test_respects_preferences(self):
        state = {
            "dominant_emotion": "joy",
            "intensity_level": "medium",
        }

        results = generate_recommendations(
            state,
            preferences=["learning"],
        )

        self.assertTrue(
            any(item["category"] == "learning" for item in results)
        )

    def test_uses_liked_history(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_recommendations(
            state,
            history={"liked": ["calm_music"]},
        )

        self.assertTrue(
            any(item["id"] == "calm_music" for item in results)
        )

    def test_top_n_limit(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_recommendations(state, top_n=2)
        self.assertLessEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()