import streamlit as st


def render(df):
    st.title("💡 Business Insights")
    insights = []
    if "station_name" in df.columns:
        top = df["station_name"].value_counts().head(1)
        if not top.empty: insights.append(("Busiest station", f"{top.index[0]} has the highest schedule activity with {int(top.iloc[0]):,} records."))
    if "from_station_name" in df.columns:
        top = df["from_station_name"].value_counts().head(1)
        if not top.empty: insights.append(("Strongest origin station", f"{top.index[0]} appears most often as a source station with {int(top.iloc[0]):,} records."))
    if "to_station_name" in df.columns:
        top = df["to_station_name"].value_counts().head(1)
        if not top.empty: insights.append(("Strongest destination station", f"{top.index[0]} appears most often as a destination station with {int(top.iloc[0]):,} records."))
    if "train_zone" in df.columns:
        top = df["train_zone"].value_counts().head(1)
        if not top.empty: insights.append(("Dominant railway zone", f"{top.index[0]} contributes the largest share of records ({int(top.iloc[0]):,})."))
    if "train_type" in df.columns:
        top = df["train_type"].value_counts().head(1)
        if not top.empty: insights.append(("Most common train type", f"{top.index[0]} is the most frequent train type in the dataset."))
    if "arrival_hour" in df.columns:
        top = df["arrival_hour"].dropna().astype(int).value_counts().head(1)
        if not top.empty: insights.append(("Peak arrival hour", f"Hour {int(top.index[0]):02d}:00 has the highest arrival activity."))
    if "departure_hour" in df.columns:
        top = df["departure_hour"].dropna().astype(int).value_counts().head(1)
        if not top.empty: insights.append(("Peak departure hour", f"Hour {int(top.index[0]):02d}:00 has the highest departure activity."))
    if "distance" in df.columns:
        insights.append(("Distance profile", f"Average route distance is {df['distance'].mean():,.1f} km; maximum observed distance is {df['distance'].max():,.1f} km."))
    if "duration_h" in df.columns:
        insights.append(("Duration profile", f"Average journey duration is {df['duration_h'].mean():,.1f} hours; maximum observed duration is {df['duration_h'].max():,.1f} hours."))

    if not insights:
        st.warning("No supported insight columns are available in the uploaded dataset.")
    for title, text in insights:
        st.markdown(f"<div class='insight-card'><strong>{title}</strong><br>{text}</div>", unsafe_allow_html=True)
