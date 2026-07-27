import streamlit as st


def render(df):
    st.title("🧭 Route Explorer")
    required = {"from_station_name", "to_station_name"}
    if not required.issubset(df.columns):
        st.error("Route Explorer requires `from_station_name` and `to_station_name` columns, which are not both present.")
        return
    c1, c2 = st.columns(2)
    sources = sorted(df["from_station_name"].dropna().astype(str).unique())
    source = c1.selectbox("Source station", ["All"] + sources)
    route_df = df if source == "All" else df[df["from_station_name"].astype(str) == source]
    destinations = sorted(route_df["to_station_name"].dropna().astype(str).unique())
    dest = c2.selectbox("Destination station", ["All"] + destinations)
    if dest != "All": route_df = route_df[route_df["to_station_name"].astype(str) == dest]
    search = st.text_input("Search train number or train name")
    if search and {"train_number", "train_name"}.issubset(route_df.columns):
        mask = route_df["train_number"].astype(str).str.contains(search, case=False, na=False) | route_df["train_name"].astype(str).str.contains(search, case=False, na=False)
        route_df = route_df[mask]
    st.metric("Matching schedule records", f"{len(route_df):,}")
    cols = [c for c in ["train_number", "train_name", "train_type", "train_zone", "from_station_name", "to_station_name", "station_name", "arrival", "departure", "schedule_day", "distance", "duration_h"] if c in route_df.columns]
    st.dataframe(route_df[cols].drop_duplicates(), use_container_width=True, hide_index=True)
