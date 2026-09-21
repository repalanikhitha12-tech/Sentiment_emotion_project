import unittest

from milestone3.emotion_analysis.state import analyze_emotional_state


class TestEmotionAnalysis(unittest.TestCase):

    def test_dominant_emotion(self):
        result = analyze_emotional_state({
            "joy": 0.20,
            "sadness": 0.10,
            "anger": 0.10,
            "fear": 0.80,
            "surprise": 0.05,
            "disgust": 0.10,
        })

        self.assertEqual(result["dominant_emotion"], "fear")

    def test_mixed_emotions(self):
        result = analyze_emotional_state({
            "joy": 0.70,
            "sadness": 0.10,
            "anger": 0.10,
            "fear": 0.80,
            "surprise": 0.05,
            "disgust": 0.05,
        })

        self.assertTrue(result["mixed_emotional_state"])
        self.assertEqual(result["polarity"], "mixed")

    def test_intensity_changes(self):
        low = analyze_emotional_state({
            "joy": 0.10,
            "sadness": 0.10,
            "anger": 0.10,
            "fear": 0.10,
            "surprise": 0.10,
            "disgust": 0.10,
        })

        high = analyze_emotional_state({
            "joy": 0.90,
            "sadness": 0.05,
            "anger": 0.05,
            "fear": 0.05,
            "surprise": 0.05,
            "disgust": 0.05,
        })

        self.assertGreater(high["intensity"], low["intensity"])


if __name__ == "__main__":
    unittest.main()