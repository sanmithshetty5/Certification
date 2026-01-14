import streamlit as st

st.set_page_config(
    page_title="Certification Management System",
    layout="wide"
)

st.sidebar.title("🎓 Certification Portal")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Welcome",
        "✍️ Certification Tracker",
        "📊 Certification Analytics"
    ]
)

if page == "🏠 Welcome":
    st.switch_page("pages/Welcome_Page.py")

elif page == "✍️ Certification Tracker":
    st.switch_page("pages/Data_Entry.py")

elif page == "📊 Certification Analytics":
    st.switch_page("pages/2_Realtime_Analysis.py")
