import streamlit as st

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="About | Employee Certification Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
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

/* --- Main Container --- */
.stApp {
    background: #f8fafc; /* Very light slate background */
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

/* --- Feature Cards --- */
.feature-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    height: 100%;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    top: 0;
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
    border-color: #6366f1;
}

.icon-box {
    width: 50px;
    height: 50px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
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

/* --- Stats/Numbers Section --- */
.stat-box {
    text-align: center;
    padding: 1.5rem;
    background: linear-gradient(to bottom right, #ffffff, #f8fafc);
    border-radius: 12px;
    border: 1px solid #f1f5f9;
}
.stat-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #4f46e5;
}
.stat-label {
    font-size: 0.875rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    font-weight: 600;
}

/* --- Partners --- */
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
}
.partner-img {
    height: 50px;
    object-fit: contain;
    margin-bottom: 1rem;
}

</style>
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
# CORE FEATURES GRID (3 Columns)
# -------------------------------
st.markdown("### 🚀 Core Capabilities", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #e0e7ff; color: #4338ca; margin-bottom: 1.5rem;">📝</div>
        <div class="card-title">Streamlined Tracking</div>
        <div class="card-desc">
            Effortlessly log employee details, certification tracks, and exam statuses. 
            Smart validation ensures data integrity before it ever hits the database.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #fce7f3; color: #be185d; margin-bottom: 1.5rem;">📊</div>
        <div class="card-title">Intelligent Analytics</div>
        <div class="card-desc">
            Visualize completion rates and skill distribution. 
            Identify seasonal trends in learning and export high-resolution charts for executive reporting.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card-v">
        <div class="icon-box" style="background: #dcfce7; color: #15803d; margin-bottom: 1.5rem;">☁️</div>
        <div class="card-title">Cloud Native</div>
        <div class="card-desc">
            Powered by <b>Snowflake</b> for infinite scalability. 
            Your certification data is secure, instantly accessible, and always up to date across the organization.
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# SECONDARY FEATURE (Centered)
# -------------------------------
st.markdown("<br>", unsafe_allow_html=True)

# Use columns to center the remaining utility feature
# [1, 2, 1] ratio creates a wide center column with padding on sides
c_pad1, c_center, c_pad2 = st.columns([1, 2, 1])

with c_center:
    # Using the horizontal card layout here for contrast
    st.markdown("""
    <div class="feature-card-h">
        <div class="icon-box" style="background: #e0f2fe; color: #0369a1; margin-bottom:0;">📥</div>
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

p1, p2, p3 = st.columns([1, 4, 1]) # Centering the middle content

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
