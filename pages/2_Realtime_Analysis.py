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
import altair as alt

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Certification Analytics",
    layout="wide"
)

# --------------------------------------------------
# GLOBAL CSS – MATCH REFERENCE UI
# --------------------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: "Inter", sans-serif;
}

/* PAGE TITLE */
.page-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.page-subtitle {
    color: #64748b;
    font-size: 1.05rem;
    max-width: 900px;
}

/* KPI CARDS */
.kpi-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(15,23,42,0.06);
    height: 150px;
}
.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.kpi-icon {
    background: #f1f5f9;
    border-radius: 12px;
    padding: 10px;
    font-size: 18px;
}
.kpi-delta {
    color: #22c55e;
    font-weight: 600;
    font-size: 0.85rem;
}
.kpi-label {
    margin-top: 1rem;
    color: #64748b;
    font-size: 0.95rem;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 0.2rem;
}

/* CHART CARDS */
.chart-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 6px 20px rgba(15,23,42,0.06);
}

/* BUTTONS */
div.stButton > button {
    background-color: #0f172a !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA (REPLACE WITH YOUR SOURCE)
# --------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("certification_data.csv")  # replace if needed

df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()

# --------------------------------------------------
# ENROLMENT MONTH FIX (Jan-24 & Jan-2024)
# --------------------------------------------------
df["Enrolment Month"] = (
    df["Enrolment Month"]
    .astype(str)
    .str.replace(r"-(\d{2})$", r"-20\1", regex=True)
)

df["Enrolment Month Parsed"] = pd.to_datetime(
    df["Enrolment Month"],
    format="%b-%Y",
    errors="coerce"
)

df["Enrolment Month Filter"] = df["Enrolment Month Parsed"].dt.strftime("%b-%Y")
df["Completed Flag"] = df["Actual Date of completion"].notna()

# --------------------------------------------------
# HEADER
# --------------------------------------------------
h1, h2 = st.columns([4, 1])
with h1:
    st.markdown("""
    <div class="page-title">Certification Analytics</div>
    <div class="page-subtitle">
        Real-time overview of employee certification progress, voucher lifecycle,
        and vertical-specific distribution.
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
with st.sidebar:
    st.header("🔎 Analytics Filters")

    enrolment_month = st.multiselect(
        "Enrolment Month",
        sorted(df["Enrolment Month Filter"].dropna().unique())
    )

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

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------
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

# --------------------------------------------------
# KPI CARDS (MATCH IMAGE)
# --------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, icon, label, value, delta):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-header">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-delta">{delta}</div>
            </div>
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

kpi_card(k1, "🗄️", "Total Records", len(filtered_df), "+12.5%")
kpi_card(k2, "👥", "Unique Employees", filtered_df["EMP ID"].nunique(), "+5.2%")
kpi_card(k3, "🎓", "Completed Certifications", int(filtered_df["Completed Flag"].sum()), "+18.1%")
kpi_card(
    k4,
    "📊",
    "Completion %",
    f"{round(filtered_df['Completed Flag'].mean() * 100, 1)}%",
    "+2.4%"
)

# --------------------------------------------------
# CHARTS
# --------------------------------------------------
cert_chart = (
    alt.Chart(filtered_df)
    .mark_bar(color="#0ea5a4", cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X("Certification:N", sort="-y", title=None),
        y=alt.Y("count()", title=None),
        tooltip=["count()"]
    )
    .properties(height=320)
)

snowpro_chart = (
    alt.Chart(filtered_df)
    .mark_bar(color="#0284c7", cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
    .encode(
        x=alt.X("SnowPro Certified:N", title=None),
        y=alt.Y("count()", title=None),
        tooltip=["count()"]
    )
    .properties(height=320)
)

c1, c2 = st.columns(2)
with c1:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.subheader("Certifications Distribution")
    st.altair_chart(cert_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("<div class='chart-card'>", unsafe_allow_html=True)
    st.subheader("SnowPro Status")
    st.altair_chart(snowpro_chart, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# DRILL DOWN TABLE
# --------------------------------------------------
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

