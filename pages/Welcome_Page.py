import streamlit as st

st.set_page_config(
    page_title="Welcome | Certification Portal",
    layout="wide"
)

# -------------------------------
# GLOBAL CSS – Quantask-style UI
# -------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
    color: #0f172a;
}

/* Header */
.welcome-title {
    font-size: 2.3rem;
    font-weight: 700;
    margin-bottom: 0.3rem;
}

.subtitle {
    color: #64748b;
    font-size: 1.05rem;
    margin-bottom: 2.5rem;
}

/* Section title */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
}

/* Cards */
.card {
    background: #ffffff;
    border-radius: 14px;
    padding: 1.8rem;
    box-shadow: 0px 8px 20px rgba(15,23,42,0.08);
    height: 100%;
    transition: all 0.25s ease-in-out;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0px 14px 30px rgba(15,23,42,0.12);
}

.card h3 {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
}

.card p {
    font-size: 0.95rem;
    color: #64748b;
    margin-bottom: 1.5rem;
}

/* Badge */
.badge {
    display: inline-block;
    font-size: 0.75rem;
    padding: 0.25rem 0.6rem;
    border-radius: 999px;
    background: #e0f2fe;
    color: #0369a1;
    margin-bottom: 0.8rem;
}

/* CTA Button */
.black-btn > button {
    background-color: #ffffff !important;
    color: #020617 !important;
    border: 2px solid #020617 !important;
    border-radius: 10px;
    font-weight: 600;
    transition: all 0.25s ease-in-out;
}

/* Hover */
.black-btn > button:hover {
    background-color: #ffffff !important;
    color: #020617 !important;
}

/* Footer tip */
.footer-tip {
    margin-top: 2rem;
    color: #64748b;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# WELCOME HEADER
# -------------------------------
st.markdown("""
<div>
    <div class="welcome-title">Welcome to Certification Portal 👋</div>
    <div class="subtitle">
        Organize employee certifications, track progress, and gain insights — all in one place.
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# TRY THINGS OUT
# -------------------------------
st.markdown('<div class="section-title">Try things out</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4, gap="large")

# -------------------------------
# CARD 1 – ADD / UPDATE
# -------------------------------
with c1:
    st.markdown("""
    <div class="card">
        <div class="badge">Getting Started</div>
        <h3>Add / Update Certification</h3>
        <p>
            Add new employees or update certification details including
            exams, badges, and completion status.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="black-btn">', unsafe_allow_html=True)
    if st.button("Open Certification Tracker", use_container_width=True):
        st.switch_page("pages/Data_Entry.py")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# CARD 2 – DASHBOARD
# -------------------------------
with c2:
    st.markdown("""
    <div class="card">
        <div class="badge">Insights</div>
        <h3>View Analytics Dashboard</h3>
        <p>
            Monitor certification KPIs, completion trends,
            and team-level readiness in real time.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="black-btn">', unsafe_allow_html=True)
    if st.button("View Analytics", use_container_width=True):
        st.switch_page("pages/2_Realtime_Analysis.py")
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# CARD 3 – AI INSIGHT
# -------------------------------
with c3:
    st.markdown("""
    <div class="card">
        <div class="badge">AI Powered</div>
        <h3>AI Insight</h3>
        <p>
            Discover certification gaps, readiness scores,
            and AI-driven recommendations for next actions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="black-btn">', unsafe_allow_html=True)
    st.button("Explore AI Insights", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# CARD 4 – HOW IT WORKS
# -------------------------------
with c4:
    st.markdown("""
    <div class="card">
        <div class="badge">Help</div>
        <h3>How It Works</h3>
        <p>
            Learn the simple 3-step workflow to manage
            employee certifications confidently.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="black-btn">', unsafe_allow_html=True)
    st.button("View Help Guide", disabled=True, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------
# FOOTER
# -------------------------------
st.markdown(
    '<div class="footer-tip">💡 Tip: Use the left sidebar to navigate between sections anytime.</div>',
    unsafe_allow_html=True
)

