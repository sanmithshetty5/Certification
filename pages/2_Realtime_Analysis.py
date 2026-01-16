

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
# # GLOBAL CSS – ENTERPRISE UI (MATCHES HOME PAGE)
# # -----------------------------------------
# st.markdown("""
# <style>
# /* App background */
# .stApp {
#     background-color: #f8fafc;
#     color: #0f172a;
#     font-family: Inter, sans-serif;
# }

# /* Header */
# .page-title {
#     font-size: 2.4rem;
#     font-weight: 800;
# }
# .page-subtitle {
#     font-size: 1.05rem;
#     color: #64748b;
#     margin-top: 0.3rem;
# }

# /* Card */
# .card {
#     background: #ffffff;
#     border-radius: 16px;
#     padding: 1.6rem;
#     border: 1px solid #e2e8f0;
#     box-shadow: 0 8px 24px rgba(15,23,42,0.06);
# }

# /* KPI */
# .kpi-label {
#     font-size: 0.9rem;
#     color: #64748b;
# }
# .kpi-value {
#     font-size: 2rem;
#     font-weight: 800;
# }

# /* Chart title */
# .chart-title {
#     font-size: 1.1rem;
#     font-weight: 700;
#     margin-bottom: 1rem;
# }

# /* -------------------------------
#    GLOBAL BUTTON OVERRIDE (FIXED)
# --------------------------------*/

# /* NORMAL BUTTON + DOWNLOAD BUTTON */
# div.stButton > button,
# div.stDownloadButton > button {
#     background-color: #030712 !important;
#     color: #ffffff !important;
#     border: 2px solid #030712 !important;
#     border-radius: 10px !important;
#     font-weight: 700 !important;
#     padding: 0.75rem 1rem !important;
#     transition: all 0.25s ease-in-out !important;
# }

# /* HOVER */
# div.stButton > button:hover,
# div.stDownloadButton > button:hover {
#     background-color: #ffffff !important;
#     color: #030712 !important;
# }

# /* FOCUS / ACTIVE */
# div.stButton > button:focus,
# div.stButton > button:active,
# div.stDownloadButton > button:focus,
# div.stDownloadButton > button:active {
#     background-color: #ffffff !important;
#     color: #030712 !important;
#     outline: none !important;
#     box-shadow: none !important;
# }

# /* DISABLED */
# div.stButton > button:disabled,
# div.stDownloadButton > button:disabled {
#     background-color: #f1f5f9 !important;
#     color: #94a3b8 !important;
#     border: 2px solid #e2e8f0 !important;
#     cursor: not-allowed !important;
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
# # DATE HANDLING
# # -----------------------------------------
# DATE_COLUMN = "Enrolment Month"

# df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
# df["Year"] = df[DATE_COLUMN].dt.year
# df["Month"] = df[DATE_COLUMN].dt.month_name()
# df["Date"] = df[DATE_COLUMN].dt.date
# df["Completed Flag"] = df["Actual Date of completion"].notna()

# # -----------------------------------------
# # SIDEBAR FILTERS
# # -----------------------------------------
# with st.sidebar:
#     st.markdown("## 🔎 Analytics Filters")

#     year_filter = st.multiselect("Year", sorted(df["Year"].dropna().unique()))
#     month_filter = st.multiselect("Month", df["Month"].dropna().unique())
#     date_filter = st.date_input("Date Range", [])

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

# if year_filter:
#     filtered_df = filtered_df[filtered_df["Year"].isin(year_filter)]
# if month_filter:
#     filtered_df = filtered_df[filtered_df["Month"].isin(month_filter)]
# if len(date_filter) == 2:
#     filtered_df = filtered_df[
#         (filtered_df["Date"] >= date_filter[0]) &
#         (filtered_df["Date"] <= date_filter[1])
#     ]
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
#             ax.set_xlabel("")
#             ax.set_ylabel("Count")
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
#     st.markdown("""
#     <div class="page-title">Certification Analytics</div>
#     <div class="page-subtitle">
#         Real-time overview of employee certification progress,
#         voucher lifecycle, and vertical-wise distribution.
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
# st.markdown("<br>", unsafe_allow_html=True)
# k1, k2, k3, k4 = st.columns(4)

# def kpi(col, label, value):
#     with col:
#         st.markdown(f"""
#         <div class="card">
#             <div class="kpi-label">{label}</div>
#             <div class="kpi-value">{value}</div>
#         </div>
#         """, unsafe_allow_html=True)

# kpi(k1, "Total Records", len(filtered_df))
# kpi(k2, "Unique Employees", filtered_df["EMP ID"].nunique())
# kpi(k3, "Completed Certifications", int(filtered_df["Completed Flag"].sum()))

# with k4:
#     completion = round(filtered_df["Completed Flag"].mean() * 100, 1)
#     st.markdown(f"""
#     <div class="card">
#         <div class="kpi-label">Completion %</div>
#         <div class="kpi-value">{completion}%</div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.progress(completion / 100)

# # -----------------------------------------
# # CHARTS
# # -----------------------------------------
# st.markdown("<br>", unsafe_allow_html=True)

# c1, c2 = st.columns([3, 2])

# with c1:
#     st.markdown('<div class="card"><div class="chart-title">Certifications Distribution</div>', unsafe_allow_html=True)
#     st.bar_chart(filtered_df["Certification"].value_counts())
#     st.markdown("</div>", unsafe_allow_html=True)

# with c2:
#     st.markdown('<div class="card"><div class="chart-title">SnowPro Status</div>', unsafe_allow_html=True)
#     st.bar_chart(filtered_df["SnowPro Certified"].value_counts())
#     st.markdown("</div>", unsafe_allow_html=True)

# st.markdown("<br>", unsafe_allow_html=True)
# st.markdown('<div class="card"><div class="chart-title">Voucher Usage</div>', unsafe_allow_html=True)
# st.bar_chart(filtered_df["Voucher Status"].value_counts())
# st.markdown("</div>", unsafe_allow_html=True)

# # -----------------------------------------
# # DRILL-DOWN TABLE
# # -----------------------------------------
# st.markdown("<br>", unsafe_allow_html=True)
# with st.expander("🔍 View Detailed Records"):
#     st.dataframe(
#         filtered_df[
#             [
#                 "EMP ID",
#                 "EMP Name",
#                 "Certification",
#                 DATE_COLUMN,
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
# 💡 Tip: Use filters to explore certification insights across teams and time periods.
# </div>
# """, unsafe_allow_html=True)

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
    page_icon="📊",
    layout="wide"
)

# -----------------------------------------
# CLEAR PAGE STATE (Logic Preserved)
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
# GLOBAL CSS - PROFESSIONAL THEME
# -----------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* --- GLOBAL RESET --- */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* --- APP BACKGROUND --- */
.stApp {
    background-color: #f1f5f9; /* Light Slate Gray */
    color: #1e293b; /* Dark Slate Blue */
}

/* --- HEADER STYLING --- */
.header-container {
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 2rem;
}
.page-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0f172a;
    letter-spacing: -0.025em;
}
.page-subtitle {
    font-size: 1rem;
    color: #64748b;
    margin-top: 0.2rem;
}

/* --- CARD CONTAINERS --- */
.card-container {
    background-color: #ffffff;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
    margin-bottom: 1rem;
}

/* --- KPI METRIC CARDS --- */
.metric-card {
    background-color: white;
    border-radius: 10px;
    padding: 1.2rem;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    border: 1px solid #e2e8f0;
    border-left: 5px solid #4f46e5; /* Indigo Accent */
    transition: transform 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.metric-label {
    font-size: 0.875rem;
    font-weight: 600;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 0.05em;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #1e293b;
    margin-top: 0.25rem;
}

/* --- CHART HEADERS --- */
.chart-header {
    font-size: 1.125rem;
    font-weight: 700;
    color: #334155;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* --- BUTTON OVERRIDES --- */
div.stButton > button, 
div.stDownloadButton > button {
    background-color: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
}
div.stButton > button:hover, 
div.stDownloadButton > button:hover {
    background-color: #4338ca !important; /* Darker Indigo */
    box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3) !important;
    transform: translateY(-1px);
}
div.stButton > button:active, 
div.stDownloadButton > button:active {
    transform: translateY(0px);
}

/* --- DATAFRAME & SIDEBAR --- */
[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    overflow: hidden;
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
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
    """).to_pandas()

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------------------
# DATE HANDLING
# -----------------------------------------
DATE_COLUMN = "Enrolment Month"

df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors="coerce")
df["Year"] = df[DATE_COLUMN].dt.year
df["Month"] = df[DATE_COLUMN].dt.month_name()
df["Date"] = df[DATE_COLUMN].dt.date
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# SIDEBAR FILTERS
# -----------------------------------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=50) # Optional Icon
    st.markdown("### 🔎 Analytics Filters")
    st.markdown("<div style='margin-bottom: 20px; font-size: 0.9em; color: #64748b;'>Refine your data view</div>", unsafe_allow_html=True)

    year_filter = st.multiselect("Year", sorted(df["Year"].dropna().unique()))
    month_filter = st.multiselect("Month", df["Month"].dropna().unique())
    date_filter = st.date_input("Date Range", [])

    st.divider()

    cert_filter = st.multiselect("Certification", sorted(df["Certification"].dropna().unique()))
    snowpro_filter = st.multiselect("SnowPro Status", sorted(df["SnowPro Certified"].dropna().unique()))
    voucher_filter = st.multiselect("Voucher Status", sorted(df["Voucher Status"].dropna().unique()))
    account_filter = st.multiselect("Account", sorted(df["Account"].dropna().unique()))
    vertical_filter = st.multiselect("Vertical / SL", sorted(df["Vertical / SL"].dropna().unique()))

# -----------------------------------------
# APPLY FILTERS
# -----------------------------------------
filtered_df = df.copy()

if year_filter:
    filtered_df = filtered_df[filtered_df["Year"].isin(year_filter)]
if month_filter:
    filtered_df = filtered_df[filtered_df["Month"].isin(month_filter)]
if len(date_filter) == 2:
    filtered_df = filtered_df[
        (filtered_df["Date"] >= date_filter[0]) &
        (filtered_df["Date"] <= date_filter[1])
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

# -----------------------------------------
# EXPORT CHART FUNCTION
# -----------------------------------------
def export_charts_as_zip(data):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        charts = {
            "certifications_distribution.png": data["Certification"].value_counts(),
            "snowpro_status.png": data["SnowPro Certified"].value_counts(),
            "voucher_usage.png": data["Voucher Status"].value_counts()
        }

        for name, series in charts.items():
            fig, ax = plt.subplots(figsize=(7, 5))
            series.plot(kind="bar", ax=ax, color='#4f46e5') # Added brand color to export
            ax.set_title(name.replace("_", " ").replace(".png", "").title())
            ax.set_xlabel("")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45, ha="right")

            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight")
            plt.close(fig)
            z.writestr(name, img.getvalue())

    buffer.seek(0)
    return buffer

# -----------------------------------------
# HEADER
# -----------------------------------------
h1, h2 = st.columns([7, 2])

with h1:
    st.markdown("""
    <div class="header-container">
        <div class="page-title">Certification Analytics</div>
        <div class="page-subtitle">Real-time insights into employee certification progress, voucher lifecycle, and vertical distribution.</div>
    </div>
    """, unsafe_allow_html=True)

with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "📥 Export Report Charts",
        data=export_charts_as_zip(filtered_df),
        file_name="certification_analytics_charts.zip",
        mime="application/zip",
        use_container_width=True
    )

# -----------------------------------------
# KPI CARDS
# -----------------------------------------
col1, col2, col3, col4 = st.columns(4)

def display_kpi(column, title, value, color_border="#4f46e5"):
    with column:
        st.markdown(f"""
        <div class="metric-card" style="border-left: 5px solid {color_border};">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

# Calculation
completion_rate = round(filtered_df["Completed Flag"].mean() * 100, 1) if not filtered_df.empty else 0

display_kpi(col1, "Total Records", f"{len(filtered_df):,}")
display_kpi(col2, "Unique Employees", f"{filtered_df['EMP ID"].nunique():,}")
display_kpi(col3, "Completed Certs", f"{int(filtered_df['Completed Flag'].sum()):,}", color_border="#10b981") # Green

# Special formatting for the 4th KPI to include progress bar
with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left: 5px solid #f59e0b;">
        <div class="metric-label">Completion Rate</div>
        <div class="metric-value">{completion_rate}%</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 5px;'></div>", unsafe_allow_html=True)
    st.progress(completion_rate / 100)

# -----------------------------------------
# CHARTS ROW 1
# -----------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns([3, 2])

with c1:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">📚 Certifications Distribution</div>', unsafe_allow_html=True)
    # Using st.bar_chart as requested, wrapped in our container
    st.bar_chart(filtered_df["Certification"].value_counts(), color="#4f46e5")
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="card-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-header">❄️ SnowPro Status</div>', unsafe_allow_html=True)
    st.bar_chart(filtered_df["SnowPro Certified"].value_counts(), color="#3b82f6")
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# CHARTS ROW 2
# -----------------------------------------
st.markdown('<div class="card-container">', unsafe_allow_html=True)
st.markdown('<div class="chart-header">💳 Voucher Usage</div>', unsafe_allow_html=True)
st.bar_chart(filtered_df["Voucher Status"].value_counts(), color="#0ea5e9")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# DRILL-DOWN TABLE
# -----------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Styled Expander
with st.expander("🔍  View Detailed Records", expanded=False):
    st.markdown('<div style="background-color: white; padding: 10px; border-radius: 8px;">', unsafe_allow_html=True)
    st.dataframe(
        filtered_df[
            [
                "EMP ID",
                "EMP Name",
                "Certification",
                DATE_COLUMN,
                "SnowPro Certified",
                "Voucher Status",
                "Account",
                "Vertical / SL"
            ]
        ],
        use_container_width=True,
        height=400,
        hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div style="text-align: center; margin-top: 3rem; color: #94a3b8; font-size: 0.8rem;">
    Certification Analytics Dashboard • Updated Realtime
</div>
""", unsafe_allow_html=True)
