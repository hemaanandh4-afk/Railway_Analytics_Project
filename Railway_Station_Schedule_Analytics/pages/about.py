import streamlit as st

from utils import PROJECT_TITLE


def render(df):
    st.title("ℹ️ About")
    st.subheader(PROJECT_TITLE)
    st.write("This Streamlit system helps railway administrators analyze train schedules, station operations, route patterns, journey duration, railway zones, and train activity using only the uploaded railway dataset.")
    st.subheader("Technologies Used")
    st.markdown("- Streamlit\n- Pandas\n- NumPy\n- Plotly Express\n- Plotly Graph Objects\n- OpenPyXL for Excel support")
    st.subheader("Dataset Description")
    st.write(f"Current dataset shape: **{df.shape[0]:,} rows × {df.shape[1]:,} columns**.")
    st.write("Available columns:")
    st.code(", ".join(df.columns))
    st.subheader("Administrative Benefits")
    st.markdown("- Identify busy stations and high-demand routes.\n- Monitor arrival and departure peaks by hour.\n- Compare railway zone and train type contributions.\n- Explore source-destination schedules and train details.\n- Download filtered operational data for reporting.")
