# import streamlit as st

# st.set_page_config(
#     page_title="Certification Management System",
#     layout="wide"
# )

# st.sidebar.title("🎓 Certification Portal")

# page = st.sidebar.radio(
#     "Navigate",
#     [
#         "🏠 Welcome",
#         "✍️ Certification Tracker",
#         "📊 Certification Analytics"
#     ]
# )

# if page == "🏠 Welcome":
#     st.switch_page("pages/Welcome_Page.py")

# elif page == "✍️ Certification Tracker":
#     st.switch_page("pages/Data_Entry.py")

# elif page == "📊 Certification Analytics":
#     st.switch_page("pages/dashboard.py")


import streamlit as st

st.set_page_config(
    page_title="Welcome | Employee Certification Portal",
    layout="wide"
)

# -------------------------------
# GLOBAL CSS – Enterprise UI
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: Inter, sans-serif;
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
    margin-bottom: 0.8rem;
}

.card p {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* Badge */
.badge {
    display: inline-block;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    margin-bottom: 1.4rem;
    text-transform: uppercase;
}

/* -------------------------------
   GLOBAL BUTTON OVERRIDE
--------------------------------*/
div.stButton > button {
    background-color: #030712 !important;
    color: #ffffff !important;
    border: 2px solid #030712 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.25s ease-in-out !important;
}

div.stButton > button:hover {
    background-color: #ffffff !important;
    color: #030712 !important;
}

div.stButton > button:focus,
div.stButton > button:active {
    background-color: #ffffff !important;
    color: #030712 !important;
    outline: none !important;
    box-shadow: none !important;
}

div.stButton > button:disabled {
    background-color: #f1f5f9 !important;
    color: #94a3b8 !important;
    border: 2px solid #e2e8f0 !important;
    cursor: not-allowed !important;
}

/* Row spacing */
.row-spacing {
    margin-top: 3rem;
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
    align-items: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# HEADER
# -------------------------------
st.markdown("""
<div>
    <div class="welcome-title">
        Welcome to the Employee Certification Portal 👋
    </div>
    <div class="subtitle">
        This portal helps to track employee certifications, ensure compliance,
        monitor readiness, and gain actionable insights across teams and departments.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# TRY THINGS OUT
# -------------------------------
st.markdown('<div class="section-title">Try things out</div>', unsafe_allow_html=True)

# -------- ROW 1 --------
r1c1, r1c2 = st.columns(2, gap="large")

with r1c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">Getting Started</div>
            <h3>Add / Update Certification</h3>
            <p>
                Add new employees or update certification details including exams,
                badges, issue dates, and completion status.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(
    "Open Certification Tracker",
    key="btn_open_tracker",
    use_container_width=True):
        st.switch_page("pages/Data_Entry.py")



with r1c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">Insights</div>
            <h3>View Analytics Dashboard</h3>
            <p>
                Monitor certification KPIs, expiring certifications,
                and team-level readiness in real time.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button(
    "Open Certification Tracker",
    key="btn_open_ana;lytics",
    use_container_width=True):
        st.switch_page("pages/2_Realtime_Analysis.py")


# -------- ROW 2 --------
st.markdown('<div class="row-spacing"></div>', unsafe_allow_html=True)

r2c1, r2c2 = st.columns(2, gap="large")

with r2c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">AI Powered</div>
            <h3>AI Insight</h3>
            <p>
                Identify certification gaps, predict risk areas,
                and receive AI-driven recommendations for action.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button(
    "Explore AI Insights 🔒",
    key="btn_ai_insight",
    disabled=True,
    use_container_width=True)
    
with r2c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge">Help</div>
            <h3>How It Works</h3>
            <p>
                Learn the simple 3-step workflow to manage employee
                certifications confidently across the organization.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button(
    "View Help Guide",
    key="btn_help",
    disabled=True,
    use_container_width=True)
    

# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<div class="footer-tip">
    <div>💡 Tip: Use the left sidebar to navigate between sections anytime.</div>
    <div>Hexaware © 2024 • Snowflake</div>
</div>
""", unsafe_allow_html=True)
