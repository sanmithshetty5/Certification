
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
# Enhanced Professional UI Theme (CSS FIXED)
# -----------------------------------------
st.markdown("""
<style>
    /* 1. Global Page Settings */
    .stApp {
        background-color: #F8FAFC; /* Light Blue-Grey Background */
        font-family: 'Inter', sans-serif;
    }
    
    /* SELECTIVE CARD BORDER — CLOUD & SNOWFLAKE SAFE */
    .section-card {
        background-color: #FFFFFF;
        border: 1.5px solid #1E293B;
        border-radius: 8px;
        padding: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* TOP-RIGHT LOGO */
    .app-logo {
        position: fixed;
        top: 18px;
        right: 24px;
        z-index: 1000;
    }
    
    .app-logo img {
        height: 1000px;       /* adjust if needed */
        width: auto;
    }


    /* 3. WIDGET LABELS (The "Headers" above inputs) - CRITICAL FIX */
    .stTextInput label, .stSelectbox label, .stDateInput label, .stTextArea label {
        color: #1E293B !important; /* Dark Slate - High Contrast */
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* 4. CHECKBOX TEXT - CRITICAL FIX */
    .stCheckbox label p {
        color: #1E293B !important; /* Dark Text */
        font-weight: 600 !important;
    }

    /* 5. Input Field Styling */
    .stTextInput input, .stSelectbox div[data-baseweb="select"], .stDateInput input, textarea {
        color: #0F172A !important; /* Text user types is dark */
        background-color: #FFFFFF !important; /* Background is white */
        border-color: #E2E8F0 !important;
    }
    
    /* 6. Section Headers (Custom Divs) */
    .section-header {
        color: #0F172A;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #E2E8F0;
        padding-bottom: 0.5rem;
        display: block;
    }

    /* 7. Button Styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 600;
        height: 3em;
    }
    
    /* 8. Fix specific Streamlit spacing quirks */
    [data-testid="stForm"] {
        background-color: transparent;
    }

        /* 3. HEADINGS (Fixes 'Certification Tracker' visibility) */
    h1, h2, h3, h4, h5, h6, h1 span, h2 span, h3 span {
        color: #0F172A !important; /* Force Dark Navy Color */
        font-weight: 700 !important;
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

title_col, logo_col = st.columns([8, 1])

with title_col:
    st.title("🎓 Certification Tracker")

with logo_col:
    st.image(
        "https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png",
        width=80
    )
st.markdown("---")

# -----------------------------------------
# Employee + Certification (UI FIXED)
# -----------------------------------------
# Using border=True creates the container, CSS styles it as a card
with st.container(border=True):
    st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 2])

    with c1:
        emp_id = st.text_input("Employee ID", value=emp_id)
    with c2:
        emp_name = st.text_input(
            "Employee Name",
            value=(
                st.session_state.record.get("EMP Name")
                or st.session_state.autofill_emp_name
                or ""
            )
        )
    with c3:
        certification = st.selectbox("Certification Track", certifications, index=certifications.index(certification) if certification in certifications else 0)

# -----------------------------------------
# Enrolment & Planning (UI FIXED)
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)

    with m1:
        # Nested columns for Month/Year to keep them tight
        c_sub1, c_sub2 = st.columns(2)
        month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]
        
        with c_sub1:
            enrol_month = st.selectbox("Enrolment Month", month_opts)
        with c_sub2:
            enrol_year = st.selectbox("Enrolment Year", year_opts)
            
        planned_date = st.date_input("Planned Certification Date", date.today())
        
    with m2:
        # Added spacer to align checkbox with the dropdowns on the left
        st.write("") 
        st.write("") 
        completed = st.checkbox("Certification Completed?")
        
        if completed:
            actual_date = st.date_input(
                "Actual Completion Date",
                max_value=date.today()
            )
            snowpro = st.selectbox(
                "SnowPro Certified",
                ("Completed","Failed")
            )
        else:
            actual_date = None
            snowpro = "Incomplete" # Default value logic preserved but hidden from UI
            # Just placeholder logic for UI consistency if needed
            st.markdown("*Mark completed to see date options*")

        voucher_status = st.selectbox(
            "Voucher Status",
            ("Voucher Received","Voucher Applied","Own Payment")
        )

# -----------------------------------------
# Badge Progress (UI FIXED)
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)
    
    badge_opts = ("Completed","In-Progress")
    
    # Row 1: Badges
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5)
    badge1 = b_col1.selectbox("Badge 1", badge_opts)
    badge2 = b_col2.selectbox("Badge 2", badge_opts)
    badge3 = b_col3.selectbox("Badge 3", badge_opts)
    badge4 = b_col4.selectbox("Badge 4", badge_opts)
    badge5 = b_col5.selectbox("Badge 5", badge_opts)

    st.markdown("---")
    
    # Row 2: Prep Work
    c_prep1, c_prep2, c_prep3 = st.columns(3)
    cert_prep = c_prep1.selectbox("CertPrepOD", badge_opts)
    level_up = c_prep2.selectbox("Level Up Courses", ("Completed","Not Started"))
    trial_exam = c_prep3.selectbox("Trial Exams", ("Completed","Not Started"))

# -----------------------------------------
# Courses & Organization (UI FIXED)
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🏢 Department Info</div>', unsafe_allow_html=True)
    r1, r2 = st.columns(2)

    with r1:
        account = st.text_input("Account")
        account_spoc = st.text_input("Account SPOC")
    with r2:
        vertical = st.text_input("Vertical / SL")
        batch = st.text_input("Batch")
        
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
# Action Bar (UNCHANGED LOGIC)
# -----------------------------------------
st.write("")
st.write("")
a1, a2, a3 = st.columns([3,1,1])

with a1:
    if st.session_state.edit_mode:
        if st.button("💾 Update Record", type="primary", use_container_width=True):
            if validate_mandatory_fields(emp_id, emp_name):
                st.session_state.pending_data = prepare_payload()
                st.session_state.pending_action = "update"
                st.session_state.save_completed = False
    else:
        if st.button("➕ Add New Certification", type="primary", use_container_width=True):
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
        with st.popover("🗑 Delete"):
            st.write("Are you sure?")
            if st.button("Confirm Delete", type="primary", use_container_width=True):
                session.sql(f"""
                    DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
                    WHERE "EMP ID" = '{emp_id}'
                      AND "Certification" = '{certification}'
                """).collect()
                st.success("Record deleted")
                st.session_state.edit_mode = False
                st.session_state.record = {}
                st.rerun()

# -----------------------------------------
# Confirm & Save (UNCHANGED)
# -----------------------------------------
if st.session_state.pending_data:
    st.divider()
    with st.container(border=True):
        st.subheader("🔍 Review Before Saving")
        st.dataframe(pd.DataFrame([st.session_state.pending_data]), use_container_width=True)

        if st.button("✅ Confirm & Save", disabled=st.session_state.save_completed, type="primary"):
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

# import streamlit as st
# import re
# from datetime import datetime, date
# import pandas as pd
# from snowflake.snowpark import Row

# # -----------------------------------------
# # Page Config
# # -----------------------------------------
# st.set_page_config(
#     page_title="Certification Tracker",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # -----------------------------------------
# # Enhanced Professional UI Theme (CSS FIXED FOR CLOUD)
# # -----------------------------------------
# st.markdown("""
# <style>
#     /* 1. Global Page Background - Light Grey */
#     .stApp {
#         background-color: #F8FAFC !important;
#         font-family: 'Inter', sans-serif;
#     }

#     /* 2. FORCE Main Text Color to Dark (Fixes invisible title in Dark Mode) */
#     .stApp > header, .stApp .main .block-container {
#         color: #0F172A !important;
#     }
    
#     /* 3. HEADINGS (Fixes 'Certification Tracker' visibility) */
#     h1, h2, h3, h4, h5, h6, h1 span, h2 span, h3 span {
#         color: #0F172A !important; /* Force Dark Navy Color */
#         font-weight: 700 !important;
#     }

#     /* 4. CONTAINER BORDERS (Fixes missing borders) */
#     /* Target the specific wrapper Streamlit uses for st.container(border=True) */
#     div[data-testid="stVerticalBlockBorderWrapper"] {
#         background-color: #FFFFFF !important;
#         border: 1px solid #94A3B8 !important; /* Darker Grey Border for visibility */
#         border-radius: 10px;
#         padding: 20px;
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
#         margin-bottom: 20px;
#     }

#     /* 5. MAIN AREA INPUT LABELS (Force Dark Text) */
#     /* This applies ONLY to the main area, not the sidebar */
#     .main .stTextInput label, 
#     .main .stSelectbox label, 
#     .main .stDateInput label, 
#     .main .stTextArea label,

#     .stCheckbox label p {
#         color: #1E293B !important; /* Dark Text */
#         font-weight: 600 !important;
#     }
#     /* 6. SIDEBAR STYLING (Keep Sidebar Text Light if background is dark) */
#     [data-testid="stSidebar"] {
#         background-color: #0F172A; /* Optional: Force dark sidebar background */
#     }
#     [data-testid="stSidebar"] h1, 
#     [data-testid="stSidebar"] h2, 
#     [data-testid="stSidebar"] h3, 
#     [data-testid="stSidebar"] label, 
#     [data-testid="stSidebar"] p {
#         color: #F8FAFC !important; /* Light text for Sidebar visibility */
#     }
#     /* Ensure sidebar input backgrounds are light for readability */
#     [data-testid="stSidebar"] input, 
#     [data-testid="stSidebar"] div[data-baseweb="select"] > div {
#         background-color: #FFFFFF !important;
#         color: #0F172A !important;
#     }

#     /* 7. GENERAL INPUT STYLING */
#     input, textarea, select {
#         color: #0F172A !important;
#         background-color: #FFFFFF !important;
#     }
#     /* Fix for Selectbox dropdown text */
#     div[data-baseweb="select"] > div {
#         background-color: #FFFFFF !important;
#         color: #0F172A !important;
#         border-color: #CBD5E1 !important;
#     }
    
#     /* 8. Button Styling */
#     .stButton > button {
#         border-radius: 6px;
#         font-weight: 600;
#         height: 3em;
#     }
    
#     /* 9. Divider styling */
#     .section-header {
#         color: #0F172A;
#         font-size: 1.15rem;
#         font-weight: 700;
#         margin-bottom: 1rem;
#         border-bottom: 2px solid #E2E8F0;
#         padding-bottom: 0.5rem;
#         display: block;
#     }
# </style>
# """, unsafe_allow_html=True)


# # -----------------------------------------
# # Snowflake Session
# # -----------------------------------------
# cnx = st.connection("snowflake")
# session = cnx.session()

# # -----------------------------------------
# # Session State Initialization (UNCHANGED)
# # -----------------------------------------
# for key in [
#     "edit_mode",
#     "record",
#     "pending_data",
#     "pending_action",
#     "last_emp_id",
#     "save_completed",
#     "autofill_emp_name"
# ]:
#     if key not in st.session_state:
#         st.session_state[key] = None

# # -----------------------------------------
# # Helper Functions (UNCHANGED)
# # -----------------------------------------
# def cert_date_to_str(val):
#     return val.strftime("%d-%m-%Y") if val else None

# def validate_mandatory_fields(emp_id, emp_name):
#     if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
#         st.error("❌ Employee ID must be exactly 10 digits.")
#         return False
#     if not emp_name or emp_name.strip() == "":
#         st.error("❌ Employee Name is mandatory.")
#         return False
#     return True

# def validate_emp_name_consistency(emp_id, emp_name):
#     df = session.sql(f"""
#         SELECT DISTINCT "EMP Name"
#         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#         WHERE "EMP ID" = '{emp_id}'
#     """).to_pandas()
#     if not df.empty:
#         if df.iloc[0]["EMP Name"].lower() != emp_name.lower():
#             st.error("❌ EMP ID exists with different name.")
#             return False
#     return True

# def autofill_employee_name(emp_id):
#     if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
#         return ""
#     df = session.sql(f"""
#         SELECT DISTINCT "EMP Name"
#         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#         WHERE "EMP ID" = '{emp_id}'
#     """).to_pandas()
#     return df.iloc[0]["EMP Name"] if not df.empty else ""

# # -----------------------------------------
# # Sidebar – Search (UNCHANGED LOGIC)
# # -----------------------------------------
# with st.sidebar:
#     st.markdown("## 🔍 Search Employee")

#     emp_id = st.text_input("Employee ID (10 digits)")

#     certifications = (
#         "Advanced Analyst",
#         "Advanced Architect",
#         "Advanced Data Engineer",
#         "Core",
#         "Associate",
#         "Speciality Gen AI",
#         "Speciality Native App",
#         "Advanced Data Scientist",
#         "Speciality Snowpark"
#     )

#     certification = st.selectbox("Certification", certifications)

#     if st.button("Search", type="primary", use_container_width=True):
#         if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
#             st.error("Enter valid 10-digit EMP ID")
#             st.stop()

#         result = session.sql(f"""
#             SELECT *
#             FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#             WHERE "EMP ID" = '{emp_id}'
#               AND "Certification" = '{certification}'
#         """).to_pandas()

#         if result.empty:
#             st.session_state.edit_mode = False
#             st.session_state.record = {}
#             st.toast("No record found. Add new.", icon="➕")
#         else:
#             st.session_state.edit_mode = True
#             st.session_state.record = result.iloc[0].to_dict()
#             st.toast("Record loaded", icon="✅")

# # -----------------------------------------
# # Reset on EMP ID change (UNCHANGED)
# # -----------------------------------------
# if st.session_state.last_emp_id != emp_id:
#     st.session_state.record = {}
#     st.session_state.edit_mode = False
#     st.session_state.pending_data = None
#     st.session_state.pending_action = None
#     st.session_state.save_completed = None
#     st.session_state.autofill_emp_name = autofill_employee_name(emp_id)
#     st.session_state.last_emp_id = emp_id

# # -----------------------------------------
# # Header
# # -----------------------------------------
# st.title("🎓 Certification Tracker")
# st.markdown("---")

# # -----------------------------------------
# # Employee + Certification (UNCHANGED LOGIC)
# # -----------------------------------------
# with st.container(border=True):
#     st.markdown('<div class="section-header">👤 Employee Details</div>', unsafe_allow_html=True)
#     c1, c2, c3 = st.columns([1, 2, 2])

#     with c1:
#         emp_id = st.text_input("Employee ID", value=emp_id)
#     with c2:
#         emp_name = st.text_input(
#             "Employee Name",
#             value=(
#                 st.session_state.record.get("EMP Name")
#                 or st.session_state.autofill_emp_name
#                 or ""
#             )
#         )
#     with c3:
#         certification = st.selectbox("Certification Track", certifications, index=certifications.index(certification) if certification in certifications else 0)

# # -----------------------------------------
# # Enrolment & Planning (UNCHANGED LOGIC)
# # -----------------------------------------
# with st.container(border=True):
#     st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
#     m1, m2 = st.columns(2)

#     with m1:
#         c_sub1, c_sub2 = st.columns(2)
#         month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
#         year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]
        
#         with c_sub1:
#             enrol_month = st.selectbox("Enrolment Month", month_opts)
#         with c_sub2:
#             enrol_year = st.selectbox("Enrolment Year", year_opts)
            
#         planned_date = st.date_input("Planned Certification Date", date.today())
        
#     with m2:
#         st.write("") 
#         st.write("") 
#         completed = st.checkbox("Certification Completed?")
        
#         if completed:
#             actual_date = st.date_input(
#                 "Actual Completion Date",
#                 max_value=date.today()
#             )
#             snowpro = st.selectbox(
#                 "SnowPro Certified",
#                 ("Completed","Failed")
#             )
#         else:
#             actual_date = None
#             snowpro = "Incomplete" 
#             st.caption("*Mark completed to see date options*")

#         voucher_status = st.selectbox(
#             "Voucher Status",
#             ("Voucher Received","Voucher Applied","Own Payment")
#         )

# # -----------------------------------------
# # Badge Progress (UNCHANGED LOGIC)
# # -----------------------------------------
# with st.container(border=True):
#     st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)
    
#     badge_opts = ("Completed","In-Progress")
    
#     b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5) 
#     badge1 = b_col1.selectbox("Badge 1", badge_opts)
#     badge2 = b_col2.selectbox("Badge 2", badge_opts)
#     badge3 = b_col3.selectbox("Badge 3", badge_opts)
#     badge4 = b_col4.selectbox("Badge 4", badge_opts)
#     badge5 = b_col5.selectbox("Badge 5", badge_opts)

#     st.markdown("---")
    
#     c_prep1, c_prep2, c_prep3 = st.columns(3)
#     cert_prep = c_prep1.selectbox("CertPrepOD", badge_opts)
#     level_up = c_prep2.selectbox("Level Up Courses", ("Completed","Not Started"))
#     trial_exam = c_prep3.selectbox("Trial Exams", ("Completed","Not Started"))

# # -----------------------------------------
# # Courses & Organization (UNCHANGED LOGIC)
# # -----------------------------------------
# with st.container(border=True):
#     st.markdown('<div class="section-header">🏢 Department Info</div>', unsafe_allow_html=True)
#     r1, r2 = st.columns(2)

#     with r1:
#         account = st.text_input("Account")
#         account_spoc = st.text_input("Account SPOC")
#     with r2:
#         vertical = st.text_input("Vertical / SL")
#         batch = st.text_input("Batch")
        
#     comment = st.text_area("Comment", height=100)

# # -----------------------------------------
# # Prepare Payload (UNCHANGED)
# # -----------------------------------------
# def prepare_payload():
#     return {
#         "EMP ID": emp_id,
#         "EMP Name": emp_name,
#         "Enrolment Month": f"{enrol_month}-{enrol_year}",
#         "Certification": certification,
#         "Badge 1 Status": badge1,
#         "Badge 2 Status": badge2,
#         "Badge 3 Status": badge3,
#         "Badge 4 Status": badge4,
#         "Badge 5 Status": badge5,
#         "CertPrepOD Course": cert_prep,
#         "Level Up Courses": level_up,
#         "# Trial Exams": trial_exam,
#         "Account": account,
#         "Account SPOC": account_spoc,
#         "Vertical / SL": vertical,
#         "Batch": batch,
#         "Planned Certification date": cert_date_to_str(planned_date),
#         "Actual Date of completion": cert_date_to_str(actual_date),
#         "Voucher Status": voucher_status,
#         "SnowPro Certified": snowpro,
#         "Comment": comment
#     }

# # -----------------------------------------
# # Action Bar (UNCHANGED)
# # -----------------------------------------
# st.write("")
# st.write("")
# a1, a2, a3 = st.columns([3,1,1])

# with a1:
#     if st.session_state.edit_mode:
#         if st.button("💾 Update Record", type="primary", use_container_width=True):
#             if validate_mandatory_fields(emp_id, emp_name):
#                 st.session_state.pending_data = prepare_payload()
#                 st.session_state.pending_action = "update"
#                 st.session_state.save_completed = False
#     else:
#         if st.button("➕ Add New Certification", type="primary", use_container_width=True):
#             if validate_mandatory_fields(emp_id, emp_name) and validate_emp_name_consistency(emp_id, emp_name):
#                 st.session_state.pending_data = prepare_payload()
#                 st.session_state.pending_action = "insert"
#                 st.session_state.save_completed = False

# with a2:
#     if st.button("Cancel", use_container_width=True):
#         st.session_state.pending_data = None
#         st.session_state.pending_action = None
#         st.session_state.save_completed = None

# with a3:
#     if st.session_state.edit_mode:
#         with st.popover("🗑 Delete"):
#             st.write("Are you sure?")
#             if st.button("Confirm Delete", type="primary", use_container_width=True):
#                 session.sql(f"""
#                     DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#                     WHERE "EMP ID" = '{emp_id}'
#                       AND "Certification" = '{certification}'
#                 """).collect()
#                 st.success("Record deleted")
#                 st.session_state.edit_mode = False
#                 st.session_state.record = {}
#                 st.rerun()

# # -----------------------------------------
# # Confirm & Save (UNCHANGED)
# # -----------------------------------------
# if st.session_state.pending_data:
#     st.divider()
#     with st.container(border=True):
#         st.subheader("🔍 Review Before Saving")
#         st.dataframe(pd.DataFrame([st.session_state.pending_data]), use_container_width=True)

#         if st.button("✅ Confirm & Save", disabled=st.session_state.save_completed, type="primary"):
#             if st.session_state.pending_action == "insert":
#                 session.create_dataframe(
#                     [Row(**st.session_state.pending_data)]
#                 ).write.mode("append").save_as_table(
#                     "USE_CASE.CERTIFICATION.NEW_CERTIFICATION"
#                 )
#             else:
#                 updates = [
#                     f'"{k}" = \'{v}\'' if v else f'"{k}" = NULL'
#                     for k, v in st.session_state.pending_data.items()
#                     if k not in ["EMP ID", "Certification"]
#                 ]
#                 session.sql(f"""
#                     UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
#                     SET {", ".join(updates)}
#                     WHERE "EMP ID" = '{emp_id}'
#                       AND "Certification" = '{certification}'
#                 """).collect()

#             st.success("✅ Data saved successfully")
#             st.session_state.save_completed = True
#             st.session_state.pending_data = None
#             st.session_state.pending_action = None
            
