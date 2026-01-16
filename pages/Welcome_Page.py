import streamlit as st

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Welcome | Employee Certification Portal",
    layout="wide"
)

# --------------------------------
# GLOBAL CSS
# --------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: Inter, sans-serif;
}

/* LOGO CONTAINER */
.logo-container {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 1.4rem 2rem;
    margin-bottom: 2.5rem;
}

/* Header */
.welcome-title {
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.6rem;
}
.subtitle {
    color: #64748b;
    font-size: 1.05rem;
    max-width: 980px;
    line-height: 1.6;
    margin-bottom: 3rem;
}

/* Section title */
.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.25em;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* Cards */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 2rem;
    border: 1px solid #e2e8f0;
    height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.25s ease-in-out;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0px 14px 28px rgba(15,23,42,0.08);
}
.card h3 {
    font-size: 1.2rem;
    font-weight: 700;
}
.card p {
    font-size: 0.95rem;
    color: #64748b;
}

/* Badge */
.badge {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 1.2rem;
}

/* Button override */
div.stButton > button {
    background-color: #030712 !important;
    color: #ffffff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.75rem 1rem !important;
}
div.stButton > button:hover {
    background-color: #ffffff !important;
    color: #030712 !important;
    border: 2px solid #030712 !important;
}

/* Footer */
.footer-tip {
    margin-top: 4rem;
    padding-top: 1.5rem;
    border-top: 1px solid #e2e8f0;
    color: #64748b;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# LOGO CONTAINER (ONLY LOGOS)
# --------------------------------
with st.container():
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("pages/snowflake_logo.png", width=210)

    with col2:
        st.image("pages/logo.png", width=200)

    st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------
# WELCOME TEXT (OUTSIDE LOGO BOX)
# --------------------------------
st.markdown("""
<div class="welcome-title">
    Welcome to the Employee Certification Portal 👋
</div>
<div class="subtitle">
    This portal helps your organization track employee certifications,
    ensure compliance, monitor readiness, and gain actionable insights
    across Hexaware teams and Snowflake environments.
</div>
""", unsafe_allow_html=True)

# --------------------------------
# TRY THINGS OUT
# --------------------------------
st.markdown('<div class="section-title">Try things out</div>', unsafe_allow_html=True)

r1c1, r1c2 = st.columns(2, gap="large")

with r1c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">Getting Started</div>
            <h3>Add / Update Certification</h3>
            <p>Add new employees or update certification details.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Certification Tracker", use_container_width=True):
        st.switch_page("pages/Data_Entry.py")

with r1c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">Insights</div>
            <h3>View Analytics Dashboard</h3>
            <p>Monitor certification KPIs and readiness.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Open Analytics", use_container_width=True):
        st.switch_page("pages/2_Realtime_Analysis.py")

# --------------------------------
# FOOTER
# --------------------------------
st.markdown("""
<div class="footer-tip">
    <div>💡 Tip: Use the left sidebar to navigate anytime.</div>
    <div>Hexaware © 2024 • Snowflake</div>
</div>
""", unsafe_allow_html=True)
