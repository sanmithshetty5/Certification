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
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# Custom CSS (Professional Dark UI)
# -----------------------------------------
st.markdown("""
<style>
body { background-color: #0E1117; }
.block-container { padding-top: 1.5rem; }
.card {
    background-color: #161B22;
    padding: 1.2rem;
    border-radius: 12px;
    margin-bottom: 1rem;
}
h3 { color: #E5E7EB; }
label, .stMarkdown { color: #9CA3AF !important; }
.stButton>button { border-radius: 8px; height: 3rem; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# Session State Initialization
# -----------------------------------------
for key in [
    "edit_mode",
    "record",
    "pending_data",
    "pending_action",
    "last_emp_id",
    "save_completed",
    "autofill_emp_name"
]:
    if key not in st.session_state:
        st.session_state[key] = None

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
    if not df.empty and df.iloc[0]["EMP Name"].lower() != emp_name.lower():
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
# Sidebar – Search (RESTORED)
# -----------------------------------------
with st.sidebar:
    st.markdown("## 🔍 Search Employee")

    emp_id = st.text_input("Employee ID (10 digits)")

    certifications = (
        "Advanced Analyst",
        "Advanced Architect",
        "Advanced Data Engineer",
        "Core",
        "Associate",
        "Speciality Gen AI",
        "Speciality Native App",
        "Advanced Data Scientist",
        "Speciality Snowpark"
    )

    certification = st.selectbox("Certification", certifications)

    st.divider()

    if st.button("Search", type="primary", use_container_width=True):
        if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
            st.error("Enter a valid 10-digit Employee ID")
            st.stop()

        result = session.sql(f"""
            SELECT *
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID" = '{emp_id}'
              AND "Certification" = '{certification}'
        """).to_pandas()

        if result.empty:
            st.session_state.edit_mode = False
            st.session_state.record = {}
            st.toast("No record found. Add new certification.", icon="➕")
        else:
            st.session_state.edit_mode = True
            st.session_state.record = result.iloc[0].to_dict()
            st.toast("Record loaded successfully", icon="✅")

# -----------------------------------------
# Reset on EMP ID change
# -----------------------------------------
if st.session_state.last_emp_id != emp_id:
    st.session_state.record = {}
    st.session_state.edit_mode = False
    st.session_state.autofill_emp_name = autofill_employee_name(emp_id)
    st.session_state.last_emp_id = emp_id

# -----------------------------------------
# Header
# -----------------------------------------
st.markdown("## 🎓 Certification Tracker")

# -----------------------------------------
# Employee + Certification
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 2])
emp_id = c1.text_input("Employee ID", value=emp_id)
emp_name = c2.text_input(
    "Employee Name",
    value=st.session_state.record.get("EMP Name") or st.session_state.autofill_emp_name or ""
)
certification = c3.selectbox("Certification Track", certifications)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Planning & Completion
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
p1, p2 = st.columns(2)

with p1:
    month = st.selectbox("Enrolment Month", ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    year = st.selectbox("Enrolment Year", [str(y) for y in range(date.today().year-5, date.today().year+5)])
    planned_date = st.date_input("Planned Certification Date", date.today())

with p2:
    completed = st.checkbox("Certification Completed?")
    actual_date = st.date_input("Actual Completion Date", max_value=date.today()) if completed else None
    snowpro = st.selectbox("SnowPro Status", ("Completed","Failed") if completed else ("Incomplete",))
    voucher_status = st.selectbox("Voucher Status", ("Voucher Received","Voucher Applied","Own Payment"))
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Badges
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
b1, b2, b3 = st.columns(3)
badge_opts = ("Completed","In-Progress")
badge1 = b1.selectbox("Badge 1", badge_opts)
badge4 = b1.selectbox("Badge 4", badge_opts)
badge2 = b2.selectbox("Badge 2", badge_opts)
badge5 = b2.selectbox("Badge 5", badge_opts)
badge3 = b3.selectbox("Badge 3", badge_opts)
cert_prep = b3.selectbox("CertPrepOD", badge_opts)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Action Bar (Confirm Delete RESTORED)
# -----------------------------------------
st.divider()
a1, a2, a3 = st.columns([3,1,1])

with a1:
    label = "Update Record" if st.session_state.edit_mode else "Add New Certification"
    if st.button(label, type="primary", use_container_width=True):
        if validate_mandatory_fields(emp_id, emp_name):
            st.success("Ready to save")

with a2:
    st.button("Cancel", use_container_width=True)

with a3:
    if st.session_state.edit_mode:
        confirm = st.checkbox("Confirm Delete")
        if confirm and st.button("🗑 Delete", use_container_width=True):
            session.sql(f"""
                DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                WHERE "EMP ID" = '{emp_id}'
                  AND "Certification" = '{certification}'
            """).collect()
            st.success("Record deleted")
            st.session_state.edit_mode = False
            st.session_state.record = {}
