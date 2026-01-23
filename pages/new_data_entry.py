import streamlit as st
import pandas as pd
from datetime import date
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
# Global CSS
# -----------------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}
.section-header {
    color: #000000;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.4rem;
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
CERTIFICATIONS = (
    "Advanced Analyst",
    "Advanced Architect",
    "Advanced Data Engineer",
    "Advanced Data Scientist",
    "Core",
    "Associate",
    "Speciality Gen AI",
    "Speciality Native App",
    "Speciality Snowpark"
)

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# -----------------------------------------
# Session State
# -----------------------------------------
for key in [
    "page_mode",
    "last_emp_id",
    "autofill_profile"
]:
    st.session_state.setdefault(key, None)

if not st.session_state.page_mode:
    st.session_state.page_mode = "ENTRY"

# -----------------------------------------
# Helper Functions
# -----------------------------------------
def get_latest_employee_profile(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return None

    df = session.sql(f"""
        SELECT *
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
        ORDER BY 
            TRY_TO_DATE("Actual Date of completion", 'DD-MM-YYYY') DESC,
            TRY_TO_DATE("Planned Certification date", 'DD-MM-YYYY') DESC
        LIMIT 1
    """).to_pandas()

    return df.iloc[0].to_dict() if not df.empty else None

def get_existing_certifications(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return []

    df = session.sql(f"""
        SELECT DISTINCT "Certification"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
    """).to_pandas()

    return df["Certification"].tolist() if not df.empty else []

def validate_emp(emp_id, emp_name):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        st.error("❌ Employee ID must be exactly 10 digits")
        return False
    if not emp_name.strip():
        st.error("❌ Employee Name is mandatory")
        return False
    return True

def fmt_date(d):
    return d.strftime("%d-%m-%Y") if d else None

def get_vertical_options():
    df = session.sql("""
        SELECT DISTINCT "Vertical / SL"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "Vertical / SL" IS NOT NULL
        ORDER BY "Vertical / SL"
    """).to_pandas()
    return sorted(df["Vertical / SL"].dropna().tolist())

def normalize(val):
    if not val or (isinstance(val, str) and not val.strip()):
        return None
    return val.strip() if isinstance(val, str) else val

# =========================================================
# ENTRY MODE
# =========================================================
if st.session_state.page_mode == "ENTRY":

    st.subheader("🔍 Find Employee")

    c1, c2, c3 = st.columns([2.5, 1.5, 3])

    with c1:
        emp_id_search = st.text_input("Employee ID", max_chars=10)

    with c2:
        search_clicked = st.button("🔍 Search", type="primary", use_container_width=True)

    with c3:
        add_clicked = st.button("➕ Add New Certification", use_container_width=True)

    if search_clicked:
        if not emp_id_search or not emp_id_search.isdigit() or len(emp_id_search) != 10:
            st.error("❌ Enter valid 10-digit Employee ID")
        else:
            df = session.sql(f"""
                SELECT *
                FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                WHERE "EMP ID" = '{emp_id_search}'
            """).to_pandas()

            if df.empty:
                st.warning("No records found")
            else:
                with st.expander("🔎 Filter Results", expanded=False):
                    search_text = st.text_input("Search across all columns")

                if search_text:
                    df = df[df.apply(
                        lambda r: r.astype(str).str.contains(search_text, case=False).any(),
                        axis=1
                    )]

                st.dataframe(df, use_container_width=True, hide_index=True)

    if add_clicked:
        emp_id_val = emp_id_search.strip() if emp_id_search else ""
        st.session_state.last_emp_id = emp_id_val
        st.session_state.autofill_profile = get_latest_employee_profile(emp_id_val)
        st.session_state.page_mode = "ADD"
        st.rerun()

# =========================================================
# ADD MODE
# =========================================================
if st.session_state.page_mode == "ADD":

    profile = st.session_state.autofill_profile or {}

    if st.button("⬅ Back"):
        st.session_state.page_mode = "ENTRY"
        st.rerun()

    st.markdown("---")

    # ---------------- Employee Details ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            emp_id = st.text_input("Employee ID", value=st.session_state.last_emp_id)
        with c2:
            emp_name = st.text_input("Employee Name", value=profile.get("EMP Name", ""))

        existing_certs = get_existing_certifications(emp_id)
        available_certs = [c for c in CERTIFICATIONS if c not in existing_certs]

        certification = st.selectbox(
            "Certification",
            available_certs if available_certs else ["—"],
            disabled=not available_certs
        )

    if not available_certs:
        st.error("❌ No available certification to add")
        st.stop()

    # ---------------- Schedule ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
        enrol_month = st.selectbox("Enrolment Month", MONTHS)
        enrol_year = st.selectbox("Enrolment Year", [str(y) for y in range(date.today().year - 5, date.today().year + 5)])
        planned_date = st.date_input("Planned Certification Date", date.today())

        completed = st.checkbox("Certification Completed?")
        if completed:
            actual_date = st.date_input("Actual Completion Date", max_value=date.today())
            snowpro = st.selectbox("SnowPro Certified", ("Completed", "Failed"))
        else:
            actual_date = None
            snowpro = "Incomplete"

        voucher_status = st.selectbox("Voucher Status", ("Voucher Received","Voucher Applied","Own Payment"))

    # ---------------- Badges ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)

        badge_opts = ("Completed","In-Progress")
        b1, b2, b3, b4, b5 = st.columns(5)

        def bi(v): return badge_opts.index(v) if v in badge_opts else 1

        badge1 = b1.selectbox("Badge 1", badge_opts, index=bi(profile.get("Badge 1 Status")))
        badge2 = b2.selectbox("Badge 2", badge_opts, index=bi(profile.get("Badge 2 Status")))
        badge3 = b3.selectbox("Badge 3", badge_opts, index=bi(profile.get("Badge 3 Status")))
        badge4 = b4.selectbox("Badge 4", badge_opts, index=bi(profile.get("Badge 4 Status")))
        badge5 = b5.selectbox("Badge 5", badge_opts, index=bi(profile.get("Badge 5 Status")))

        cert_prep = st.selectbox("CertPrepOD", badge_opts)
        level_up = st.selectbox("Level Up Courses", ("Completed","Not Started"))
        trial_exam = st.selectbox("Trial Exams", ("Completed","Not Started"))

    # ---------------- Department ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🏢 Department Info</div>', unsafe_allow_html=True)

        account = st.text_input("Account", value=profile.get("Account", ""))
        account_spoc = st.text_input("Account SPOC", value=profile.get("Account SPOC", ""))

        vertical_opts = get_vertical_options()
        vertical_sel = st.multiselect(
            "Vertical / SL",
            vertical_opts,
            default=[profile.get("Vertical / SL")] if profile.get("Vertical / SL") in vertical_opts else [],
            max_selections=1,
            accept_new_options=True
        )
        vertical = vertical_sel[0] if vertical_sel else None
        batch = st.text_input("Batch")

        comment = st.text_area("Comment")

    # ---------------- Save ----------------
    if st.button("💾 Add New Certification", type="primary", use_container_width=True):

        if validate_emp(emp_id, emp_name):
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
                "Batch": normalize(batch),
                "Planned Certification date": fmt_date(planned_date),
                "Actual Date of completion": fmt_date(actual_date),
                "Voucher Status": voucher_status,
                "SnowPro Certified": snowpro,
                "Comment": normalize(comment)
            }

            session.create_dataframe([Row(**payload)]) \
                .write.mode("append") \
                .save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")

            st.success("✅ Certification added successfully")
            st.session_state.page_mode = "ENTRY"
            st.rerun()
