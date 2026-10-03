
import streamlit as st
import pandas as pd

from milestone4.data.history import (
    load_emotion_history,
    save_emotion_record,
)
from milestone4.data.trend import (
    calculate_daily_average,
    calculate_weekly_average,
    calculate_monthly_average,
)
from milestone4.data.feedback_history import (
    load_feedback_history,
    save_feedback,
)
from milestone4.data.recommendation_history import (
    load_recommendation_history,
    save_recommendation_history,
    update_recommendation_feedback,
)
from milestone4.data.search_filter import filter_recommendation_history
from milestone4.reports.export_reports import (
    generate_csv_report,
    generate_pdf_report,
)

st.set_page_config(
    page_title="MoodMentor",
    page_icon="🧠",
    layout="wide",
)

EMOTIONS = ["joy", "sadness", "anger", "fear", "surprise", "disgust"]

# --------------------------------------------------
# RECOMMENDATION DATA
# --------------------------------------------------

RECOMMENDATIONS = {
    "joy": [
        {
            "id": "joy_activity",
            "title": "Explore a fun activity",
            "description": "Try a hobby or activity that you enjoy.",
            "ranking_score": 6.5,
        },
        {
            "id": "learn_something",
            "title": "Learn something new",
            "description": "Explore a topic that interests you.",
            "ranking_score": 6.5,
        },
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": "Take a comfortable pause and breathe slowly.",
            "ranking_score": 5.0,
        },
    ],
    "sadness": [
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": "Write a few words about what is on your mind.",
            "ranking_score": 6.5,
        },
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": "Choose music you enjoy and take a quiet break.",
            "ranking_score": 6.0,
        },
        {
            "id": "talk_someone",
            "title": "Connect with someone you trust",
            "description": "Consider talking with a trusted person.",
            "ranking_score": 5.5,
        },
    ],
    "anger": [
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": "Pause and breathe slowly at a comfortable pace.",
            "ranking_score": 6.5,
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": "Write down what happened and how you feel.",
            "ranking_score": 6.0,
        },
        {
            "id": "short_break",
            "title": "Take a quiet break",
            "description": "Step away briefly if possible.",
            "ranking_score": 5.5,
        },
    ],
    "fear": [
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": "Take a comfortable pause and breathe slowly.",
            "ranking_score": 6.9,
        },
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": "Choose music you enjoy and take a quiet break.",
            "ranking_score": 5.7,
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": "Write a few words about what is on your mind.",
            "ranking_score": 5.7,
        },
    ],
    "surprise": [
        {
            "id": "journal",
            "title": "Reflect on what happened",
            "description": "Write down what surprised you and how you feel.",
            "ranking_score": 6.0,
        },
        {
            "id": "learn_something",
            "title": "Learn something new",
            "description": "Explore a topic that interests you.",
            "ranking_score": 5.5,
        },
        {
            "id": "calm_breathing",
            "title": "Take a mindful pause",
            "description": "Pause and notice how you feel.",
            "ranking_score": 5.0,
        },
    ],
    "disgust": [
        {
            "id": "short_break",
            "title": "Take a quiet break",
            "description": "Give yourself some space from the situation.",
            "ranking_score": 6.0,
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": "Write down what is bothering you, if helpful.",
            "ranking_score": 5.5,
        },
        {
            "id": "talk_someone",
            "title": "Talk with someone you trust",
            "description": "Consider sharing your thoughts with a trusted person.",
            "ranking_score": 5.0,
        },
    ],
}

# --------------------------------------------------
# KEYWORD-BASED EMOTION ANALYSIS
# --------------------------------------------------

KEYWORDS = {
    "joy": [
        "happy", "happiness", "joy", "excited", "exciting",
        "glad", "great", "good", "wonderful", "love",
        "cheerful", "delighted",
    ],
    "sadness": [
        "sad", "unhappy", "lonely", "disappointed",
        "upset", "heartbroken", "miserable", "down",
    ],
    "anger": [
        "angry", "anger", "furious", "annoyed",
        "irritated", "frustrated", "mad",
    ],
    "fear": [
        "afraid", "fear", "scared", "worried",
        "anxious", "nervous", "panic", "stress", "stressed",
    ],
    "surprise": [
        "surprised", "surprise", "amazed", "astonished",
        "unexpected", "shocked",
    ],
    "disgust": [
        "disgusted", "disgust", "revolting", "gross",
    ],
}


def analyze_emotion(text):
    """Perform simple keyword-based emotion analysis."""
    text_lower = text.lower()
    scores = {}

    for emotion, keywords in KEYWORDS.items():
        matches = sum(
            1 for keyword in keywords
            if keyword in text_lower
        )
        scores[emotion] = min(matches * 0.2, 1.0)

    dominant = max(scores, key=scores.get)
    confidence = scores[dominant]

    if confidence == 0:
        dominant = "joy"

    detected = [
        emotion for emotion, score in scores.items()
        if score > 0
    ]

    intensity = round(min(confidence * 75, 100), 1)

    if intensity < 25:
        intensity_level = "low"
    elif intensity < 60:
        intensity_level = "medium"
    else:
        intensity_level = "high"

    positive = scores["joy"] + scores["surprise"]
    negative = (
        scores["sadness"]
        + scores["anger"]
        + scores["fear"]
        + scores["disgust"]
    )

    if positive > 0 and negative > 0:
        polarity = "mixed"
    elif positive > negative:
        polarity = "positive"
    elif negative > positive:
        polarity = "negative"
    else:
        polarity = "neutral"

    state = {
        "dominant_emotion": dominant,
        "multiple_emotions": detected,
        "confidence": confidence,
        "intensity": intensity,
        "intensity_level": intensity_level,
        "polarity": polarity,
        "mixed_emotional_state": positive > 0 and negative > 0,
        "emotional_state": dominant,
    }

    return state, scores


def build_recommendations(dominant_emotion):
    return [
        dict(item)
        for item in RECOMMENDATIONS.get(
            dominant_emotion, RECOMMENDATIONS["joy"]
        )
    ]


# --------------------------------------------------
# HELPER FUNCTIONS FOR HISTORY
# --------------------------------------------------

def get_recommendation_list(record):
    """Support list and nested-dictionary history formats."""
    items = record.get("recommendations", [])

    if isinstance(items, dict):
        items = items.get("recommendations", [])

    return items if isinstance(items, list) else []


def get_recommendation_title(item, rank):
    if isinstance(item, dict):
        return (
            item.get("title")
            or item.get("name")
            or item.get("recommendation")
            or item.get("activity")
            or item.get("recommendation_id")
            or item.get("id")
            or f"Recommendation {rank}"
        )

    return str(item)


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

st.title("🧠 MoodMentor")
st.subheader("Emotion Analysis & Personalized Wellness Dashboard")
st.write(
    "Enter your thoughts or feelings below. MoodMentor analyzes "
    "your text using keywords and displays wellness suggestions."
)
st.caption(
    "Note: This dashboard uses a simple keyword-based analysis, "
    "not the BERT/DistilBERT model."
)

# --------------------------------------------------
# INPUT AND CURRENT ANALYSIS
# --------------------------------------------------

st.divider()
st.header("Analyze Your Emotions")

user_text = st.text_area(
    "How are you feeling today?",
    placeholder="Example: I am feeling worried and anxious today.",
    height=120,
)

if st.button("Analyze Emotion", type="primary"):
    if not user_text.strip():
        st.warning("Please enter your thoughts or feelings first.")
    else:
        try:
            state, emotion_scores = analyze_emotion(user_text)
            recommendations = build_recommendations(
                state["dominant_emotion"]
            )

            save_emotion_record(emotion_scores)

            save_recommendation_history(
                user_text,
                state,
                emotion_scores,
                recommendations,
            )

            st.session_state["current_analysis"] = {
                "user_text": user_text,
                "state": state,
                "emotion_scores": emotion_scores,
                "recommendations": recommendations,
            }

            st.success("Emotion analysis completed!")

        except Exception as error:
            st.error("Could not complete the analysis.")
            st.exception(error)

# --------------------------------------------------
# DISPLAY CURRENT ANALYSIS
# --------------------------------------------------

current = st.session_state.get("current_analysis")

if current:
    state = current["state"]
    scores = current["emotion_scores"]
    recommendations = current["recommendations"]

    st.subheader("Your Emotional State")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Dominant Emotion",
        state["dominant_emotion"].capitalize(),
    )
    col2.metric("Confidence", f'{state["confidence"] * 100:.0f}%')
    col3.metric("Intensity", f'{state["intensity"]}%')

    st.write(
        "**Intensity level:**",
        state["intensity_level"].capitalize(),
    )
    st.write("**Polarity:**", state["polarity"].capitalize())
    st.write(
        "**Detected emotions:**",
        ", ".join(state["multiple_emotions"]).capitalize()
        if state["multiple_emotions"]
        else "None detected",
    )

    st.write("### Emotion Scores")
    score_frame = pd.DataFrame({
        "Emotion": list(scores.keys()),
        "Score": list(scores.values()),
    }).set_index("Emotion")

    st.bar_chart(score_frame, horizontal=True)

    st.subheader("Personalized Recommendations")

    for rank, item in enumerate(recommendations, start=1):
        with st.container(border=True):
            st.markdown(f"**{rank}. {item['title']}**")
            st.write(item["description"])
            st.write(f"Ranking score: {item['ranking_score']}")

            col_like, col_dislike = st.columns(2)

            if col_like.button("👍 Like", key=f"like_{rank}_{item['id']}"):
                try:
                    records = load_recommendation_history()

                    if records:
                        update_recommendation_feedback(
                            records[-1]["timestamp"],
                            item["id"],
                            "liked",
                        )

                    save_feedback(
                        item["id"],
                        item["title"],
                        "liked",
                    )
                    st.success("Feedback saved!")
                except Exception as error:
                    st.error("Could not save feedback.")
                    st.exception(error)

            if col_dislike.button(
                "👎 Dislike",
                key=f"dislike_{rank}_{item['id']}",
            ):
                try:
                    records = load_recommendation_history()

                    if records:
                        update_recommendation_feedback(
                            records[-1]["timestamp"],
                            item["id"],
                            "disliked",
                        )

                    save_feedback(
                        item["id"],
                        item["title"],
                        "disliked",
                    )
                    st.success("Feedback saved!")
                except Exception as error:
                    st.error("Could not save feedback.")
                    st.exception(error)

# --------------------------------------------------
# EMOTIONAL TRENDS
# --------------------------------------------------

st.divider()
st.header("Emotional Trends")

emotion_history = load_emotion_history()
st.write(f"Total emotion records: {len(emotion_history)}")

trend_period = st.selectbox(
    "Choose trend period",
    ["Daily", "Weekly", "Monthly"],
)

if emotion_history:
    if trend_period == "Daily":
        trend_data = calculate_daily_average(emotion_history)
    elif trend_period == "Weekly":
        trend_data = calculate_weekly_average(emotion_history)
    else:
        trend_data = calculate_monthly_average(emotion_history)

    if trend_data:
        trend_frame = pd.DataFrame.from_dict(
            trend_data,
            orient="index",
        ).fillna(0)

        trend_frame.index = trend_frame.index.map(str)
        st.line_chart(trend_frame)
    else:
        st.info("There is not enough data to display trends yet.")
else:
    st.info("Analyze some text to begin building emotion trends.")

# --------------------------------------------------
# RECOMMENDATION FEEDBACK HISTORY
# --------------------------------------------------

st.divider()
st.header("Recommendation Feedback History")

feedback_records = load_feedback_history()
st.write(f"Total feedback records: {len(feedback_records)}")

if feedback_records:
    for item in reversed(feedback_records):
        title = (
            item.get("title")
            or item.get("recommendation_title")
            or item.get("recommendation_name")
            or item.get("recommendation_id")
            or "Unknown"
        )

        st.write(f"**Recommendation:** {title}")
        st.write(
            "**Feedback:**",
            str(item.get("feedback", "Not provided")).capitalize(),
        )
        st.caption(
            f"Date: {item.get('timestamp', 'Unknown')} | "
            f"ID: {item.get('recommendation_id', 'Unknown')}"
        )
        st.divider()
else:
    st.info("No feedback submitted yet.")

# --------------------------------------------------
# COMPLETE RECOMMENDATION HISTORY
# --------------------------------------------------

st.divider()
st.header("Complete Recommendation History")

history_records = load_recommendation_history()
st.write(f"Total analyses: {len(history_records)}")

if history_records:
    for record in reversed(history_records):
        state = record.get("emotional_state", {})
        previous_scores = record.get("emotion_probabilities", {})
        previous_recommendations = get_recommendation_list(record)
        feedback = record.get("feedback", {})

        if not isinstance(state, dict):
            state = {}
        if not isinstance(previous_scores, dict):
            previous_scores = {}
        if not isinstance(feedback, dict):
            feedback = {}

        with st.expander(
            f"Analysis: {record.get('timestamp', 'Unknown')}"
        ):
            st.write("**Your input:**")
            st.write(record.get("user_text", ""))

            st.write(
                "**Dominant emotion:**",
                str(state.get("dominant_emotion", "Unknown")).capitalize(),
            )

            st.write(
                "**Intensity:**",
                f"{state.get('intensity', 'Unknown')}% "
                f"({state.get('intensity_level', 'Unknown')})",
            )

            st.write("**Emotion scores:**")

            if previous_scores:
                score_frame = pd.DataFrame({
                    "Emotion": list(previous_scores.keys()),
                    "Score (%)": [
                        round(score * 100, 1)
                        if isinstance(score, (int, float))
                        else score
                        for score in previous_scores.values()
                    ],
                })
                st.dataframe(score_frame, hide_index=True)
            else:
                st.write("No emotion scores available.")

            st.write("**Recommendations:**")

            if previous_recommendations:
                for rank, item in enumerate(
                    previous_recommendations, start=1
                ):
                    title = get_recommendation_title(item, rank)

                    if isinstance(item, dict):
                        recommendation_id = str(
                            item.get("id")
                            or item.get("recommendation_id")
                            or f"recommendation_{rank}"
                        )
                        description = item.get("description", "")
                        score = item.get(
                            "ranking_score",
                            item.get(
                                "hybrid_score",
                                item.get("score", ""),
                            ),
                        )
                        explanation = item.get("explanation", [])
                    else:
                        recommendation_id = f"recommendation_{rank}"
                        description = ""
                        score = ""
                        explanation = []

                    st.markdown(f"**{rank}. {title}**")
                    st.caption(f"Recommendation ID: {recommendation_id}")

                    if description:
                        st.write(description)

                    if score != "":
                        st.write(f"Ranking score: {score}")

                    if explanation:
                        st.write("**Why this was recommended:**")
                        if isinstance(explanation, list):
                            for reason in explanation:
                                st.write(f"- {reason}")
                        else:
                            st.write(explanation)

                    status = feedback.get(
                        recommendation_id,
                        "Not provided",
                    )
                    st.caption(f"Feedback: {str(status).capitalize()}")
                    st.divider()
            else:
                st.info("No recommendations recorded.")
else:
    st.info("No recommendation history available yet.")

# --------------------------------------------------
# SEARCH, FILTER AND EXPORT
# --------------------------------------------------

st.divider()
st.header("Search, Filter & Export Reports")

search_history = load_recommendation_history()

if search_history:
    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "Start date",
            value=None,
            key="report_start_date",
        )

    with col2:
        end_date = st.date_input(
            "End date",
            value=None,
            key="report_end_date",
        )

    selected_emotion = st.selectbox(
        "Filter by emotion",
        ["All", "joy", "sadness", "anger", "fear", "surprise", "disgust"],
    )

    selected_intensity = st.selectbox(
        "Filter by intensity",
        ["All", "low", "moderate", "medium", "high"],
    )

    selected_feedback = st.selectbox(
        "Filter by feedback",
        ["All", "liked", "disliked", "not provided"],
    )

    search_title = st.text_input(
        "Search recommendation title",
        placeholder="Enter a recommendation name",
    )

    try:
        filtered_records = filter_recommendation_history(
            search_history,
            start_date=start_date,
            end_date=end_date,
            emotion=selected_emotion,
            intensity=selected_intensity,
            recommendation_type="All",
            feedback_status=selected_feedback,
        )

        if search_title.strip():
            search_term = search_title.strip().lower()

            filtered_records = [
                record
                for record in filtered_records
                if any(
                    search_term in get_recommendation_title(
                        item, rank
                    ).lower()
                    for rank, item in enumerate(
                        get_recommendation_list(record), start=1
                    )
                )
            ]

        st.write(f"Matching analyses: {len(filtered_records)}")

        if filtered_records:
            st.subheader("Filtered Results")

            for record in filtered_records:
                st.write(
                    f"**Date:** {record.get('timestamp', 'Unknown')}"
                )
                st.write(f"**Input:** {record.get('user_text', '')}")

                state = record.get("emotional_state", {})
                if not isinstance(state, dict):
                    state = {}

                st.write(
                    "**Dominant emotion:** "
                    + str(state.get("dominant_emotion", "Unknown"))
                )

                titles = [
                    get_recommendation_title(item, rank)
                    for rank, item in enumerate(
                        get_recommendation_list(record), start=1
                    )
                ]

                if titles:
                    st.write("**Recommendations:** " + ", ".join(titles))

                st.divider()

            csv_data = generate_csv_report(filtered_records)
            pdf_data = generate_pdf_report(filtered_records)

            col_csv, col_pdf = st.columns(2)

            with col_csv:
                st.download_button(
                    "Download CSV Report",
                    data=csv_data,
                    file_name="moodmentor_report.csv",
                    mime="text/csv",
                )

            with col_pdf:
                st.download_button(
                    "Download PDF Report",
                    data=pdf_data,
                    file_name="moodmentor_report.pdf",
                    mime="application/pdf",
                )
        else:
            st.info("No records match the selected filters.")

    except Exception as error:
        st.error("Could not filter or export the report.")
        st.exception(error)

else:
    st.info("No history records available to search or export.")