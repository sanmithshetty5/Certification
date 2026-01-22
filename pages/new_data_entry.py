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
    color: #0F172A; font-size: 1.2rem; font-weight: 700;
    border-bottom: 2px solid #E2E8F0; margin-bottom: 1.5rem;
}
.stButton > button { border-radius: 6px; font-weight: 600; height: 3em; }
h1,h2,h3,h4,h5 { color:#0F172A !important; font-weight:700; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

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
    df = session.sql(f"""
        SELECT 1 FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID"='{emp_id}' AND "Certification"='{cert}'
        LIMIT 1
    """).to_pandas()
    return not df.empty

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

    emp_id = c1.text_input("Employee ID")
    emp_name = c2.text_input("Employee Name")

    certifications = (
        "Advanced Analyst","Advanced Architect","Advanced Data Engineer",
        "Advanced Data Scientist","Core","Associate",
        "Speciality Gen AI","Speciality Native App","Speciality Snowpark"
    )
    certification = c3.selectbox("Certification", certifications)

# -----------------------------------------
# Schedule & Status
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
    m1,m2 = st.columns(2)

    enrol_month = m1.selectbox("Enrolment Month",
        ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
    enrol_year = m1.selectbox("Enrolment Year",
        [str(y) for y in range(date.today().year-5, date.today().year+5)])
    planned_date = m1.date_input("Planned Certification Date", date.today())

    completed = m2.checkbox("Certification Completed?")
    actual_date = m2.date_input("Actual Completion Date", max_value=date.today()) if completed else None
    snowpro = m2.selectbox("SnowPro Certified",("Completed","Failed")) if completed else "Incomplete"
    voucher_status = m2.selectbox("Voucher Status",
        ("Voucher Received","Voucher Applied","Own Payment"))

# -----------------------------------------
# Badges & Progress
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)
    badge_opts = ("Completed","In-Progress")
    badge1,badge2,badge3,badge4,badge5 = [
        st.selectbox(f"Badge {i}", badge_opts) for i in range(1,6)
    ]
    cert_prep = st.selectbox("CertPrepOD", badge_opts)
    level_up = st.selectbox("Level Up Courses",("Completed","Not Started"))
    trial_exam = st.selectbox("Trial Exams",("Completed","Not Started"))

# -----------------------------------------
# Department Info
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🏢 Department Info</div>', unsafe_allow_html=True)
    account = st.text_input("Account")
    account_spoc = st.text_input("Account SPOC")
    vertical = st.text_input("Vertical / SL")
    comment = st.text_area("Comment")

# -----------------------------------------
# Payload
# -----------------------------------------
payload = {
    "EMP ID": emp_id,
    "EMP Name": emp_name,
    "Enrolment Month": f"{enrol_month}-{enrol_year}",
    "Certification": certification,
    "Badge 1 Status": badge1,
    "Badge 2 Status": badge2,
    "Badge 3 Status": badge3,
    "Badge 4 Status": badge4,
    "Badge 5 Status": badge5,
    "CertPrepOD Course": cert_prep,
    "Level Up Courses": level_up,
    "# Trial Exams": trial_exam,
    "Account": normalize(account),
    "Account SPOC": normalize(account_spoc),
    "Vertical / SL": normalize(vertical),
    "Planned Certification date": date_str(planned_date),
    "Actual Date of completion": date_str(actual_date),
    "Voucher Status": voucher_status,
    "SnowPro Certified": snowpro,
    "Comment": normalize(comment)
}

# -----------------------------------------
# Add Button
# -----------------------------------------
st.markdown("---")

if st.button("➕ Add New Certification", type="primary", use_container_width=True):
    if validate(emp_id, emp_name):
        if duplicate_exists(emp_id, certification):
            st.error("❌ Duplicate Employee ID + Certification")
        else:
            session.create_dataframe([Row(**payload)]) \
                .write.mode("append") \
                .save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")
            st.success("✅ Record added successfully")
            st.rerun()
