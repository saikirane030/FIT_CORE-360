import streamlit as st
from dashboard import show_dashboard
from user_entry import show_user_entry
from csv_manager import show_csv_manager
from bmi_calculator import show_bmi_calculator
from calorie_recommendation import show_calorie_recommendation
from nutrition_tracker import show_nutrition_tracker
from analytics import show_analytics
from gym_map import show_gym_map
from report_generator import show_report_generator

st.set_page_config(page_title="FitCore360", page_icon="💪", layout="wide")
st.title("FitCore360 - Fitness Tracking Application")
st.sidebar.title("Navigation")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("Dashboard", use_container_width=True):
        st.session_state.menu = "Dashboard"
    if st.button("User Entry", use_container_width=True):
        st.session_state.menu = "User Entry"
    if st.button("CSV Upload", use_container_width=True):
        st.session_state.menu = "CSV Manager"
    if st.button("BMI Calc", use_container_width=True):
        st.session_state.menu = "BMI Calculator"

with col2:
    if st.button("Calories", use_container_width=True):
        st.session_state.menu = "Calorie Recommendation"
    if st.button("Nutrition", use_container_width=True):
        st.session_state.menu = "Nutrition Tracker"
    if st.button("Analytics", use_container_width=True):
        st.session_state.menu = "Analytics"
    if st.button("Gym Map", use_container_width=True):
        st.session_state.menu = "Gym Map"

st.sidebar.markdown("---")
if st.sidebar.button("Reports", use_container_width=True):
    st.session_state.menu = "Reports"

menu = st.session_state.get("menu", "Dashboard")

if menu == "Dashboard":
    show_dashboard()
elif menu == "User Entry":
    show_user_entry()
elif menu == "CSV Manager":
    show_csv_manager()
elif menu == "BMI Calculator":
    show_bmi_calculator()
elif menu == "Calorie Recommendation":
    show_calorie_recommendation()
elif menu == "Nutrition Tracker":
    show_nutrition_tracker()
elif menu == "Analytics":
    show_analytics()
elif menu == "Gym Map":
    show_gym_map()
elif menu == "Reports":
    show_report_generator()
