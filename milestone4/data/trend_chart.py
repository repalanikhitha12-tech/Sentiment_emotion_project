
import pandas as pd
import streamlit as st


EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]


def show_emotion_trend(daily_data, period_name="Daily"):
    """Display emotion trends with dates on the X-axis."""

    if not daily_data:
        st.info("No emotion history available yet.")
        return

    dates = sorted(daily_data.keys())

    chart_data = pd.DataFrame(
        {
            "Date": [str(date) for date in dates],
            **{
                emotion.capitalize(): [
                    daily_data[date].get(emotion, 0.0)
                    for date in dates
                ]
                for emotion in EMOTIONS
            },
        }
    )

    chart_data = chart_data.set_index("Date")

    st.subheader(f"{period_name} Emotion Trends")
    st.line_chart(chart_data, y=list(chart_data.columns))

    st.caption(
        f"Showing {len(dates)} {period_name.lower()} data point(s)."
    )