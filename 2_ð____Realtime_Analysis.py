import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

# -----------------------------------------
# Page Config
# -----------------------------------------
st.set_page_config(
    page_title="Certification Analytics",
    layout="wide"
)

# -----------------------------------------
# Clear Page-1 State (important)
# -----------------------------------------
for key in [
    "record",
    "edit_mode",
    "pending_data",
    "pending_action",
    "last_emp_id"
]:
    if key in st.session_state:
        del st.session_state[key]

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
session = get_active_session()

# -----------------------------------------
# Load Data
# -----------------------------------------
@st.cache_data(show_spinner="Loading certification data...")
def load_data():
    return session.sql("""
        SELECT *
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
    """).to_pandas()

df = load_data()

st.title("📊 Certification Analytics (Realtime)")

if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
    
if df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------------------
# Derived Columns
# -----------------------------------------
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# Sidebar Filters
# -----------------------------------------
with st.sidebar:
    st.header("🔎 Filters")

    cert_filter = st.multiselect(
        "Certification",
        sorted(df["Certification"].dropna().unique())
    )

    snowpro_filter = st.multiselect(
        "SnowPro Status",
        sorted(df["SnowPro Certified"].dropna().unique())
    )

    voucher_filter = st.multiselect(
        "Voucher Status",
        sorted(df["Voucher Status"].dropna().unique())
    )

    account_filter = st.multiselect(
        "Account",
        sorted(df["Account"].dropna().unique())
    )

    vertical_filter = st.multiselect(
        "Vertical / SL",
        sorted(df["Vertical / SL"].dropna().unique())
    )

    st.divider()

    # if st.button("🔄 Refresh Data", use_container_width=True):
    #     st.cache_data.clear()
    #     st.rerun()

# -----------------------------------------
# Apply Filters Dynamically
# -----------------------------------------
filtered_df = df.copy()

if cert_filter:
    filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]

if snowpro_filter:
    filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]

if voucher_filter:
    filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]

if account_filter:
    filtered_df = filtered_df[filtered_df["Account"].isin(account_filter)]

if vertical_filter:
    filtered_df = filtered_df[filtered_df["Vertical / SL"].isin(vertical_filter)]

# -----------------------------------------
# KPIs (Dynamic)
# -----------------------------------------
st.subheader("📌 Key Metrics")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Records", len(filtered_df))
k2.metric("Unique Employees", filtered_df["EMP ID"].nunique())
k3.metric("Completed Certifications", filtered_df["Completed Flag"].sum())
k4.metric(
    "Completion %",
    f"{round(filtered_df['Completed Flag'].mean() * 100, 1)}%" if len(filtered_df) else "0%"
)

st.divider()

# -----------------------------------------
# Charts
# -----------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.markdown("### 📚 Certifications Distribution")
    st.bar_chart(filtered_df["Certification"].value_counts())

with c2:
    st.markdown("### ❄️ SnowPro Status")
    st.bar_chart(filtered_df["SnowPro Certified"].value_counts())

st.divider()

st.markdown("### 💳 Voucher Usage")
st.bar_chart(filtered_df["Voucher Status"].value_counts())

st.divider()

# -----------------------------------------
# Drill-Down Table
# -----------------------------------------
with st.expander("🔍 Drill-Down Data View"):
    st.dataframe(
        filtered_df[
            [
                "EMP ID",
                "EMP Name",
                "Certification",
                "Enrolment Month",
                "SnowPro Certified",
                "Voucher Status",
                "Account",
                "Vertical / SL"
            ]
        ],
        use_container_width=True
    )
