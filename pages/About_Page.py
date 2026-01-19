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
# GLOBAL & CUSTOM CSS
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

/* --- Global Reset & Typography --- */
.stApp {
    background-color: #f8fafc; /* Slate-50 */
    color: #0f172a; /* Slate-900 */
    font-family: 'Inter', sans-serif;
}

/* --- Hero Section --- */
.hero-container {
    padding: 4rem 2rem;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 24px;
    color: white;
    margin-bottom: 3rem;
    text-align: center;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #fff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.25rem;
    color: #cbd5e1; /* Slate-300 */
    font-weight: 300;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

/* --- Section Headers --- */
.section-header {
    text-align: center;
    margin-bottom: 2rem;
    margin-top: 1rem;
}
.section-header h2 {
    font-size: 2rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.5rem;
}
.section-header p {
    color: #64748b;
    font-size: 1rem;
}

/* --- Value Proposition Cards --- */
.value-card {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    height: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}

.value-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
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

.blue-icon { background: #e0f2fe; color: #0284c7; }
.purple-icon { background: #f3e8ff; color: #9333ea; }
.green-icon { background: #dcfce7; color: #16a34a; }

.value-card h3 {
    font-size: 1.25rem;
    font-weight: 700;
    color: #0f172a;
    margin-bottom: 0.75rem;
}

.value-card p {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* --- Tech Stack Strip --- */
.tech-strip {
    background-color: #ffffff;
    border-top: 1px solid #e2e8f0;
    border-bottom: 1px solid #e2e8f0;
    padding: 3rem 0;
    margin-top: 4rem;
}

.tech-grid {
    display: flex;
    justify-content: center;
    gap: 4rem;
    flex-wrap: wrap;
    align-items: center;
}

.tech-item {
    text-align: center;
}

.tech-label {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.5rem;
}

/* --- Footer --- */
.footer-container {
    text-align: center;
    padding: 4rem 0 2rem 0;
    color: #94a3b8;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HERO SECTION
# -------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Mastery in Motion</div>
    <div class="hero-subtitle">
        Bridging the gap between talent and technology. The Employee Certification Portal is your 
        centralized ecosystem for tracking professional growth, ensuring compliance, and unlocking 
        organizational intelligence.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# MISSION & VISION (Visual Layout)
# -------------------------------
c1, c2 = st.columns([1, 1], gap="large")

with c1:
    
    st.markdown("###") # Spacer

with c2:
    st.markdown("""
    <div style="padding-top: 1rem;">
        <h2 style="font-weight:800; color:#1e293b; font-size:2rem; margin-bottom:1rem;">Why This Exists</h2>
        <p style="color:#475569; font-size:1.05rem; line-height:1.7; margin-bottom:1.5rem;">
            In a rapidly evolving landscape, static spreadsheets are no longer sufficient. 
            We built this portal to transform certification data into a strategic asset.
        </p>
        <ul style="list-style: none; padding: 0; color:#475569; font-size:1rem; line-height: 1.8;">
            <li style="margin-bottom:0.5rem;">✅ <b>Eliminate Ambiguity:</b> Single source of truth for all certifications.</li>
            <li style="margin-bottom:0.5rem;">✅ <b>Accelerate Readiness:</b> Identify skill gaps before they become blockers.</li>
            <li>✅ <b>Data-Driven Decisions:</b> Real-time analytics powered by Snowflake.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# VALUE PROPOSITION CARDS
# -------------------------------
st.markdown("""
<div class="section-header">
    <h2>Core Capabilities</h2>
    <p>Everything you need to manage organizational excellence.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="value-card">
        <div class="icon-box blue-icon">⚡</div>
        <h3>Streamlined Operations</h3>
        <p>
            Say goodbye to manual tracking. Input certification details effortlessly, manage voucher statuses, and keep employee records up-to-date with a user-friendly interface.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="value-card">
        <div class="icon-box purple-icon">📊</div>
        <h3>Deep Analytics</h3>
        <p>
            Visualize success. Our dashboards provide granular views on completion rates, monthly trends, and voucher utilization, empowering leadership with actionable insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="value-card">
        <div class="icon-box green-icon">🛡️</div>
        <h3>Compliance & Security</h3>
        <p>
            Built on enterprise-grade infrastructure. Your data is secure, and compliance reporting is automated, ensuring the organization remains audit-ready at all times.
        </p>
    </div>
    """, unsafe_allow_html=True)


# -------------------------------
# TECH STACK SECTION
# -------------------------------
st.markdown("""
<div class="tech-strip">
    <div class="section-header" style="margin-top:0;">
        <h2>Powered By</h2>
    </div>
    <div class="tech-grid">
        <div class="tech-item">
            <h1 style="margin:0; font-size:2.5rem;">❄️</h1>
            <div class="tech-label">Snowflake Data Cloud</div>
        </div>
        <div class="tech-item">
            <h1 style="margin:0; font-size:2.5rem;">👑</h1>
            <div class="tech-label">Streamlit UI</div>
        </div>
        <div class="tech-item">
            <h1 style="margin:0; font-size:2.5rem;">🐍</h1>
            <div class="tech-label">Python Logic</div>
        </div>
        <div class="tech-item">
            <h1 style="margin:0; font-size:2.5rem;">🐼</h1>
            <div class="tech-label">Pandas Analytics</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<div class="footer-container">
    <p>Designed for Hexaware • In Partnership with Snowflake</p>
    <p style="opacity: 0.6; font-size: 0.8rem; margin-top:0.5rem;">© 2024 Employee Certification Portal. All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
