import streamlit as st

from utils import filtered_data_controls


def render(df):
    st.title("🔎 Data Explorer")
    data = filtered_data_controls(df, "explorer")
    query = st.text_input("Global search")
    if query:
        text_cols = data.select_dtypes(include="object").columns
        mask = False
        for col in text_cols:
            mask = mask | data[col].astype(str).str.contains(query, case=False, na=False)
        data = data[mask]
    sort_col = st.selectbox("Sort by", data.columns.tolist())
    ascending = st.toggle("Ascending", value=True)
    data = data.sort_values(sort_col, ascending=ascending, kind="mergesort")
    st.caption(f"{len(data):,} records selected")
    st.download_button("Download filtered CSV", data.to_csv(index=False).encode("utf-8"), "filtered_railway_data.csv", "text/csv")
    st.dataframe(data, use_container_width=True, hide_index=True)
