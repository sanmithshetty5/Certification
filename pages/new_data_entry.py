import streamlit as st
import pandas as pd
from datetime import date
import time
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

/* ================================
   BASE APP STYLING
================================ */
.stApp {
    background-color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

/* ================================
   GLOBAL TEXT (SAFE ELEMENTS ONLY)
================================ */
p, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* Section headers */
.section-header {
    color: #000000 !important;
    font-size: 1.1rem;
    font-weight: 700;
    margin-bottom: 1rem;
    border-bottom: 2px solid #E2E8F0;
    padding-bottom: 0.4rem;
}

/* ================================
   BUTTON FIX (THIS WAS BROKEN)
================================ */
.stButton > button {
    color: #FFFFFF !important;
}

.stButton > button span {
    color: #FFFFFF !important;
}

/* Icons inside buttons */
.stButton svg {
    fill: #FFFFFF !important;
}

/* ================================
   INPUTS & SELECTBOXES (VISIBLE TEXT)
================================ */

/* Closed selectbox text */
div[data-baseweb="select"] > div {
    color: #FFFFFF !important;
}

/* Dropdown menu container */
ul[data-baseweb="menu"] {
    background-color: #1F2937 !important;
}

/* Dropdown options */
ul[data-baseweb="menu"] li {
    color: #FFFFFF !important;
}

/* Hovered option */
ul[data-baseweb="menu"] li:hover {
    background-color: #374151 !important;
}

/* Selected option */
ul[data-baseweb="menu"] li[aria-selected="true"] {
    background-color: #4B5563 !important;
    color: #FFFFFF !important;
}

/* ================================
   TEXT INPUTS / DATE INPUTS
================================ */
input, textarea {
    color: #FFFFFF !important;
}

/* ================================
   NAVBAR
================================ */
.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 64px;
    background-color: #0F172A;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 2rem;
    z-index: 10000;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.top-nav,
.top-nav * {
    color: #FFFFFF !important;
}

.nav-links a {
    color: #E5E7EB;
    margin-left: 1.5rem;
    text-decoration: none;
    font-weight: 600;
    font-size: 0.95rem;
}

.nav-links a:hover {
    color: #38BDF8;
}

/* ================================
   LAYOUT FIXES
================================ */
header[data-testid="stHeader"] {
    display: none;
}

.block-container {
    padding-top: 0rem !important;
}

section[data-testid="stSidebar"] {
    display: none;
}

div[data-testid="stAppViewContainer"] {
    margin-left: 0;
}

div[data-testid="stMainBlockContainer"] {
    padding-left: 2rem;
    max-width: 100%;
}

.page-spacer {
    height: 80px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------
# Snowflake Session
# -----------------------------------------
cnx = st.connection("snowflake")
session = cnx.session()


st.markdown("""
<div class="top-nav">
    <div class="nav-left">Certification Tracker</div>
    <div class="nav-links">
        <a href="/" target="_self">Welcome Page</a>
        <a href="/Data_Entry" target="_self">Data Entry</a>
        <a href="/Realtime_Analysis" target="_self">Realtime Analysis</a>
        <a href="/new_data_entry" target="_self">New Data Entry</a>
        <a href="/About_Page" target="_self">About</a>
    </div>
</div>

<div class="page-spacer"></div>
""", unsafe_allow_html=True)
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
    "autofill_profile",
    "last_autofill_emp_id",
    "pending_data",
    "duplicate_exists",
    "save_completed",
    "review_payload"
]:
    st.session_state.setdefault(key, None)
st.session_state.setdefault("last_autofill_emp_id", None)
st.session_state.setdefault("autofill_profile", None)
st.session_state.setdefault("review_mode", False)
st.session_state.setdefault("review_payload", None)


if not st.session_state.page_mode:
    st.session_state.page_mode = "ENTRY"

# -----------------------------------------
# Helper Functions
# -----------------------------------------
def get_latest_employee_profile(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return {}

    df = session.sql(f"""
        SELECT *
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
        ORDER BY 
            CASE WHEN "Account" IS NOT NULL THEN 0 ELSE 1 END,
            TRY_TO_DATE("Actual Date of completion", 'DD-MM-YYYY') DESC,
            TRY_TO_DATE("Planned Certification date", 'DD-MM-YYYY') DESC
        LIMIT 1
    """).to_pandas()
    return df.iloc[0].to_dict() if not df.empty else {}

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

def autofill_employee_name(emp_id):
    if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
        return ""
    df = session.sql(f"""
        SELECT DISTINCT "EMP Name"
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
    """).to_pandas()
    return df.iloc[0]["EMP Name"] if not df.empty else ""

def check_duplicate(emp_id, certification):
    if not emp_id or not certification:
        return False
    df = session.sql(f"""
        SELECT 1
        FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
        WHERE "EMP ID" = '{emp_id}'
          AND "Certification" = '{certification}'
        LIMIT 1
    """).to_pandas()
    return not df.empty

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
    if val is None:
        return None
    if isinstance(val, str) and val.strip() == "":
        return None
    return val.strip() if isinstance(val, str) else val

# =========================================================
# ENTRY MODE
# =========================================================
if st.session_state.page_mode == "ENTRY":

    st.subheader("🔍 Find Employee")

    c1, c2, c3 = st.columns([3, 1.5, 4])

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
                st.success("Employee records found")
                NULL_PLACEHOLDER = "—"
                df_display = df.copy()
                # Replace NaN / None / empty strings for display only
                df_display = df_display.fillna(NULL_PLACEHOLDER)
                
                df_display = df_display.replace(
                    to_replace=r'^\s*$',
                    value=NULL_PLACEHOLDER,
                    regex=True
                )


                # Tick / cross for SnowPro Certified
                df_display["SnowPro Status"] = df_display["SnowPro Certified"].map({
                    "Completed": "✔ Completed",
                    "Failed": "✖ Failed",
                    "Incomplete": "⏳ Incomplete"
                }).fillna("⏳ Incomplete")
                
                # Optional: Certification completion flag
                df_display["Completed?"] = df_display["SnowPro Certified"] == "Completed"

                st.dataframe(
                    df_display,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "SnowPro Status": st.column_config.TextColumn(
                            "SnowPro Status",
                            help="Certification result",
                            width="medium"
                        ),
                        "Completed?": st.column_config.CheckboxColumn(
                            "Completed",
                            help="✔ = Completed, ✖ = Not completed"
                        )
                    }
                )
                st.markdown("### ✏️ Edit / Delete Record")

                selected_cert = st.selectbox(
                    "Select Certification to Edit",
                    df["Certification"].tolist()
                )

                row = df[df["Certification"] == selected_cert].iloc[0].to_dict()
                
                c1, c2 = st.columns(2)
                
                with c1:
                    if st.button("✏️ Edit Selected Record", type="primary"):
                        st.session_state.edit_payload = row
                        st.switch_page("pages/update_data_page.py")
                
                with c2:
                    if st.button("🗑️ Delete Selected Record"):
                        if st.confirm("Are you sure you want to delete this record?"):
                            session.sql(f"""
                                DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                                WHERE "EMP ID" = '{row["EMP ID"]}'
                                  AND "Certification" = '{selected_cert}'
                            """).collect()
                        
                            st.success("Record deleted")
                            st.rerun()


    if add_clicked:
        emp_id_val = emp_id_search.strip() if emp_id_search else ""
        st.session_state.last_emp_id = emp_id_val
    
        profile = get_latest_employee_profile(emp_id_val)

        st.session_state.autofill_profile = profile
        st.session_state.page_mode = "ADD"
        st.rerun()


# =========================================================
# ADD MODE
# ========================================================
 

if st.session_state.page_mode == "ADD":

    profile = st.session_state.autofill_profile or {}
    if not isinstance(profile, dict):
        profile = {}

    if st.button("⬅ Back"):
        st.session_state.page_mode = "ENTRY"
        st.session_state.last_autofill_emp_id = None
        st.session_state.autofill_profile = {}
        st.rerun()
    st.markdown("---")

    # ---------------- Employee Details ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)
        
        
        c1, c2 = st.columns(2)

        with c1:
            emp_id = st.text_input(
                "Employee ID",
                value=st.session_state.last_emp_id or "",
                disabled=st.session_state.review_mode

            )
            if (
                emp_id
                and emp_id.isdigit()
                and len(emp_id) == 10
                and emp_id != st.session_state.last_autofill_emp_id
            ):
                profile = get_latest_employee_profile(emp_id)
            
                st.session_state.autofill_profile = profile or {}
                st.session_state.last_autofill_emp_id = emp_id
            

        with c2:
            # emp_name = st.text_input(
            #     "Employee Name",
            #     value=st.session_state.autofill_emp_name or ""
            # )
            emp_name = st.text_input(
                "Employee Name",
                value=(profile.get("EMP Name") if isinstance(profile, dict) else ""),
                disabled=st.session_state.review_mode
            )

        # Fetch existing certs for this EMP ID
        existing_certs = get_existing_certifications(emp_id)
        
        # Filter out already-used certifications
        available_certs = [
            cert for cert in CERTIFICATIONS
            if cert not in existing_certs
        ]
        
        if not available_certs:
            st.warning("⚠️ All certifications are already assigned to this employee.")
            certification = None
        else:
            certification = st.selectbox(
                "Certification",
                available_certs,
                key=f"cert_select_{emp_id}_{len(existing_certs)}",
                disabled=st.session_state.review_mode
            )


  
    if certification is None:
        st.error("❌ No available certification to add for this employee.")
        st.stop()

    # ---------------- Schedule & Status ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)

        with m1:
            c_m, c_y = st.columns(2)
            enrol_month = c_m.selectbox("Enrolment Month", MONTHS,disabled=st.session_state.review_mode)
            enrol_year = c_y.selectbox(
                "Enrolment Year",
                [str(y) for y in range(date.today().year - 5, date.today().year + 5)],disabled=st.session_state.review_mode
            )
            planned_date = st.date_input("Planned Certification Date", date.today(),disabled=st.session_state.review_mode)

        with m2:
            completed = st.checkbox(
                "Certification Completed?",
                disabled=st.session_state.review_mode
            )

            if completed:
                actual_date = st.date_input("Actual Completion Date", max_value=date.today(),disabled=st.session_state.review_mode)
                snowpro = st.selectbox("SnowPro Certified", ("Completed","Failed"),disabled=st.session_state.review_mode)
            else:
                actual_date = None
                snowpro = "Incomplete"

            voucher_status = st.selectbox(
                "Voucher Status",
                ("Voucher Received","Voucher Applied","Own Payment"),disabled=st.session_state.review_mode
            )

    # ---------------- Badges ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)
        badge_opts = ("Completed","In Progress")
        b1, b2, b3, b4, b5 = st.columns(5)
        def badge_index(val):
            return badge_opts.index(val) if val in badge_opts else badge_opts.index("In Progress")

        badge1 = b1.selectbox(
            "Badge 1",
            badge_opts,
            index=badge_index(profile.get("Badge 1 Status")),disabled=st.session_state.review_mode
        )
        badge2 = b2.selectbox(
            "Badge 2",
            badge_opts,
            index=badge_index(profile.get("Badge 2 Status")),disabled=st.session_state.review_mode

        )
        badge3 = b3.selectbox(
            "Badge 3",
            badge_opts,
            index=badge_index(profile.get("Badge 3 Status")),disabled=st.session_state.review_mode

        )
        badge4 = b4.selectbox(
            "Badge 4",
            badge_opts,
            index=badge_index(profile.get("Badge 4 Status")),disabled=st.session_state.review_mode

        )
        badge5 = b5.selectbox(
            "Badge 5",
            badge_opts,
            index=badge_index(profile.get("Badge 5 Status")),disabled=st.session_state.review_mode

        )

        p1, p2, p3 = st.columns(3)
       
        cert_prep = p1.selectbox("CertPrepOD", badge_opts,index=badge_index(profile.get("cert_prep")),disabled=st.session_state.review_mode)
        cnc_opts =  ("Completed","Not Started")
        def cnc_index(val):
            return cnc_opts.index(val) if val in cnc_opts else cnc_opts.index("Not Started")
        level_up = p2.selectbox("Level Up Courses", cnc_opts,index=cnc_index(profile.get("level_up")),disabled=st.session_state.review_mode)
        trial_exam = p3.selectbox(
            "Trial Exams",
            cnc_opts,
            index=cnc_index(profile.get("Trial Exam")),disabled=st.session_state.review_mode
        )


    # ---------------- Department ----------------
    with st.container(border=True):
        st.markdown('<div class="section-header">🏢 Department Info</div>', unsafe_allow_html=True)
        r1, r2 = st.columns(2)

        with r1:
            account = st.text_input(
                "Account",
                value=profile.get("Account", "") or "",disabled=st.session_state.review_mode

            )

            account_spoc = st.text_input("Account SPOC",value=profile.get("Account SPOC", "") or "",disabled=st.session_state.review_mode)

        with r2:
            vertical_opts = get_vertical_options()
            existing_vertical = profile.get("Vertical / SL")
            vertical_sel = st.multiselect(
                "Vertical / SL",
                vertical_opts,
                default=[existing_vertical] if existing_vertical in vertical_opts else [],
                disabled=st.session_state.review_mode,
                max_selections=1,
                accept_new_options=True
            )
            vertical = vertical_sel[0] if vertical_sel else None
            batch = st.text_input("Batch",value=profile.get("Batch", "") or "",disabled=st.session_state.review_mode)
           

        comment = st.text_area("Comment",disabled=st.session_state.review_mode)

    # ---------------- Prepare Payload ----------------
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
        "Batch":normalize(batch),
        "Planned Certification date": fmt_date(planned_date),
        "Actual Date of completion": fmt_date(actual_date),
         "Voucher Status": voucher_status,
        "SnowPro Certified": snowpro,
        "Comment": normalize(comment)
    }

    # ---------------- Save ----------------
    if st.button(
        "💾 Add New Certification",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.review_mode
    ):
        if certification is None:
            st.error("❌ No available certification")
            st.stop()

        if validate_emp(emp_id, emp_name):
            st.session_state.review_payload = payload
            st.session_state.review_mode = True
            st.rerun()

    
    if st.session_state.review_mode and st.session_state.review_payload:

        st.markdown("### 🔍 Review Before Saving")
    
        review_df = pd.DataFrame([st.session_state.review_payload])

        st.dataframe(
            review_df,
            use_container_width=True,
            hide_index=True
        )

        c1, c2 = st.columns(2)

        with c1:
            if st.button("✅ Confirm Save", type="primary", use_container_width=True):

                # 1. Save to DB
                session.create_dataframe([Row(**st.session_state.review_payload)]) \
                    .write \
                    .mode("append") \
                    .save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")
            
                # 2. Acknowledgement            
                # 3. HARD RESET of ADD-page state
                st.session_state.save_completed = True

                st.session_state.review_mode = False
                st.session_state.review_payload = None
                st.session_state.last_autofill_emp_id = None
                st.session_state.autofill_profile = {}
            
                # Optional: clear EMP ID if you want a fresh form
                st.session_state.last_emp_id = ""
                if st.session_state.get("save_completed"):
                    st.success("🎉 Certification saved successfully")
                    st.session_state.save_completed = False
                time.sleep(3)

                
                # 4. Rerun so UI fully refreshes
                st.rerun()                
                

        
        with c2:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.review_mode = False
                st.session_state.review_payload = None
                st.session_state.last_autofill_emp_id = None
                st.rerun()


    
            # session.sql("SELECT 1").collect()  # force execution
    
            # st.success("✅ Certification added successfully")
            # st.session_state.last_emp_id = emp_id
            # st.session_state.autofill_emp_name = emp_name
            # st.rerun()
