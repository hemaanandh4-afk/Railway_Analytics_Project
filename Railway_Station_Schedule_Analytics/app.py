import streamlit as st

from utils import PROJECT_TITLE, get_data, inject_global_css
from pages import about, dashboard, data_explorer, home, insights, route_explorer

st.set_page_config(page_title=PROJECT_TITLE, page_icon="🚆", layout="wide")
inject_global_css()

PAGES = {
    "Home": home.render,
    "Dashboard": dashboard.render,
    "Business Insights": insights.render,
    "Route Explorer": route_explorer.render,
    "Data Explorer": data_explorer.render,
    "About": about.render,
}

st.sidebar.title("🚆 Railway Analytics")
page_name = st.sidebar.radio("Navigate", list(PAGES.keys()))
df = get_data()

if df is None:
    st.title(PROJECT_TITLE)
    st.info("Place your cleaned dataset in `Railway_Station_Schedule_Analytics/data/` or upload it from the sidebar. The app uses only the columns available in your uploaded data.")
else:
    PAGES[page_name](df)
