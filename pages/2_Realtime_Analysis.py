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
# GLOBAL THEME COLORS
# -----------------------------------------
# Indigo Blue - Professional, high contrast against white cards
CHART_COLOR = "#4f46e5" 
# Matplotlib colormap for Heatmap (Light Blue to Dark Blue)
HEATMAP_CMAP = "Blues"  

# -----------------------------------------
# CLEAR PAGE STATE
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
# GLOBAL CSS – ENTERPRISE UI
# -----------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: Inter, sans-serif;
}
.page-title { font-size: 2.4rem; font-weight: 800; }
.page-subtitle { font-size: 1.05rem; color: #64748b; margin-top: 0.3rem; }
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 1.6rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 24px rgba(15,23,42,0.06);
}
.metric-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #64748b;
    text-transform: uppercase;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
}
.chart-title {
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
}
div.stButton > button,
div.stDownloadButton > button {
    background-color: #030712 !important;
    color: #ffffff !important;
    border: 2px solid #030712 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}
div.stButton > button:hover,
div.stDownloadButton > button:hover {
    background-color: #ffffff !important;
    color: #030712 !important;
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
    st.error("No data available.")
    st.stop()

# -----------------------------------------
# DERIVE MONTH & YEAR FROM VARCHAR COLUMN
# -----------------------------------------
df["Enrolment Month"] = df["Enrolment Month"].astype(str)
df = df[df["Enrolment Month"] != "nan"]

# Normalize Enrolment Month safely (e.g., "Dec- 2024")
df["Enrolment Month"] = df["Enrolment Month"].astype(str).str.strip()

# Extract Month and Year separately
df["Enroll_Month_Name"] = df["Enrolment Month"].apply(lambda x: x.split("-")[0].strip()[:3].title())
df["Enroll_Year"] = df["Enrolment Month"].apply(lambda x: x.split("-")[-1].strip())

# Ensure only numeric years
df.loc[~df["Enroll_Year"].str.isdigit(), "Enroll_Year"] = None

# -----------------------------------------
# COMPLETION FLAG
# -----------------------------------------
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# SIDEBAR FILTERS (MULTIPLE MONTHS + YEARS)
# -----------------------------------------
with st.sidebar:
    st.markdown("## 🔎 Analytics Filters")

    # Month options in correct order
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]

    available_months = sorted(
        df["Enroll_Month_Name"].dropna().unique(),
        key=lambda x: month_order.index(x) if x in month_order else 99
    )

    selected_months = st.multiselect(
        "Enrollment Month(s)",
        available_months,
        default=None 
    )

    # Year options
    available_years = sorted(
        df["Enroll_Year"].dropna().unique()
    )

    selected_years = st.multiselect(
        "Enrollment Year(s)",
        available_years,
        default=None 
    )

    st.divider()

    # Other existing multiselect filters
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

    # --- NEW: Badge Filters (Fixed Values) ---
    badge_status_values = ["Completed", "In-Progress"]

    badge1_filter = st.multiselect("Badge 1 Status", badge_status_values)
    badge2_filter = st.multiselect("Badge 2 Status", badge_status_values)
    badge3_filter = st.multiselect("Badge 3 Status", badge_status_values)
    badge4_filter = st.multiselect("Badge 4 Status", badge_status_values)
    badge5_filter = st.multiselect("Badge 5 Status", badge_status_values)

    # --- NEW: CertPrepOD Filter (Fixed Values) ---
    certprepod_filter = st.multiselect(
        "CertPrepOD Status",
        ["Completed", "Not Started"]
    )

# -----------------------------------------
# APPLY FILTERS (OPTIONAL MULTIPLE MONTHS + YEARS)
# -----------------------------------------
filtered_df = df.copy()

# Filter by months if selected
if selected_months:
    filtered_df = filtered_df[filtered_df["Enroll_Month_Name"].isin(selected_months)]

# Filter by years if selected
if selected_years:
    filtered_df = filtered_df[filtered_df["Enroll_Year"].isin(selected_years)]

# Other filters
if cert_filter:
    filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]
if snowpro_filter:
    filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]
if voucher_filter:
    filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]
# Badge filters
if badge1_filter:
    filtered_df = filtered_df[filtered_df["Badge 1 Status"].isin(badge1_filter)]

if badge2_filter:
    filtered_df = filtered_df[filtered_df["Badge 2 Status"].isin(badge2_filter)]

if badge3_filter:
    filtered_df = filtered_df[filtered_df["Badge 3 Status"].isin(badge3_filter)]

if badge4_filter:
    filtered_df = filtered_df[filtered_df["Badge 4 Status"].isin(badge4_filter)]

if badge5_filter:
    filtered_df = filtered_df[filtered_df["Badge 5 Status"].isin(badge5_filter)]

# CertPrepOD filter
if certprepod_filter:
    filtered_df = filtered_df[
        filtered_df["CertPrepOD Course"].isin(certprepod_filter)
    ]


# Prepare header labels
months_label = ", ".join(selected_months) if selected_months else ""
years_label = ", ".join(selected_years) if selected_years else ""


# -----------------------------------------
# EXPORT CHART FUNCTION (Updated Colors)
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
            # Set colors for export to match app
            series.plot(kind="bar", ax=ax, color=CHART_COLOR)
            ax.set_title(name.replace("_", " ").replace(".png", "").title())
            plt.xticks(rotation=45, ha="right")
            # Remove spines for cleaner look
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight")
            plt.close(fig)
            z.writestr(name, img.getvalue())
    buffer.seek(0)
    return buffer

# -----------------------------------------
# HEADER
# -----------------------------------------
h1,h2 = st.columns([6, 2])

with h1:
    st.markdown(f"""
    <div class="page-title">Certification Analytics</div>
    <div class="page-subtitle">
        Enrollment Period: <b>{months_label}{' - ' if months_label and years_label else ''}{years_label}</b>
    </div>""", unsafe_allow_html=True)

# Show message if no data
if filtered_df.empty:
    st.error("No data is available for the selected filters.")
    st.stop()  # Stop further rendering to avoid errors


with h2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.download_button(
        "⬇ Export Charts",
        data=export_charts_as_zip(filtered_df),
        file_name="certification_analytics_charts.zip",
        mime="application/zip"
    )

# -----------------------------------------
# KPI CARDS
# -----------------------------------------
k1, k2, k3, k4 = st.columns(4)

def kpi(col, label, value):
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

kpi(k1, "Total Records", len(filtered_df))
kpi(k2, "Unique Employees", filtered_df["EMP ID"].nunique())
kpi(k3, "Completed Certifications", int(filtered_df["Completed Flag"].sum()))

with k4:
    completion = round(filtered_df["Completed Flag"].mean() * 100, 1) if len(filtered_df) else 0
    st.markdown(f"""
    <div class="card">
        <div class="metric-label">Completion %</div>
        <div class="metric-value">{completion}%</div>
    </div>
    """, unsafe_allow_html=True)
    st.progress(completion / 100 if completion else 0)

# -----------------------------------------
# CHARTS – ROW 1
# -----------------------------------------
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown(
        '<div class="card"><div class="chart-title">Certification Funnel</div>',
        unsafe_allow_html=True
    )

    funnel_df = (
        filtered_df
        .groupby("Certification")["EMP ID"]
        .nunique()
        .sort_values(ascending=True)
        .reset_index()
        .rename(columns={"EMP ID": "Employees"})
    )

    st.bar_chart(
        funnel_df.set_index("Certification"),
        horizontal=True,
        color=CHART_COLOR  # Applied new color
    )

    st.markdown("</div>", unsafe_allow_html=True)


with r1c2:
    st.markdown('<div class="card"><div class="chart-title">SnowPro Status</div>', unsafe_allow_html=True)
    st.bar_chart(
        filtered_df["SnowPro Certified"].value_counts(),
        color=CHART_COLOR  # Applied new color
    )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------
# CHARTS – ROW 2
# -----------------------------------------
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown('<div class="card"><div class="chart-title">Voucher Usage</div>', unsafe_allow_html=True)
    st.bar_chart(
        filtered_df["Voucher Status"].value_counts(),
        color=CHART_COLOR  # Applied new color
    )
    st.markdown("</div>", unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="card"><div class="chart-title">Employees Growth Over Years</div>', unsafe_allow_html=True)

    emp_year_df = (
        filtered_df
        .dropna(subset=["Enroll_Year"])
        .groupby("Enroll_Year")["EMP ID"]
        .nunique()
        .sort_index()
    )

    st.line_chart(
        emp_year_df,
        color=CHART_COLOR  # Applied new color
    )
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------
# CHART – ROW 3 (FULL WIDTH – BADGE FUNNEL)
# -----------------------------------------
st.markdown(
    '<div class="card"><div class="chart-title">Badge Completion Funnel</div>',
    unsafe_allow_html=True
)

funnel_data = {
    "Stage": [
        "Badge 1 Completed",
        "Badge 2 Completed",
        "Badge 3 Completed",
        "Badge 4 Completed",
        "Badge 5 Completed"
    ],
    "Employees": [
        filtered_df[filtered_df["Badge 1 Status"] == "Completed"]["EMP ID"].nunique(),
        filtered_df[filtered_df["Badge 2 Status"] == "Completed"]["EMP ID"].nunique(),
        filtered_df[filtered_df["Badge 3 Status"] == "Completed"]["EMP ID"].nunique(),
        filtered_df[filtered_df["Badge 4 Status"] == "Completed"]["EMP ID"].nunique(),
        filtered_df[filtered_df["Badge 5 Status"] == "Completed"]["EMP ID"].nunique()
    ]
}

funnel_df = pd.DataFrame(funnel_data)

st.bar_chart(
    funnel_df.set_index("Stage"),
    color=CHART_COLOR  # Applied new color
)
st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------
# CHART – ROW 4 (FULL WIDTH – HEATMAP)
# -----------------------------------------
st.markdown(
    '<div class="card"><div class="chart-title">Employee Enrollment Heatmap (Month vs Year)</div>',
    unsafe_allow_html=True
)

heatmap_df = (
    filtered_df
    .dropna(subset=["Enroll_Month_Name", "Enroll_Year"])
    .groupby(["Enroll_Year", "Enroll_Month_Name"])["EMP ID"]
    .nunique()
    .reset_index()
)

heatmap_pivot = heatmap_df.pivot(
    index="Enroll_Month_Name",
    columns="Enroll_Year",
    values="EMP ID"
).fillna(0)

month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
heatmap_pivot = heatmap_pivot.reindex(month_order)

# Set background to match card (white)
fig, ax = plt.subplots(figsize=(12, 5))
fig.patch.set_facecolor('#ffffff')
ax.set_facecolor('#ffffff')

# Updated Color Map to 'Blues' for better UI integration
im = ax.imshow(heatmap_pivot, aspect="auto", cmap=HEATMAP_CMAP) 

ax.set_xticks(range(len(heatmap_pivot.columns)))
ax.set_xticklabels(heatmap_pivot.columns, fontsize=10, color="#64748b", weight="bold")
ax.set_yticks(range(len(heatmap_pivot.index)))
ax.set_yticklabels(heatmap_pivot.index, fontsize=10, color="#64748b", weight="bold")

# Customize Colorbar
cbar = plt.colorbar(im, ax=ax, label="No. of Employees")
cbar.ax.yaxis.set_tick_params(color="#64748b")
cbar.outline.set_visible(False)

# Clean up spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#e2e8f0')
ax.spines['left'].set_color('#e2e8f0')

for i in range(len(heatmap_pivot.index)):
    for j in range(len(heatmap_pivot.columns)):
        # Calculate color for text based on background intensity
        val = int(heatmap_pivot.iloc[i, j])
        text_color = "white" if val > heatmap_pivot.values.max() * 0.5 else "#0f172a"
        ax.text(j, i, val, ha="center", va="center", fontsize=9, color=text_color, fontweight="bold")

ax.set_xlabel("Year", fontsize=10, color="#64748b", labelpad=10)
ax.set_ylabel("Month", fontsize=10, color="#64748b", labelpad=10)

st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------
# DRILL-DOWN TABLE (BOTTOM)
# -----------------------------------------
with st.expander("🔍 View Detailed Records"):
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
        use_container_width=True,
        height=450
    )


# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div style="margin-top:3rem;color:#64748b;font-size:0.85rem;">
💡 Tip: Select Enrollment Month and Year to explore certification trends.
</div>
""", unsafe_allow_html=True)
