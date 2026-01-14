# -----------------------------------------
# Imports
# -----------------------------------------
import streamlit as st
import re
from datetime import datetime, date
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark import Row
import pandas as pd

# -----------------------------------------
# Page Config
# -----------------------------------------
st.set_page_config(
    page_title="Certification Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
# Helper Functions
# -----------------------------------------
def cert_date_to_str(val):
    return val.strftime("%d-%m-%Y") if val else None


def safe_date(val):
    try:
        return datetime.strptime(val, "%d-%m-%Y").date()
    except Exception:
        return None


def get_index(options, value):
    if value is None:
        return 0
    return options.index(value) if value in options else 0


def validate_mandatory_fields(emp_id, emp_name):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        st.error("❌ Employee ID must be exactly 10 digits.")
        return False
    if not emp_name or emp_name.strip() == "":
        st.error("❌ Employee Name is mandatory.")
        return False
    return True


def validate_emp_name_consistency(emp_id, emp_name):
    df = session.sql(
        f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
        """
    ).to_pandas()

    if not df.empty:
        existing_name = df.iloc[0]["EMP Name"]
        if existing_name.strip().lower() != emp_name.strip().lower():
            st.error(
                f"❌ EMP ID {emp_id} already exists with name "
                f"'{existing_name}'. Same name must be used."
            )
            return False
    return True


def autofill_employee_name(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return ""
    df = session.sql(
        f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
        """
    ).to_pandas()
    return df.iloc[0]["EMP Name"] if not df.empty else ""


# -----------------------------------------
# Sidebar – Search
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

        result = session.sql(
            f"""
            SELECT *
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID" = '{emp_id}'
              AND "Certification" = '{certification}'
            """
        ).to_pandas()

        if result.empty:
            st.session_state.edit_mode = False
            st.session_state.record = {}
            st.toast("No record found. Add new certification.", icon="➕")
        else:
            st.session_state.edit_mode = True
            st.session_state.record = result.iloc[0].to_dict()
            st.toast("Record loaded successfully", icon="✅")


# -----------------------------------------
# Reset state on EMP ID change + autofill
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
st.markdown("# 🎓 Certification Tracker")


# -----------------------------------------
# Employee Information
# -----------------------------------------
with st.expander("👤 Employee Information", expanded=True):
    emp_name = st.text_input(
        "Employee Name",
        value=(
            st.session_state.record.get("EMP Name")
            or st.session_state.autofill_emp_name
            or ""
        )
    )

    if emp_name and not re.fullmatch(r"[A-Za-z\s]+", emp_name):
        st.error("Employee name must contain only letters")
        st.stop()


# -----------------------------------------
# Enrolment & Planning
# -----------------------------------------
with st.expander("📅 Enrolment & Planning", expanded=True):
    month_options = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    year_options = [
        str(y)[:] for y in range(date.today().year - 5, date.today().year + 5)
    ]

    enrol_month = st.selectbox("Enrolment Month", month_options)
    enrol_year = st.selectbox("Enrolment Year (YYYY)", year_options)

    enrolment_month = f"{enrol_month}-{enrol_year}"

    planned_date = st.date_input("Planned Certification Date", date.today())


# -----------------------------------------
# Badge Progress
# -----------------------------------------
with st.expander("🏅 Badge Progress"):
    badge_opts = ("Completed", "In-Progress")

    badge1 = st.selectbox("Badge 1 Status", badge_opts)
    badge2 = st.selectbox("Badge 2 Status", badge_opts)
    badge3 = st.selectbox("Badge 3 Status", badge_opts)
    badge4 = st.selectbox("Badge 4 Status", badge_opts)
    badge5 = st.selectbox("Badge 5 Status", badge_opts)

    cert_prep = st.selectbox("CertPrepOD Course", badge_opts)


# -----------------------------------------
# Courses & Practice
# -----------------------------------------
with st.expander("📚 Courses & Practice"):
    level_opts = ("Completed", "Not Started")
    level_up = st.selectbox("Level Up Courses", level_opts)
    trial_exam = st.selectbox("Trial Exams", level_opts)


# -----------------------------------------
# Account & Organization Details
# -----------------------------------------
with st.expander("🏢 Account & Organization Details", expanded=True):
    account = st.text_input("Account")
    account_spoc = st.text_input("Account SPOC")
    vertical = st.text_input("Vertical / SL")
    batch = st.text_input("Batch")


# -----------------------------------------
# Completion & Payment
# -----------------------------------------
with st.expander("💰 Completion & Payment", expanded=True):
    completed = st.checkbox("Certification Completed?")

    actual_date = (
        st.date_input(
            "Actual Date of Completion",
            max_value=date.today()
        )
        if completed else None
    )

    snowpro_opts = ("Completed", "Failed") if completed else ("Incomplete",)
    snowpro = st.selectbox("SnowPro Certified", snowpro_opts)

    voucher_status = st.selectbox(
        "Voucher Status",
        ("Voucher Received", "Voucher Applied", "Own Payment")
    )


# -----------------------------------------
# Comment
# -----------------------------------------
with st.expander("📝 Additional Comments"):
    comment = st.text_area("Comment")


# -----------------------------------------
# Prepare Payload
# -----------------------------------------
def prepare_payload():
    return {
        "EMP ID": emp_id,
        "EMP Name": emp_name,
        "Enrolment Month": enrolment_month,
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
# Action Bar
# -----------------------------------------
st.divider()
a1, a2 ,a3 = st.columns([3, 1,1])

with a1:
    if st.session_state.edit_mode:
        if st.button("Update Record", type="primary", use_container_width=True):
            if validate_mandatory_fields(emp_id, emp_name):
                st.session_state.pending_data = prepare_payload()
                st.session_state.pending_action = "update"
                st.session_state.save_completed = False
    else:
        if st.button("Add New Certification", type="primary", use_container_width=True):
            if validate_mandatory_fields(emp_id, emp_name):
                if validate_emp_name_consistency(emp_id, emp_name):
                    st.session_state.pending_data = prepare_payload()
                    st.session_state.pending_action = "insert"
                    st.session_state.save_completed = False

with a2:
    if st.button("Cancel", use_container_width=True):
        st.session_state.pending_data = None
        st.session_state.pending_action = None
        st.session_state.save_completed = None


# -----------------------------------------
# DELETE BUTTON (EDIT MODE ONLY)
# -----------------------------------------
with a3:
    if st.session_state.edit_mode:
        confirm_delete = st.checkbox("Confirm Delete")
        if confirm_delete:
            if st.button("🗑️ Delete", use_container_width=True):
                
                session.sql(f"""
                    DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                    WHERE "EMP ID" = '{emp_id}'
                      AND "Certification" = '{certification}'
                """).collect()

                st.success("✅ Record deleted successfully")

                # Clear state after delete
                st.session_state.record = {}
                st.session_state.edit_mode = False
                st.session_state.pending_data = None
                st.session_state.pending_action = None
# -----------------------------------------
# Confirmation & Save
# -----------------------------------------
if st.session_state.pending_data:
    st.subheader("🔍 Review Before Saving")
    st.dataframe(
        pd.DataFrame([st.session_state.pending_data]),
        use_container_width=True
    )

    if st.button(
        "✅ Confirm & Save",
        disabled=st.session_state.save_completed is True
    ):
        if st.session_state.pending_action == "insert":
            session.create_dataframe(
                [Row(**st.session_state.pending_data)]
            ).write.mode("append").save_as_table(
                "USE_CASE.CERTIFICATION.NEW_CERTIFICATION"
            )

            st.session_state.edit_mode = True
            st.session_state.record = st.session_state.pending_data

        else:
            set_parts = [
                f'"{k}" = \'{v}\'' if v is not None else f'"{k}" = NULL'
                for k, v in st.session_state.pending_data.items()
                if k not in ["EMP ID", "Certification"]
            ]

            session.sql(
                f"""
                UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                SET {", ".join(set_parts)}
                WHERE "EMP ID" = '{emp_id}'
                  AND "Certification" = '{certification}'
                """
            ).collect()

        st.success("✅ Data saved successfully")
        st.session_state.save_completed = True
        st.session_state.pending_data = None
        st.session_state.pending_action = None
