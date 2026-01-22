import streamlit as st
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
    color: #0F172A;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1.2rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.4rem;
}
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
    height: 3em;
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
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "ENTRY"

for k in ["record", "last_emp_id"]:
    st.session_state.setdefault(k, None)

# -----------------------------------------
# Helpers
# -----------------------------------------
def reset_state():
    st.session_state.record = {}
    st.session_state.last_emp_id = None

def validate_emp(emp_id, emp_name):
    if not emp_id.isdigit() or len(emp_id) != 10:
        st.error("❌ Employee ID must be exactly 10 digits")
        return False
    if not emp_name.strip():
        st.error("❌ Employee Name is mandatory")
        return False
    return True

def fmt_date(d):
    return d.strftime("%d-%m-%Y") if d else None

# -----------------------------------------
# Header
# -----------------------------------------
title_col, logo_col = st.columns([8, 1])
with title_col:
    st.title("🎓 Certification Tracker")
with logo_col:
    st.image(
        "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/image.png",
        width=160
    )

# =========================================================
# ENTRY MODE
# =========================================================
if st.session_state.page_mode == "ENTRY":

    st.subheader("🔍 Find Employee")

    c1, c2, c3 = st.columns([2.5, 1.5, 6])

    with c1:
        emp_id_input = st.text_input(
            "Employee ID",
            max_chars=10,
            placeholder="Optional"
        )

    with c2:
        search_clicked = st.button(
            "🔍 Search",
            type="primary",
            use_container_width=True
        )

    with c3:
        add_clicked = st.button(
            "➕ Add New Certification",
            use_container_width=True
        )

    # -------- SEARCH (VALIDATES) --------
    if search_clicked:
        if not emp_id_input or not emp_id_input.isdigit() or len(emp_id_input) != 10:
            st.error("❌ Enter valid 10-digit Employee ID to search")
            st.stop()

        df = session.sql(f"""
            SELECT *
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID" = '{emp_id_input}'
        """).to_pandas()

        if df.empty:
            st.warning("No records found")
        else:
            st.success("Employee data found")
            st.dataframe(
                df[["Certification","Enrolment Month","SnowPro Certified"]],
                use_container_width=True
            )

    # -------- ADD (NO VALIDATION) --------
    if add_clicked:
        reset_state()
        st.session_state.last_emp_id = emp_id_input.strip() or None
        st.session_state.page_mode = "ADD"
        st.rerun()

# =========================================================
# ADD / UPDATE MODE
# =========================================================
if st.session_state.page_mode in ("ADD", "UPDATE"):

    if st.button("⬅ Back"):
        reset_state()
        st.session_state.page_mode = "ENTRY"
        st.rerun()

    st.markdown("---")

    # ---------------- Employee Info ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)

        emp_id = st.text_input(
            "Employee ID",
            value=st.session_state.last_emp_id or "",
            disabled=bool(st.session_state.last_emp_id)
        )

        emp_name = st.text_input(
            "Employee Name",
            value=st.session_state.record.get("EMP Name","") if st.session_state.record else ""
        )

        certification = st.selectbox(
            "Certification",
            CERTIFICATIONS,
            index=CERTIFICATIONS.index(
                st.session_state.record.get("Certification")
            ) if st.session_state.record else 0
        )

    # ---------------- Schedule Info ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)

        enrol_month = st.selectbox("Enrolment Month", MONTHS)
        enrol_year = st.selectbox(
            "Enrolment Year",
            [str(y) for y in range(date.today().year - 5, date.today().year + 5)]
        )

        planned_date = st.date_input("Planned Certification Date", date.today())

        completed = st.checkbox("Certification Completed?")
        actual_date = st.date_input(
            "Actual Completion Date",
            max_value=date.today()
        ) if completed else None

        snowpro = (
            st.selectbox("SnowPro Certified", ("Completed","Failed"))
            if completed else "Incomplete"
        )

    # ---------------- Payload ----------------
    payload = {
        "EMP ID": emp_id,
        "EMP Name": emp_name,
        "Certification": certification,
        "Enrolment Month": f"{enrol_month}-{enrol_year}",
        "Planned Certification date": fmt_date(planned_date),
        "Actual Date of completion": fmt_date(actual_date),
        "SnowPro Certified": snowpro
    }

    # ---------------- Save ----------------
    if st.button("💾 Save", type="primary"):
        if validate_emp(emp_id, emp_name):

            session.create_dataframe([Row(**payload)]) \
                .write.mode("append") \
                .save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")

            st.success("Data saved successfully")
            reset_state()
            st.session_state.page_mode = "ENTRY"
            st.rerun()
