
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

EMOTIONS = [
    "joy",
    "sadness",
    "anger",
    "fear",
    "surprise",
    "disgust",
]


def show_emotion_trend(daily_data, period_name="Daily"):
    """Display readable emotion trends over time."""

    if not daily_data:
        st.info("No emotion history available yet.")
        return

    dates = sorted(daily_data.keys())

    chart_data = pd.DataFrame(
        {
            emotion.capitalize(): [
                daily_data[date].get(emotion, 0.0)
                for date in dates
            ]
            for emotion in EMOTIONS
        },
        index=[str(date) for date in dates],
    )

    st.subheader(f"{period_name} Emotion Trends")

    fig, ax = plt.subplots(figsize=(10, 5))

    for emotion in chart_data.columns:
        ax.plot(
            chart_data.index,
            chart_data[emotion],
            marker="o",
            label=emotion,
        )

    ax.set_xlabel("Date")
    ax.set_ylabel("Average Emotion Score")
    ax.set_title(f"{period_name} Emotion Trends")
    ax.set_ylim(0, 1)
    ax.legend(title="Emotions", bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(True, alpha=0.3)

    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.caption(
        f"Showing {len(dates)} {period_name.lower()} data point(s)."
    )