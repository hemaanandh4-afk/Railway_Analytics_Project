from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd
import streamlit as st

PROJECT_TITLE = "Railway Station and Schedule Analytical System"
DATA_COLUMNS = [
    "train_number", "train_name", "train_zone", "train_type", "from_station_name",
    "to_station_name", "station_name", "station_state", "arrival", "departure",
    "schedule_day", "distance", "duration_h", "duration_m", "second_ac", "sleeper",
]
REQUIRED_COLUMNS = [
    "train_number", "train_name", "train_zone", "train_type", "from_station_name",
    "to_station_name", "station_name", "arrival", "departure", "schedule_day", "distance",
]
DATA_DIR = Path(__file__).resolve().parent / "data"


def inject_global_css() -> None:
    st.markdown(
        """
        <style>
        .main .block-container {padding-top: 1.4rem; padding-bottom: 2rem; max-width: 1280px;}
        .metric-card {background: linear-gradient(135deg,#0f172a,#1e40af); color:#fff; padding:1.1rem; border-radius:18px; box-shadow:0 8px 22px rgba(15,23,42,.18);}
        .metric-card h3 {font-size:.9rem; margin:0; color:#bfdbfe; font-weight:600;}
        .metric-card p {font-size:1.8rem; margin:.25rem 0 0; font-weight:800;}
        .insight-card {border-left:5px solid #2563eb; background:#f8fafc; padding:1rem; border-radius:12px; margin:.7rem 0;}
        .small-muted {color:#64748b; font-size:.92rem;}
        </style>
        """,
        unsafe_allow_html=True,
    )


def find_local_data_files() -> list[Path]:
    if not DATA_DIR.exists():
        return []
    return sorted([p for p in DATA_DIR.iterdir() if p.suffix.lower() in {".csv", ".xlsx", ".xls"}])


def read_table(source) -> pd.DataFrame:
    name = getattr(source, "name", str(source)).lower()
    if name.endswith(".csv"):
        return pd.read_csv(source)
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(source)
    raise ValueError("Unsupported file type. Please provide a CSV or Excel file.")


def clean_railway_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Replicates the notebook cleaning flow without inventing columns or values."""
    df = raw_df.copy()
    keep_columns = [col for col in DATA_COLUMNS if col in df.columns]
    if keep_columns:
        df = df[keep_columns]
    df = df.drop_duplicates().copy()

    for col in df.select_dtypes(include=np.number).columns:
        median = df[col].median()
        if pd.isna(median):
            median = 0
        df[col] = df[col].fillna(median)
    for col in df.select_dtypes(include="object").columns:
        mode = df[col].mode(dropna=True)
        fill_value = mode.iloc[0] if not mode.empty else "Unknown"
        df[col] = df[col].fillna(fill_value)

    if "train_zone" in df.columns:
        df["train_zone"] = df["train_zone"].replace("?", "Unknown")
    for col in ["distance", "duration_h", "duration_m", "schedule_day"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["arrival", "departure"]:
        if col in df.columns:
            df[f"{col}_hour"] = pd.to_datetime(df[col], format="%H:%M:%S", errors="coerce").dt.hour
            fallback = pd.to_datetime(df[col], errors="coerce").dt.hour
            df[f"{col}_hour"] = df[f"{col}_hour"].fillna(fallback)
    return df


@st.cache_data(show_spinner="Loading and cleaning railway data...")
def load_data_from_path(path: str) -> pd.DataFrame:
    return clean_railway_data(read_table(path))


@st.cache_data(show_spinner="Cleaning uploaded railway data...")
def load_data_from_upload(file_name: str, file_bytes: bytes) -> pd.DataFrame:
    import io
    buffer = io.BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        raw_df = pd.read_csv(buffer)
    elif file_name.lower().endswith((".xlsx", ".xls")):
        raw_df = pd.read_excel(buffer)
    else:
        raise ValueError("Unsupported file type. Please provide a CSV or Excel file.")
    return clean_railway_data(raw_df)


def get_data() -> pd.DataFrame | None:
    st.sidebar.markdown("### Data Source")
    local_files = find_local_data_files()
    uploaded = st.sidebar.file_uploader("Upload your cleaned railway CSV/XLSX", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        return load_data_from_upload(uploaded.name, uploaded.getvalue())
    if local_files:
        selected = st.sidebar.selectbox("Local data file", local_files, format_func=lambda p: p.name)
        return load_data_from_path(str(selected))
    st.warning("No dataset file is present in `Railway_Station_Schedule_Analytics/data/`. Upload the cleaned CSV/XLSX in the sidebar to run the dashboards.")
    return None


def require_columns(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [c for c in columns if c not in df.columns]


def kpi_value(df: pd.DataFrame, column: str) -> int:
    return int(df[column].nunique()) if column in df.columns else 0


def metric_card(label: str, value) -> None:
    st.markdown(f"<div class='metric-card'><h3>{label}</h3><p>{value}</p></div>", unsafe_allow_html=True)


def filtered_data_controls(df: pd.DataFrame, key_prefix: str = "filter") -> pd.DataFrame:
    out = df.copy()
    with st.sidebar.expander("Interactive Filters", expanded=True):
        for col in ["train_zone", "train_type", "station_state"]:
            if col in out.columns:
                values = sorted(out[col].dropna().astype(str).unique())
                chosen = st.multiselect(col.replace("_", " ").title(), values, default=[], key=f"{key_prefix}_{col}")
                if chosen:
                    out = out[out[col].astype(str).isin(chosen)]
        if "distance" in out.columns and out["distance"].notna().any():
            min_v, max_v = float(out["distance"].min()), float(out["distance"].max())
            rng = st.slider("Distance range", min_v, max_v, (min_v, max_v), key=f"{key_prefix}_distance")
            out = out[out["distance"].between(rng[0], rng[1], inclusive="both")]
    return out


def dataset_profile(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({"Column": df.columns, "Datatype": df.dtypes.astype(str).values, "Missing Values": df.isna().sum().values, "Unique Values": df.nunique(dropna=True).values})
