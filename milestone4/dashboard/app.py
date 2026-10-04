import streamlit as st
import pandas as pd
from datetime import datetime

from milestone4.data.history import (
    load_emotion_history,
    save_emotion_record,
)

from milestone4.data.trend import (
    calculate_daily_average,
    calculate_weekly_average,
    calculate_monthly_average,
    get_dominant_emotion,
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

from milestone4.data.search_filter import (
    filter_recommendation_history,
)

from milestone4.reports.export_reports import (
    generate_csv_report,
    generate_pdf_report,
)


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="MoodMentor",
    page_icon="🧠",
    layout="wide",
)


# ==================================================
# TITLE
# ==================================================

st.title("🧠 MoodMentor")

st.subheader(
    "Emotion Analysis & Personalized Wellness Dashboard"
)

st.write(
    "Enter your thoughts or feelings below. "
    "MoodMentor analyzes your text using keywords "
    "and displays wellness suggestions."
)

st.info(
    "Note: This dashboard uses a simple keyword-based "
    "analysis, not the BERT/DistilBERT model."
)


# ==================================================
# EMOTION DEFINITIONS
# ==================================================

EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]


# ==================================================
# RECOMMENDATION DATA
# ==================================================

RECOMMENDATIONS = {
    "joy": [
        {
            "id": "joy_activity",
            "title": "Explore a fun activity",
            "description": (
                "Try a hobby or activity that you enjoy."
            ),
            "category": "fun",
        },
        {
            "id": "learn_something",
            "title": "Learn something new",
            "description": (
                "Explore a topic that interests you."
            ),
            "category": "learning",
        },
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
    ],
    "fear": [
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": (
                "Choose music you enjoy and take a quiet break."
            ),
            "category": "music",
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": (
                "Write a few words about what is on your mind."
            ),
            "category": "journaling",
        },
    ],
    "sadness": [
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": (
                "Choose music you enjoy and take a quiet break."
            ),
            "category": "music",
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": (
                "Write a few words about what is on your mind."
            ),
            "category": "journaling",
        },
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
    ],
    "anger": [
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": (
                "Choose music you enjoy and take a quiet break."
            ),
            "category": "music",
        },
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": (
                "Write a few words about what is on your mind."
            ),
            "category": "journaling",
        },
    ],
    "surprise": [
        {
            "id": "joy_activity",
            "title": "Explore a fun activity",
            "description": (
                "Try a hobby or activity that you enjoy."
            ),
            "category": "fun",
        },
        {
            "id": "learn_something",
            "title": "Learn something new",
            "description": (
                "Explore a topic that interests you."
            ),
            "category": "learning",
        },
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
    ],
    "disgust": [
        {
            "id": "journal",
            "title": "Write a short journal entry",
            "description": (
                "Write a few words about what is on your mind."
            ),
            "category": "journaling",
        },
        {
            "id": "calm_breathing",
            "title": "Try a short breathing exercise",
            "description": (
                "Take a comfortable pause and breathe slowly."
            ),
            "category": "relaxation",
        },
        {
            "id": "calm_music",
            "title": "Listen to calming music",
            "description": (
                "Choose music you enjoy and take a quiet break."
            ),
            "category": "music",
        },
    ],
}


# ==================================================
# EMOTION KEYWORDS
# ==================================================

KEYWORDS = {
    "joy": [
        "happy",
        "joy",
        "excited",
        "good",
        "great",
        "love",
        "wonderful",
        "cheerful",
    ],
    "sadness": [
        "sad",
        "unhappy",
        "cry",
        "lonely",
        "upset",
        "depressed",
        "hurt",
    ],
    "anger": [
        "angry",
        "anger",
        "mad",
        "furious",
        "annoyed",
        "irritated",
        "rage",
    ],
    "fear": [
        "afraid",
        "fear",
        "scared",
        "worried",
        "anxious",
        "nervous",
        "panic",
    ],
    "surprise": [
        "surprised",
        "surprise",
        "shocked",
        "unexpected",
        "amazed",
    ],
    "disgust": [
        "disgust",
        "disgusted",
        "gross",
        "hate",
        "awful",
    ],
}


# ==================================================
# EMOTION ANALYSIS
# ==================================================

def analyze_emotion(text):

    text_lower = text.lower()

    emotion_scores = {}

    for emotion in EMOTIONS:

        count = 0

        for keyword in KEYWORDS[emotion]:

            if keyword in text_lower:
                count += 1

        emotion_scores[emotion] = round(
            min(count * 0.2, 1.0),
            2,
        )

    dominant_emotion = max(
        emotion_scores,
        key=emotion_scores.get,
    )

    max_score = emotion_scores[dominant_emotion]

    detected_emotions = [
        emotion
        for emotion, score
        in emotion_scores.items()
        if score > 0
    ]

    confidence = max_score

    intensity = round(
        confidence * 75,
        1,
    )

    if intensity >= 60:
        intensity_level = "high"
    elif intensity >= 30:
        intensity_level = "medium"
    else:
        intensity_level = "low"

    positive_score = (
        emotion_scores["joy"]
        + emotion_scores["surprise"]
    )

    negative_score = (
        emotion_scores["sadness"]
        + emotion_scores["anger"]
        + emotion_scores["fear"]
        + emotion_scores["disgust"]
    )

    if (
        positive_score > 0
        and negative_score > 0
    ):
        polarity = "mixed"
    elif positive_score > negative_score:
        polarity = "positive"
    elif negative_score > positive_score:
        polarity = "negative"
    else:
        polarity = "neutral"

    mixed_state = len(detected_emotions) > 1

    if not detected_emotions:

        dominant_emotion = "joy"
        confidence = 0.0
        intensity = 0.0
        intensity_level = "low"
        polarity = "neutral"
        mixed_state = False

    return {
        "dominant_emotion": dominant_emotion,
        "multiple_emotions": detected_emotions,
        "confidence": confidence,
        "intensity": intensity,
        "intensity_level": intensity_level,
        "polarity": polarity,
        "mixed_emotional_state": mixed_state,
        "emotional_state": dominant_emotion,
        "emotion_probabilities": emotion_scores,
    }


# ==================================================
# RECOMMENDATIONS
# ==================================================

def generate_recommendations(
    dominant_emotion,
    emotion_scores,
):

    recommendations = RECOMMENDATIONS.get(
        dominant_emotion,
        [],
    )

    result = []

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        item = recommendation.copy()

        score = round(
            5.0
            + emotion_scores.get(
                dominant_emotion,
                0,
            ) * 2.5
            - (index - 1) * 0.25,
            2,
        )

        item["ranking_score"] = score

        result.append(item)

    return result


# ==================================================
# ANALYZE YOUR EMOTIONS
# ==================================================

st.divider()

st.header("Analyze Your Emotions")

user_text = st.text_area(
    "Enter your thoughts or feelings:",
    height=120,
    placeholder=(
        "Example: I am feeling worried and anxious today."
    ),
)

analyze_button = st.button(
    "Analyze Emotion",
    type="primary",
)


if analyze_button:

    if not user_text.strip():

        st.warning(
            "Please enter some text before analyzing."
        )

    else:

        analysis = analyze_emotion(
            user_text
        )

        emotion_scores = analysis[
            "emotion_probabilities"
        ]

        dominant_emotion = analysis[
            "dominant_emotion"
        ]

        recommendations = (
            generate_recommendations(
                dominant_emotion,
                emotion_scores,
            )
        )

        timestamp = datetime.now().isoformat(
            timespec="seconds"
        )

        save_emotion_record(
            emotion_scores,
            timestamp=timestamp,
        )

        save_recommendation_history(
            user_text,
            analysis,
            emotion_scores,
            recommendations,
        )

        st.session_state[
            "latest_analysis"
        ] = analysis

        st.session_state[
            "latest_recommendations"
        ] = recommendations

        st.success(
            "Emotion analysis completed."
        )


# ==================================================
# DISPLAY LATEST ANALYSIS
# ==================================================

if "latest_analysis" in st.session_state:

    analysis = st.session_state[
        "latest_analysis"
    ]

    recommendations = st.session_state.get(
        "latest_recommendations",
        [],
    )

    st.subheader(
        "Latest Emotion Analysis"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Dominant Emotion",
            str(
                analysis[
                    "dominant_emotion"
                ]
            ).capitalize(),
        )

    with col2:

        st.metric(
            "Confidence",
            f"{analysis['confidence'] * 100:.1f}%",
        )

    with col3:

        st.metric(
            "Intensity",
            f"{analysis['intensity']}%",
        )

    st.write(
        "**Polarity:**",
        analysis["polarity"].capitalize(),
    )

    st.write(
        "**Multiple emotions:**",
        ", ".join(
            analysis["multiple_emotions"]
        )
        if analysis["multiple_emotions"]
        else "None",
    )

    st.write(
        "**Emotional state:**",
        analysis["emotional_state"].capitalize(),
    )

    st.write(
        "**Intensity level:**",
        analysis["intensity_level"].capitalize(),
    )

    st.subheader(
        "Emotion Scores"
    )

    score_data = pd.DataFrame(
        {
            "Emotion": list(
                analysis[
                    "emotion_probabilities"
                ].keys()
            ),
            "Score (%)": [
                round(
                    score * 100,
                    1,
                )
                for score in analysis[
                    "emotion_probabilities"
                ].values()
            ],
        }
    )

    st.dataframe(
        score_data,
        hide_index=True,
    )

    st.subheader(
        "Personalized Wellness Suggestions"
    )

    for rank, recommendation in enumerate(
        recommendations,
        start=1,
    ):

        st.markdown(
            f"**{rank}. "
            f"{recommendation['title']}**"
        )

        st.write(
            recommendation["description"]
        )

        st.caption(
            f"Category: "
            f"{recommendation.get('category', '')} | "
            f"Ranking score: "
            f"{recommendation.get('ranking_score', '')}"
        )

        recommendation_id = (
            recommendation["id"]
        )

        feedback_col1, feedback_col2 = st.columns(2)

        with feedback_col1:

            if st.button(
                "👍 Like",
                key=f"latest_like_{recommendation_id}",
            ):

                save_feedback(
                    recommendation_id,
                    recommendation["title"],
                    "liked",
                )

                update_recommendation_feedback(
                    datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    recommendation_id,
                    "liked",
                )

                st.success(
                    "Feedback saved: Liked"
                )

        with feedback_col2:

            if st.button(
                "👎 Dislike",
                key=f"latest_dislike_{recommendation_id}",
            ):

                save_feedback(
                    recommendation_id,
                    recommendation["title"],
                    "disliked",
                )

                update_recommendation_feedback(
                    datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    recommendation_id,
                    "disliked",
                )

                st.warning(
                    "Feedback saved: Disliked"
                )

        st.divider()


# ==================================================
# EMOTIONAL TRENDS
# ==================================================

st.divider()

st.header("Emotional Trends")

emotion_history = load_emotion_history()

st.write(
    f"Total emotion records: "
    f"{len(emotion_history)}"
)

if emotion_history:

    daily_average = calculate_daily_average(
        emotion_history
    )

    if daily_average:

        trend_frame = pd.DataFrame(
            daily_average
        ).T

        trend_frame.index.name = "Date"

        st.line_chart(
            trend_frame
        )

    else:

        st.info(
            "Not enough data for daily trends."
        )

else:

    st.info(
        "No emotion history available yet."
    )


# ==================================================
# RECOMMENDATION FEEDBACK HISTORY
# ==================================================

st.divider()

st.header(
    "Recommendation Feedback History"
)

feedback_records = load_feedback_history()

st.write(
    f"Total feedback records: "
    f"{len(feedback_records)}"
)

if feedback_records:

    for feedback_record in reversed(
        feedback_records
    ):

        st.write(
            f"**Recommendation:** "
            f"{feedback_record.get('recommendation', '')}"
        )

        st.write(
            f"**Feedback:** "
            f"{str(feedback_record.get('feedback', '')).capitalize()}"
        )

        st.caption(
            f"Date: "
            f"{feedback_record.get('timestamp', 'Unknown')}"
            f" | ID: "
            f"{feedback_record.get('recommendation_id', 'Unknown')}"
        )

        st.divider()

else:

    st.info(
        "No recommendation feedback available yet."
    )


# ==================================================
# COMPLETE RECOMMENDATION HISTORY
# ==================================================

st.divider()

st.header(
    "Complete Recommendation History"
)

history_records = load_recommendation_history()

st.write(
    f"Total analyses: {len(history_records)}"
)

if history_records:

    for record in reversed(history_records):

        state = record.get(
            "emotional_state",
            {},
        )

        previous_scores = record.get(
            "emotion_probabilities",
            {},
        )

        recommendations = record.get(
            "recommendations",
            [],
        )

        feedback = record.get(
            "feedback",
            {},
        )

        if not isinstance(
            state,
            dict,
        ):
            state = {}

        if not isinstance(
            previous_scores,
            dict,
        ):
            previous_scores = {}

        if not isinstance(
            recommendations,
            list,
        ):
            recommendations = []

        if not isinstance(
            feedback,
            dict,
        ):
            feedback = {}

        with st.expander(
            f"Analysis: "
            f"{record.get('timestamp', 'Unknown')}"
        ):

            # INPUT
            st.write(
                "**Your input:**"
            )

            st.write(
                record.get(
                    "user_text",
                    "No input recorded.",
                )
            )

            # DOMINANT EMOTION
            st.write(
                "**Dominant emotion:**",
                str(
                    state.get(
                        "dominant_emotion",
                        "Unknown",
                    )
                ).capitalize(),
            )

            # INTENSITY
            intensity = state.get(
                "intensity",
                "Unknown",
            )

            intensity_level = state.get(
                "intensity_level",
                "Unknown",
            )

            st.write(
                "**Intensity:**",
                f"{intensity}% "
                f"({intensity_level})",
            )

            # EMOTION SCORES
            st.write(
                "**Emotion scores:**"
            )

            if previous_scores:

                score_rows = []

                for emotion, score in (
                    previous_scores.items()
                ):

                    if isinstance(
                        score,
                        (int, float),
                    ):

                        score_value = round(
                            score * 100,
                            1,
                        )

                    else:

                        score_value = score

                    score_rows.append(
                        {
                            "Emotion": emotion,
                            "Score (%)": score_value,
                        }
                    )

                score_frame = pd.DataFrame(
                    score_rows
                )

                st.dataframe(
                    score_frame,
                    hide_index=True,
                )

            else:

                st.write(
                    "No emotion scores available."
                )

            # RECOMMENDATIONS
            st.write(
                "**Recommendations:**"
            )

            if recommendations:

                for rank, recommendation in enumerate(
                    recommendations,
                    start=1,
                ):

                    if not isinstance(
                        recommendation,
                        dict,
                    ):

                        st.write(
                            f"{rank}. "
                            f"{str(recommendation)}"
                        )

                        continue

                    recommendation_id = str(
                        recommendation.get(
                            "id",
                            f"recommendation_{rank}",
                        )
                    )

                    title = str(
                        recommendation.get(
                            "title",
                            recommendation_id,
                        )
                    )

                    description = recommendation.get(
                        "description",
                        "",
                    )

                    ranking_score = recommendation.get(
                        "ranking_score",
                        "",
                    )

                    category = recommendation.get(
                        "category",
                        "",
                    )

                    st.markdown(
                        f"### {rank}. {title}"
                    )

                    st.write(
                        f"**Recommendation ID:** "
                        f"{recommendation_id}"
                    )

                    if category:

                        st.write(
                            f"**Category:** "
                            f"{category}"
                        )

                    if description:

                        st.write(
                            description
                        )

                    if ranking_score != "":

                        st.write(
                            f"**Ranking score:** "
                            f"{ranking_score}"
                        )

                    explanation = recommendation.get(
                        "explanation",
                        [],
                    )

                    if explanation:

                        st.write(
                            "**Why this was recommended:**"
                        )

                        if isinstance(
                            explanation,
                            list,
                        ):

                            for reason in explanation:

                                st.write(
                                    f"• {reason}"
                                )

                        else:

                            st.write(
                                str(explanation)
                            )

                    feedback_status = feedback.get(
                        recommendation_id,
                        "Not provided",
                    )

                    st.write(
                        f"**Feedback:** "
                        f"{str(feedback_status).capitalize()}"
                    )

                    st.divider()

            else:

                st.info(
                    "No recommendations recorded."
                )

else:

    st.info(
        "No recommendation history available yet."
    )


# ==================================================
# SEARCH, FILTER & EXPORT REPORTS
# ==================================================

st.divider()

st.header(
    "Search, Filter & Export Reports"
)


col1, col2 = st.columns(2)

with col1:

    start_date = st.date_input(
        "Start date",
        value=None,
    )

with col2:

    end_date = st.date_input(
        "End date",
        value=None,
    )


emotion_filter = st.selectbox(
    "Emotion",
    [
        "All",
        "joy",
        "sadness",
        "anger",
        "fear",
        "surprise",
        "disgust",
    ],
)


intensity_filter = st.selectbox(
    "Intensity",
    [
        "All",
        "low",
        "medium",
        "high",
    ],
)


recommendation_type_filter = st.selectbox(
    "Recommendation type",
    [
        "All",
        "relaxation",
        "music",
        "journaling",
        "fun",
        "learning",
    ],
)


feedback_filter = st.selectbox(
    "Feedback status",
    [
        "All",
        "liked",
        "disliked",
        "Not provided",
    ],
)


filtered_records = filter_recommendation_history(
    history_records,
    start_date=start_date,
    end_date=end_date,
    emotion=emotion_filter,
    intensity=intensity_filter,
    recommendation_type=recommendation_type_filter,
    feedback_status=feedback_filter,
)


st.write(
    f"Matching analyses: "
    f"{len(filtered_records)}"
)


st.subheader(
    "Filtered Results"
)


if filtered_records:

    for record in filtered_records:

        state = record.get(
            "emotional_state",
            {},
        )

        recommendations = record.get(
            "recommendations",
            [],
        )

        st.write(
            f"**Date:** "
            f"{record.get('timestamp', 'Unknown')}"
        )

        st.write(
            f"**Input:** "
            f"{record.get('user_text', '')}"
        )

        st.write(
            f"**Dominant emotion:** "
            f"{state.get('dominant_emotion', 'Unknown')}"
        )

        titles = []

        if isinstance(
            recommendations,
            list,
        ):

            for recommendation in recommendations:

                if isinstance(
                    recommendation,
                    dict,
                ):

                    titles.append(
                        recommendation.get(
                            "title",
                            recommendation.get(
                                "id",
                                "Unknown",
                            ),
                        )
                    )

                else:

                    titles.append(
                        str(recommendation)
                    )

        st.write(
            "**Recommendations:** "
            + (
                ", ".join(
                    titles
                )
                if titles
                else "None"
            )
        )

        st.divider()

else:

    st.info(
        "No records match the selected filters."
    )


# ==================================================
# EXPORT REPORTS
# ==================================================

st.subheader(
    "Export Reports"
)


export_col1, export_col2 = st.columns(2)


with export_col1:

    if st.button(
        "Export CSV",
        key="export_csv",
    ):

        csv_data = generate_csv_report(
            filtered_records
        )

        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="moodmentor_report.csv",
            mime="text/csv",
            key="download_csv",
        )


with export_col2:

    if st.button(
        "Export PDF",
        key="export_pdf",
    ):

        pdf_data = generate_pdf_report(
            filtered_records
        )

        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="moodmentor_report.pdf",
            mime="application/pdf",
            key="download_pdf",
        )


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "MoodMentor | Milestone 4 Dashboard"
)