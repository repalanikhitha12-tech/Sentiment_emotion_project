import unittest

from milestone3.hybrid.engine import (
    generate_hybrid_recommendations,
)


class TestHybridRecommendations(unittest.TestCase):

    def test_returns_recommendations(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_hybrid_recommendations(state)

        self.assertGreater(len(results), 0)

    def test_preference_affects_results(self):
        state = {
            "dominant_emotion": "joy",
            "intensity_level": "medium",
        }

        results = generate_hybrid_recommendations(
            state,
            preferences=["learning"],
        )

        self.assertTrue(
            any(
                item["category"] == "learning"
                for item in results
            )
        )

    def test_no_duplicate_recommendations(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_hybrid_recommendations(state)

        ids = [item["id"] for item in results]

        self.assertEqual(len(ids), len(set(ids)))

    def test_top_n_limit(self):
        state = {
            "dominant_emotion": "fear",
            "intensity_level": "high",
        }

        results = generate_hybrid_recommendations(
            state,
            top_n=2,
        )

        self.assertLessEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()