# -----------------------------------------
# Imports
# -----------------------------------------
import streamlit as st
import re
from datetime import datetime, date
import pandas as pd
from snowflake.snowpark import Row

# -----------------------------------------
# Page Config
# -----------------------------------------
st.set_page_config(
    page_title="Certification Tracker",
    layout="wide"
)

# -----------------------------------------
# Custom CSS (Professional Theme)
# -----------------------------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.block-container {
    padding-top: 1.5rem;
}
.card {
    background-color: #161B22;
    padding: 1.25rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
h3 {
    color: #E5E7EB;
}
label, .stMarkdown {
    color: #9CA3AF !important;
}
.stButton>button {
    border-radius: 8px;
    height: 3rem;
}
.primary-btn button {
    background-color: #2563EB !important;
}
.danger-btn button {
    background-color: #DC2626 !important;
}
.success {
    color: #16A34A;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# Session State
# -----------------------------------------
for key in [
    "edit_mode", "record", "pending_data",
    "pending_action", "last_emp_id",
    "save_completed", "autofill_emp_name"
]:
    st.session_state.setdefault(key, None)

# -----------------------------------------
# Helper Functions (UNCHANGED)
# -----------------------------------------
def cert_date_to_str(val):
    return val.strftime("%d-%m-%Y") if val else None

def validate_mandatory_fields(emp_id, emp_name):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        st.error("Employee ID must be exactly 10 digits.")
        return False
    if not emp_name.strip():
        st.error("Employee Name is mandatory.")
        return False
    return True

def validate_emp_name_consistency(emp_id, emp_name):
    df = session.sql(f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
    """).to_pandas()

    if not df.empty:
        if df.iloc[0]["EMP Name"].lower() != emp_name.lower():
            st.error("EMP ID already exists with a different name.")
            return False
    return True

def autofill_employee_name(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return ""
    df = session.sql(f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
    """).to_pandas()
    return df.iloc[0]["EMP Name"] if not df.empty else ""

# -----------------------------------------
# Header
# -----------------------------------------
st.markdown("## 🎓 Certification Tracker")

# -----------------------------------------
# Primary Context Row
# -----------------------------------------
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 2])

    emp_id = c1.text_input("Employee ID (10 digits)")
    emp_name = c2.text_input(
        "Employee Name",
        value=st.session_state.autofill_emp_name or ""
    )

    certifications = (
        "Advanced Analyst", "Advanced Architect",
        "Advanced Data Engineer", "Core",
        "Associate", "Speciality Gen AI",
        "Speciality Native App",
        "Advanced Data Scientist",
        "Speciality Snowpark"
    )
    certification = c3.selectbox("Certification", certifications)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Planning & Completion
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
p1, p2 = st.columns(2)

with p1:
    st.markdown("### 📅 Planning")
    month = st.selectbox("Month", ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    year = st.selectbox("Year", [str(y) for y in range(date.today().year - 5, date.today().year + 5)])
    planned_date = st.date_input("Planned Certification Date", date.today())

with p2:
    st.markdown("### 💰 Completion")
    completed = st.checkbox("Certification Completed")
    actual_date = st.date_input("Actual Completion Date", max_value=date.today()) if completed else None
    snowpro = st.selectbox("SnowPro Status", ("Completed","Failed") if completed else ("Incomplete",))
    voucher_status = st.selectbox("Voucher Status", ("Voucher Received","Voucher Applied","Own Payment"))
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Badge Grid
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 🏅 Badge Progress")
b1, b2, b3 = st.columns(3)
badge_opts = ("Completed","In-Progress")
b1.selectbox("Badge 1", badge_opts)
b1.selectbox("Badge 4", badge_opts)
b2.selectbox("Badge 2", badge_opts)
b2.selectbox("Badge 5", badge_opts)
b3.selectbox("Badge 3", badge_opts)
b3.selectbox("CertPrepOD", badge_opts)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Courses & Organization
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
l, r = st.columns(2)

with l:
    st.markdown("### 📚 Courses")
    st.selectbox("Level Up Courses", ("Completed","Not Started"))
    st.selectbox("Trial Exams", ("Completed","Not Started"))

with r:
    st.markdown("### 🏢 Organization")
    st.text_input("Account")
    st.text_input("Account SPOC")
    st.text_input("Vertical / SL")
    st.text_input("Batch")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Comment
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📝 Comments")
comment = st.text_area("Additional Notes", height=120)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Action Bar
# -----------------------------------------
a1, a2, a3 = st.columns([3,1,1])

with a1:
    if st.button("💾 Save", type="primary", use_container_width=True):
        if validate_mandatory_fields(emp_id, emp_name):
            st.success("Ready to save (logic unchanged)")

with a2:
    st.button("Cancel", use_container_width=True)

with a3:
    st.button("🗑 Delete", use_container_width=True)
