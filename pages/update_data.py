import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Update Certification",
    layout="wide"
)


st.markdown("""
<style>
/* ================================
   BASE APP STYLING
================================ */
.stApp {
    background-color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

p, label, h1, h2, h3, h4, h5, h6 {
    color: #000000 !important;
}

/* ================================
   BUTTON TEXT COLOR FIX
================================ */
.stButton > button,
.stButton > button span {
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
   HIDE STREAMLIT DEFAULT HEADER/SIDEBAR
================================ */
header[data-testid="stHeader"] {
    display: none;
}

section[data-testid="stSidebar"] {
    display: none;
}

.block-container {
    padding-top: 0rem !important;
}

.page-spacer {
    height: 80px;
}
</style>
""", unsafe_allow_html=True)

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


# ===============================
# GUARD
# ===============================
if "edit_payload" not in st.session_state:
    st.warning("No record selected for update")
    st.stop()

data = st.session_state.edit_payload
original_data = data.copy()
original_certification = data["Certification"]

st.markdown("## ✏️ Update Certification")

# ---------------- Employee Details ----------------
with st.container(border=True):
    st.markdown("### 👤 Employee Details")

    emp_id = st.text_input("Employee ID", data["EMP ID"], disabled=True)
    emp_name = st.text_input("Employee Name", data["EMP Name"])
    def get_emp_certifications(emp_id):
        df = st.connection("snowflake").session().sql(f"""
            SELECT DISTINCT "Certification"
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "EMP ID" = '{emp_id}'
        """).to_pandas()
        
        return df["Certification"].tolist() if not df.empty else []
        ALL_CERTIFICATIONS = [
        "Advanced Analyst",
        "Advanced Architect",
        "Advanced Data Engineer",
        "Advanced Data Scientist",
        "Core",
        "Associate",
        "Speciality Gen AI",
        "Speciality Native App",
        "Speciality Snowpark"
        ]
        
        existing_certs = get_emp_certifications(emp_id)
        current_cert = data["Certification"]
        
        # Allow:
        # - the current certification
        # - certifications NOT already assigned
        certification_options = [
        cert for cert in ALL_CERTIFICATIONS
        if cert == current_cert or cert not in existing_certs
        ]
        certification = st.selectbox(
        "Certification",
        certification_options,
        index=certification_options.index(current_cert)
        )


# ---------------- Schedule & Status ----------------
with st.container(border=True):
    st.markdown("### 🗓️ Schedule & Status")

    enrol_month, enrol_year = data["Enrolment Month"].split("-")

    c1, c2 = st.columns(2)
    with c1:
        enrol_month = st.selectbox(
            "Enrolment Month",
            ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],
            index=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"].index(enrol_month)
        )
        enrol_year = st.text_input("Enrolment Year", enrol_year)

    with c2:
        planned_date = st.date_input(
            "Planned Certification Date",
            datetime.strptime(data["Planned Certification date"], "%d-%m-%Y")
        )

# ---------------- Badges ----------------
with st.container(border=True):
    st.markdown("### 🏅 Badges & Progress")

    badge_opts = ("Completed","In Progress")

    b1, b2, b3, b4, b5 = st.columns(5)

    badge1 = b1.selectbox("Badge 1", badge_opts, badge_opts.index(data["Badge 1 Status"]))
    badge2 = b2.selectbox("Badge 2", badge_opts, badge_opts.index(data["Badge 2 Status"]))
    badge3 = b3.selectbox("Badge 3", badge_opts, badge_opts.index(data["Badge 3 Status"]))
    badge4 = b4.selectbox("Badge 4", badge_opts, badge_opts.index(data["Badge 4 Status"]))
    badge5 = b5.selectbox("Badge 5", badge_opts, badge_opts.index(data["Badge 5 Status"]))

# ---------------- Department ----------------
with st.container(border=True):
    st.markdown("### 🏢 Department Info")

    def get_account_options():
        df = st.connection("snowflake").session().sql("""
            SELECT DISTINCT "Account"
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "Account" IS NOT NULL
            ORDER BY "Account"
        """).to_pandas()
    
        return df["Account"].tolist()
    account_opts = get_account_options()
    existing_account = data.get("Account")
    
    account_sel = st.multiselect(
        "Account",
        account_opts,
        default=[existing_account] if existing_account in account_opts else [],
        max_selections=1,
        accept_new_options=True
    )
    
    account = account_sel[0] if account_sel else None
    
        
    spoc = st.text_input("Account SPOC", data["Account SPOC"] or "")
    
    def get_vertical_sl():
        df = st.connection("snowflake").session().sql("""
            SELECT DISTINCT "Vertical / SL"
            FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            WHERE "Vertical / SL" IS NOT NULL
            ORDER BY "Vertical / SL"
        """).to_pandas()
    
        return df["Vertical / SL"].tolist()

    vertical_options = get_vertical_sl()
    existing_vertical = data.get("Vertical / SL")
    
    vertical_sel = st.multiselect(
        "Vertical / SL",
        vertical_options,
        default=[existing_vertical] if existing_vertical in vertical_options else [],
        max_selections=1,
        accept_new_options=True
    )

    vertical = vertical_sel[0] if vertical_sel else None


    batch = st.text_input("Batch", data["Batch"] or "")
    comment = st.text_area("Comment", data.get("Comment",""))

# ===============================
# CHANGE DETECTION
# ===============================
updated_payload = {
    "EMP Name": emp_name,
    'Certification': certification,
    "Enrolment Month": f"{enrol_month}-{enrol_year}",
    "Planned Certification date": planned_date.strftime("%d-%m-%Y"),
    "Badge 1 Status": badge1,
    "Badge 2 Status": badge2,
    "Badge 3 Status": badge3,
    "Badge 4 Status": badge4,
    "Badge 5 Status": badge5,
    "Account": account,
    "Account SPOC": spoc,
    "Vertical / SL": vertical,
    "Batch": batch,
    "Comment": comment
}

is_changed = any(
    updated_payload[k] != original_data.get(k)
    for k in updated_payload
)

# ===============================
# ACTIONS
# ===============================
st.divider()

c1, c2 = st.columns(2)

with c1:
    if st.button("🔄 Update Entry", type="primary", disabled=not is_changed):
        set_clause = ", ".join(
            f'"{k}" = \'{v}\''
            for k, v in updated_payload.items()
        )

        st.connection("snowflake").session().sql(f"""
            UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
            SET {set_clause}
            WHERE "EMP ID" = '{emp_id}'
              AND "Certification" = '{original_certification}'
        """).collect()

        st.success("✅ Record updated successfully")

        del st.session_state.edit_payload
        st.switch_page("pages/new_data_entry.py")

with c2:
    if st.button("❌ Cancel"):
        del st.session_state.edit_payload
        st.switch_page("pages/new_data_entry.py")
