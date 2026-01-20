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
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# GLOBAL THEME & CONSTANTS
# -----------------------------------------
# Professional Indigo Palette
CHART_COLOR = "#6366f1"  # Indigo-500
HEATMAP_CMAP = "Blues"   
PRIMARY_COLOR = "#4f46e5" # Indigo-600
BACKGROUND_COLOR = "#f1f5f9" # Slate-100

# -----------------------------------------
# GLOBAL CSS – MODERN DASHBOARD UI
# -----------------------------------------
st.markdown("""
<style>
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main Background */
    .stApp {
        background-color: #f8fafc;
    }

    /* HEADER STYLING */
    .page-header {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .page-title {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1e293b;
        margin: 0;
    }
    .page-subtitle {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.2rem;
        font-weight: 500;
    }

    /* CARD STYLING */
    .metric-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        border-color: #cbd5e1;
    }
    .metric-label {
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0f172a;
    }
    .metric-icon {
        font-size: 1.2rem;
        margin-right: 0.5rem;
        opacity: 0.7;
    }

    /* CHART CONTAINER */
    .chart-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    .chart-header {
        font-size: 1rem;
        font-weight: 700;
        color: #334155;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f1f5f9;
    }

    /* BUTTONS */
    div.stButton > button, div.stDownloadButton > button {
        width: 100%;
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-color: #0f172a !important;
    }

    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* CUSTOM PROGRESS BAR */
    div.stProgress > div > div > div > div {
        background-color: #4f46e5 !important;
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
@st.cache_data(show_spinner="Fetching certification records...")
def load_data():
    return session.sql("""
        SELECT *
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
    """).to_pandas()

df = load_data()

if df.empty:
    st.error("⚠️ No data available in the database.")
    st.stop()

# -----------------------------------------
# DATA PREPROCESSING
# -----------------------------------------
df["Enrolment Month"] = df["Enrolment Month"].astype(str)
df = df[df["Enrolment Month"] != "nan"]
df["Enrolment Month"] = df["Enrolment Month"].astype(str).str.strip()
df["Enroll_Month_Name"] = df["Enrolment Month"].apply(lambda x: x.split("-")[0].strip()[:3].title())
df["Enroll_Year"] = df["Enrolment Month"].apply(lambda x: x.split("-")[-1].strip())
df.loc[~df["Enroll_Year"].str.isdigit(), "Enroll_Year"] = None
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# SIDEBAR FILTERS (GROUPED FOR UX)
# -----------------------------------------
with st.sidebar:
    st.markdown("### 📊 Control Panel")
    
    # --- Time Filters ---
    st.markdown("#### 📅 Time Period")
    
    month_order = ["Jan","Feb","Mar","Apr","May","Jun",
                   "Jul","Aug","Sep","Oct","Nov","Dec"]
    available_months = sorted(
        df["Enroll_Month_Name"].dropna().unique(),
        key=lambda x: month_order.index(x) if x in month_order else 99
    )
    
    col_y, col_m = st.columns([1, 1])
    with col_y:
        available_years = sorted(df["Enroll_Year"].dropna().unique())
        selected_years = st.multiselect("Year", available_years, placeholder="All")
    with col_m:
        selected_months = st.multiselect("Month", available_months, placeholder="All")

    st.divider()

    # --- Core Filters ---
    st.markdown("#### 🎓 Certification Details")
    cert_filter = st.multiselect("Certification Type", sorted(df["Certification"].dropna().unique()))
    snowpro_filter = st.multiselect("SnowPro Status", sorted(df["SnowPro Certified"].dropna().unique()))
    voucher_filter = st.multiselect("Voucher Status", sorted(df["Voucher Status"].dropna().unique()))

    st.divider()

    # --- Advanced Filters (Collapsible) ---
    with st.expander("🛠️ Advanced Badge Filters"):
        badge_status_values = ["Completed", "In-Progress"]
        badge1_filter = st.multiselect("Badge 1", badge_status_values)
        badge2_filter = st.multiselect("Badge 2", badge_status_values)
        badge3_filter = st.multiselect("Badge 3", badge_status_values)
        badge4_filter = st.multiselect("Badge 4", badge_status_values)
        badge5_filter = st.multiselect("Badge 5", badge_status_values)
        
        st.markdown("---")
        certprepod_filter = st.multiselect("CertPrepOD", ["Completed", "Not Started"])

# -----------------------------------------
# APPLY FILTERS
# -----------------------------------------
filtered_df = df.copy()

if selected_months:
    filtered_df = filtered_df[filtered_df["Enroll_Month_Name"].isin(selected_months)]
if selected_years:
    filtered_df = filtered_df[filtered_df["Enroll_Year"].isin(selected_years)]
if cert_filter:
    filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]
if snowpro_filter:
    filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]
if voucher_filter:
    filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]
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
if certprepod_filter:
    filtered_df = filtered_df[filtered_df["CertPrepOD Course"].isin(certprepod_filter)]

months_label = ", ".join(selected_months) if selected_months else "All Months"
years_label = ", ".join(selected_years) if selected_years else "All Years"

# -----------------------------------------
# EXPORT FUNCTION
# -----------------------------------------
def export_charts_as_zip(data):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as z:
        charts = {
            "cert_dist.png": data["Certification"].value_counts(),
            "snowpro_stat.png": data["SnowPro Certified"].value_counts(),
            "voucher_stat.png": data["Voucher Status"].value_counts()
        }
        for name, series in charts.items():
            fig, ax = plt.subplots(figsize=(7, 5))
            series.plot(kind="bar", ax=ax, color=CHART_COLOR)
            ax.set_title(name.replace("_", " ").replace(".png", "").title())
            plt.xticks(rotation=45, ha="right")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight", dpi=100)
            plt.close(fig)
            z.writestr(name, img.getvalue())
    buffer.seek(0)
    return buffer

# -----------------------------------------
# MAIN UI
# -----------------------------------------

# 1. Header Section
col_head, col_btn = st.columns([0.85, 0.15])
with col_head:
    st.markdown(f"""
    <div class="page-header">
        <div>
            <div class="page-title">Certification Analytics Dashboard</div>
            <div class="page-subtitle">Viewing Data for: <b>{years_label}</b> • <b>{months_label}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    if not filtered_df.empty:
        st.download_button(
            "📥 Export",
            data=export_charts_as_zip(filtered_df),
            file_name="charts.zip",
            mime="application/zip",
            help="Download charts as images"
        )

if filtered_df.empty:
    st.warning("⚠️ No records found for the selected filters. Please adjust your selection.")
    st.stop()

# 2. KPI Cards
k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, icon, label, value, subtext=None):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label"><span class="metric-icon">{icon}</span>{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

kpi_card(k1, "👥", "Total Enrollments", len(filtered_df))
kpi_card(k2, "🆔", "Unique Employees", filtered_df["EMP ID"].nunique())
kpi_card(k3, "🏆", "Certifications Won", int(filtered_df["Completed Flag"].sum()))

with k4:
    completion = round(filtered_df["Completed Flag"].mean() * 100, 1) if len(filtered_df) else 0
    # Custom HTML for Progress to keep styling tight
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label"><span class="metric-icon">📈</span>Completion Rate</div>
        <div class="metric-value">{completion}%</div>
    </div>
    """, unsafe_allow_html=True)
    # Render native Streamlit progress bar below the card text
    st.progress(completion / 100 if completion else 0)

st.markdown("<br>", unsafe_allow_html=True)

# 3. Row 1: Funnel & SnowPro
r1c1, r1c2 = st.columns(2)

with r1c1:
    st.markdown('<div class="chart-container"><div class="chart-header">Certification Demand Funnel</div>', unsafe_allow_html=True)
    funnel_df = (
        filtered_df.groupby("Certification")["EMP ID"]
        .nunique().sort_values(ascending=True).reset_index()
        .rename(columns={"EMP ID": "Employees"})
    )
    st.bar_chart(funnel_df.set_index("Certification"), horizontal=True, color=CHART_COLOR)
    st.markdown("</div>", unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="chart-container"><div class="chart-header">SnowPro Certification Status</div>', unsafe_allow_html=True)
    st.bar_chart(filtered_df["SnowPro Certified"].value_counts(), color=CHART_COLOR)
    st.markdown("</div>", unsafe_allow_html=True)

# 4. Row 2: Vouchers & Growth
r2c1, r2c2 = st.columns(2)

with r2c1:
    st.markdown('<div class="chart-container"><div class="chart-header">Voucher Usage Distribution</div>', unsafe_allow_html=True)
    st.bar_chart(filtered_df["Voucher Status"].value_counts(), color=CHART_COLOR)
    st.markdown("</div>", unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="chart-container"><div class="chart-header">Enrollment Growth Trend</div>', unsafe_allow_html=True)
    emp_year_df = (
        filtered_df.dropna(subset=["Enroll_Year"])
        .groupby("Enroll_Year")["EMP ID"].nunique().sort_index()
    )
    st.line_chart(emp_year_df, color=CHART_COLOR)
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Full Width Badge Funnel
st.markdown('<div class="chart-container"><div class="chart-header">Badge Completion Journey</div>', unsafe_allow_html=True)
badge_data = {
    "Stage": ["Badge 1", "Badge 2", "Badge 3", "Badge 4", "Badge 5"],
    "Employees": [
        filtered_df[filtered_df[f"Badge {i} Status"] == "Completed"]["EMP ID"].nunique()
        for i in range(1, 6)
    ]
}
st.bar_chart(pd.DataFrame(badge_data).set_index("Stage"), color=CHART_COLOR)
st.markdown("</div>", unsafe_allow_html=True)

# 6. Heatmap (Polished Matplotlib)
st.markdown('<div class="chart-container"><div class="chart-header">Seasonal Enrollment Intensity</div>', unsafe_allow_html=True)

heatmap_df = (
    filtered_df.dropna(subset=["Enroll_Month_Name", "Enroll_Year"])
    .groupby(["Enroll_Year", "Enroll_Month_Name"])["EMP ID"].nunique().reset_index()
)

if not heatmap_df.empty:
    heatmap_pivot = heatmap_df.pivot(
        index="Enroll_Month_Name", columns="Enroll_Year", values="EMP ID"
    ).fillna(0).reindex(month_order)

    # Matplotlib Setup
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor('#ffffff')
    ax.set_facecolor('#ffffff')

    # Draw Heatmap
    im = ax.imshow(heatmap_pivot, aspect="auto", cmap=HEATMAP_CMAP)

    # Styling Ticks
    ax.set_xticks(range(len(heatmap_pivot.columns)))
    ax.set_xticklabels(heatmap_pivot.columns, fontsize=9, color="#475569", weight="600")
    ax.set_yticks(range(len(heatmap_pivot.index)))
    ax.set_yticklabels(heatmap_pivot.index, fontsize=9, color="#475569", weight="600")

    # Remove Spines
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Styling Colorbar
    cbar = plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.outline.set_visible(False)
    cbar.ax.tick_params(colors="#64748b", size=0)

    # Annotations
    for i in range(len(heatmap_pivot.index)):
        for j in range(len(heatmap_pivot.columns)):
            val = int(heatmap_pivot.iloc[i, j])
            if pd.notna(val) and val > 0:
                text_color = "white" if val > heatmap_pivot.values.max() * 0.6 else "#1e293b"
                ax.text(j, i, val, ha="center", va="center", fontsize=8, color=text_color, fontweight="bold")
    
    ax.set_xlabel("")
    ax.set_ylabel("")
    st.pyplot(fig)
else:
    st.info("Not enough data to generate heatmap for the selected period.")
st.markdown("</div>", unsafe_allow_html=True)

# 7. Detailed Table
with st.expander("📄 View Detailed Enrollment Records", expanded=False):
    st.dataframe(
        filtered_df[[
            "EMP ID", "EMP Name", "Certification", "Enrolment Month",
            "SnowPro Certified", "Voucher Status", "Account", "Vertical / SL"
        ]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Enrolment Month": st.column_config.TextColumn("Month"),
            "SnowPro Certified": st.column_config.TextColumn("SnowPro", help="Certification Status"),
            "Voucher Status": st.column_config.TextColumn("Voucher", help="Voucher Usage")
        },
        height=400
    )

# 8. Footer
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding: 2rem; border-top:1px solid #e2e8f0; color:#94a3b8; font-size:0.8rem;">
    Certification Analytics Dashboard • Generated via Streamlit
</div>
""", unsafe_allow_html=True)
