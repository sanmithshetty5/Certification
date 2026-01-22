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
    initial_sidebar_state="collapsed"
)

# -----------------------------------------
# Global CSS (UNCHANGED)
# -----------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}
.section-header {
    color: #0F172A;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.5rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.5rem;
}
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
    height: 3em;
}
h1,h2,h3,h4 {
    color: #0F172A !important;
}
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

# -----------------------------------------
# Session State
# -----------------------------------------
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "ENTRY"  # ENTRY | ADD | UPDATE

for key in [
    "edit_mode", "record", "pending_data", "pending_action",
    "save_completed", "duplicate_exists", "last_emp_id"
]:
    st.session_state.setdefault(key, None)

# -----------------------------------------
# Helpers
# -----------------------------------------
def reset_form_state():
    st.session_state.record = {}
    st.session_state.pending_data = None
    st.session_state.pending_action = None
    st.session_state.save_completed = None
    st.session_state.duplicate_exists = False

def validate_emp(emp_id, emp_name):
    if not emp_id.isdigit() or len(emp_id) != 10:
        st.error("❌ Employee ID must be exactly 10 digits.")
        return False
    if not emp_name.strip():
        st.error("❌ Employee Name is mandatory.")
        return False
    return True

def cert_date_to_str(val):
    return val.strftime("%d-%m-%Y") if val else None

# -----------------------------------------
# Header
# -----------------------------------------
title_col, logo_col = st.columns([7, 1])
with title_col:
    st.title("🎓 Certification Tracker")
with logo_col:
    st.image(
        "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/image.png",
        width=180
    )

# -----------------------------------------
# ENTRY MODE (SEARCH ONLY)
# -----------------------------------------
if st.session_state.page_mode == "ENTRY":

    st.subheader("🔍 Find Employee")
    emp_id_input = st.text_input("Enter Employee ID (10 digits)", max_chars=10)
    search_clicked = st.button("Search Employee", type="primary")

    if search_clicked:
        if not emp_id_input.isdigit() or len(emp_id_input) != 10:
            st.error("❌ Invalid Employee ID")
            st.stop()

        df = session.sql(f"""
            SELECT *
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID" = '{emp_id_input}'
        """).to_pandas()

        if df.empty:
            st.warning("⚠️ No data found for this Employee ID.")
            if st.button("➕ Add New Certification"):
                reset_form_state()
                st.session_state.page_mode = "ADD"
                st.session_state.last_emp_id = emp_id_input
                st.rerun()
        else:
            st.success("✅ Employee data found")
            st.dataframe(
                df[["Certification", "Enrolment Month", "SnowPro Certified"]],
                use_container_width=True
            )

            col1, col2 = st.columns(2)

            with col1:
                if st.button("➕ Add New Certification"):
                    reset_form_state()
                    st.session_state.page_mode = "ADD"
                    st.session_state.last_emp_id = emp_id_input
                    st.rerun()

            with col2:
                cert = st.selectbox("Select Certification to Update", df["Certification"])
                if st.button("✏️ Update Selected"):
                    reset_form_state()
                    st.session_state.page_mode = "UPDATE"
                    st.session_state.edit_mode = True
                    st.session_state.record = df[df["Certification"] == cert].iloc[0].to_dict()
                    st.session_state.last_emp_id = emp_id_input
                    st.rerun()

# -----------------------------------------
# ADD / UPDATE MODE (FORM)
# -----------------------------------------
if st.session_state.page_mode in ("ADD", "UPDATE"):

    if st.button("⬅ Back to Search"):
        reset_form_state()
        st.session_state.page_mode = "ENTRY"
        st.rerun()

    st.markdown("---")

    with st.container(border=True):
        st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)

        emp_id = st.text_input(
            "Employee ID",
            value=st.session_state.last_emp_id,
            disabled=True
        )

        emp_name = st.text_input(
            "Employee Name",
            value=st.session_state.record.get("EMP Name", "")
        )

        certification = st.selectbox(
            "Certification",
            certifications,
            index=certifications.index(
                st.session_state.record.get("Certification")
            ) if st.session_state.record else 0
        )

    with st.container(border=True):
        st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
        enrol_month = st.selectbox("Enrolment Month",
                                   ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
        enrol_year = st.selectbox("Enrolment Year", [str(y) for y in range(date.today().year-5, date.today().year+5)])
        planned_date = st.date_input("Planned Certification Date", date.today())
        completed = st.checkbox("Certification Completed?")
        actual_date = st.date_input("Actual Completion Date", max_value=date.today()) if completed else None
        snowpro = st.selectbox("SnowPro Certified", ("Completed","Failed")) if completed else "Incomplete"

    payload = {
        "EMP ID": emp_id,
        "EMP Name": emp_name,
        "Enrolment Month": f"{enrol_month}-{enrol_year}",
        "Certification": certification,
        "Planned Certification date": cert_date_to_str(planned_date),
        "Actual Date of completion": cert_date_to_str(actual_date),
        "SnowPro Certified": snowpro
    }

    if st.button("💾 Save", type="primary"):
        if validate_emp(emp_id, emp_name):
            if st.session_state.page_mode == "ADD":
                session.create_dataframe([Row(**payload)]).write.mode("append").save_as_table(
                    "USE_CASE.CERTIFICATION.NEW_CERTIFICATION"
                )
            else:
                updates = ", ".join(
                    f'"{k}" = \'{v}\'' if v else f'"{k}" = NULL'
                    for k, v in payload.items()
                    if k not in ("EMP ID", "Certification")
                )
                session.sql(f"""
                    UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                    SET {updates}
                    WHERE "EMP ID" = '{emp_id}'
                    AND "Certification" = '{certification}'
                """).collect()

            st.success("✅ Data saved successfully")
            reset_form_state()
            st.session_state.page_mode = "ENTRY"
            st.rerun()
