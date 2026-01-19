import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Certification Analytics",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA (example – keep your existing loader)
# ---------------------------------------------------
# df = load_from_snowflake()
# Assuming df already exists

# ---------------------------------------------------
# TEMPORARY SPLIT (DO NOT TOUCH DB)
# ---------------------------------------------------
df["Enroll_Month_Name"] = df["Enrolment Month"].str.split("-").str[0]
df["Enroll_Year"] = df["Enrolment Month"].str.split("-").str[1]

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------
with st.sidebar:
    st.markdown("## 🔎 Analytics Filters")

    # ----- YEAR -----
    enrollment_years = sorted(
        df["Enroll_Year"].dropna().unique().tolist()
    )

    selected_year = st.selectbox(
        "Enrollment Year",
        enrollment_years
    )

    # ----- MONTH -----
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    available_months = (
        df[df["Enroll_Year"] == selected_year]["Enroll_Month_Name"]
        .dropna()
        .unique()
        .tolist()
    )

    available_months = sorted(
        available_months,
        key=lambda x: month_order.index(x)
    )

    selected_month = st.selectbox(
        "Enrollment Month",
        available_months
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
    account_filter = st.multiselect(
        "Account",
        sorted(df["Account"].dropna().unique())
    )
    vertical_filter = st.multiselect(
        "Vertical / SL",
        sorted(df["Vertical / SL"].dropna().unique())
    )

# ---------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------
filtered_df = df.copy()

selected_enrollment_value = f"{selected_month}-{selected_year}"
filtered_df = filtered_df[
    filtered_df["Enrolment Month"] == selected_enrollment_value
]

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

# ---------------------------------------------------
# PAGE TITLE
# ---------------------------------------------------
st.markdown(
    f"## 📊 Certification Analytics – {selected_month} {selected_year}"
)

# ---------------------------------------------------
# KPI ROW
# ---------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Enrollments", len(filtered_df))
k2.metric(
    "SnowPro Certified",
    filtered_df["SnowPro Certified"].value_counts().get("Yes", 0)
)
k3.metric(
    "Voucher Issued",
    filtered_df["Voucher Status"].value_counts().get("Issued", 0)
)
k4.metric(
    "Unique Certifications",
    filtered_df["Certification"].nunique()
)

st.divider()

# ---------------------------------------------------
# GRAPH 1: CERTIFICATION DISTRIBUTION
# ---------------------------------------------------
cert_chart = (
    filtered_df.groupby("Certification")
    .size()
    .reset_index(name="Employees")
)

fig1 = px.bar(
    cert_chart,
    x="Certification",
    y="Employees",
    title="Employees by Certification",
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------------------------------------------
# 🔥 NEW GRAPH: YEAR-WISE COMPARISON (ALL YEARS)
# ---------------------------------------------------
st.markdown("### 📈 Enrollment Trend Over the Years")

yearly_trend = (
    df.groupby("Enroll_Year")
    .size()
    .reset_index(name="Employees Enrolled")
    .sort_values("Enroll_Year")
)

fig2 = px.line(
    yearly_trend,
    x="Enroll_Year",
    y="Employees Enrolled",
    markers=True,
    title="Year-wise Employee Enrollment Comparison"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# DATA PREVIEW (OPTIONAL)
# ---------------------------------------------------
with st.expander("🔍 View Filtered Data"):
    st.dataframe(filtered_df)




# import streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt
# import io
# import zipfile

# # -----------------------------------------
# # PAGE CONFIG
# # -----------------------------------------
# st.set_page_config(
#     page_title="Certification Analytics",
#     layout="wide"
# )

# # -----------------------------------------
# # CLEAR PAGE STATE
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
# # GLOBAL CSS – ENTERPRISE UI
# # -----------------------------------------
# st.markdown("""
# <style>
# .stApp {
#     background-color: #f8fafc;
#     color: #0f172a;
#     font-family: Inter, sans-serif;
# }
# .page-title { font-size: 2.4rem; font-weight: 800; }
# .page-subtitle { font-size: 1.05rem; color: #64748b; margin-top: 0.3rem; }
# .card {
#     background: #ffffff;
#     border-radius: 16px;
#     padding: 1.6rem;
#     border: 1px solid #e2e8f0;
#     box-shadow: 0 8px 24px rgba(15,23,42,0.06);
# }
# .metric-label {
#     font-size: 0.75rem;
#     font-weight: 700;
#     letter-spacing: 0.1em;
#     color: #64748b;
#     text-transform: uppercase;
# }
# .metric-value {
#     font-size: 2rem;
#     font-weight: 800;
# }
# .chart-title {
#     font-size: 1.1rem;
#     font-weight: 700;
#     margin-bottom: 1rem;
# }
# div.stButton > button,
# div.stDownloadButton > button {
#     background-color: #030712 !important;
#     color: #ffffff !important;
#     border: 2px solid #030712 !important;
#     border-radius: 10px !important;
#     font-weight: 700 !important;
# }
# div.stButton > button:hover,
# div.stDownloadButton > button:hover {
#     background-color: #ffffff !important;
#     color: #030712 !important;
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------------------
# # SNOWFLAKE CONNECTION
# # -----------------------------------------
# cnx = st.connection("snowflake")
# session = cnx.session()

# # -----------------------------------------
# # LOAD DATA
# # -----------------------------------------
# @st.cache_data(show_spinner="Loading certification data...")
# def load_data():
#     return session.sql("""
#         SELECT *
#         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#     """).to_pandas()

# df = load_data()

# if df.empty:
#     st.warning("No data available.")
#     st.stop()

# # -----------------------------------------
# # COMPLETION FLAG (NO DATE PARSING)
# # -----------------------------------------
# df["Completed Flag"] = df["Actual Date of completion"].notna()

# # -----------------------------------------
# # SIDEBAR FILTERS (UPDATED – ENROLLMENT MONTH ONLY)
# # -----------------------------------------
# with st.sidebar:
#     st.markdown("## 🔎 Analytics Filters")

#     enrollment_months = (
#         df["Enrolment Month"]
#         .dropna()
#         .unique()
#         .tolist()
#     )

#     enrollment_months = sorted(
#         enrollment_months,
#         key=lambda x: pd.to_datetime(x, format="%b-%Y", errors="coerce")
#     )

#     selected_month = st.selectbox(
#         "Enrollment Month",
#         enrollment_months
#     )

#     st.divider()

#     cert_filter = st.multiselect("Certification", sorted(df["Certification"].dropna().unique()))
#     snowpro_filter = st.multiselect("SnowPro Status", sorted(df["SnowPro Certified"].dropna().unique()))
#     voucher_filter = st.multiselect("Voucher Status", sorted(df["Voucher Status"].dropna().unique()))
#     account_filter = st.multiselect("Account", sorted(df["Account"].dropna().unique()))
#     vertical_filter = st.multiselect("Vertical / SL", sorted(df["Vertical / SL"].dropna().unique()))

# # -----------------------------------------
# # APPLY FILTERS
# # -----------------------------------------
# filtered_df = df.copy()

# filtered_df = filtered_df[
#     filtered_df["Enrolment Month"] == selected_month
# ]

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
# # EXPORT CHART FUNCTION
# # -----------------------------------------
# def export_charts_as_zip(data):
#     buffer = io.BytesIO()
#     with zipfile.ZipFile(buffer, "w") as z:
#         charts = {
#             "certifications_distribution.png": data["Certification"].value_counts(),
#             "snowpro_status.png": data["SnowPro Certified"].value_counts(),
#             "voucher_usage.png": data["Voucher Status"].value_counts()
#         }
#         for name, series in charts.items():
#             fig, ax = plt.subplots(figsize=(7, 5))
#             series.plot(kind="bar", ax=ax)
#             ax.set_title(name.replace("_", " ").replace(".png", "").title())
#             plt.xticks(rotation=45, ha="right")
#             img = io.BytesIO()
#             fig.savefig(img, format="png", bbox_inches="tight")
#             plt.close(fig)
#             z.writestr(name, img.getvalue())
#     buffer.seek(0)
#     return buffer

# # -----------------------------------------
# # HEADER
# # -----------------------------------------
# h1, h2 = st.columns([6, 2])

# with h1:
#     st.markdown(f"""
#     <div class="page-title">Certification Analytics</div>
#     <div class="page-subtitle">
#         Enrollment Month: <b>{selected_month}</b>
#     </div>
#     """, unsafe_allow_html=True)

# with h2:
#     st.markdown("<br>", unsafe_allow_html=True)
#     st.download_button(
#         "⬇ Export Charts",
#         data=export_charts_as_zip(filtered_df),
#         file_name="certification_analytics_charts.zip",
#         mime="application/zip"
#     )

# # -----------------------------------------
# # KPI CARDS
# # -----------------------------------------
# k1, k2, k3, k4 = st.columns(4)

# def kpi(col, label, value):
#     with col:
#         st.markdown(f"""
#         <div class="card">
#             <div class="metric-label">{label}</div>
#             <div class="metric-value">{value}</div>
#         </div>
#         """, unsafe_allow_html=True)

# kpi(k1, "Total Records", len(filtered_df))
# kpi(k2, "Unique Employees", filtered_df["EMP ID"].nunique())
# kpi(k3, "Completed Certifications", int(filtered_df["Completed Flag"].sum()))

# with k4:
#     completion = round(filtered_df["Completed Flag"].mean() * 100, 1) if len(filtered_df) else 0
#     st.markdown(f"""
#     <div class="card">
#         <div class="metric-label">Completion %</div>
#         <div class="metric-value">{completion}%</div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.progress(completion / 100 if completion else 0)

# # -----------------------------------------
# # CHARTS
# # -----------------------------------------
# c1, c2 = st.columns([3, 2])

# with c1:
#     st.markdown('<div class="card"><div class="chart-title">Certifications Distribution</div>', unsafe_allow_html=True)
#     st.bar_chart(filtered_df["Certification"].value_counts())
#     st.markdown("</div>", unsafe_allow_html=True)

# with c2:
#     st.markdown('<div class="card"><div class="chart-title">SnowPro Status</div>', unsafe_allow_html=True)
#     st.bar_chart(filtered_df["SnowPro Certified"].value_counts())
#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown('<div class="card"><div class="chart-title">Voucher Usage</div>', unsafe_allow_html=True)
# st.bar_chart(filtered_df["Voucher Status"].value_counts())
# st.markdown("</div>", unsafe_allow_html=True)

# # -----------------------------------------
# # DRILL-DOWN TABLE
# # -----------------------------------------
# with st.expander("🔍 View Detailed Records"):
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
#         use_container_width=True,
#         height=450
#     )

# # -----------------------------------------
# # FOOTER
# # -----------------------------------------
# st.markdown("""
# <div style="margin-top:3rem;color:#64748b;font-size:0.85rem;">
# 💡 Tip: Select an enrollment month to see employee certification trends.
# </div>
# """, unsafe_allow_html=True)
