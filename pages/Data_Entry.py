# # # -----------------------------------------
# # # Imports
# # # -----------------------------------------
# # import streamlit as st
# # import re
# # from datetime import datetime, date
# # import pandas as pd
# # from snowflake.snowpark import Row

# # # -----------------------------------------
# # # Page Config
# # # -----------------------------------------
# # st.set_page_config(
# #     page_title="Certification Tracker",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # -----------------------------------------
# # # Enhanced Professional UI Theme (COLORS ONLY)
# # # -----------------------------------------
# # st.markdown("""
# # <style>

# # /* App Background */
# # body {
# #     background-color: #0B1220;
# # }

# # /* Main container spacing */
# # .block-container {
# #     padding-top: 1.5rem;
# # }

# # /* Cards */
# # .card {
# #     background-color: #111827;
# #     padding: 1.25rem;
# #     border-radius: 14px;
# #     border: 1px solid #1F2937;
# #     margin-bottom: 1.2rem;
# # }

# # /* Headings */
# # h1, h2, h3 {
# #     color: #F9FAFB;
# #     font-weight: 600;
# # }

# # /* Labels & text */
# # label, .stMarkdown {
# #     color: #CBD5E1 !important;
# #     font-size: 0.9rem;
# # }

# # /* Inputs */
# # input, textarea, select {
# #     background-color: #020617 !important;
# #     color: #E5E7EB !important;
# #     border: 1px solid #334155 !important;
# #     border-radius: 8px !important;
# # }

# # /* Input focus */
# # input:focus, textarea:focus, select:focus {
# #     border-color: #3B82F6 !important;
# #     box-shadow: 0 0 0 1px #3B82F6;
# # }

# # /* Buttons */
# # .stButton > button {
# #     background-color: #3B82F6;
# #     color: white;
# #     border-radius: 10px;
# #     height: 3rem;
# #     font-weight: 600;
# #     border: none;
# # }

# # .stButton > button:hover {
# #     background-color: #2563EB;
# # }

# # /* Success / Error */
# # .stAlert-success {
# #     background-color: #052E16;
# #     color: #22C55E;
# # }

# # .stAlert-error {
# #     background-color: #450A0A;
# #     color: #EF4444;
# # }

# # /* Divider */
# # hr {
# #     border: 1px solid #1F2937;
# # }

# # </style>
# # """, unsafe_allow_html=True)


# # # -----------------------------------------
# # # Snowflake Session
# # # -----------------------------------------
# # cnx = st.connection("snowflake")
# # session = cnx.session()

# # # -----------------------------------------
# # # Session State Initialization (UNCHANGED)
# # # -----------------------------------------
# # for key in [
# #     "edit_mode",
# #     "record",
# #     "pending_data",
# #     "pending_action",
# #     "last_emp_id",
# #     "save_completed",
# #     "autofill_emp_name"
# # ]:
# #     if key not in st.session_state:
# #         st.session_state[key] = None

# # # -----------------------------------------
# # # Helper Functions (UNCHANGED)
# # # -----------------------------------------
# # def cert_date_to_str(val):
# #     return val.strftime("%d-%m-%Y") if val else None

# # def validate_mandatory_fields(emp_id, emp_name):
# #     if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
# #         st.error("❌ Employee ID must be exactly 10 digits.")
# #         return False
# #     if not emp_name or emp_name.strip() == "":
# #         st.error("❌ Employee Name is mandatory.")
# #         return False
# #     return True

# # def validate_emp_name_consistency(emp_id, emp_name):
# #     df = session.sql(f"""
# #         SELECT DISTINCT "EMP Name"
# #         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
# #         WHERE "EMP ID" = '{emp_id}'
# #     """).to_pandas()
# #     if not df.empty:
# #         if df.iloc[0]["EMP Name"].lower() != emp_name.lower():
# #             st.error("❌ EMP ID exists with different name.")
# #             return False
# #     return True

# # def autofill_employee_name(emp_id):
# #     if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
# #         return ""
# #     df = session.sql(f"""
# #         SELECT DISTINCT "EMP Name"
# #         FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
# #         WHERE "EMP ID" = '{emp_id}'
# #     """).to_pandas()
# #     return df.iloc[0]["EMP Name"] if not df.empty else ""

# # # -----------------------------------------
# # # Sidebar – Search (UNCHANGED LOGIC)
# # # -----------------------------------------
# # with st.sidebar:
# #     st.markdown("## 🔍 Search Employee")

# #     emp_id = st.text_input("Employee ID (10 digits)")

# #     certifications = (
# #         "Advanced Analyst",
# #         "Advanced Architect",
# #         "Advanced Data Engineer",
# #         "Core",
# #         "Associate",
# #         "Speciality Gen AI",
# #         "Speciality Native App",
# #         "Advanced Data Scientist",
# #         "Speciality Snowpark"
# #     )

# #     certification = st.selectbox("Certification", certifications)

# #     if st.button("Search", type="primary", use_container_width=True):
# #         if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
# #             st.error("Enter valid 10-digit EMP ID")
# #             st.stop()

# #         result = session.sql(f"""
# #             SELECT *
# #             FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
# #             WHERE "EMP ID" = '{emp_id}'
# #               AND "Certification" = '{certification}'
# #         """).to_pandas()

# #         if result.empty:
# #             st.session_state.edit_mode = False
# #             st.session_state.record = {}
# #             st.toast("No record found. Add new.", icon="➕")
# #         else:
# #             st.session_state.edit_mode = True
# #             st.session_state.record = result.iloc[0].to_dict()
# #             st.toast("Record loaded", icon="✅")

# # # -----------------------------------------
# # # Reset on EMP ID change (UNCHANGED)
# # # -----------------------------------------
# # if st.session_state.last_emp_id != emp_id:
# #     st.session_state.record = {}
# #     st.session_state.edit_mode = False
# #     st.session_state.pending_data = None
# #     st.session_state.pending_action = None
# #     st.session_state.save_completed = None
# #     st.session_state.autofill_emp_name = autofill_employee_name(emp_id)
# #     st.session_state.last_emp_id = emp_id

# # # -----------------------------------------
# # # Header
# # # -----------------------------------------
# # st.markdown("## 🎓 Certification Tracker")

# # # -----------------------------------------
# # # Employee + Certification (UI ONLY)
# # # -----------------------------------------
# # st.markdown('<div class="card">', unsafe_allow_html=True)
# # c1, c2, c3 = st.columns([1, 2, 2])

# # emp_id = c1.text_input("Employee ID", value=emp_id)
# # emp_name = c2.text_input(
# #     "Employee Name",
# #     value=(
# #         st.session_state.record.get("EMP Name")
# #         or st.session_state.autofill_emp_name
# #         or ""
# #     )
# # )
# # certification = c3.selectbox("Certification Track", certifications)
# # st.markdown('</div>', unsafe_allow_html=True)

# # # -----------------------------------------
# # # Enrolment & Planning (UNCHANGED LOGIC)
# # # -----------------------------------------
# # month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
# # year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]

# # st.markdown('<div class="card">', unsafe_allow_html=True)
# # m1, m2 = st.columns(2)

# # with m1:
# #     enrol_month = st.selectbox("Enrolment Month", month_opts)
# #     enrol_year = st.selectbox("Enrolment Year", year_opts)
# #     planned_date = st.date_input("Planned Certification Date", date.today())

# # with m2:
# #     completed = st.checkbox("Certification Completed?")
# #     actual_date = st.date_input(
# #         "Actual Completion Date",
# #         max_value=date.today()
# #     ) if completed else None

# #     snowpro = st.selectbox(
# #         "SnowPro Certified",
# #         ("Completed","Failed") if completed else ("Incomplete",)
# #     )

# #     voucher_status = st.selectbox(
# #         "Voucher Status",
# #         ("Voucher Received","Voucher Applied","Own Payment")
# #     )
# # st.markdown('</div>', unsafe_allow_html=True)

# # # -----------------------------------------
# # # Badge Progress (UNCHANGED LOGIC)
# # # -----------------------------------------
# # st.markdown('<div class="card">', unsafe_allow_html=True)
# # b1, b2, b3 = st.columns(3)
# # badge_opts = ("Completed","In-Progress")

# # badge1 = b1.selectbox("Badge 1", badge_opts)
# # badge4 = b1.selectbox("Badge 4", badge_opts)
# # badge2 = b2.selectbox("Badge 2", badge_opts)
# # badge5 = b2.selectbox("Badge 5", badge_opts)
# # badge3 = b3.selectbox("Badge 3", badge_opts)
# # cert_prep = b3.selectbox("CertPrepOD", badge_opts)
# # st.markdown('</div>', unsafe_allow_html=True)

# # # -----------------------------------------
# # # Courses & Organization (UNCHANGED)
# # # -----------------------------------------
# # st.markdown('<div class="card">', unsafe_allow_html=True)
# # l, r = st.columns(2)

# # with l:
# #     level_up = st.selectbox("Level Up Courses", ("Completed","Not Started"))
# #     trial_exam = st.selectbox("Trial Exams", ("Completed","Not Started"))

# # with r:
# #     account = st.text_input("Account")
# #     account_spoc = st.text_input("Account SPOC")
# #     vertical = st.text_input("Vertical / SL")
# #     batch = st.text_input("Batch")
# # st.markdown('</div>', unsafe_allow_html=True)

# # # -----------------------------------------
# # # Comment
# # # -----------------------------------------
# # comment = st.text_area("Comment", height=100)

# # # -----------------------------------------
# # # Prepare Payload (UNCHANGED)
# # # -----------------------------------------
# # def prepare_payload():
# #     return {
# #         "EMP ID": emp_id,
# #         "EMP Name": emp_name,
# #         "Enrolment Month": f"{enrol_month}-{enrol_year}",
# #         "Certification": certification,
# #         "Badge 1 Status": badge1,
# #         "Badge 2 Status": badge2,
# #         "Badge 3 Status": badge3,
# #         "Badge 4 Status": badge4,
# #         "Badge 5 Status": badge5,
# #         "CertPrepOD Course": cert_prep,
# #         "Level Up Courses": level_up,
# #         "# Trial Exams": trial_exam,
# #         "Account": account,
# #         "Account SPOC": account_spoc,
# #         "Vertical / SL": vertical,
# #         "Batch": batch,
# #         "Planned Certification date": cert_date_to_str(planned_date),
# #         "Actual Date of completion": cert_date_to_str(actual_date),
# #         "Voucher Status": voucher_status,
# #         "SnowPro Certified": snowpro,
# #         "Comment": comment
# #     }

# # # -----------------------------------------
# # # Action Bar (ORIGINAL LOGIC RESTORED)
# # # -----------------------------------------
# # st.divider()
# # a1, a2, a3 = st.columns([3,1,1])

# # with a1:
# #     if st.session_state.edit_mode:
# #         if st.button("Update Record", type="primary", use_container_width=True):
# #             if validate_mandatory_fields(emp_id, emp_name):
# #                 st.session_state.pending_data = prepare_payload()
# #                 st.session_state.pending_action = "update"
# #                 st.session_state.save_completed = False
# #     else:
# #         if st.button("Add New Certification", type="primary", use_container_width=True):
# #             if validate_mandatory_fields(emp_id, emp_name) and validate_emp_name_consistency(emp_id, emp_name):
# #                 st.session_state.pending_data = prepare_payload()
# #                 st.session_state.pending_action = "insert"
# #                 st.session_state.save_completed = False

# # with a2:
# #     if st.button("Cancel", use_container_width=True):
# #         st.session_state.pending_data = None
# #         st.session_state.pending_action = None
# #         st.session_state.save_completed = None

# # with a3:
# #     if st.session_state.edit_mode:
# #         if st.checkbox("Confirm Delete"):
# #             if st.button("🗑 Delete", use_container_width=True):
# #                 session.sql(f"""
# #                     DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION
# #                     WHERE "EMP ID" = '{emp_id}'
# #                       AND "Certification" = '{certification}'
# #                 """).collect()
# #                 st.success("Record deleted")
# #                 st.session_state.edit_mode = False
# #                 st.session_state.record = {}

# # # -----------------------------------------
# # # Confirm & Save (UNCHANGED – THIS IS KEY)
# # # -----------------------------------------
# # if st.session_state.pending_data:
# #     st.subheader("🔍 Review Before Saving")
# #     st.dataframe(pd.DataFrame([st.session_state.pending_data]), use_container_width=True)

# #     if st.button("✅ Confirm & Save", disabled=st.session_state.save_completed):
# #         if st.session_state.pending_action == "insert":
# #             session.create_dataframe(
# #                 [Row(**st.session_state.pending_data)]
# #             ).write.mode("append").save_as_table(
# #                 "USE_CASE.CERTIFICATION.NEW_CERTIFICATION"
# #             )
# #         else:
# #             updates = [
# #                 f'"{k}" = \'{v}\'' if v else f'"{k}" = NULL'
# #                 for k, v in st.session_state.pending_data.items()
# #                 if k not in ["EMP ID", "Certification"]
# #             ]
# #             session.sql(f"""
# #                 UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION
# #                 SET {", ".join(updates)}
# #                 WHERE "EMP ID" = '{emp_id}'
# #                   AND "Certification" = '{certification}'
# #             """).collect()

# #         st.success("✅ Data saved successfully")
# #         st.session_state.save_completed = True
# #         st.session_state.pending_data = None
# #         st.session_state.pending_action = None


# # -----------------------------------------
# # Imports
# # -----------------------------------------
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
#     page_icon="🎓",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # -----------------------------------------
# # PROFESSIONAL ENTERPRISE THEME (CSS)
# # -----------------------------------------
# st.markdown("""
# <style>
#     /* 1. Main Background - Light Gray for Contrast */
#     .stApp {
#         background-color: #F1F5F9; /* Slate-100 */
#     }

#     /* 2. Remove default top padding */
#     .block-container {
#         padding-top: 1.5rem;
#         padding-bottom: 3rem;
#     }

#     /* 3. Card Styling (The White Boxes) */
#     [data-testid="stVerticalBlockBorderWrapper"] {
#         background-color: #FFFFFF;
#         border-radius: 12px;
#         padding: 20px;
#         border: 1px solid #E2E8F0; /* Slate-200 */
#         box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
#         margin-bottom: 1rem;
#     }

#     /* 4. Input Fields - Force White Background & Dark Text */
#     input[type="text"], input[type="number"], .stDateInput input, .stSelectbox div[data-baseweb="select"] {
#         background-color: #FFFFFF !important;
#         color: #1E293B !important; /* Dark Slate Text */
#         border: 1px solid #CBD5E1 !important;
#         border-radius: 6px !important;
#     }
    
#     /* Input Focus State */
#     input:focus, .stSelectbox div[data-baseweb="select"]:focus-within {
#         border-color: #3B82F6 !important; /* Blue border on focus */
#         box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important;
#     }

#     /* 5. Labels - Bold and Dark */
#     label p {
#         font-weight: 600 !important;
#         font-size: 0.9rem !important;
#         color: #475569 !important; /* Slate-600 */
#     }
    
#     /* 6. Headers */
#     h1, h2, h3 {
#         color: #0F172A; /* Slate-900 */
#         font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#     }
    
#     .section-title {
#         color: #334155;
#         font-size: 1.1rem;
#         font-weight: 700;
#         margin-bottom: 5px;
#         display: flex;
#         align-items: center;
#         gap: 8px;
#     }
    
#     .section-divider {
#         height: 2px;
#         background-color: #F1F5F9;
#         margin-bottom: 20px;
#         margin-top: 5px;
#     }

#     /* 7. Buttons */
#     .stButton > button {
#         border-radius: 6px;
#         font-weight: 600;
#         border: none;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#         transition: all 0.2s;
#     }
    
#     /* Primary Button override */
#     button[kind="primary"] {
#         background-color: #2563EB; /* Royal Blue */
#     }
#     button[kind="primary"]:hover {
#         background-color: #1D4ED8;
#     }

# </style>
# """, unsafe_allow_html=True)


# # -----------------------------------------
# # Snowflake Session
# # -----------------------------------------
# try:
#     cnx = st.connection("snowflake")
#     session = cnx.session()
# except Exception as e:
#     # Fallback for UI testing if Snowflake isn't connected
#     st.warning("⚠️ Snowflake connection not active. UI loaded in offline mode.")

# # -----------------------------------------
# # Session State Initialization (UNCHANGED)
# # -----------------------------------------
# for key in ["edit_mode", "record", "pending_data", "pending_action", "last_emp_id", "save_completed", "autofill_emp_name"]:
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
#     # Wrapped in try/except for offline UI safety
#     try:
#         df = session.sql(f"""SELECT DISTINCT "EMP Name" FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION WHERE "EMP ID" = '{emp_id}'""").to_pandas()
#         if not df.empty:
#             if df.iloc[0]["EMP Name"].lower() != emp_name.lower():
#                 st.error("❌ EMP ID exists with different name.")
#                 return False
#     except:
#         pass
#     return True

# def autofill_employee_name(emp_id):
#     if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
#         return ""
#     try:
#         df = session.sql(f"""SELECT DISTINCT "EMP Name" FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION WHERE "EMP ID" = '{emp_id}'""").to_pandas()
#         return df.iloc[0]["EMP Name"] if not df.empty else ""
#     except:
#         return ""

# # -----------------------------------------
# # Sidebar
# # -----------------------------------------
# with st.sidebar:
#     st.markdown("### 🔍 Search Employee")
#     st.info("Enter details below to search existing records.")
    
#     emp_id = st.text_input("Employee ID (10 Digits)", placeholder="e.g. 1234567890")
    
#     certifications = (
#         "Advanced Analyst", "Advanced Architect", "Advanced Data Engineer",
#         "Core", "Associate", "Speciality Gen AI", "Speciality Native App",
#         "Advanced Data Scientist", "Speciality Snowpark"
#     )
#     certification = st.selectbox("Certification Track", certifications)
    
#     st.write("")
#     if st.button("Search Database", type="primary", use_container_width=True):
#         if not emp_id or not emp_id.isdigit() or len(emp_id) != 10:
#             st.error("Invalid Employee ID")
#         else:
#             try:
#                 result = session.sql(f"""
#                     SELECT * FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION 
#                     WHERE "EMP ID" = '{emp_id}' AND "Certification" = '{certification}'
#                 """).to_pandas()

#                 if result.empty:
#                     st.session_state.edit_mode = False
#                     st.session_state.record = {}
#                     st.toast("No record found. Ready to create.", icon="🆕")
#                 else:
#                     st.session_state.edit_mode = True
#                     st.session_state.record = result.iloc[0].to_dict()
#                     st.toast("Record loaded.", icon="✅")
#             except:
#                 st.error("DB Connection Error")

# # Reset Logic
# if st.session_state.last_emp_id != emp_id:
#     st.session_state.record = {}
#     st.session_state.edit_mode = False
#     st.session_state.pending_data = None
#     st.session_state.autofill_emp_name = autofill_employee_name(emp_id)
#     st.session_state.last_emp_id = emp_id

# # -----------------------------------------
# # Main Page Layout
# # -----------------------------------------
# st.title("🎓 Certification Manager")
# st.markdown("Use this portal to track, update, and manage employee certification lifecycles.")
# st.write("") # Spacer

# # --- CARD 1: Employee Details ---
# with st.container(border=True):
#     st.markdown('<div class="section-title">👤 Employee Information</div><div class="section-divider"></div>', unsafe_allow_html=True)
    
#     c1, c2, c3 = st.columns([1, 2, 2])
#     with c1:
#         emp_id = st.text_input("Employee ID", value=emp_id, disabled=True if st.session_state.edit_mode else False)
#     with c2:
#         emp_name = st.text_input("Employee Name", value=(st.session_state.record.get("EMP Name") or st.session_state.autofill_emp_name or ""))
#     with c3:
#         certification = st.selectbox("Certification", certifications, index=certifications.index(certification) if certification in certifications else 0, disabled=True)

# # --- CARD 2: Timeline & Status ---
# with st.container(border=True):
#     st.markdown('<div class="section-title">📅 Timeline & Exam Status</div><div class="section-divider"></div>', unsafe_allow_html=True)
    
#     r1_c1, r1_c2, r1_c3 = st.columns([1.5, 1.5, 2])
    
#     with r1_c1:
#         st.markdown("**Enrolment**")
#         ec1, ec2 = st.columns(2)
#         month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
#         year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]
        
#         with ec1: enrol_month = st.selectbox("Month", month_opts)
#         with ec2: enrol_year = st.selectbox("Year", year_opts)
        
#     with r1_c2:
#         st.markdown("**Planning**")
#         planned_date = st.date_input("Planned Exam Date", date.today())
        
#     with r1_c3:
#         st.markdown("**Outcome**")
#         # Using a toggle for cleaner UI
#         completed = st.toggle("Certification Completed?", value=False)
        
#     st.markdown("---") # Subtle separator inside card
    
#     r2_c1, r2_c2, r2_c3 = st.columns(3)
    
#     with r2_c1:
#         if completed:
#             actual_date = st.date_input("Actual Completion Date", max_value=date.today())
#         else:
#             st.markdown("*(Mark completed to enable date)*")
#             actual_date = None

#     with r2_c2:
#         snowpro = st.selectbox("SnowPro Status", ("Completed","Failed") if completed else ("Incomplete",))

#     with r2_c3:
#         voucher_status = st.selectbox("Voucher Status", ("Voucher Received","Voucher Applied","Own Payment"))

# # --- CARD 3: Progress Tracker ---
# with st.container(border=True):
#     st.markdown('<div class="section-title">📊 Badge Progress</div><div class="section-divider"></div>', unsafe_allow_html=True)
    
#     badge_opts = ("Completed", "In-Progress")
    
#     # Using columns for a dashboard grid look
#     b1, b2, b3, b4, b5 = st.columns(5)
#     badge1 = b1.selectbox("Badge 1", badge_opts)
#     badge2 = b2.selectbox("Badge 2", badge_opts)
#     badge3 = b3.selectbox("Badge 3", badge_opts)
#     badge4 = b4.selectbox("Badge 4", badge_opts)
#     badge5 = b5.selectbox("Badge 5", badge_opts)
    
#     st.markdown("")
#     st.markdown("**Additional Coursework**")
#     p1, p2, p3 = st.columns(3)
#     cert_prep = p1.selectbox("CertPrepOD Course", badge_opts)
#     level_up = p2.selectbox("Level Up Courses", ("Completed","Not Started"))
#     trial_exam = p3.selectbox("Trial Exams", ("Completed","Not Started"))

# # --- CARD 4: Organizational Data ---
# with st.container(border=True):
#     st.markdown('<div class="section-title">🏢 Organizational Details</div><div class="section-divider"></div>', unsafe_allow_html=True)
    
#     o1, o2, o3, o4 = st.columns(4)
#     account = o1.text_input("Account Name")
#     account_spoc = o2.text_input("Account SPOC")
#     vertical = o3.text_input("Vertical / SL")
#     batch = o4.text_input("Batch ID")
    
#     st.write("")
#     comment = st.text_area("Manager Comments", height=80, placeholder="Enter any specific notes regarding this certification...")

# # -----------------------------------------
# # Logic: Payload & Actions (UNCHANGED)
# # -----------------------------------------
# def prepare_payload():
#     return {
#         "EMP ID": emp_id, "EMP Name": emp_name, "Enrolment Month": f"{enrol_month}-{enrol_year}",
#         "Certification": certification, "Badge 1 Status": badge1, "Badge 2 Status": badge2,
#         "Badge 3 Status": badge3, "Badge 4 Status": badge4, "Badge 5 Status": badge5,
#         "CertPrepOD Course": cert_prep, "Level Up Courses": level_up, "# Trial Exams": trial_exam,
#         "Account": account, "Account SPOC": account_spoc, "Vertical / SL": vertical, "Batch": batch,
#         "Planned Certification date": cert_date_to_str(planned_date),
#         "Actual Date of completion": cert_date_to_str(actual_date),
#         "Voucher Status": voucher_status, "SnowPro Certified": snowpro, "Comment": comment
#     }

# # Action Bar - Fixed at bottom or just cleanly separated
# st.write("")
# ac1, ac2, ac3 = st.columns([1, 1, 4])

# with ac1:
#     if st.session_state.edit_mode:
#         if st.button("💾 Update Record", type="primary", use_container_width=True):
#             if validate_mandatory_fields(emp_id, emp_name):
#                 st.session_state.pending_data = prepare_payload()
#                 st.session_state.pending_action = "update"
#                 st.session_state.save_completed = False
#     else:
#         if st.button("➕ Create New", type="primary", use_container_width=True):
#             if validate_mandatory_fields(emp_id, emp_name) and validate_emp_name_consistency(emp_id, emp_name):
#                 st.session_state.pending_data = prepare_payload()
#                 st.session_state.pending_action = "insert"
#                 st.session_state.save_completed = False

# with ac2:
#     if st.button("❌ Cancel", use_container_width=True):
#         st.session_state.pending_data = None
#         st.session_state.pending_action = None
#         st.session_state.save_completed = None
#         st.rerun()

# with ac3:
#     if st.session_state.edit_mode:
#         with st.popover("🗑 Delete Record"):
#             st.write("Are you sure?")
#             if st.button("Confirm Delete", type="primary"):
#                 try:
#                     session.sql(f"""DELETE FROM USE_CASE.CERTIFICATION.NEW_CERTIFICATION WHERE "EMP ID" = '{emp_id}' AND "Certification" = '{certification}'""").collect()
#                     st.success("Deleted")
#                     st.session_state.edit_mode = False
#                     st.session_state.record = {}
#                     st.rerun()
#                 except:
#                     st.error("Delete failed")

# # Save Confirmation
# if st.session_state.pending_data:
#     st.divider()
#     st.info("Review Data Summary")
#     st.dataframe(pd.DataFrame([st.session_state.pending_data]), hide_index=True)
    
#     if st.button("✅ Confirm Save to Database", disabled=st.session_state.save_completed, type="primary"):
#         try:
#             if st.session_state.pending_action == "insert":
#                 session.create_dataframe([Row(**st.session_state.pending_data)]).write.mode("append").save_as_table("USE_CASE.CERTIFICATION.NEW_CERTIFICATION")
#             else:
#                 updates = [f'"{k}" = \'{v}\'' if v else f'"{k}" = NULL' for k, v in st.session_state.pending_data.items() if k not in ["EMP ID", "Certification"]]
#                 session.sql(f"""UPDATE USE_CASE.CERTIFICATION.NEW_CERTIFICATION SET {", ".join(updates)} WHERE "EMP ID" = '{emp_id}' AND "Certification" = '{certification}'""").collect()
#             st.success("Saved Successfully!")
#             st.session_state.save_completed = True
#         except Exception as e:
#             st.error(f"Error: {e}")

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

# -----------------------------------------
# Enhanced Professional UI Theme (CSS)
# -----------------------------------------
st.markdown("""
<style>
/* 1. Page Background - Clean Light Grey */
.stApp {
    background-color: #F1F5F9;
    font-family: 'Inter', sans-serif;
}

/* 2. Containers (Cards) - White background with shadow */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid #E2E8F0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    margin-bottom: 1rem;
}

/* 3. Input Fields - FORCE White Background & Dark Text */
input, select, textarea {
    background-color: #FFFFFF !important;
    color: #0F172A !important; /* Dark text */
    border: 1px solid #CBD5E1 !important;
}

/* Fix for Streamlit's specific widget structures to ensure visibility */
.stTextInput > div > div > input {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
}
.stSelectbox > div > div > div {
    background-color: #FFFFFF !important;
    color: #0F172A !important;
}
.stDateInput > div > div > input {
    color: #0F172A !important;
}

/* 4. Headings */
h1, h2, h3 {
    color: #1E293B;
    font-weight: 700;
}

/* 5. Custom Dividers for Sections */
.section-header {
    color: #334155;
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    border-bottom: 2px solid #F1F5F9;
    padding-bottom: 5px;
}

/* 6. Buttons */
.stButton > button {
    border-radius: 6px;
    font-weight: 600;
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
st.title("🎓 Certification Tracker")
st.markdown("---")

# -----------------------------------------
# Employee + Certification (UI IMPROVED - LOGIC KEPT)
# -----------------------------------------
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
# Enrolment & Planning (UI IMPROVED - LOGIC KEPT)
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🗓️ Schedule & Status</div>', unsafe_allow_html=True)
    m1, m2 = st.columns(2)

    with m1:
        c_sub1, c_sub2 = st.columns(2)
        month_opts = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        year_opts = [str(y) for y in range(date.today().year - 5, date.today().year + 5)]
        
        with c_sub1:
            enrol_month = st.selectbox("Enrolment Month", month_opts)
        with c_sub2:
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

# -----------------------------------------
# Badge Progress (UI IMPROVED - LOGIC KEPT)
# -----------------------------------------
with st.container(border=True):
    st.markdown('<div class="section-header">🏅 Badges & Progress</div>', unsafe_allow_html=True)
    
    badge_opts = ("Completed","In-Progress")
    b_col1, b_col2, b_col3, b_col4, b_col5 = st.columns(5) # 5 columns for badges looks cleaner

    badge1 = b_col1.selectbox("Badge 1", badge_opts)
    badge2 = b_col2.selectbox("Badge 2", badge_opts)
    badge3 = b_col3.selectbox("Badge 3", badge_opts)
    badge4 = b_col4.selectbox("Badge 4", badge_opts)
    badge5 = b_col5.selectbox("Badge 5", badge_opts)

    st.divider()
    
    c_prep1, c_prep2, c_prep3 = st.columns(3)
    cert_prep = c_prep1.selectbox("CertPrepOD", badge_opts)
    level_up = c_prep2.selectbox("Level Up Courses", ("Completed","Not Started"))
    trial_exam = c_prep3.selectbox("Trial Exams", ("Completed","Not Started"))

# -----------------------------------------
# Courses & Organization (UI IMPROVED - LOGIC KEPT)
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
# Action Bar (ORIGINAL LOGIC RESTORED)
# -----------------------------------------
st.write("")
st.write("")
a1, a2, a3 = st.columns([3,1,1])

with a1:
    # Logic: Show Update ONLY if edit_mode is True, else Show Add New
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
        # Using a popover for safety, but keeping your delete logic
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
# Confirm & Save (UNCHANGED – THIS IS KEY)
# -----------------------------------------
if st.session_state.pending_data:
    st.divider()
    # Encapsulate the review section in a nice container
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
