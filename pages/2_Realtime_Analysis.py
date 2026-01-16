# import streamlit as st
# import pandas as pd


# # -----------------------------------------
# # Page Config
# # -----------------------------------------
# st.set_page_config(
#     page_title="Certification Analytics",
#     layout="wide"
# )

# # -----------------------------------------
# # Clear Page-1 State (important)
# # -----------------------------------------
# for key in [
#     "record",
#     "edit_mode",
#     "pending_data",
#     "pending_action",
#     "last_emp_id"
# ]:
#     if key in st.session_state:
#         del st.session_state[key]

# # -----------------------------------------
# # Snowflake Session
# # -----------------------------------------
# cnx = st.connection("snowflake")
# session = cnx.session()


# # -----------------------------------------
# # Load Data
# # -----------------------------------------
# @st.cache_data(show_spinner="Loading certification data...")
# def load_data():
#     return session.sql("""
#         SELECT *
#         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#     """).to_pandas()

# df = load_data()

# st.title("📊 Certification Analytics (Realtime)")

# if st.button("🔄 Refresh Data"):
#     st.cache_data.clear()
#     st.rerun()
    
# if df.empty:
#     st.warning("No data available.")
#     st.stop()

# # -----------------------------------------
# # Derived Columns
# # -----------------------------------------
# df["Completed Flag"] = df["Actual Date of completion"].notna()

# # -----------------------------------------
# # Sidebar Filters
# # -----------------------------------------
# with st.sidebar:
#     st.header("🔎 Filters")

#     cert_filter = st.multiselect(
#         "Certification",
#         sorted(df["Certification"].dropna().unique())
#     )

#     snowpro_filter = st.multiselect(
#         "SnowPro Status",
#         sorted(df["SnowPro Certified"].dropna().unique())
#     )

#     voucher_filter = st.multiselect(
#         "Voucher Status",
#         sorted(df["Voucher Status"].dropna().unique())
#     )

#     account_filter = st.multiselect(
#         "Account",
#         sorted(df["Account"].dropna().unique())
#     )

#     vertical_filter = st.multiselect(
#         "Vertical / SL",
#         sorted(df["Vertical / SL"].dropna().unique())
#     )

#     st.divider()

#     # if st.button("🔄 Refresh Data", use_container_width=True):
#     #     st.cache_data.clear()
#     #     st.rerun()

# # -----------------------------------------
# # Apply Filters Dynamically
# # -----------------------------------------
# filtered_df = df.copy()

# if cert_filter:
#     filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]

# if snowpro_filter:
#     filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]

# if voucher_filter:
#     filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]

# if account_filter:
#     filtered_df = filtered_df[filtered_df["Account"].isin(account_filter)]

# if vertical_filter:
#     filtered_df = filtered_df[filtered_df["Vertical / SL"].isin(vertical_filter)]

# # -----------------------------------------
# # KPIs (Dynamic)
# # -----------------------------------------
# st.subheader("📌 Key Metrics")

# k1, k2, k3, k4 = st.columns(4)

# k1.metric("Total Records", len(filtered_df))
# k2.metric("Unique Employees", filtered_df["EMP ID"].nunique())
# k3.metric("Completed Certifications", filtered_df["Completed Flag"].sum())
# k4.metric(
#     "Completion %",
#     f"{round(filtered_df['Completed Flag'].mean() * 100, 1)}%" if len(filtered_df) else "0%"
# )

# st.divider()

# # -----------------------------------------
# # Charts
# # -----------------------------------------
# c1, c2 = st.columns(2)

# with c1:
#     st.markdown("### 📚 Certifications Distribution")
#     st.bar_chart(filtered_df["Certification"].value_counts())

# with c2:
#     st.markdown("### ❄️ SnowPro Status")
#     st.bar_chart(filtered_df["SnowPro Certified"].value_counts())

# st.divider()

# st.markdown("### 💳 Voucher Usage")
# st.bar_chart(filtered_df["Voucher Status"].value_counts())

# st.divider()

# # -----------------------------------------
# # Drill-Down Table
# # -----------------------------------------
# with st.expander("🔍 Drill-Down Data View"):
#     st.dataframe(
#         filtered_df[
#             [
#                 "EMP ID",
#                 "EMP Name",
#                 "Certification",
#                 "Enrolment Month",
#                 "SnowPro Certified",
#                 "Voucher Status",
#                 "Account",
#                 "Vertical / SL"
#             ]
#         ],
#         use_container_width=True
#     )



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import zipfile

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Certification Analytics",
    layout="wide"
)

# -----------------------------------------
# GLOBAL CSS – MATCH REFERENCE UI
# -----------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}
.page-title {
    font-size: 2.3rem;
    font-weight: 800;
}
.page-subtitle {
    color: #64748b;
    font-size: 1.05rem;
    max-width: 900px;
    margin-bottom: 2rem;
}
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}
.chart-card {
    background: white;
    border-radius: 14px;
    padding: 1.5rem;
    box-shadow: 0 6px 18px rgba(15,23,42,0.06);
}
div.stButton > button {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600;
    padding: 0.6rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# SNOWFLAKE CONNECTION
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
@st.cache_data(show_spinner="Loading certification data...")
def load_data():
    return session.sql("""
        SELECT *
        FROM USE_CASE.DETAILS.NEW_CERTIFICATION
    """).to_pandas()

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------------------
# DATE HANDLING
# -----------------------------------------
df["Enrolment Month"] = pd.to_datetime(df["Enrolment Month"], errors="coerce")
df["Enrolment Month Filter"] = df["Enrolment Month"].dt.to_period("M").astype(str)
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# HEADER
# -----------------------------------------
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown("""
    <div class="page-title">Certification Analytics</div>
    <div class="page-subtitle">
        Real-time overview of employee certification progress, voucher lifecycle,
        and vertical-wise distribution.
    </div>
    """, unsafe_allow_html=True)

# -----------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------
with st.sidebar:
    st.header("🔎 Analytics Filters")

    enrolment_month = st.multiselect(
        "Enrolment Month",
        sorted(df["Enrolment Month Filter"].dropna().unique())
    )

    st.divider()

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

    vertical_filter = st.multiselect(
        "Vertical / SL",
        sorted(df["Vertical / SL"].dropna().unique())
    )

# -----------------------------------------
# APPLY FILTERS
# -----------------------------------------
filtered_df = df.copy()

if enrolment_month:
    filtered_df = filtered_df[
        filtered_df["Enrolment Month Filter"].isin(enrolment_month)
    ]

if cert_filter:
    filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]

if snowpro_filter:
    filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]

if voucher_filter:
    filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]

if vertical_filter:
    filtered_df = filtered_df[filtered_df["Vertical / SL"].isin(vertical_filter)]

# -----------------------------------------
# KPI METRICS
# -----------------------------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Records", len(filtered_df))
k2.metric("Unique Employees", filtered_df["EMP ID"].nunique())
k3.metric("Completed Certifications", int(filtered_df["Completed Flag"].sum()))
k4.metric(
    "Completion %",
    f"{round(filtered_df['Completed Flag'].mean() * 100, 1)}%" if len(filtered_df) else "0%"
)

# -----------------------------------------
# CHARTS (DISPLAY)
# -----------------------------------------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Certifications Distribution")
    st.bar_chart(filtered_df["Certification"].value_counts())

with c2:
    st.subheader("SnowPro Status")
    st.bar_chart(filtered_df["SnowPro Certified"].value_counts())

# -----------------------------------------
# EXPORT CHARTS (MATPLOTLIB – SAFE)
# -----------------------------------------
def export_charts():
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as z:

        # Certification chart
        fig1, ax1 = plt.subplots()
        filtered_df["Certification"].value_counts().plot(kind="bar", ax=ax1)
        ax1.set_title("Certifications Distribution")
        img1 = io.BytesIO()
        fig1.savefig(img1, format="png", bbox_inches="tight")
        plt.close(fig1)
        z.writestr("certifications_distribution.png", img1.getvalue())

        # SnowPro chart
        fig2, ax2 = plt.subplots()
        filtered_df["SnowPro Certified"].value_counts().plot(kind="bar", ax=ax2)
        ax2.set_title("SnowPro Status")
        img2 = io.BytesIO()
        fig2.savefig(img2, format="png", bbox_inches="tight")
        plt.close(fig2)
        z.writestr("snowpro_status.png", img2.getvalue())

    buffer.seek(0)
    return buffer

st.download_button(
    "📊 Export Charts",
    data=export_charts(),
    file_name="certification_charts.zip",
    mime="application/zip"
)

# -----------------------------------------
# DRILL-DOWN TABLE
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

