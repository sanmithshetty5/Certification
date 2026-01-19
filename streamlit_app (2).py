# # import streamlit as st

# # st.set_page_config(
# #     page_title="Welcome | Employee Certification Portal",
# #     layout="wide",
# #     initial_sidebar_state="collapsed"
# # )


# # # -------------------------------
# # # GLOBAL CSS – Enterprise UI
# # # -------------------------------
# # st.markdown("""
# # <style>
# # .stApp {
# #     background-color: #f8fafc;
# #     color: #0f172a;
# #     font-family: Inter, sans-serif;
# # }

# # /* -------------------------
# #    UPDATED: Logo Header Container
# #    ------------------------- */
# # .logo-container {
# #     background-color: #ffffff;
# #     border: 1px solid #e2e8f0;
# #     border-radius: 10px;
# #     /* Height constrained to approx 2cm */
# #     height: 2cm; 
# #     display: flex;
# #     align-items: center; /* Vertically center the logos */
# #     padding-left: 20px;
# #     padding-right: 20px;
# #     gap: 20px;
# #     margin-bottom: 2rem;
# #     box-shadow: 0px 4px 6px rgba(0,0,0,0.02);
# #     overflow: hidden; /* Ensures nothing spills out */
# # }

# # /* STRICTLY FORCE IMAGE SIZES */
# # .logo-container img {
# #     height: 2cm !important; /* Force scale down to 1.5cm */
# #     width: auto !important;   /* Maintain aspect ratio */
# #     object-fit: contain !important;
# #     margin-bottom: 0 !important;
# # }

# # /* Header */
# # .welcome-title {
# #     font-size: 2.4rem;
# #     font-weight: 800;
# #     margin-bottom: 0.6rem;
# # }
# # .subtitle {
# #     color: #64748b;
# #     font-size: 1.05rem;
# #     max-width: 980px;
# #     line-height: 1.6;
# #     margin-bottom: 3rem;
# # }

# # /* Section title */
# # .section-title {
# #     font-size: 0.7rem;
# #     font-weight: 700;
# #     letter-spacing: 0.25em;
# #     color: #94a3b8;
# #     text-transform: uppercase;
# #     margin-bottom: 2rem;
# # }

# # /* Cards */
# # .card {
# #     background: #ffffff;
# #     border-radius: 14px;
# #     padding: 2rem;
# #     border: 1px solid #e2e8f0;
# #     height: 320px;
# #     display: flex;
# #     flex-direction: column;
# #     justify-content: space-between;
# #     transition: all 0.25s ease-in-out;
# # }

# # .card:hover {
# #     transform: translateY(-3px);
# #     box-shadow: 0px 14px 28px rgba(15,23,42,0.08);
# # }

# # .card h3 {
# #     font-size: 1.2rem;
# #     font-weight: 700;
# #     margin-bottom: 0.8rem;
# # }

# # .card p {
# #     font-size: 0.95rem;
# #     color: #64748b;
# #     line-height: 1.6;
# # }

# # /* Badge */
# # .badge {
# #     display: inline-block;
# #     font-size: 0.65rem;
# #     font-weight: 700;
# #     letter-spacing: 0.1em;
# #     padding: 0.3rem 0.65rem;
# #     border-radius: 999px;
# #     background: #e0f2fe;
# #     color: #0369a1;
# #     margin-bottom: 1.4rem;
# #     text-transform: uppercase;
# # }

# # /* -------------------------------
# #    GLOBAL BUTTON OVERRIDE
# # --------------------------------*/
# # div.stButton > button {
# #     background-color: #030712 !important;
# #     color: #ffffff !important;
# #     border: 2px solid #030712 !important;
# #     border-radius: 10px !important;
# #     font-weight: 700 !important;
# #     padding: 0.75rem 1rem !important;
# #     transition: all 0.25s ease-in-out !important;
# # }

# # div.stButton > button:hover {
# #     background-color: #ffffff !important;
# #     color: #030712 !important;
# # }

# # div.stButton > button:focus,
# # div.stButton > button:active {
# #     background-color: #ffffff !important;
# #     color: #030712 !important;
# #     outline: none !important;
# #     box-shadow: none !important;
# # }

# # div.stButton > button:disabled {
# #     background-color: #f1f5f9 !important;
# #     color: #94a3b8 !important;
# #     border: 2px solid #e2e8f0 !important;
# #     cursor: not-allowed !important;
# # }

# # /* Row spacing */
# # .row-spacing {
# #     margin-top: 3rem;
# # }

# # /* Footer */
# # .footer-tip {
# #     margin-top: 4rem;
# #     padding-top: 1.5rem;
# #     border-top: 1px solid #e2e8f0;
# #     color: #64748b;
# #     font-size: 0.85rem;
# #     display: flex;
# #     justify-content: space-between;
# #     align-items: center;
# # }
# # </style>
# # """, unsafe_allow_html=True)


# # # -------------------------------
# # # HEADER LOGOS (UPDATED)
# # # -------------------------------
# # # Ensure your image URLs are correct. 
# # # The CSS above will force them to fit within the 2cm height.
# # st.markdown("""
# # <div class="logo-container">
# #     <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png">
# #     <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png">
# # </div>
# # """, unsafe_allow_html=True)


# # # -------------------------------
# # # PAGE TITLE / WELCOME
# # # -------------------------------
# # st.markdown("""
# # <div>
# #     <div class="welcome-title">
# #         Welcome to the Employee Certification Portal 👋
# #     </div>
# #     <div class="subtitle">
# #         This portal helps to track employee certifications, ensure compliance,
# #         monitor readiness, and gain actionable insights across teams and departments.
# #     </div>
# # </div>
# # """, unsafe_allow_html=True)

# # # -------------------------------
# # # TRY THINGS OUT
# # # -------------------------------
# # st.markdown('<div class="section-title">Try things out</div>', unsafe_allow_html=True)

# # # -------- ROW 1 --------
# # r1c1, r1c2 = st.columns(2, gap="large")

# # with r1c1:
# #     st.markdown("""
# #     <div class="card">
# #         <div>
# #             <div class="badge">Getting Started</div>
# #             <h3>Add / Update Certification</h3>
# #             <p>
# #                 Add new employees or update certification details including exams,
# #                 badges, issue dates, and completion status.
# #             </p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     if st.button(
# #     "Open Certification Tracker",
# #     key="btn_open_tracker",
# #     use_container_width=True):
# #         st.switch_page("pages/Data_Entry.py")



# # with r1c2:
# #     st.markdown("""
# #     <div class="card">
# #         <div>
# #             <div class="badge">Insights</div>
# #             <h3>View Analytics Dashboard</h3>
# #             <p>
# #                 Monitor certification KPIs, expiring certifications,
# #                 and team-level readiness in real time.
# #             </p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     if st.button(
# #     "Open Certification Tracker",
# #     key="btn_open_ana;lytics",
# #     use_container_width=True):
# #         st.switch_page("pages/2_Realtime_Analysis.py")


# # # -------- ROW 2 --------
# # st.markdown('<div class="row-spacing"></div>', unsafe_allow_html=True)

# # r2c1, r2c2 = st.columns(2, gap="large")

# # with r2c1:
# #     st.markdown("""
# #     <div class="card">
# #         <div>
# #             <div class="badge">AI Powered</div>
# #             <h3>AI Insight</h3>
# #             <p>
# #                 Identify certification gaps, predict risk areas,
# #                 and receive AI-driven recommendations for action.
# #             </p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     st.button(
# #     "Explore AI Insights 🔒",
# #     key="btn_ai_insight",
# #     disabled=True,
# #     use_container_width=True)
    
# # with r2c2:
# #     st.markdown("""
# #     <div class="card">
# #         <div>
# #             <div class="badge">Help</div>
# #             <h3>How It Works</h3>
# #             <p>
# #                 Learn the simple 3-step workflow to manage employee
# #                 certifications confidently across the organization.
# #             </p>
# #         </div>
# #     </div>
# #     """, unsafe_allow_html=True)
# #     st.button(
# #     "View Help Guide",
# #     key="btn_help",
# #     disabled=True,
# #     use_container_width=True)
    

# # # -------------------------------
# # # FOOTER
# # # -------------------------------
# # st.markdown("""
# # <div class="footer-tip">
# #     <div>💡 Tip: Use the left sidebar to navigate between sections anytime.</div>
# #     <div>Hexaware © 2024 • Snowflake</div>
# # </div>
# # """, unsafe_allow_html=True)


# import streamlit as st

# st.set_page_config(
#     page_title="Welcome | Employee Certification Portal",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )


# # -------------------------------
# # GLOBAL CSS – Enterprise UI
# # -------------------------------
# st.markdown("""
# <style>
# .stApp {
#     background-color: #f8fafc;
#     color: #0f172a;
#     font-family: Inter, sans-serif;
# }

# /* -------------------------
#    UPDATED: Logo Header Container
#    ------------------------- */
# .logo-container {
#     background-color: #ffffff;
#     border: 1px solid #e2e8f0;
#     border-radius: 10px;
#     height: 2cm; 
#     display: flex;
#     align-items: center; 
    
#     /* CHANGE HERE: This pushes the logos to the far left and right edges */
#     justify-content: space-between; 
    
#     padding-left: 20px;
#     padding-right: 20px;
#     margin-bottom: 2rem;
#     box-shadow: 0px 4px 6px rgba(0,0,0,0.02);
#     overflow: hidden; 
# }

# /* STRICTLY FORCE IMAGE SIZES */
# .logo-container img {
#     height: 2cm !important; /* Adjusted to 1.5cm to fit comfortably inside the 2cm container */
#     width: auto !important;   
#     object-fit: contain !important;
#     margin-bottom: 0 !important;
# }

# /* Header */
# .welcome-title {
#     font-size: 2.4rem;
#     font-weight: 800;
#     margin-bottom: 0.6rem;
# }
# .subtitle {
#     color: #64748b;
#     font-size: 1.05rem;
#     max-width: 980px;
#     line-height: 1.6;
#     margin-bottom: 3rem;
# }

# /* Section title */
# .section-title {
#     font-size: 0.7rem;
#     font-weight: 700;
#     letter-spacing: 0.25em;
#     color: #94a3b8;
#     text-transform: uppercase;
#     margin-bottom: 2rem;
# }

# /* Cards */
# .card {
#     background: #ffffff;
#     border-radius: 14px;
#     padding: 2rem;
#     border: 1px solid #e2e8f0;
#     height: 320px;
#     display: flex;
#     flex-direction: column;
#     justify-content: space-between;
#     transition: all 0.25s ease-in-out;
# }

# .card:hover {
#     transform: translateY(-3px);
#     box-shadow: 0px 14px 28px rgba(15,23,42,0.08);
# }

# .card h3 {
#     font-size: 1.2rem;
#     font-weight: 700;
#     margin-bottom: 0.8rem;
# }

# .card p {
#     font-size: 0.95rem;
#     color: #64748b;
#     line-height: 1.6;
# }

# /* Badge */
# .badge {
#     display: inline-block;
#     font-size: 0.65rem;
#     font-weight: 700;
#     letter-spacing: 0.1em;
#     padding: 0.3rem 0.65rem;
#     border-radius: 999px;
#     background: #e0f2fe;
#     color: #0369a1;
#     margin-bottom: 1.4rem;
#     text-transform: uppercase;
# }

# /* -------------------------------
#    GLOBAL BUTTON OVERRIDE
# --------------------------------*/
# div.stButton > button {
#     background-color: #030712 !important;
#     color: #ffffff !important;
#     border: 2px solid #030712 !important;
#     border-radius: 10px !important;
#     font-weight: 700 !important;
#     padding: 0.75rem 1rem !important;
#     transition: all 0.25s ease-in-out !important;
# }

# div.stButton > button:hover {
#     background-color: #ffffff !important;
#     color: #030712 !important;
# }

# div.stButton > button:focus,
# div.stButton > button:active {
#     background-color: #ffffff !important;
#     color: #030712 !important;
#     outline: none !important;
#     box-shadow: none !important;
# }

# div.stButton > button:disabled {
#     background-color: #f1f5f9 !important;
#     color: #94a3b8 !important;
#     border: 2px solid #e2e8f0 !important;
#     cursor: not-allowed !important;
# }

# /* Row spacing */
# .row-spacing {
#     margin-top: 3rem;
# }

# /* Footer */
# .footer-tip {
#     margin-top: 4rem;
#     padding-top: 1.5rem;
#     border-top: 1px solid #e2e8f0;
#     color: #64748b;
#     font-size: 0.85rem;
#     display: flex;
#     justify-content: space-between;
#     align-items: center;
# }
# </style>
# """, unsafe_allow_html=True)


# # -------------------------------
# # HEADER LOGOS (UPDATED)
# # -------------------------------
# st.markdown("""
# <div class="logo-container">
#     <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png" alt="Snowflake">
#     <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png" alt="Hexaware">
# </div>
# """, unsafe_allow_html=True)


# # -------------------------------
# # PAGE TITLE / WELCOME
# # -------------------------------
# st.markdown("""
# <div>
#     <div class="welcome-title">
#         Welcome to the Employee Certification Portal 👋
#     </div>
#     <div class="subtitle">
#         This portal helps to track employee certifications, ensure compliance,
#         monitor readiness, and gain actionable insights across teams and departments.
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # -------------------------------
# # TRY THINGS OUT
# # -------------------------------
# st.markdown('<div class="section-title">Try things out</div>', unsafe_allow_html=True)

# # -------- ROW 1 --------
# r1c1, r1c2 = st.columns(2, gap="large")

# with r1c1:
#     st.markdown("""
#     <div class="card">
#         <div>
#             <div class="badge">Getting Started</div>
#             <h3>Add / Update Certification</h3>
#             <p>
#                 Add new employees or update certification details including exams,
#                 badges, issue dates, and completion status.
#             </p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     if st.button(
#     "Open Certification Tracker",
#     key="btn_open_tracker",
#     use_container_width=True):
#         st.switch_page("pages/Data_Entry.py")



# with r1c2:
#     st.markdown("""
#     <div class="card">
#         <div>
#             <div class="badge">Insights</div>
#             <h3>View Analytics Dashboard</h3>
#             <p>
#                 Monitor certification KPIs, expiring certifications,
#                 and team-level readiness in real time.
#             </p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     if st.button(
#     "Open Certification Tracker",
#     key="btn_open_ana;lytics",
#     use_container_width=True):
#         st.switch_page("pages/2_Realtime_Analysis.py")


# # -------- ROW 2 --------
# st.markdown('<div class="row-spacing"></div>', unsafe_allow_html=True)

# r2c1, r2c2 = st.columns(2, gap="large")

# with r2c1:
#     st.markdown("""
#     <div class="card">
#         <div>
#             <div class="badge">AI Powered</div>
#             <h3>AI Insight</h3>
#             <p>
#                 Identify certification gaps, predict risk areas,
#                 and receive AI-driven recommendations for action.
#             </p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.button(
#     "Explore AI Insights 🔒",
#     key="btn_ai_insight",
#     disabled=True,
#     use_container_width=True)
    
# with r2c2:
#     st.markdown("""
#     <div class="card">
#         <div>
#             <div class="badge">Help</div>
#             <h3>How It Works</h3>
#             <p>
#                 Learn the simple 3-step workflow to manage employee
#                 certifications confidently across the organization.
#             </p>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.button(
#     "View Help Guide",
#     key="btn_help",
#     disabled=True,
#     use_container_width=True)
    

# # -------------------------------
# # FOOTER
# # -------------------------------
# st.markdown("""
# <div class="footer-tip">
#     <div>💡 Tip: Use the left sidebar to navigate between sections anytime.</div>
#     <div>Hexaware © 2024 • Snowflake</div>
# </div>
# """, unsafe_allow_html=True)

import streamlit as st

st.set_page_config(
    page_title="Welcome | Employee Certification Portal",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# -------------------------------
# GLOBAL CSS – Enterprise UI (Improved)
# -------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

.stApp {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: 'Inter', sans-serif;
}

/* --- Header Section --- */
.header-container {
    /* Removed border, made it cleaner */
    background-color: transparent;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
}

/* Force image sizes nicely */
.header-container img {
    height: 50px !important; /* Fixed height for consistency */
    width: auto !important;
    object-fit: contain !important;
}

/* --- Typography --- */
.welcome-title {
    font-size: 2.8rem; /* Slightly larger */
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #1e293b;
    margin-bottom: 0.8rem;
}

.subtitle {
    color: #64748b;
    font-size: 1.1rem;
    max-width: 800px;
    line-height: 1.6;
    margin-bottom: 3rem;
}

.section-title {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    color: #94a3b8;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    margin-top: 2rem;
}

/* --- Metric Container (New) --- */
[data-testid="stMetric"] {
    background-color: #ffffff;
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.01), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
}

[data-testid="stMetricLabel"] {
    font-size: 0.9rem;
    color: #64748b;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    color: #0f172a;
    font-weight: 800;
}

/* --- Cards (Enhanced) --- */
.card {
    background: #ffffff;
    border-radius: 16px; /* Softer corners */
    padding: 2rem;
    border: 1px solid #e2e8f0;
    height: 340px; /* Slightly taller for icons */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 10px 10px -5px rgba(0, 0, 0, 0.02);
    border-color: #cbd5e1;
}

/* Card Header Layout with Icon */
.card-header-row {
    display: flex;
    align-items: flex-start;
    gap: 1rem;
    margin-bottom: 1rem;
}

.card-icon {
    font-size: 2rem;
    padding: 0.5rem;
    background: #f1f5f9;
    border-radius: 10px;
    line-height: 1;
}

.card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    margin-top: 0.2rem;
    color: #1e293b;
}

.card p {
    font-size: 0.95rem;
    color: #64748b;
    line-height: 1.6;
}

/* Badge */
.badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    padding: 0.35rem 0.8rem;
    border-radius: 6px;
    background: #e0f2fe;
    color: #0284c7;
    margin-bottom: 1rem;
    text-transform: uppercase;
}

.badge-blue { background: #e0f2fe; color: #0284c7; }
.badge-purple { background: #f3e8ff; color: #9333ea; }
.badge-green { background: #dcfce7; color: #16a34a; }
.badge-gray { background: #f1f5f9; color: #475569; }


/* --- Buttons --- */
div.stButton > button {
    background-color: #0f172a !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1rem !important;
    transition: all 0.2s ease-in-out !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

div.stButton > button:hover {
    background-color: #1e293b !important;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    transform: translateY(-1px);
}

div.stButton > button:active {
     transform: translateY(0px);
}

div.stButton > button:disabled {
    background-color: #e2e8f0 !important;
    color: #94a3b8 !important;
    box-shadow: none !important;
    cursor: not-allowed !important;
}

/* Row spacing */
.row-spacing {
    margin-top: 3rem;
}

/* Footer */
.footer-tip {
    margin-top: 5rem;
    padding-top: 2rem;
    border-top: 1px solid #e2e8f0;
    color: #94a3b8;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)


# -------------------------------
# HEADER Section (Cleaner layout)
# -------------------------------
st.markdown("""
<div class="header-container">
    <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/snowflake_logo.png" alt="Snowflake">
    <img src="https://raw.githubusercontent.com/sanmithshetty5/Certification/main/pages/logo.png" alt="Hexaware">
</div>
<div class="welcome-title">
    Employee Certification Portal 👋
</div>
<div class="subtitle">
    Your central hub to track certifications, ensure compliance, maintain readiness, and unlock actionable insights across the organization.
</div>
""", unsafe_allow_html=True)


# # -------------------------------
# # NEW: Quick Glance Metrics
# # -------------------------------
# # This adds immediate visual value before the navigation cards.
# st.markdown('<div class="section-title">At a Glance (Dummy Data)</div>', unsafe_allow_html=True)
# m1, m2, m3, m4 = st.columns(4)
# with m1:
#     st.metric(label="Total Certified Employees", value="1,245", delta="12 this month")
# with m2:
#     st.metric(label="Active Certifications", value="3,502")
# with m3:
#     st.metric(label="Expiring (30 Days)", value="45", delta="-5", delta_color="inverse")
# with m4:
#     # A simple visual trick for a compliance score
#     st.metric(label="Overall Compliance Score", value="92%", delta="On Track")


# -------------------------------
# MAIN NAVIGATION CARDS (Enhanced with Icons)
# -------------------------------
st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)

# -------- ROW 1 --------
r1c1, r1c2 = st.columns(2, gap="large")

with r1c1:
    # Added icon and adjusted layout inside the card
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-blue">Manage Data</div>
            <div class="card-header-row">
                <div class="card-icon">📝</div>
                <div>
                    <h3>Add / Update Certification</h3>
                    <p>
                        Maintain accurate records. Add new employees or update details for exams, badges, and completion dates.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    # Using a slightly different button label for clarity
    if st.button("Launch Data Entry Tool", key="btn_open_tracker", use_container_width=True):
        st.switch_page("pages/Data_Entry.py")

with r1c2:
    st.markdown("""
    <div class="card">
        <div>
             <div class="badge badge-purple">Analytics</div>
             <div class="card-header-row">
                <div class="card-icon">📊</div>
                <div>
                    <h3>View Analytics Dashboard</h3>
                    <p>
                        Visualize real-time KPIs. Monitor team readiness, track expiring certificates, and identify trends.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Go to Dashboard", key="btn_open_analytics", use_container_width=True):
        st.switch_page("pages/2_Realtime_Analysis.py")


# -------- ROW 2 --------
st.markdown('<div class="row-spacing"></div>', unsafe_allow_html=True)

r2c1, r2c2 = st.columns(2, gap="large")

with r2c1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-green">Intelligence</div>
            <div class="card-header-row">
                <div class="card-icon">🤖</div>
                <div>
                    <h3>AI-Driven Insights</h3>
                    <p>
                        Leverage AI to identify skill gaps, predict compliance risks, and receive tailored recommendations.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("Explore AI (Coming Soon) 🔒", key="btn_ai_insight", disabled=True, use_container_width=True)

with r2c2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="badge badge-gray">Support</div>
            <div class="card-header-row">
                <div class="card-icon">💡</div>
                <div>
                    <h3>Help & Resources</h3>
                    <p>
                        Learn the workflow. Access guides and documentation on how to manage certifications effectively.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.button("View Documentation", key="btn_help", disabled=True, use_container_width=True)


# -------------------------------
# FOOTER
# -------------------------------
st.markdown("""
<div class="footer-tip">
    <div style="display:flex; align-items:center; gap:0.5rem;">
        <span style="font-size:1.2rem;">←</span> Tip: Use the sidebar menu to navigate between pages.
    </div>
    <div>Hexaware © 2024 • Snowflake Partnership</div>
</div>
""", unsafe_allow_html=True)
