
import streamlit as st
from datetime import datetime

from milestone3.integration import generate_final_recommendations
from milestone4.data.trend import (
    calculate_daily_average,
    calculate_weekly_average,
    calculate_monthly_average,
)
from milestone4.data.trend_chart import show_emotion_trend
from milestone4.data.history import (
    save_emotion_record,
    load_emotion_history,
)


st.set_page_config(
    page_title="MoodMentor",
    page_icon="M",
    layout="wide",
)

st.title("MoodMentor")
st.subheader("Emotion Analysis & Personalized Wellness Dashboard")
st.write(
    "Enter your thoughts or feelings below. "
    "MoodMentor analyzes your emotional state and provides "
    "personalized recommendations."
)

user_text = st.text_area(
    "Enter your text",
    placeholder="Example: I am feeling happy and excited today!",
    height=150,
)

if st.button("Analyze Emotion"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        text = user_text.lower()

        emotion_probabilities = {
            "joy": 0.0,
            "sadness": 0.0,
            "anger": 0.0,
            "fear": 0.0,
            "surprise": 0.0,
            "disgust": 0.0,
        }

        emotion_word_groups = {
            "joy": [
                "happy", "happiness", "joy", "excited",
                "great", "good", "love", "wonderful",
            ],
            "sadness": [
                "sad", "unhappy", "cry", "lonely",
                "depressed", "upset", "hurt",
            ],
            "anger": [
                "angry", "anger", "mad", "furious",
                "annoyed", "irritated",
            ],
            "fear": [
                "fear", "afraid", "scared", "worried",
                "anxious", "nervous", "panic",
            ],
            "surprise": [
                "surprise", "surprised", "shocked",
                "unexpected", "amazed",
            ],
            "disgust": [
                "disgust", "disgusted", "hate", "gross", "awful",
            ],
        }

        for emotion, words in emotion_word_groups.items():
            for word in words:
                if word in text:
                    emotion_probabilities[emotion] += 0.20

        for emotion in emotion_probabilities:
            emotion_probabilities[emotion] = min(
                emotion_probabilities[emotion], 1.0
            )

        if max(emotion_probabilities.values()) == 0:
            emotion_probabilities["joy"] = 0.20

        try:
            results = generate_final_recommendations(
                emotion_probabilities=emotion_probabilities,
                preferences=["relaxation"],
                history={},
                top_n=3,
            )
        except Exception as e:
            st.error("An error occurred during emotion analysis.")
            st.code(str(e))
            st.stop()

        emotional_state = results["emotional_state"]
        recommendations = results["recommendations"]

        try:
            save_emotion_record(
                emotion_probabilities,
                timestamp=datetime.now(),
            )
        except Exception as e:
            st.error("Could not save emotion history.")
            st.code(str(e))

        st.divider()
        st.header("Emotional Analysis")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            dominant = emotional_state.get(
                "dominant_emotion", "Unknown"
            )
            st.metric("Dominant Emotion", str(dominant).capitalize())

        with col2:
            confidence = emotional_state.get("confidence", 0)
            confidence_text = (
                f"{confidence:.2f}"
                if isinstance(confidence, (int, float))
                else str(confidence)
            )
            st.metric("Confidence", confidence_text)

        with col3:
            intensity = emotional_state.get("intensity", 0)
            intensity_text = (
                f"{intensity:.1f}%"
                if isinstance(intensity, (int, float))
                else str(intensity)
            )
            st.metric("Intensity", intensity_text)

        with col4:
            polarity = emotional_state.get("polarity", "Unknown")
            st.metric("Polarity", str(polarity).capitalize())

        st.subheader("Emotion Scores")

        for emotion, score in emotion_probabilities.items():
            st.write(f"{emotion.capitalize()}: {int(score * 100)}%")
            st.progress(score)

        st.divider()
        st.subheader("Wellness Recommendations")

        if recommendations:
            for rank, recommendation in enumerate(
                recommendations, start=1
            ):
                title = recommendation.get(
                    "title",
                    recommendation.get("id", "Recommendation"),
                )
                score = recommendation.get("ranking_score", "")
                explanation = recommendation.get("explanation", "")

                st.markdown(f"### {rank}. {title}")

                if score != "":
                    st.write(f"Ranking Score: {score}")

                if explanation:
                    if isinstance(explanation, list):
                        for reason in explanation:
                            st.write(f"- {reason}")
                    else:
                        st.write(f"Why: {explanation}")

                st.divider()
        else:
            st.info("No recommendations available.")

        st.subheader("Emotional State Details")

        for key, value in emotional_state.items():
            st.write(f"{key.replace('_', ' ').title()}: {value}")

        st.divider()
        st.subheader("Your Input")
        st.info(user_text)
        st.success("Emotion analysis and recommendations completed.")


st.divider()
st.header("Emotional Trends")

emotion_history = load_emotion_history()
st.write(f"Total emotion records: {len(emotion_history)}")

trend_period = st.selectbox(
    "Select trend period",
    ["Daily", "Weekly", "Monthly"],
)

if trend_period == "Daily":
    trend_data = calculate_daily_average(emotion_history)
elif trend_period == "Weekly":
    trend_data = calculate_weekly_average(emotion_history)
else:
    trend_data = calculate_monthly_average(emotion_history)

show_emotion_trend(trend_data, period_name=trend_period)

