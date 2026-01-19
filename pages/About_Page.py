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
# These are the links provided in your earlier prompts.
LOGO_SNOWFLAKE = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png"
LOGO_HEXAWARE = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png"

# 🛑 TODO: Upload your screenshots to your GitHub repo and update these filenames if needed
# For now, I'm assuming you might name them 'tracker_ui.png' and 'analytics_ui.png'
# If you haven't uploaded them yet, these sections will show a "broken image" icon until you do.
SCREENSHOT_TRACKER = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/tracker_ui.png" 
SCREENSHOT_ANALYTICS = "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/analytics_ui.png"


# -------------------------------
# GLOBAL CSS
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

/* --- Hero --- */
.hero-box {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 24px;
    padding: 4rem 2rem;
    color: white;
    text-align: center;
    margin-bottom: 4rem;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #fff, #cbd5e1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.2rem;
    color: #94a3b8;
    font-weight: 300;
    max-width: 700px;
    margin: 0 auto;
}

/* --- Feature Sections --- */
.feature-container {
    padding: 2rem 0;
    border-bottom: 1px solid #e2e8f0;
}
.feature-title {
    font-size: 1.8rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 1rem;
}
.feature-desc {
    font-size: 1rem;
    color: #64748b;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}
.step-badge {
    display: inline-block;
    background: #e0f2fe;
    color: #0284c7;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 1rem;
    letter-spacing: 0.05em;
}

/* --- Tech/Partner Section --- */
.partner-box {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    height: 100%;
    transition: transform 0.2s;
}
.partner-box:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}
.partner-logo {
    height: 60px; /* Fixed height for logos */
    object-fit: contain;
    margin-bottom: 1.5rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HERO SECTION
# -------------------------------
st.markdown("""
<div class="hero-box">
    <div class="hero-title">Empower Your Workforce</div>
    <div class="hero-sub">
        The definitive platform for tracking certifications, visualizing skill gaps, and 
        driving organizational readiness with Snowflake & Streamlit.
    </div>
</div>
""", unsafe_allow_html=True)


# -------------------------------
# FEATURE 1: DATA ENTRY (Left Text, Right Image)
# -------------------------------
c1, c2 = st.columns([1, 1.2], gap="large")

with c1:
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge">Step 1: Manage</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Certification Tracker</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-desc">
        The <b>Data Entry</b> module is your command center for maintaining accurate employee records.
        <br><br>
        ✅ <b>Employee Details:</b> Input names, IDs, and select specific Certification Tracks (e.g., Advanced Analyst).<br>
        ✅ <b>Schedule & Status:</b> Log enrollment dates and toggle completion status effortlessly.<br>
        ✅ <b>Voucher Management:</b> Track whether vouchers are "Received" or "Used" to optimize budget allocation.<br>
        <br>
        <em>All data is validated instantly and stored securely in the Snowflake cloud.</em>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    # Display the Tracker Screenshot
    # Note: If image is missing on GitHub, this will show a broken image icon.
    st.image(SCREENSHOT_TRACKER, caption="Fig 1. Data Entry Interface", use_container_width=True)


# -------------------------------
# SPACER
# -------------------------------
st.markdown("---")


# -------------------------------
# FEATURE 2: ANALYTICS (Left Image, Right Text)
# -------------------------------
c3, c4 = st.columns([1.2, 1], gap="large")

with c3:
    # Display the Analytics Screenshot
    st.image(SCREENSHOT_ANALYTICS, caption="Fig 2. Analytics Dashboard", use_container_width=True)

with c4:
    st.markdown('<div class="feature-container" style="border:none;">', unsafe_allow_html=True)
    st.markdown('<div class="step-badge" style="background:#f3e8ff; color:#9333ea;">Step 2: Analyze</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-title">Real-Time Insights</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="feature-desc">
        The <b>Analytics Dashboard</b> transforms raw data into executive-level intelligence.
        <br><br>
        📊 <b>Key Metrics:</b> Monitor "Total Certified" and "Completion %" at a glance.<br>
        🔍 <b>Deep Dive:</b> Filter by Enrollment Month or Year to identify seasonal trends.<br>
        📉 <b>Visualizations:</b> Breakdown certification distribution and SnowPro status with interactive charts.<br>
        <br>
        <em>Export charts directly to ZIP for your presentations.</em>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------
# PARTNERS SECTION (Using GitHub Logos)
# -------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div style="text-align:center; margin-bottom:2rem; font-weight:700; color:#94a3b8; letter-spacing:0.1em; text-transform:uppercase;">POWERED BY</div>', unsafe_allow_html=True)

p1, p2 = st.columns(2, gap="large")

with p1:
    st.markdown(f"""
    <div class="partner-box">
        <img src="{LOGO_HEXAWARE}" class="partner-logo" alt="Hexaware">
        <div style="text-align:left;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:0.5rem;">Hexaware Technologies</h3>
            <p style="font-size:0.9rem; color:#64748b; line-height:1.6;">
                A global leader in digital transformation. We prioritize continuous learning to ensure our teams 
                are equipped with the latest cloud capabilities to serve our clients better.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with p2:
    st.markdown(f"""
    <div class="partner-box">
        <img src="{LOGO_SNOWFLAKE}" class="partner-logo" alt="Snowflake">
        <div style="text-align:left;">
            <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:0.5rem;">Snowflake Data Cloud</h3>
            <p style="font-size:0.9rem; color:#64748b; line-height:1.6;">
                The backbone of our application. Snowflake provides the scalability, security, and 
                performance needed to handle our certification data in real-time.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# FOOTER
# -------------------------------
st.markdown("<br><br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top:1px solid #e2e8f0; padding-top:2rem; text-align: center; color: #94a3b8; font-size: 0.85rem;">
    © 2024 Hexaware Certification Portal • Maintained by the Learning & Development Team
</div>
""", unsafe_allow_html=True)
