
import unittest
from datetime import datetime

from milestone4.data.trend import (
    calculate_daily_average,
    calculate_weekly_average,
    calculate_monthly_average,
    get_dominant_emotion,
)


class TestEmotionTrends(unittest.TestCase):

    def setUp(self):
        self.records = [
            {
                "timestamp": datetime(2026, 10, 1, 10, 0),
                "emotion_scores": {
                    "joy": 0.8,
                    "sadness": 0.2,
                },
            },
            {
                "timestamp": datetime(2026, 10, 1, 18, 0),
                "emotion_scores": {
                    "joy": 0.6,
                    "sadness": 0.4,
                },
            },
            {
                "timestamp": datetime(2026, 10, 5, 10, 0),
                "emotion_scores": {
                    "joy": 0.4,
                    "sadness": 0.6,
                },
            },
        ]

    def test_daily_average(self):
        result = calculate_daily_average(self.records)
        self.assertEqual(len(result), 2)
        self.assertAlmostEqual(
            result[datetime(2026, 10, 1).date()]["joy"],
            0.7,
        )

    def test_weekly_average(self):
        result = calculate_weekly_average(self.records)
        self.assertEqual(len(result), 2)

    def test_monthly_average(self):
        result = calculate_monthly_average(self.records)
        self.assertEqual(len(result), 1)
        self.assertAlmostEqual(
            result[datetime(2026, 10, 1).date()]["joy"],
            0.6,
        )

    def test_dominant_emotion(self):
        result = get_dominant_emotion({
            "joy": 0.3,
            "fear": 0.8,
            "sadness": 0.2,
        })
        self.assertEqual(result, "fear")

    def test_empty_emotion_scores(self):
        self.assertIsNone(get_dominant_emotion({}))


if __name__ == "__main__":
    unittest.main()