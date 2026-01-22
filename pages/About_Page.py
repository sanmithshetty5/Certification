import streamlit as st

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="About | Employee Certification Portal",
    layout="wide"
)

# -------------------------------
# CONFIG: IMAGE URLS (GITHUB)
# -------------------------------
LOGO_SNOWFLAKE = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png"
LOGO_HEXAWARE = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png"

# -------------------------------
# GLOBAL CSS & THEME
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
/* --- REMOVE STREAMLIT TOP HEADER COMPLETELY --- */
header[data-testid="stHeader"] {
    display: none;
}

/* --- REMOVE DEFAULT TOP PADDING STREAMLIT ADDS --- */
.block-container {
    padding-top: 0rem !important;
}

/* ===== REMOVE STREAMLIT SIDEBAR COMPLETELY (THIS PAGE ONLY) ===== */

/* Hide the entire sidebar container */
section[data-testid="stSidebar"] {
    display: none;
}

/* Remove the space reserved for the sidebar */
div[data-testid="stAppViewContainer"] {
    margin-left: 0;
}

/* Ensure main content uses full width */
div[data-testid="stMainBlockContainer"] {
    padding-left: 2rem;
    max-width: 100%;
}
.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: #0F172A;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
/* --- PUSH CONTENT BELOW NAVBAR --- */
.page-spacer {
    height: 90px;
}
.nav-left {
    color: #FFFFFF;
    font-size: 1.3rem;
    font-weight: 700;
}
.nav-links a {
    color: #E5E7EB;
    margin-left: 1.5rem;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
}
.nav-links a:hover {
    color: #38BDF8;
}
.page-spacer {
    height: 80px;
}

/* --- Main Container --- */
.stApp {
    background: #f8fafc;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #334155;
}

/* --- Typography --- */
h1, h2, h3 {
    letter-spacing: -0.025em;
}

/* --- Hero Section --- */
.hero-container {
    background: linear-gradient(135deg, #4f46e5 0%, #3b82f6 100%);
    border-radius: 20px;
    padding: 5rem 2rem;
    color: white;
    text-align: center;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 25px -5px rgba(79, 70, 229, 0.3);
    margin-bottom: 3rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 800;
    margin-bottom: 1rem;
    line-height: 1.1;
    text-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.hero-sub {
    font-size: 1.25rem;
    font-weight: 300;
    color: #e0e7ff;
    max-width: 750px;
    margin: 0 auto;
    line-height: 1.6;
}

/* --- Feature Cards (Vertical) --- */
.feature-card-v {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    top: 0;
    display: flex;
    flex-direction: column;
}

.feature-card-v:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    border-color: #6366f1;
}

/* --- Feature Cards (Horizontal) --- */
.feature-card-h {
    background: white;
    padding: 1.5rem 2rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    transition: all 0.3s ease;
}

.feature-card-h:hover {
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    border-color: #6366f1;
    transform: translateY(-2px);
}

/* --- Icon & Text Styling --- */
.icon-box {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
    margin-bottom: 1.5rem; /* Only for vertical layout */
}
/* Remove bottom margin for icon in horizontal layout */
.feature-card-h .icon-box {
    margin-bottom: 0;
}

.card-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.75rem;
}

.card-desc {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* --- Partners Section --- */
.partner-section {
    margin-top: 4rem;
    text-align: center;
}

.partner-logo-container {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    transition: transform 0.2s;
}

.partner-logo-container:hover {
    transform: scale(1.02);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
}

.partner-img {
    height: 50px;
    object-fit: contain;
    margin-bottom: 1rem;
}

</style>
""", unsafe_allow_html=True)
st.markdown("""
<div class="top-nav">
    <div class="nav-left">Certification Tracker</div>
    <div class="nav-links">
        <a href="/" target="_self">Welcome Page</a>
        <a href="/Data_Entry" target="_self">Data Entry</a>
        <a href="/Realtime_Analysis" target="_self">Realtime Analysis</a>
        <a href="/new_data_entry" target="_self">New Data Entry</a>
        <a href="/About_Page" target="_self">About</a>
    </div>
</div>

<div class="page-spacer"></div>
""", unsafe_allow_html=True)

# -------------------------------
# HERO SECTION
# -------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Snowflake Certification Control Center<br>Track Your Success.</div>
    <div class="hero-sub">
        Track, manage, and monitor Snowflake certification completion across Hexaware teams with clarity and confidence.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# CORE FEATURES (2x2 Grid)
# -------------------------------
st.markdown("### 🚀 Core Capabilities", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Row 1: Tracking & Analytics
row1_col1, row1_col2 = st.columns(2, gap="medium")

with row1_col1:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #e0e7ff; color: #4338ca;">&#128221;</div>
        <div class="card-title">Streamlined Tracking</div>
        <div class="card-desc">
            Effortlessly log employee details, certification tracks, and exam statuses. 
            Smart validation ensures data integrity before it ever hits the database.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row1_col2:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #fce7f3; color: #be185d;">&#128202;</div>
        <div class="card-title">Intelligent Analytics</div>
        <div class="card-desc">
            Visualize completion rates and skill distribution. 
            Identify seasonal trends in learning and export high-resolution charts for executive reporting.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Spacer between rows
st.markdown("<br>", unsafe_allow_html=True)

# Row 2: AI & Cloud
row2_col1, row2_col2 = st.columns(2, gap="medium")

with row2_col1:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #f3e8ff; color: #7c3aed;">&#129302;</div>
        <div class="card-title">AI-Assisted Insights</div>
        <div class="card-desc">
           Use intelligent analysis to uncover skill gaps, flag potential compliance risks, and deliver focused, actionable recommendations.
        </div>
    </div>
    """, unsafe_allow_html=True)

with row2_col2:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #dcfce7; color: #15803d;">&#9729;&#65039;</div>
        <div class="card-title">Cloud Native</div>
        <div class="card-desc">
            Powered by <b>Snowflake</b> for infinite scalability. 
            Your certification data is secure, instantly accessible, and always up to date across the organization.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# UTILITY FEATURE (Centered)
# -------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# [1, 2, 1] ratio creates a wide center column for the export utility
c_pad1, c_center, c_pad2 = st.columns([1, 2, 1])

with c_center:
    st.markdown("""
    <div class="feature-card-h">
        <div class="icon-box" style="background: #e0f2fe; color: #0369a1;">&#128229;</div>
        <div>
            <div class="card-title" style="margin-bottom:0.25rem;">Instant Export Utility</div>
            <div class="card-desc">Download complete datasets and visual reports with one click for offline analysis.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# PARTNERS SECTION
# -------------------------------
st.markdown("<div class='partner-section'>", unsafe_allow_html=True)
st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#94a3b8; letter-spacing:0.1em; text-transform:uppercase; margin-bottom:1.5rem;'>Built with Modern Tech</div>", unsafe_allow_html=True)

# Centering the partners block
p1, p2, p3 = st.columns([1, 4, 1]) 

with p2:
    pp1, pp2 = st.columns(2, gap="large")
    
    with pp1:
        st.markdown(f"""
        <div class="partner-logo-container">
            <img src="{LOGO_HEXAWARE}" class="partner-img" alt="Hexaware">
            <div style="font-weight:600; color:#334155;">Hexaware Technologies</div>
            <div style="font-size:0.85rem; color:#64748b; margin-top:0.5rem;">Driving Digital Transformation</div>
        </div>
        """, unsafe_allow_html=True)
    
    with pp2:
        st.markdown(f"""
        <div class="partner-logo-container">
            <img src="{LOGO_SNOWFLAKE}" class="partner-img" alt="Snowflake">
            <div style="font-weight:600; color:#334155;">Snowflake Data Cloud</div>
            <div style="font-size:0.85rem; color:#64748b; margin-top:0.5rem;">Secure & Scalable Storage</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #e2e8f0; padding-top:2rem; text-align: center; color: #94a3b8; font-size: 0.85rem;">
    &copy; 2024 Certification Portal • Internal Tool for Learning & Development
</div>
""", unsafe_allow_html=True)
