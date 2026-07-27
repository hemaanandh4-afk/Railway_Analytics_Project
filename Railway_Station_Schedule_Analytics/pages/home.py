import streamlit as st

from utils import PROJECT_TITLE, dataset_profile, kpi_value, metric_card


def render(df):
    st.title(f"🚆 {PROJECT_TITLE}")
    st.markdown("A professional dashboard for analyzing railway stations, schedules, train movement patterns, routes, zones, and operational performance using the uploaded railway dataset only.")

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("Total Trains", f"{kpi_value(df, 'train_number'):,}")
    with c2: metric_card("Total Stations", f"{kpi_value(df, 'station_name'):,}")
    with c3: metric_card("Railway Zones", f"{kpi_value(df, 'train_zone'):,}")
    with c4: metric_card("Train Types", f"{kpi_value(df, 'train_type'):,}")
    with c5:
        routes = df[["from_station_name", "to_station_name"]].drop_duplicates().shape[0] if {"from_station_name", "to_station_name"}.issubset(df.columns) else 0
        metric_card("Total Routes", f"{routes:,}")

    st.subheader("Dataset Summary")
    st.write(f"The cleaned working dataset contains **{df.shape[0]:,} records** and **{df.shape[1]:,} columns** after notebook-style duplicate removal and missing-value handling.")
    st.dataframe(dataset_profile(df), use_container_width=True, hide_index=True)

    st.subheader("Sample Records")
    st.dataframe(df.head(25), use_container_width=True)
