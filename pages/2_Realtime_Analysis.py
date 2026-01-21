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
# GLOBAL THEME & CONSTANTS
# -----------------------------------------
# Professional Palette
PRIMARY_COLOR = "#2563eb"    # Blue-600
SECONDARY_COLOR = "#475569"  # Slate-600
ACCENT_COLOR = "#3b82f6"     # Blue-500
BACKGROUND_COLOR = "#f8fafc" # Slate-50 (Very light grey)
TEXT_COLOR = "#1e293b"# Slate-800 (Very dark grey)
SB_TEXT="ffffff"
SB_BACKGROUND_COLOR="000000"
# Matplotlib Colors
CHART_COLOR = "#2563eb"      
HEATMAP_CMAP = "Blues"

# -----------------------------------------
# GLOBAL CSS – FORCE LIGHT MODE & MODERN UI
# -----------------------------------------
st.markdown(f"""
<style>
    /* 1. FORCE LIGHT THEME BASE */
    .stApp {{
        background-color: {BACKGROUND_COLOR};
    }}
    
    /* 2. TYPOGRAPHY & TEXT COLORS */
    h1, h2, h3, h4, h5, h6, p, div, span, label {{
        color: {SB_TEXT} !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
    
    /* Exception: White text on buttons or specific badges */
    button p, div[data-testid="stMetricValue"] {{
        color: inherit !important;
    }}

    /* 3. MODERN CARD DESIGN */
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

    /* 4. KPI CARDS WITH ACCENT BORDER */
    .kpi-card {{
        background-color: #ffffff;
        padding: 1.25rem;
        border-radius: 8px;
        border-left: 5px solid {PRIMARY_COLOR}; /* Left accent bar */
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

    /* 5. HEADER STYLING */
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

    
    /* SIDEBAR EXPANDER – FORCE WHITE TEXT */
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {{
        color: #ffffff !important;
    }}
    section[data-testid="stSidebar"] div[data-testid="stExpander"] summary:hover {{
        background-color: rgba(255,255,255,0.08);
    }}

    /* 7. MATPLOTLIB TRANSPARENCY FIX */
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
    div.stDownloadButton > button:hover {{
        background-color: #4ED95E;
        transform: translateY(-3px);
        color: #ffffff !important;
    }}

        /* EXPANDER HEADER */
    div[data-testid="stExpander"] summary {{
        background-color: transparent;
        color: #1e293b;
        border-radius: 6px;
    }}
    
    /* HOVER */
    div[data-testid="stExpander"] summary:hover {{
        background-color: #e2e8f0;  /* Light slate */
    }}
    
    /* EXPANDER CONTENT */
    div[data-testid="stExpander"] > div {{
        background-color: #ffffff;
        border-radius: 6px;
    }}

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
df["Completed Flag"] = df["Actual Date of completion"].notna()

# -----------------------------------------
# SIDEBAR
# -----------------------------------------
with st.sidebar:
    st.image("https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/analytics.png", width=60) # Placeholder Logo
    st.markdown("## Analytics Console")
    st.markdown("---")
    
    # Month & Year
    st.caption("TIME PERIOD")
    col1, col2 = st.columns(2)
    with col1:
        available_years = sorted(df["Enroll_Year"].dropna().unique())
        selected_years = st.multiselect("Year", available_years)
    with col2:
        month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        available_months = sorted(
            df["Enroll_Month_Name"].dropna().unique(),
            key=lambda x: month_order.index(x) if x in month_order else 99
        )
        selected_months = st.multiselect("Month", available_months)

    st.markdown("---")
    st.caption("FILTERS")
    
    cert_filter = st.multiselect("Certification", sorted(df["Certification"].dropna().unique()))
    snowpro_filter = st.multiselect("SnowPro Status", sorted(df["SnowPro Certified"].dropna().unique()))
    voucher_filter = st.multiselect("Voucher Status", sorted(df["Voucher Status"].dropna().unique()))

    with st.expander("🎖️ Badge Details"):
        badge_status_values = ["Completed", "In-Progress"]
        b1 = st.multiselect("Badge 1", badge_status_values)
        b2 = st.multiselect("Badge 2", badge_status_values)
        b3 = st.multiselect("Badge 3", badge_status_values)
        b4 = st.multiselect("Badge 4", badge_status_values)
        b5 = st.multiselect("Badge 5", badge_status_values)
        certprep = st.multiselect("CertPrepOD", ["Completed", "Not Started"])

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
    with zipfile.ZipFile(buffer, "w") as z:
        charts = {
            "cert_dist.png": data["Certification"].value_counts(),
            "snowpro_stat.png": data["SnowPro Certified"].value_counts(),
            "voucher_stat.png": data["Voucher Status"].value_counts()
        }
        for name, series in charts.items():
            fig, ax = plt.subplots(figsize=(7, 5))
            series.plot(kind="bar", ax=ax, color=CHART_COLOR)
            ax.set_title(name, color="black")
            plt.xticks(rotation=45, ha="right", color="black")
            plt.yticks(color="black")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            img = io.BytesIO()
            fig.savefig(img, format="png", bbox_inches="tight", dpi=100)
            plt.close(fig)
            z.writestr(name, img.getvalue())
    buffer.seek(0)
    return buffer

# -----------------------------------------
# UI STRUCTURE
# -----------------------------------------

# HEADER
col_h1, col_h2 = st.columns([0.85, 0.15])
with col_h1:
    st.markdown(f"""
    <div class="main-header">
        <div class="header-title">Certification Intelligence</div>
        <div class="header-subtitle">Overview for <b>{months_label}</b> in <b>{years_label}</b></div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("<br>", unsafe_allow_html=True)

    if not filtered_df.empty:
        st.download_button(
            "Export Report",
            data=export_charts_as_zip(filtered_df),
            file_name="analytics.zip"
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
    
    # 1. Prepare Data
    funnel_data = filtered_df.groupby("Certification")["EMP ID"].nunique().reset_index()
    funnel_data.columns = ["Certification", "Learners"]
    funnel_data = funnel_data.sort_values("Learners", ascending=True)

    # 2. Create Interactive Chart
    fig = px.bar(
        funnel_data, 
        x="Learners", 
        y="Certification", 
        orientation='h',
        text="Learners",
        color_discrete_sequence=[PRIMARY_COLOR]
    )

    # 3. Apply Clean Style with EXPLICIT Colors
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=0, r=0, b=0),
        
        # --- FIX: Force Dark Color on X-Axis Ticks ---
        xaxis=dict(
            showgrid=False, 
            visible=True, 
            title=None, 
            tickfont=dict(color="#1e293b", size=12) 
        ),
        
        # --- Force Dark Color on Y-Axis Ticks ---
        yaxis=dict(
            showgrid=False, 
            title=None,
            tickfont=dict(color="#1e293b", size=12)
        ),
        
        font=dict(family="Segoe UI", color="#1e293b"), # Global font color
        height=250,
        hovermode="y unified",
        dragmode="pan"
    )
    
    # Dark text for the numbers outside the bars
    fig.update_traces(textposition='outside', textfont_color="#1e293b")

    # 4. Configure Toolbar
    my_config = {
        'displayModeBar': 'hover',
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    }

    st.plotly_chart(fig, use_container_width=True, config=my_config)
    
    st.markdown("</div>", unsafe_allow_html=True)
with c2:
    st.markdown('<div class="dashboard-card"><div class="chart-title">SnowPro Status</div>', unsafe_allow_html=True)
    
    # 1. Prepare Data
    status_counts = filtered_df["SnowPro Certified"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    # 2. Create Interactive Donut Chart
    fig = px.pie(
        status_counts, 
        names="Status", 
        values="Count", 
        hole=0.5, # Creates the "Donut" look
        color_discrete_sequence=[PRIMARY_COLOR, "#64748b", "#94a3b8", "#cbd5e1"] # Blue & Greys
    )

    # 3. Apply Professional Styling
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label', # Shows Label and % inside the slice
        hovertemplate = "<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}",
        marker=dict(line=dict(color='#ffffff', width=2)) # Clean white separators
    )

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=20, l=0, r=0, b=20),
        font=dict(family="Segoe UI", color="#1e293b", size=13), # Dark text
        showlegend=False, # Hiding legend to keep the card clean (labels are already on chart)
        height=250
    )

    # 4. Toolbar Configuration
    my_config = {
        'displayModeBar': 'hover',
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    }

    st.plotly_chart(fig, use_container_width=True, config=my_config)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ROW 2 CHARTS
c3, c4 = st.columns(2)

# with c3:
#     st.markdown('<div class="dashboard-card"><div class="chart-title">Voucher Utilization</div>', unsafe_allow_html=True)
    
#     # 1. Prepare Data
#     voucher_data = filtered_df["Voucher Status"].value_counts().reset_index()
#     voucher_data.columns = ["Status", "Count"]

#     # 2. Smart Color Palette (Monochromatic Blue Gradient)
#     smart_colors = ["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#cbd5e1"]

#     # 3. Create Pie Chart
#     fig = px.pie(
#         voucher_data, 
#         names="Status", 
#         values="Count", 
#         color_discrete_sequence=smart_colors
#     )

#     # 4. Apply Clean Style with HORIZONTAL Text
#     fig.update_traces(
#         textposition='inside', 
#         textinfo='percent+label',
#         insidetextorientation='horizontal', # <--- FIX: Forces text to be straight
#         hovertemplate = "<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}",
#         marker=dict(line=dict(color='#ffffff', width=2))
#     )

#     fig.update_layout(
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)",
#         margin=dict(t=20, l=0, r=0, b=20),
#         font=dict(family="Segoe UI", color="#1e293b", size=13),
#         showlegend=False, 
#         height=250
#     )

#     # 5. Toolbar Configuration
#     my_config = {
#         'displayModeBar': 'hover',
#         'displaylogo': False,
#         'modeBarButtonsToRemove': ['lasso2d', 'select2d']
#     }

#     st.plotly_chart(fig, use_container_width=True, config=my_config)
    
#     st.markdown("</div>", unsafe_allow_html=True)
with c3:
    st.markdown('<div class="dashboard-card"><div class="chart-title">Voucher Utilization</div>', unsafe_allow_html=True)
    
    # 1. Prepare Data
    voucher_data = filtered_df["Voucher Status"].value_counts().reset_index()
    voucher_data.columns = ["Status", "Count"]

    # 2. Distinct Color Palette (Blue, Green, Amber, Slate, Red)
    distinct_colors = ["#2563eb", "#10b981", "#f59e0b", "#64748b", "#ef4444"]

    # 3. Create Pie Chart
    fig = px.pie(
        voucher_data, 
        names="Status", 
        values="Count", 
        color_discrete_sequence=distinct_colors # Applies the distinct colors
    )

    # 4. Apply Clean Style with Horizontal Text
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        insidetextorientation='horizontal', # Keeps text straight
        hovertemplate = "<b>%{label}</b><br>Count: %{value}<br>Share: %{percent}",
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

    # 5. Toolbar Configuration
    my_config = {
        'displayModeBar': 'hover',
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    }

    st.plotly_chart(fig, use_container_width=True, config=my_config)
    
    st.markdown("</div>", unsafe_allow_html=True)
with c4:
    st.markdown('<div class="dashboard-card"><div class="chart-title">Yearly Enrollment Trend</div>', unsafe_allow_html=True)
    
    # 1. Prepare Data
    trend_data = filtered_df.dropna(subset=["Enroll_Year"]).groupby("Enroll_Year")["EMP ID"].nunique().reset_index()
    trend_data.columns = ["Year", "Enrollments"]
    trend_data = trend_data.sort_values("Year")

    # 2. Create Interactive Area Chart
    fig = px.area(
        trend_data, 
        x="Year", 
        y="Enrollments",
        markers=True, # Adds dots at data points
        color_discrete_sequence=[PRIMARY_COLOR]
    )

    # 3. Apply Professional Styling
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=10, l=0, r=0, b=0),
        
        # X-Axis Styling
        xaxis=dict(
            title=None, 
            tickfont=dict(color="#1e293b", size=12),
            showgrid=False
        ),
        
        # Y-Axis Styling
        yaxis=dict(
            title=None, 
            tickfont=dict(color="#1e293b", size=12),
            showgrid=True, # Keep horizontal gridlines for reference
            gridcolor="#e2e8f0" # Very light grey grid
        ),
        
        font=dict(family="Segoe UI", color="#1e293b"),
        height=250,
        hovermode="x unified" # Shows a vertical line across the chart on hover
    )
    
    # Style the hover tooltip background
    fig.update_traces(
        line=dict(width=3), 
        marker=dict(size=8, line=dict(width=2, color="white")),
        hovertemplate = "<b>Year: %{x}</b><br>Enrollments: %{y}<extra></extra>"
    )

    # 4. Toolbar Configuration
    my_config = {
        'displayModeBar': 'hover',
        'scrollZoom': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': ['lasso2d', 'select2d']
    }

    st.plotly_chart(fig, use_container_width=True, config=my_config)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# FULL WIDTH BADGE CHART
st.markdown('<div class="dashboard-card"><div class="chart-title">Badge Progression</div>', unsafe_allow_html=True)
badge_data = {
    "Stage": ["Badge 1", "Badge 2", "Badge 3", "Badge 4", "Badge 5"],
    "Count": [
        filtered_df[filtered_df[f"Badge {i} Status"] == "Completed"]["EMP ID"].nunique() 
        for i in range(1, 6)
    ]
}
st.bar_chart(pd.DataFrame(badge_data).set_index("Stage"), color=CHART_COLOR)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# HEATMAP (STRICT COLOR CONTROL)
st.markdown('<div class="dashboard-card"><div class="chart-title">Seasonal Activity Heatmap</div>', unsafe_allow_html=True)

heatmap_df = filtered_df.dropna(subset=["Enroll_Month_Name", "Enroll_Year"]).groupby(["Enroll_Year", "Enroll_Month_Name"])["EMP ID"].nunique().reset_index()

if not heatmap_df.empty:
    heatmap_pivot = heatmap_df.pivot(index="Enroll_Month_Name", columns="Enroll_Year", values="EMP ID").fillna(0)
    month_order_map = {m: i for i, m in enumerate(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])}
    heatmap_pivot = heatmap_pivot.sort_index(key=lambda x: x.map(month_order_map))
    
    # Matplotlib Figure with Transparent BG and DARK Text
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_alpha(0)      # Transparent figure background
    ax.patch.set_alpha(0)       # Transparent axis background
    
    im = ax.imshow(heatmap_pivot, aspect="auto", cmap=HEATMAP_CMAP)
    
    # Axes Styling - FORCE DARK COLORS
    ax.set_xticks(range(len(heatmap_pivot.columns)))
    ax.set_xticklabels(heatmap_pivot.columns, color="#334155", fontweight="bold")
    ax.set_yticks(range(len(heatmap_pivot.index)))
    ax.set_yticklabels(heatmap_pivot.index, color="#334155", fontweight="bold")
    
    # Spines
    for spine in ax.spines.values(): spine.set_visible(False)
    
    # Text Annotations inside Heatmap
    for i in range(len(heatmap_pivot.index)):
        for j in range(len(heatmap_pivot.columns)):
            val = int(heatmap_pivot.iloc[i, j])
            if val > 0:
                # White text if dark block, Black text if light block
                text_c = "white" if val > heatmap_pivot.values.max() * 0.5 else "black"
                ax.text(j, i, val, ha="center", va="center", color=text_c, fontweight="bold")

    st.pyplot(fig)
else:
    st.info("Insufficient data for heatmap.")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# DATA GRID
with st.expander("🔎 Inspect Raw Data"):
    st.dataframe(filtered_df, use_container_width=True, height=400)

# FOOTER
st.markdown("""
<div style="text-align: center; margin-top: 50px; color: #94a3b8; font-size: 0.8rem;">
    Enterprise Certification Analytics • Confidential
</div>
""", unsafe_allow_html=True)
