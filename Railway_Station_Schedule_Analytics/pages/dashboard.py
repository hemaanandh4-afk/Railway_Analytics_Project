import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils import filtered_data_controls


def _bar_counts(df, col, title, n=20):
    counts = df[col].value_counts().head(n).reset_index()
    counts.columns = [col, "records"]
    return px.bar(counts, x="records", y=col, orientation="h", title=title, text="records")


def render(df):
    st.title("📊 Interactive Railway Dashboard")
    data = filtered_data_controls(df, "dashboard")
    st.caption(f"Showing {len(data):,} filtered records from {len(df):,} total records.")

    tab1, tab2, tab3, tab4 = st.tabs(["Stations & Routes", "Zones & Types", "Time Patterns", "Distance & Duration"])

    with tab1:
        c1, c2 = st.columns(2)
        if "station_name" in data.columns:
            c1.plotly_chart(_bar_counts(data, "station_name", "Top Busiest Stations"), use_container_width=True)
            freq = data.groupby("station_name").size().reset_index(name="stop_frequency")
            c2.plotly_chart(px.histogram(freq, x="stop_frequency", nbins=40, title="Station-wise Train Frequency Distribution"), use_container_width=True)
        c3, c4 = st.columns(2)
        if "from_station_name" in data.columns:
            c3.plotly_chart(_bar_counts(data, "from_station_name", "Top Source Stations"), use_container_width=True)
        if "to_station_name" in data.columns:
            c4.plotly_chart(_bar_counts(data, "to_station_name", "Top Destination Stations"), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        if "train_zone" in data.columns:
            c1.plotly_chart(px.pie(data, names="train_zone", title="Railway Zone Distribution", hole=.35), use_container_width=True)
        if "train_type" in data.columns:
            c2.plotly_chart(px.bar(data["train_type"].value_counts().reset_index(name="records"), x="train_type", y="records", title="Train Type Distribution"), use_container_width=True)

    with tab3:
        c1, c2 = st.columns(2)
        if "arrival_hour" in data.columns:
            arrivals = data["arrival_hour"].dropna().astype(int).value_counts().sort_index().reindex(range(24), fill_value=0)
            c1.plotly_chart(px.line(x=arrivals.index, y=arrivals.values, markers=True, title="Arrival Hour Distribution", labels={"x":"Hour", "y":"Arrivals"}), use_container_width=True)
        if "departure_hour" in data.columns:
            departures = data["departure_hour"].dropna().astype(int).value_counts().sort_index().reindex(range(24), fill_value=0)
            c2.plotly_chart(px.line(x=departures.index, y=departures.values, markers=True, title="Departure Hour Distribution", labels={"x":"Hour", "y":"Departures"}), use_container_width=True)
        if "schedule_day" in data.columns:
            day = data["schedule_day"].dropna().astype(int).value_counts().sort_index().reset_index()
            day.columns = ["schedule_day", "records"]
            st.plotly_chart(px.bar(day, x="schedule_day", y="records", title="Schedule Day Analysis"), use_container_width=True)
        if {"arrival_hour", "departure_hour"}.issubset(data.columns):
            heat = pd.DataFrame({
                "Arrivals": data["arrival_hour"].dropna().astype(int).value_counts().sort_index().reindex(range(24), fill_value=0),
                "Departures": data["departure_hour"].dropna().astype(int).value_counts().sort_index().reindex(range(24), fill_value=0),
            }).T
            st.plotly_chart(go.Figure(data=go.Heatmap(z=heat.values, x=list(range(24)), y=heat.index, colorscale="YlGnBu", text=heat.values, texttemplate="%{text}"), layout_title_text="Heatmap of Train Activity by Hour"), use_container_width=True)

    with tab4:
        c1, c2 = st.columns(2)
        if "distance" in data.columns:
            c1.plotly_chart(px.histogram(data, x="distance", nbins=35, marginal="box", title="Distance Distribution"), use_container_width=True)
            longest = data.sort_values("distance", ascending=False).drop_duplicates(["train_number", "from_station_name", "to_station_name"]).head(15)
            c1.plotly_chart(px.bar(longest, x="distance", y="train_name", orientation="h", title="Longest Distance Routes", hover_data=[c for c in ["train_number", "from_station_name", "to_station_name"] if c in data.columns]), use_container_width=True)
        if "duration_h" in data.columns:
            c2.plotly_chart(px.histogram(data, x="duration_h", nbins=35, marginal="box", title="Journey Duration Distribution (Hours)"), use_container_width=True)
            longest_d = data.sort_values("duration_h", ascending=False).drop_duplicates(["train_number", "from_station_name", "to_station_name"]).head(15)
            c2.plotly_chart(px.bar(longest_d, x="duration_h", y="train_name", orientation="h", title="Longest Duration Routes", hover_data=[c for c in ["train_number", "from_station_name", "to_station_name"] if c in data.columns]), use_container_width=True)
