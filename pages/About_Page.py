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
# GLOBAL CSS – Enterprise UI
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

/* --- Hero Section --- */
.hero-container {
    background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
    border-radius: 20px;
    padding: 4rem 2rem;
    color: white;
    text-align: center;
    margin-bottom: 3rem;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 1rem;
    background: linear-gradient(to right, #ffffff, #94a3b8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: #cbd5e1;
    font-weight: 300;
    max-width: 800px;
    margin: 0 auto;
    line-height: 1.6;
}

/* --- Feature Cards --- */
.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 2rem;
    height: 100%;
    transition: all 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    border-color: #cbd5e1;
}

.feature-icon {
    font-size: 2rem;
    margin-bottom: 1rem;
    display: inline-block;
    padding: 10px;
    border-radius: 12px;
}

.icon-blue { background: #e0f2fe; }
.icon-purple { background: #f3e8ff; }
.icon-green { background: #dcfce7; }

.feature-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 0.5rem;
}

.feature-desc {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* --- Partner Section --- */
.partner-section {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
}

.partner-header {
    font-size: 0.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #94a3b8;
    margin-bottom: 2rem;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# HERO SECTION
# -------------------------------
st.markdown("""
<div class="hero-container">
    <div class="hero-title">Certification Excellence</div>
    <div class="hero-subtitle">
        A comprehensive ecosystem designed to bridge the gap between talent and technology. 
        Track, analyze, and optimize organizational readiness with the power of Hexaware and Snowflake.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# APPLICATION WALKTHROUGH
# -------------------------------
st.markdown("### 🚀 Application Features & Guide")
st.markdown("Explore the core functionalities of the portal and how to leverage them effectively.")
st.write("") # Spacer

# Create 3 columns for the features
c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-blue">📝</div>
        <div class="feature-title">Data Management</div>
        <div class="feature-desc">
            <b>Page: Certification Tracker</b><br><br>
            The input engine of the portal. Use this module to maintain the integrity of employee records.
            <br><br>
            <ul>
                <li><b>Add/Update:</b> Enter Employee IDs, select certification tracks (e.g., Advanced Analyst), and log enrollment dates.</li>
                <li><b>Status Tracking:</b> Toggle "Certification Completed" and update voucher statuses (Received/Used).</li>
                <li><b>Validation:</b> Ensures data consistency before writing to Snowflake.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-purple">📊</div>
        <div class="feature-title">Advanced Analytics</div>
        <div class="feature-desc">
            <b>Page: Realtime Analysis</b><br><br>
            The intelligence hub. Visualize workforce performance through dynamic dashboards.
            <br><br>
            <ul>
                <li><b>KPI Overview:</b> Instant view of Total Records, Unique Employees, and Completion % percentages.</li>
                <li><b>Interactive Filters:</b> Drill down by Enrollment Month, Year, or Certification type.</li>
                <li><b>Export Capability:</b> Download high-res charts and data summaries for executive reporting.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon icon-green">🤖</div>
        <div class="feature-title">The Ecosystem</div>
        <div class="feature-desc">
            <b>Architecture & Security</b><br><br>
            Built for enterprise scale, ensuring your data is secure, accessible, and actionable.
            <br><br>
            <ul>
                <li><b>Single Source of Truth:</b> All data is stored directly in the Snowflake Data Cloud.</li>
                <li><b>Real-Time Sync:</b> Updates made in the Tracker are immediately reflected in the Analytics dashboard.</li>
                <li><b>User-Centric UI:</b> Designed with Streamlit for a seamless, responsive experience.</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# PARTNER / CONTEXT SECTION
# -------------------------------
st.markdown('<div class="partner-section"><div class="partner-header">Strategic Partnership & Technology</div></div>', unsafe_allow_html=True)

col_hex, col_snow = st.columns(2, gap="large")

with col_hex:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Hexaware_Technologies_Logo.svg/1200px-Hexaware_Technologies_Logo.svg.png", height=40)
    st.markdown("### About Hexaware")
    st.info("""
    **Hexaware** is a global technology and business process services company. 
    We empower enterprises to realize digital transformation at scale and speed. 
    This portal represents our commitment to continuous learning, ensuring our workforce 
    remains at the cutting edge of cloud data technologies.
    """)

with col_snow:
    st.image("https://upload.wikimedia.org/wikipedia/commons/f/ff/Snowflake_Logo.svg", height=40)
    st.markdown("### Powered by Snowflake")
    st.info("""
    **Snowflake** is the Data Cloud. It enables this application to break down data silos 
    and provide secure, governed access to the certification data. 
    By leveraging Snowflake's architecture, this portal delivers near-infinite scaling 
    and concurrency for real-time analytics.
    """)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.85rem;">
    © 2024 Hexaware Certification Portal • Built with Streamlit & Snowflake
</div>
""", unsafe_allow_html=True)
