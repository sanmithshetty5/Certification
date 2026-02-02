import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
import zipfile
import plotly.express as px


# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Certification Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# SESSION STATE FOR SIDEBAR
# -----------------------------------------
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# -----------------------------------------
# GLOBAL THEME & CONSTANTS
# -----------------------------------------
PRIMARY_COLOR = "#2563eb"
SECONDARY_COLOR = "#475569"
ACCENT_COLOR = "#3b82f6"
BACKGROUND_COLOR = "#f8fafc"
TEXT_COLOR = "#1e293b"
SIDEBAR_BG = "#2C3E50"

# Determine if sidebar should be shown
sidebar_collapsed = st.session_state.sidebar_state == 'collapsed'

st.markdown(f"""
<style>
    /* HIDE STREAMLIT BRANDING */
    [data-testid="stSidebarNav"] {{display: none;}}
    [data-testid="stHeader"] {{display: none;}} 
    [data-testid="stToolbar"] {{display: none;}}
    
    /* Hide native collapse button */
    [data-testid="stSidebarCollapseButton"] {{
        display: none !important;
    }}
    
    /* TOP NAVBAR */
    .top-nav {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        height: 60px;
        background-color: #0F172A;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;
        z-index: 10001;
        box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }}
    .nav-left {{
        color: white !important;
        font-size: 1.2rem;
        font-weight: 700;
        font-family: 'Segoe UI', sans-serif;
    }}
    .nav-links a {{
        color: #E5E7EB !important;
        margin-left: 1.5rem;
        text-decoration: none !important;
        font-weight: 600;
        font-size: 0.9rem;
        transition: color 0.3s;
    }}
    .nav-links a:hover {{
        color: #38BDF8 !important;
    }}
    
    .page-spacer {{
        height: 75px; 
    }}

    /* CUSTOM SIDEBAR STYLING */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {SIDEBAR_BG} 0%, #1a252f 100%) !important;
        padding-top: 60px !important;
        {'display: none !important;' if sidebar_collapsed else ''}
    }}
    
    section[data-testid="stSidebar"] > div {{
        background: transparent !important;
        padding-top: 1rem;
    }}

    /* Sidebar content styling */
    section[data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}
    
    section[data-testid="stSidebar"] .stMarkdown {{
        color: #E2E8F0 !important;
    }}

    /* Section titles */
    section[data-testid="stSidebar"] hr {{
        border-color: #475569;
        margin: 1.5rem 0;
    }}

    /* Multiselect styling */
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stSelectbox label {{
        color: #E2E8F0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] [data-baseweb="select"] {{
        background-color: rgba(255,255,255,0.1) !important;
    }}

    /* Caption styling */
    section[data-testid="stSidebar"] .stCaption {{
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }}

    /* Custom Toggle Button */
    .sidebar-toggle {{
        position: fixed;
        left: {'0' if sidebar_collapsed else '21rem'};
        top: 120px;
        width: 40px;
        height: 40px;
        background-color: {SIDEBAR_BG};
        border-radius: 0 8px 8px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        z-index: 10000;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
        color: white;
        font-size: 1.2rem;
        font-weight: bold;
    }}
    
    .sidebar-toggle:hover {{
        background-color: #34495E;
        width: 45px;
    }}

    /* User profile at bottom */
    .sidebar-footer {{
        position: fixed;
        bottom: 0;
        left: 0;
        width: 21rem;
        padding: 1rem 1.5rem;
        background-color: rgba(0,0,0,0.3);
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 9999;
    }}
    
    .user-avatar {{
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
    }}
    
    .user-name {{
        color: #E2E8F0;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0;
    }}
    
    .user-contract {{
        color: #94A3B8;
        font-size: 0.75rem;
        margin: 0;
    }}

    /* MAIN CONTENT STYLING */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}

    [data-testid="stMain"] h1, 
    [data-testid="stMain"] h2, 
    [data-testid="stMain"] h3, 
    [data-testid="stMain"] p, 
    [data-testid="stMain"] label,
    [data-testid="stMain"] .stMarkdown {{
        color: {TEXT_COLOR} !important;
        font-family: 'Segoe UI', Tahoma, sans-serif !important;
    }}

    /* CARD DESIGN */
    .dashboard-card {{
        background-color: #ffffff;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        transition: all 0.2s ease-in-out;
        height: 100%;
    }}
    
    .dashboard-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        border-color: {PRIMARY_COLOR};
    }}

    /* KPI CARDS */
    .kpi-card {{
        background-color: #ffffff;
        padding: 1.25rem;
        border-radius: 8px;
        border-left: 5px solid {PRIMARY_COLOR};
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
    }}
    .kpi-label {{
        font-size: 0.85rem;
        color: {SECONDARY_COLOR} !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }}
    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 800;
        color: {TEXT_COLOR} !important;
    }}

    /* HEADER STYLING */
    .main-header {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border-bottom: 2px solid {PRIMARY_COLOR};
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
    }}
    .header-title {{
        font-size: 2rem;
        font-weight: 800;
        color: {TEXT_COLOR} !important;
        margin: 0;
    }}
    .header-subtitle {{
        font-size: 1rem;
        color: {SECONDARY_COLOR} !important;
        margin-top: 5px;
    }}

    .chart-title {{
        font-weight: 700;
        font-size: 1.1rem;
        color: {TEXT_COLOR};
        margin-bottom: 1rem;
    }}

    /* BUTTONS */
    div.stDownloadButton > button {{
        background-color: #4ED95E;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }}
    div.stButton > button {{
        background-color: #2563eb;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1rem;
    }}
    div.stButton > button:hover {{
        background-color: #1d4ed8;
    }}

    /* EXPANDER */
    div[data-testid="stExpander"] summary {{
        background-color: transparent;
        color: #1e293b;
        border-radius: 6px;
    }}
    
    /* Sidebar expander */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {{
        background-color: rgba(255,255,255,0.1) !important;
        color: #E2E8F0 !important;
        border-radius: 6px;
    }}
    
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary:hover {{
        background-color: rgba(255,255,255,0.15) !important;
    }}
</style>
""", unsafe_allow_html=True)

# Top Navigation Bar
# st.markdown("""
# <div class="top-nav">
#     <div class="nav-left">Certification Tracker</div>
#     <div class="nav-links">
#         <a href="/" target="_self">Welcome Page</a>
#         <a href="/Data_Entry" target="_self">Data Entry</a>
#         <a href="/Realtime_Analysis" target="_self">Realtime Analysis</a>
#         <a href="/new_data_entry" target="_self">New Data Entry</a>
#         <a href="/About_Page" target="_self">About</a>
#     </div>
# </div>
# <div class="page-spacer"></div>
# """, unsafe_allow_html=True)

st.markdown(f"""
<div class="top-nav">
    <div class="nav-left">Certification Tracker</div>
    <div class="nav-links">
        <a href="/" target="_self">Welcome Page</a>
        <a href="/new_data_entry" target="_self">Credential Tracker</a>
        <a href="/Realtime_Analysis" target="_self">Realtime Analysis</a>
    </div>
</div>

<div class="page-spacer"></div>
""", unsafe_allow_html=True)



# -----------------------------------------
# SNOWFLAKE CONNECTION
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# LOAD DATA
# -----------------------------------------
@st.cache_data(show_spinner="Connecting to Database...")
def load_data():
    return session.sql("""
        SELECT *
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
    """).to_pandas()

df = load_data()

if df.empty:
    st.error("⚠️ No data available.")
    st.stop()

# -----------------------------------------
# DATA PREP
# -----------------------------------------
df["Enrolment Month"] = df["Enrolment Month"].astype(str)
df = df[df["Enrolment Month"] != "nan"]
df["Enrolment Month"] = df["Enrolment Month"].astype(str).str.strip()
df["Enroll_Month_Name"] = df["Enrolment Month"].apply(lambda x: x.split("-")[0].strip()[:3].title())
df["Enroll_Year"] = df["Enrolment Month"].apply(lambda x: x.split("-")[-1].strip())
df.loc[~df["Enroll_Year"].str.isdigit(), "Enroll_Year"] = None
df["Completed Flag"] = df["SnowPro Certified"]=='Completed'

# -----------------------------------------
# TOGGLE BUTTON (BEFORE SIDEBAR)
# -----------------------------------------
toggle_col1, toggle_col2, toggle_col3 = st.columns([0.05, 0.9, 0.05])
with toggle_col1:
    if st.button("◀" if not sidebar_collapsed else "▶", key="sidebar_toggle"):
        st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
        st.rerun()

# Add CSS for the toggle button positioning

st.markdown(f"""
<style>
    /* Position the toggle button */
    div[data-testid="column"]:first-child button {{
        position: fixed !important;
        left: {'0' if sidebar_collapsed else '21rem'} !important;
        top: 120px !important;
        width: 40px !important;
        height: 40px !important;
        background-color: {SIDEBAR_BG} !important;
        border-radius: 0 8px 8px 0 !important;
        border: none !important;
        z-index: 10000 !important;
        padding: 0 !important;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        color: white !important;
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }}
    
    div[data-testid="column"]:first-child button:hover {{
        background-color: #34495E !important;
        width: 45px !important;
    }}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# SIDEBAR
# -----------------------------------------

if not sidebar_collapsed:
    with st.sidebar:
        # Logo
        st.image("https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/analytics.png", width=60)
        st.markdown("## Analytics Console")
        st.markdown("---")
        
        # Time Period
        st.caption("⏱️ TIME PERIOD")
        col1, col2 = st.columns(2)
        with col1:
            available_years = sorted(df["Enroll_Year"].dropna().unique())
            selected_years = st.multiselect("Year", available_years, key="year_filter")
        with col2:
            month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            available_months = sorted(
                df["Enroll_Month_Name"].dropna().unique(),
                key=lambda x: month_order.index(x) if x in month_order else 99
            )
            selected_months = st.multiselect("Month", available_months, key="month_filter")

        st.markdown("---")
        
        # Main Filters
        st.caption("🔍 FILTERS")
        cert_filter = st.multiselect("Certification", sorted(df["Certification"].dropna().unique()), key="cert_filter")
        snowpro_filter = st.multiselect("SnowPro Status", sorted(df["SnowPro Certified"].dropna().unique()), key="snowpro_filter")
        voucher_filter = st.multiselect("Voucher Status", sorted(df["Voucher Status"].dropna().unique()), key="voucher_filter")

        st.markdown("---")
        
        # Badge Details
        st.caption("🎖️ BADGE DETAILS")
        with st.expander("Badge Filters", expanded=False):
            badge_status_values = ["Completed", "In Progress"]
            b1 = st.multiselect("Badge 1", badge_status_values, key="b1")
            b2 = st.multiselect("Badge 2", badge_status_values, key="b2")
            b3 = st.multiselect("Badge 3", badge_status_values, key="b3")
            b4 = st.multiselect("Badge 4", badge_status_values, key="b4")
            b5 = st.multiselect("Badge 5", badge_status_values, key="b5")
            certprep = st.multiselect("CertPrepOD", ["Completed", "In Progress"], key="certprep")

        # Add space for footer
        st.markdown("<br><br><br>", unsafe_allow_html=True)

else:
    # Set default values when sidebar is collapsed
    selected_years = []
    selected_months = []
    cert_filter = []
    snowpro_filter = []
    voucher_filter = []
    b1 = []
    b2 = []
    b3 = []
    b4 = []
    b5 = []
    certprep = []

# -----------------------------------------
# FILTERING LOGIC
# -----------------------------------------
filtered_df = df.copy()

if selected_months: filtered_df = filtered_df[filtered_df["Enroll_Month_Name"].isin(selected_months)]
if selected_years: filtered_df = filtered_df[filtered_df["Enroll_Year"].isin(selected_years)]
if cert_filter: filtered_df = filtered_df[filtered_df["Certification"].isin(cert_filter)]
if snowpro_filter: filtered_df = filtered_df[filtered_df["SnowPro Certified"].isin(snowpro_filter)]
if voucher_filter: filtered_df = filtered_df[filtered_df["Voucher Status"].isin(voucher_filter)]
if b1: filtered_df = filtered_df[filtered_df["Badge 1 Status"].isin(b1)]
if b2: filtered_df = filtered_df[filtered_df["Badge 2 Status"].isin(b2)]
if b3: filtered_df = filtered_df[filtered_df["Badge 3 Status"].isin(b3)]
if b4: filtered_df = filtered_df[filtered_df["Badge 4 Status"].isin(b4)]
if b5: filtered_df = filtered_df[filtered_df["Badge 5 Status"].isin(b5)]
if certprep: filtered_df = filtered_df[filtered_df["CertPrepOD Course"].isin(certprep)]

years_label = ", ".join(selected_years) if selected_years else "All Years"
months_label = ", ".join(selected_months) if selected_months else "All Months"

# -----------------------------------------
# EXPORT LOGIC
# -----------------------------------------

def export_charts_as_zip(data):
    buffer = io.BytesIO()
    skipped = []

    with zipfile.ZipFile(buffer, "w") as z:
        charts = {
            "Certification Distribution": data["Certification"].value_counts(),
            "SnowPro Status": data["SnowPro Certified"].value_counts(),
            "Voucher Status": data["Voucher Status"].value_counts()
        }

        for title, series in charts.items():
            if series.empty:
                skipped.append(title)
                continue

            fig, ax = plt.subplots(figsize=(7, 5))
            series.plot(kind="bar", ax=ax, color=PRIMARY_COLOR)
            ax.set_title(title)
            plt.xticks(rotation=45, ha="right")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight", dpi=100)
            plt.close(fig)

            z.writestr(f"{title.replace(' ', '_').lower()}.png", img.getvalue())

    buffer.seek(0)
    return buffer, skipped

# Wrap main content
st.markdown(f'<div class="main-content {"shifted" if not sidebar_collapsed else ""}">', unsafe_allow_html=True)

# -----------------------------------------
# UI STRUCTURE
# -----------------------------------------

# HEADER
col_h1, col_h2 = st.columns([0.85, 0.15])
with col_h1:
    st.markdown(f"""
    <div class="main-header">
        <div class="header-title">Certification Dashboard</div>
        <div class="header-subtitle">Overview for <b>{months_label}</b> in <b>{years_label}</b></div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)
    if not filtered_df.empty:
        zip_data, skipped_charts = export_charts_as_zip(filtered_df)
    
        if zip_data.getbuffer().nbytes == 0:
            st.info("ℹ️ No charts available to export for the selected filters.")
        else:
            st.download_button(
                "Export Report",
                data=zip_data,
                file_name="analytics.zip"
            )
            if skipped_charts:
                st.info(
                    "ℹ️ Some sections were skipped due to insufficient data: "
                    + ", ".join(skipped_charts)
                )

        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.rerun()

if filtered_df.empty:
    st.warning("⚠️ No data available matching your filters.")
    st.stop()

# METRICS ROW
m1, m2, m3, m4 = st.columns(4)

def metric_box(col, label, value):
    with col:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
        """, unsafe_allow_html=True)

metric_box(m1, "Total Records", len(filtered_df))
metric_box(m2, "Unique Learners", filtered_df["EMP ID"].nunique())
metric_box(m3, "Certified Users", int(filtered_df["Completed Flag"].sum()))

with m4:
    completion = round(filtered_df["Completed Flag"].mean() * 100, 1) if len(filtered_df) else 0
    st.markdown(f"""
    <div class="kpi-card" style="border-left-color: #10b981;">
        <div class="kpi-label">Completion Rate</div>
        <div class="kpi-value">{completion}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ROW 1 CHARTS
c1, c2 = st.columns(2)

with c1:
    st.markdown('<div class="dashboard-card"><div class="chart-title">Certification Funnel</div>', unsafe_allow_html=True)
    funnel_data = filtered_df.groupby("Certification")["EMP ID"].nunique().reset_index()
    funnel_data.columns = ["Certification", "Learners"]
    funnel_data = funnel_data.sort_values("Learners", ascending=True)
    fig = px.bar(funnel_data, x="Learners", y="Certification", orientation='h', text="Learners", color_discrete_sequence=[PRIMARY_COLOR])
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=10, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, visible=True, title=None, tickfont=dict(color="#1e293b", size=12)),
        yaxis=dict(showgrid=False, title=None, tickfont=dict(color="#1e293b", size=12)),
        font=dict(family="Segoe UI", color="#1e293b"), height=250, hovermode="y unified", dragmode="pan"
    )
    fig.update_traces(textposition='outside', textfont_color="#1e293b")
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover', 'scrollZoom': True, 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown('<div class="dashboard-card"><div class="chart-title">SnowPro Status</div>', unsafe_allow_html=True)
    status_counts = filtered_df["SnowPro Certified"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]
    fig = px.pie(status_counts, names="Status", values="Count", hole=0.5, color_discrete_sequence=[PRIMARY_COLOR, "#64748b", "#94a3b8", "#cbd5e1"])
    fig.update_traces(textposition='inside', textinfo='percent+label', hovertemplate = "<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}", marker=dict(line=dict(color='#ffffff', width=2)))
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(t=20, l=0, r=0, b=20), font=dict(family="Segoe UI", color="#1e293b", size=13), showlegend=False, height=250)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False, 'modeBarButtonsToRemove': ['lasso2d', 'select2d']})
    st.markdown("</div>", unsafe_allow_html=True)

# ROW 2 CHARTS
c3, c4 = st.columns(2)

with c3:
    st.markdown('<div class="dashboard-card"><div class="chart-title">Voucher Utilization</div>', unsafe_allow_html=True)

    # Remove NULLs explicitly
    voucher_series = filtered_df["Voucher Status"].dropna()

    # Case 1: No usable data
    if voucher_series.empty:
        st.info("ℹ️ Voucher status data is not available for the selected filters.")
    
    # Case 2: Data exists → show chart
    else:
        voucher_data = voucher_series.value_counts().reset_index()
        voucher_data.columns = ["Status", "Count"]

        distinct_colors = ["#2563eb", "#10b981", "#f59e0b", "#64748b", "#ef4444"]

        fig = px.pie(
            voucher_data,
            names="Status",
            values="Count",
            color_discrete_sequence=distinct_colors
        )

        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}",
            marker=dict(line=dict(color='#ffffff', width=2))
        )

        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=20, l=0, r=0, b=20),
            font=dict(family="Segoe UI", color="#1e293b", size=13),
            showlegend=False,
            height=250
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})

    st.markdown("</div>", unsafe_allow_html=True)

with c4:    
    # FULL WIDTH BADGE CHART
    st.markdown('<div class="dashboard-card"><div class="chart-title">Badge Progression</div>', unsafe_allow_html=True)
    
    # 1. Prepare Data
    badge_counts = [
        filtered_df[filtered_df[f"Badge {i} Status"] == "Completed"]["EMP ID"].nunique() 
        for i in range(1, 6)
    ]
    
    badge_data = pd.DataFrame({
        "Stage": ["Badge 1", "Badge 2", "Badge 3", "Badge 4", "Badge 5"],
        "Learners": badge_counts,
        "ColorGroup": ["B1", "B2", "B3", "B4", "B5"] # Dummy column to force different colors
    })
    
    # 2. Distinct Color Palette
    distinct_sequence = ["#2563eb", "#06b6d4", "#8b5cf6", "#d946ef", "#f97316"] 
    
    # 3. Create Interactive Column Chart
    fig = px.bar(
        badge_data, 
        x='Stage', 
        y='Learners', 
        color='ColorGroup', # Colors each bar differently
        color_discrete_sequence=distinct_sequence,
        text='Learners' # Shows the count on top
    )
    
    # 4. Apply Professional Styling
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, l=0, r=0, b=0),
        showlegend=False, 
        height=350,       
    
        # Axis Styling
        xaxis=dict(
            title=None,
            tickfont=dict(color="#1e293b", size=13, family="Segoe UI"),
            showgrid=False
        ),
        yaxis=dict(
            tickfont=dict(color="#1e293b", size=12, family="Segoe UI"),
            title=None,
            showgrid=True,
            gridcolor="#e2e8f0"
        ),
        font=dict(family="Segoe UI", color="#1e293b")
    )
    # Style the text on top of bars
    fig.update_traces(
        textposition="outside", 
        textfont=dict(color="#1e293b", size=14)
    )
    
    # 5. Toolbar Configuration
    my_config = {
        'displayModeBar': 'hover',
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    }
    
    st.plotly_chart(fig, use_container_width=True, config=my_config)
    



# Create two columns for the bottom row
row3_1, row3_2 = st.columns(2)

# ==============================================================================
# LEFT COLUMN: Vertical / SL Funnel (Existing Logic)
# ==============================================================================
with row3_1:
    st.markdown('<div class="dashboard-card"><div class="chart-title">Certification Funnel by Vertical</div>', unsafe_allow_html=True)

    # 1. Prepare Data
    vertical_data = (
        filtered_df[filtered_df["Completed Flag"] == True]
        .groupby("Vertical / SL")["EMP ID"]
        .nunique()
        .reset_index()
        .rename(columns={"EMP ID": "Completed Employees"})
        .sort_values("Completed Employees", ascending=True) 
    )

    # 2. Dynamic Height (Ensures no scroll bars inside the chart)
    v_height = max(400, len(vertical_data) * 35)

    # 3. Create Chart
    fig_v = px.bar(
        vertical_data,
        x="Completed Employees",
        y="Vertical / SL",
        orientation='h', 
        text="Completed Employees",
        color="Completed Employees", 
        color_continuous_scale="Blues"
    )

    fig_v.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=0, r=0, b=0),
        xaxis=dict(showgrid=False, visible=False), 
        yaxis=dict(
            title=None,
            tickfont=dict(color="#1e293b", size=12, family="Segoe UI"),
            dtick=1
        ),
        font=dict(family="Segoe UI", color="#1e293b"),
        height=v_height, 
        coloraxis_showscale=False 
    )

    fig_v.update_traces(
        textposition='outside', 
        textfont=dict(color="#1e293b", size=12),
        cliponaxis=False 
    )

    st.plotly_chart(fig_v, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})
    st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# RIGHT COLUMN: Account Certification Overview (Heatmap)
# ==============================================================================
with row3_2:
    # Title remains exactly as requested (no color change)
    st.markdown('<div class="dashboard-card"><div class="chart-title">Account-wise Certification Summary</div>', unsafe_allow_html=True)

    # --- FIX: Checking which column to use for Status ---
    status_col = "SnowPro Certified" 
    
    # 1. Prepare Table Data
    if status_col in filtered_df.columns:
        table_df = (
            filtered_df
            .groupby("Account")
            .agg(
                Total_Employees=("EMP ID", "nunique"),
                Certified=(status_col, lambda x: (x == "Completed").sum()),
                In_Progress=(status_col, lambda x: (x == "In Progress").sum()),
                Not_Started=(status_col, lambda x: (x == "Not Started").sum()),
            )
            .reset_index()
            .sort_values(by="Certified", ascending=False)
        )

        # 2. Apply Coloring for Dark Background
        # We use Pandas Styler to force Black Background and White Text on the cells
        styled_df = (
            table_df.style
            .set_properties(**{
                'background-color': '#0e1117',  # Very Dark Grey/Black to match dashboard
                'color': '#ffffff',             # White Text for visibility
                'border-color': '#333333'       # Subtle border for row separation
            })
            # Optional: Highlight the "Certified" column slightly to make it stand out
            .applymap(lambda x: 'color: #4ade80; font-weight: bold;', subset=['Certified']) 
        )

        # 3. Display Interactive Table
        st.dataframe(
            styled_df, # Pass the STYLED dataframe here
            use_container_width=True,
            height=450, 
            hide_index=True 
        )
    else:
        st.error(f"Error: Column '{status_col}' not found. Please check your Excel column names.")

    st.markdown("</div>", unsafe_allow_html=True)



## ==============================================================================
# CHART: ENROLLMENT TREND (FIXED VISIBILITY)
# ==============================================================================
# st.markdown('<div class="dashboard-card"><div class="chart-title">Completion Trend Over Time</div>', unsafe_allow_html=True)

# # 1. Prepare Data
# if "Enroll_Month_Name" in filtered_df.columns and "Enroll_Year" in filtered_df.columns:
    
#     # Create a copy to work on
#     trend_df = filtered_df.copy()

#     trend_df = trend_df[trend_df["Completed Flag"] == True]
    
#     # Drop missing values
#     trend_df = trend_df.dropna(subset=["Enroll_Year", "Enroll_Month_Name"])
    
#     # Create a Date String (e.g., "2024-Jan")
#     trend_df["DateStr"] = trend_df["Enroll_Year"].astype(str) + "-" + trend_df["Enroll_Month_Name"]
    
#     # Convert to DateTime Object
#     trend_df["Timeline"] = pd.to_datetime(trend_df["DateStr"], format='%Y-%b', errors='coerce')
    
#     # Aggregate: Count unique employees per date
#     time_series = (
#         trend_df
#         .groupby("Timeline")["EMP ID"]
#         .nunique()
#         .reset_index()
#         .rename(columns={"EMP ID": "Completed Certifications"})
#         .sort_values("Timeline") # Sort Oldest -> Newest
#     )

#     # 2. Create Line Chart
#     fig = px.line(
#         time_series, 
#         x='Timeline', 
#         y='Completed Certifications',
#         markers=True, # Show dots at data points
#     )

#     # 3. Apply High-Contrast "Dark Mode" Styling
#     fig.update_layout(
#         # --- FIX: Force Dark Background Colors (Not Transparent) ---
#         plot_bgcolor="#0e1117",  # Dark Grey/Black plot area
#         paper_bgcolor="#0e1117", # Dark Grey/Black outer area
        
#         margin=dict(t=30, l=10, r=10, b=0),
        
#         # X-Axis Styling
#         xaxis=dict(
#             title=None,
#             showgrid=True,
#             gridcolor="#333333",      # Dark grey grid lines (subtle)
#             tickformat="%b %Y",       # Formats date as "Jan 2024"
#             tickfont=dict(color="white", size=12),
#             rangeslider=dict(visible=True, bgcolor="#1e293b", thickness=0.1), # Visible slider
#             type="date"
#         ),
        
#         # Y-Axis Styling
#         yaxis=dict(
#             title=None,
#             showgrid=True,
#             gridcolor="#333333",      # Dark grey grid lines
#             tickfont=dict(color="white", size=12),
#             zerolinecolor="#333333"
#         ),
        
#         # Font & Hover Styling
#         font=dict(family="Segoe UI", color="white"),
#         height=450,
#         hovermode="x unified"
#     )

#     # Line & Marker Styling (Neon Cyan for Pop)
#     fig.update_traces(
#         line=dict(color="#22d3ee", width=3), # Bright Neon Cyan
#         marker=dict(size=8, color="#22d3ee", line=dict(width=2, color="#0e1117")), # Cyan dot with black border
#         hovertemplate='%{y} Employees<extra></extra>' # Clean hover text
#     )

#     st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})

# else:
#     st.warning("Columns 'Enroll_Year' and 'Enroll_Month_Name' are required for this chart.")

# st.markdown("</div>", unsafe_allow_html=True)


# ==============================================================================
# CHART: COMPLETION TREND (Stock Market Style)
# ==============================================================================
st.markdown('<div class="dashboard-card"><div class="chart-title">Certification Completion Trend</div>', unsafe_allow_html=True)

# --- CONFIGURATION: Enter your exact column name here ---
completion_date_col = "Actual Date of Completion" 
# If your column is named differently (e.g., "Completion Date", "Date Certified"), change the line above.

# 1. Prepare Data
if completion_date_col in filtered_df.columns:
    
    # Create a copy and handle dates
    trend_df = filtered_df.copy()
    
    # Convert to DateTime (errors='coerce' handles invalid formats gracefully)
    trend_df[completion_date_col] = pd.to_datetime(trend_df[completion_date_col], errors='coerce')
    
    # Drop rows where the completion date is missing (i.e., not certified yet)
    trend_df = trend_df.dropna(subset=[completion_date_col])
    
    if not trend_df.empty:
        # Group by Month to create a smooth "Stock Market" curve
        # We use pd.Grouper(freq='ME') to group by Month End
        time_series = (
            trend_df
            .groupby(pd.Grouper(key=completion_date_col, freq='ME'))["EMP ID"]
            .nunique()
            .reset_index()
            .rename(columns={"EMP ID": "Count", completion_date_col: "Timeline"})
        )
        
        # 2. Create Line Chart
        fig = px.line(
            time_series, 
            x='Timeline', 
            y='Count',
            markers=True, 
        )

        # 3. Apply High-Contrast "Dark Mode" Styling
        fig.update_layout(
            # Force Dark Background
            plot_bgcolor="#0e1117",  
            paper_bgcolor="#0e1117", 
            
            margin=dict(t=30, l=10, r=10, b=0),
            
            # X-Axis Styling
            xaxis=dict(
                title=None,
                showgrid=True,
                gridcolor="#333333",      
                tickformat="%b %Y",       # Format: "Jan 2024"
                tickfont=dict(color="white", size=12, family="Segoe UI"),
                rangeslider=dict(visible=True, bgcolor="#1e293b", thickness=0.1), # Zoom Slider
                type="date"
            ),
            
            # Y-Axis Styling
            yaxis=dict(
                title=None,
                showgrid=True,
                gridcolor="#333333",      
                tickfont=dict(color="white", size=12, family="Segoe UI"),
                zerolinecolor="#333333"
            ),
            
            font=dict(family="Segoe UI", color="white"),
            height=450,
            hovermode="x unified"
        )

        # Line & Marker Styling (Neon Cyan)
        fig.update_traces(
            line=dict(color="#22d3ee", width=3), 
            marker=dict(size=8, color="#22d3ee", line=dict(width=2, color="#0e1117")),
            hovertemplate='%{y} Certifications<extra></extra>' 
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': 'hover', 'displaylogo': False})
    
    else:
        st.info("No completion dates found. Employees may not be certified yet.")

else:
    st.error(f"Column '{completion_date_col}' not found. Please check your Excel column name.")

st.markdown("</div>", unsafe_allow_html=True)
# DATA GRID
with st.expander("🔎 Inspect Raw Data"):
    st.dataframe(filtered_df, use_container_width=True, height=400)
    

# FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #94a3b8; font-size: 0.8rem;">
    Enterprise Certification Analytics • Confidential
</div>
""", unsafe_allow_html=True)
