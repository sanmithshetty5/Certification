import streamlit as st
from datetime import date
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
# CSS (UNCHANGED UI)
# -----------------------------------------
st.markdown("""
<style>
.stApp { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
.section-header {
    color: #0F172A;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.5rem;
}
.stButton > button { border-radius: 6px; font-weight: 600; height: 3em; }
h1,h2,h3,h4,h5,h6 { color:#0F172A !important; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# Constants
# -----------------------------------------
CERTIFICATIONS = (
    "Advanced Analyst","Advanced Architect","Advanced Data Engineer",
    "Advanced Data Scientist","Core","Associate",
    "Speciality Gen AI","Speciality Native App","Speciality Snowpark"
)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# -----------------------------------------
# Session State
# -----------------------------------------
for k in [
    "record","last_emp_id","pending_data",
    "pending_action","save_completed",
    "autofill_emp_name","duplicate_exists","add_mode"
]:
    st.session_state.setdefault(k, None)

if st.session_state.add_mode is None:
    st.session_state.add_mode = False

# -----------------------------------------
# Helpers
# -----------------------------------------
def normalize(val):
    return val.strip() if isinstance(val,str) and val.strip() else None

def date_str(d):
    return d.strftime("%d-%m-%Y") if d else None

def validate(emp_id, emp_name):
    if not emp_id.isdigit() or len(emp_id) != 10:
        st.error("❌ Employee ID must be exactly 10 digits")
        return False
    if not emp_name.strip():
        st.error("❌ Employee Name is mandatory")
        return False
    return True

def duplicate_exists(emp_id, cert):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return False
    df = session.sql(f"""
        SELECT 1 FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID"='{emp_id}' AND "Certification"='{cert}'
        LIMIT 1
    """).to_pandas()
    return not df.empty

def autofill_name(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return ""
    df = session.sql(f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID"='{emp_id}'
    """).to_pandas()
    return df.iloc[0]["EMP Name"] if not df.empty else ""

# -----------------------------------------
# Sidebar – Search + Add New
# -----------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:1.5rem;font-weight:600;color:white;">🔍 Search Employee</div>',
        unsafe_allow_html=True
    )

    search_emp_id = st.text_input("Employee ID (10 digits)")
    search_cert = st.selectbox("Certification", CERTIFICATIONS)

    if st.button("Search", type="primary", use_container_width=True):
        if not search_emp_id.isdigit() or len(search_emp_id) != 10:
            st.error("Enter valid 10-digit EMP ID")
            st.stop()

        df = session.sql(f"""
            SELECT *
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID"='{search_emp_id}'
              AND "Certification"='{search_cert}'
        """).to_pandas()

        st.session_state.record = df.iloc[0].to_dict() if not df.empty else {}
        st.session_state.autofill_emp_name = autofill_name(search_emp_id)
        st.session_state.add_mode = False

    if st.button("➕ Add New Certification", use_container_width=True):
        st.session_state.record = {}
        st.session_state.autofill_emp_name = ""
        st.session_state.add_mode = True
        st.toast("Add new certification mode", icon="➕")

# -----------------------------------------
# Header
# -----------------------------------------
title_col, logo_col = st.columns([7,1])
with title_col:
    st.title("🎓 Certification Tracker")
with logo_col:
    st.image(
        "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png",
        width=200
    )

st.markdown("---")

# -----------------------------------------
# Employee Details
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)
    c1,c2,c3 = st.columns([1,2,2])

    emp_id = c1.text_input(
        "Employee ID",
        value="" if st.session_state.add_mode else search_emp_id
    )

    emp_name = c2.text_input(
        "Employee Name",
        value="" if st.session_state.add_mode else (
            st.session_state.record.get("EMP Name")
            or st.session_state.autofill_emp_name
            or ""
        )
    )

    certification = c3.selectbox(
        "Certification",
        CERTIFICATIONS,
        index=0 if st.session_state.add_mode else (
            CERTIFICATIONS.index(search_cert)
            if search_cert in CERTIFICATIONS else 0
        )
    )

# -----------------------------------------
# Duplicate Check
# -----------------------------------------
st.session_state.duplicate_exists = duplicate_exists(emp_id, certification)

if st.session_state.duplicate_exists:
    st.error("⚠️ Employee ID + Certification already exists.")

# -----------------------------------------
# Schedule & Status
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
    m1,m2 = st.columns(2)

    enrol_month = m1.selectbox("Enrolment Month", MONTHS)
    enrol_year = m1.selectbox(
        "Enrolment Year",
        [str(y) for y in range(date.today().year-5, date.today().year+5)]
    )
    planned_date = m1.date_input("Planned Certification Date", date.today())

    completed = m2.checkbox("Certification Completed?")
    actual_date = m2.date_input("Actual Completion Date", max_value=date.today()) if completed else None
    snowpro = m2.selectbox("SnowPro Certified",("Completed","Failed")) if completed else "Incomplete"
    voucher_status = m2.selectbox("Voucher Status",("Voucher Received","Voucher Applied","Own Payment"))

# -----------------------------------------
# Payload
# -----------------------------------------
payload = {
    "EMP ID": emp_id,
    "EMP Name": emp_name,
    "Enrolment Month": f"{enrol_month}-{enrol_year}",
    "Certification": certification,
    "Planned Certification date": date_str(planned_date),
    "Actual Date of completion": date_str(actual_date),
    "Voucher Status": voucher_status,
    "SnowPro Certified": snowpro,
}

# -----------------------------------------
# Add Button (INSERT ONLY)
# -----------------------------------------
st.markdown("---")

if st.button(
    "➕ Add New Certification",
    type="primary",
    use_container_width=True,
    disabled=st.session_state.duplicate_exists
):
    if validate(emp_id, emp_name):
        session.create_dataframe([Row(**payload)]) \
            .write.mode("append") \
            .save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")

        st.success("✅ Record added successfully")
        st.session_state.add_mode = False
        st.rerun()
