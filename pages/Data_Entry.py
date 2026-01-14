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

st.markdown("""
<style>

/* ---------- PAGE ---------- */
body {
    background-color: #F4F6F8;
    color: #0F172A;
}

.block-container {
    padding: 2rem 3rem;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E6E8EB;
}

/* ---------- HEADERS ---------- */
h1, h2, h3 {
    color: #0F172A;
    font-weight: 600;
}

/* ---------- CARDS ---------- */
.card {
    background-color: #FFFFFF;
    border: 1px solid #E6E8EB;
    border-radius: 10px;
    padding: 1.25rem;
    margin-bottom: 1.25rem;
}

/* ---------- LABELS ---------- */
label, .stMarkdown {
    color: #475569 !important;
    font-size: 0.85rem;
    font-weight: 500;
}

/* ---------- INPUTS ---------- */
input, textarea, select {
    background-color: #F9FAFB !important;
    color: #0F172A !important;
    border: 1px solid #CBD5E1 !important;
    border-radius: 6px !important;
}

input:focus, textarea:focus, select:focus {
    border-color: #2563EB !important;
    box-shadow: 0 0 0 1px #2563EB;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    border-radius: 8px;
    height: 2.8rem;
    font-weight: 600;
}

/* Add / Update */
.stButton > button[kind="primary"] {
    background-color: #16A34A;
    color: white;
}

.stButton > button[kind="primary"]:hover {
    background-color: #15803D;
}

/* Cancel / Delete */
.stButton > button:not([kind="primary"]) {
    background-color: #DC2626;
    color: white;
}

.stButton > button:not([kind="primary"]):hover {
    background-color: #B91C1C;
}

/* ---------- REMOVE UGLY DEFAULT SPACING ---------- */
hr {
    border: none;
    border-top: 1px solid #E6E8EB;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()

# -----------------------------------------
# Session State Initialization (UNCHANGED)
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
        st.error("❌ Employee ID must be exactly 10 digits.")
        return False
    if not emp_name or emp_name.strip() == "":
        st.error("❌ Employee Name is mandatory.")
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
            st.error("❌ EMP ID exists with different name.")
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
# Sidebar – Search (UNCHANGED LOGIC)
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

    if st.button("Search", type="primary", use_container_width=True):
        if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
            st.error("Enter valid 10-digit EMP ID")
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
            st.toast("No record found. Add new.", icon="➕")
        else:
            st.session_state.edit_mode = True
            st.session_state.record = result.iloc[0].to_dict()
            st.toast("Record loaded", icon="✅")

# -----------------------------------------
# Reset on EMP ID change (UNCHANGED)
# -----------------------------------------
if st.session_state.last_emp_id != emp_id:
    st.session_state.record = {}
    st.session_state.edit_mode = False
    st.session_state.pending_data = None
    st.session_state.pending_action = None
    st.session_state.save_completed = None
    st.session_state.autofill_emp_name = autofill_employee_name(emp_id)
    st.session_state.last_emp_id = emp_id

# -----------------------------------------
# Header
# -----------------------------------------
st.markdown("## 🎓 Certification Tracker")

# -----------------------------------------
# Employee + Certification (UI ONLY)
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 2])

emp_id = c1.text_input("Employee ID", value=emp_id)
emp_name = c2.text_input(
    "Employee Name",
    value=(
        st.session_state.record.get("EMP Name")
        or st.session_state.autofill_emp_name
        or ""
    )
)
certification = c3.selectbox("Certification Track", certifications)
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Enrolment & Planning (UNCHANGED LOGIC)
# -----------------------------------------
month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]

st.markdown('<div class="card">', unsafe_allow_html=True)
m1, m2 = st.columns(2)

with m1:
    enrol_month = st.selectbox("Enrolment Month", month_opts)
    enrol_year = st.selectbox("Enrolment Year", year_opts)
    planned_date = st.date_input("Planned Certification Date", date.today())

with m2:
    completed = st.checkbox("Certification Completed?")
    actual_date = st.date_input(
        "Actual Completion Date",
        max_value=date.today()
    ) if completed else None

    snowpro = st.selectbox(
        "SnowPro Certified",
        ("Completed","Failed") if completed else ("Incomplete",)
    )

    voucher_status = st.selectbox(
        "Voucher Status",
        ("Voucher Received","Voucher Applied","Own Payment")
    )
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Badge Progress (UNCHANGED LOGIC)
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
# Courses & Organization (UNCHANGED)
# -----------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
l, r = st.columns(2)

with l:
    level_up = st.selectbox("Level Up Courses", ("Completed","Not Started"))
    trial_exam = st.selectbox("Trial Exams", ("Completed","Not Started"))

with r:
    account = st.text_input("Account")
    account_spoc = st.text_input("Account SPOC")
    vertical = st.text_input("Vertical / SL")
    batch = st.text_input("Batch")
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------
# Comment
# -----------------------------------------
comment = st.text_area("Comment", height=100)

# -----------------------------------------
# Prepare Payload (UNCHANGED)
# -----------------------------------------
def prepare_payload():
    return {
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
        "Account": account,
        "Account SPOC": account_spoc,
        "Vertical / SL": vertical,
        "Batch": batch,
        "Planned Certification date": cert_date_to_str(planned_date),
        "Actual Date of completion": cert_date_to_str(actual_date),
        "Voucher Status": voucher_status,
        "SnowPro Certified": snowpro,
        "Comment": comment
    }

# -----------------------------------------
# Action Bar (ORIGINAL LOGIC RESTORED)
# -----------------------------------------
st.divider()
a1, a2, a3 = st.columns([3,1,1])

with a1:
    if st.session_state.edit_mode:
        if st.button("Update Record", type="primary", use_container_width=True):
            if validate_mandatory_fields(emp_id, emp_name):
                st.session_state.pending_data = prepare_payload()
                st.session_state.pending_action = "update"
                st.session_state.save_completed = False
    else:
        if st.button("Add New Certification", type="primary", use_container_width=True):
            if validate_mandatory_fields(emp_id, emp_name) and validate_emp_name_consistency(emp_id, emp_name):
                st.session_state.pending_data = prepare_payload()
                st.session_state.pending_action = "insert"
                st.session_state.save_completed = False

with a2:
    if st.button("Cancel", use_container_width=True):
        st.session_state.pending_data = None
        st.session_state.pending_action = None
        st.session_state.save_completed = None

with a3:
    if st.session_state.edit_mode:
        if st.checkbox("Confirm Delete"):
            if st.button("🗑 Delete", use_container_width=True):
                session.sql(f"""
                    DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                    WHERE "EMP ID" = '{emp_id}'
                      AND "Certification" = '{certification}'
                """).collect()
                st.success("Record deleted")
                st.session_state.edit_mode = False
                st.session_state.record = {}

# -----------------------------------------
# Confirm & Save (UNCHANGED – THIS IS KEY)
# -----------------------------------------
if st.session_state.pending_data:
    st.subheader("🔍 Review Before Saving")
    st.dataframe(pd.DataFrame([st.session_state.pending_data]), use_container_width=True)

    if st.button("✅ Confirm & Save", disabled=st.session_state.save_completed):
        if st.session_state.pending_action == "insert":
            session.create_dataframe(
                [Row(**st.session_state.pending_data)]
            ).write.mode("append").save_as_table(
                "USE_CASE.CERTIFICATION.NEW_CERTIFICATION"
            )
        else:
            updates = [
                f'"{k}" = \'{v}\'' if v else f'"{k}" = NULL'
                for k, v in st.session_state.pending_data.items()
                if k not in ["EMP ID", "Certification"]
            ]
            session.sql(f"""
                UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                SET {", ".join(updates)}
                WHERE "EMP ID" = '{emp_id}'
                  AND "Certification" = '{certification}'
            """).collect()

        st.success("✅ Data saved successfully")
        st.session_state.save_completed = True
        st.session_state.pending_data = None
        st.session_state.pending_action = None
