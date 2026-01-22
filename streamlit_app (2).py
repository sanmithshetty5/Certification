

import streamlit as st

# -----------------------------------------
# PAGE CONFIG
# -----------------------------------------
st.set_page_config(
    page_title="Welcome | Employee Certification Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# GLOBAL CSS – Enterprise UI
# -----------------------------------------
st.markdown("""
<style>

/* ===== REMOVE STREAMLIT SIDEBAR COMPLETELY (THIS PAGE ONLY) ===== */

/* Hide the entire sidebar container */
section[data-testid="stSidebar"] {
    display: none !important;
}

/* Remove the space reserved for the sidebar */
div[data-testid="stAppViewContainer"] {
    margin-left: 0 !important;
}

/* Ensure main content uses full width */
div[data-testid="stMainBlockContainer"] {
    padding-left: 2rem !important;
    max-width: 100% !important;
}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

/* Header */
.header-container {
    background-color: transparent;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
}

.header-container img {
    height: 2cm !important;
    width: auto !important;
    object-fit: contain !important;
}

/* Typography */
.welcome-title {
    font-size: 2.8rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #1e293b;
    margin-bottom: 0.8rem;
}

.subtitle {
    color: #64748b;
    font-size: 1.1rem;
    max-width: 800px;
    line-height: 1.6;
    margin-bottom: 3rem;
}

.section-title {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    margin-top: 2rem;
}

/* Cards */
.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 2rem;
    border: 1px solid #e2e8f0;
    height: 340px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0,0,0,0.05);
    border-color: #cbd5e1;
}

.card-header-row {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
}

.card-icon {
    font-size: 2rem;
    padding: 0.5rem;
    background: #f1f5f9;
    border-radius: 10px;
    line-height: 1;
}

.card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    color: #1e293b;
}

.card p {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* Badges */
.badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.35rem 0.8rem;
    border-radius: 6px;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.badge-blue { background: #e0f2fe; color: #0284c7; }
.badge-purple { background: #f3e8ff; color: #9333ea; }
.badge-green { background: #dcfce7; color: #16a34a; }
.badge-gray { background: #f1f5f9; color: #475569; }

/* Buttons */
div.stButton > button {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1rem !important;
}

div.stButton > button:hover {
    background-color: #1e293b !important;
}

/* Footer */
.footer-tip {
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
    color: #94a3b8;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# HEADER
# -----------------------------------------
st.markdown("""
<div class="header-container">
    <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png">
    <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png">
</div>

<div class="welcome-title">Employee Certification Portal 👋</div>

<div class="subtitle">
    Your central hub to track certifications, ensure compliance,
    maintain readiness, and unlock actionable insights.
</div>
""", unsafe_allow_html=True)

# -----------------------------------------
# NAVIGATION
# -----------------------------------------
st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)

r1c1, r1c2 = st.columns(2, gap="large")

with r1c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-blue">Manage Data</div>
            <div class="card-header-row">
                <div class="card-icon">📝</div>
                <div>
                    <h3>Add / Update Certification</h3>
                    <p>Maintain employee certification records accurately.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Launch Data Entry Tool", use_container_width=True):
        st.switch_page("pages/Data_Entry.py")

with r1c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-purple">Analytics</div>
            <div class="card-header-row">
                <div class="card-icon">
                    <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/analysis.png"
                         style="width:32px;height:32px;object-fit:contain;opacity:0.8;">
                </div>
                <div>
                    <h3>View Analytics Dashboard</h3>
                    <p>Track KPIs, completion rates, and workforce readiness.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Go to Dashboard", use_container_width=True):
        st.switch_page("pages/2_Realtime_Analysis.py")

# -----------------------------------------
# SECOND ROW
# -----------------------------------------
st.markdown("<br><br>", unsafe_allow_html=True)
r2c1, r2c2 = st.columns(2, gap="large")

with r2c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-green">Intelligence</div>
            <div class="card-header-row">
                <div class="card-icon">🤖</div>
                <div>
                    <h3>AI-Driven Insights</h3>
                    <p>Predict compliance risks and skill gaps (coming soon).</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Explore AI (Coming Soon)", disabled=True, use_container_width=True)

with r2c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-gray">Support</div>
            <div class="card-header-row">
                <div class="card-icon">💡</div>
                <div>
                    <h3>Help & Resources</h3>
                    <p>Documentation and guides for certification workflows.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("View Documentation", use_container_width=True):
        st.switch_page("pages/About_Page.py")

# -----------------------------------------
# FOOTER
# -----------------------------------------
st.markdown("""
<div class="footer-tip">
    <div>← Tip: Use sidebar to navigate</div>
    <div>Hexaware © 2024 • Snowflake Partnership</div>
</div>
""", unsafe_allow_html=True)
