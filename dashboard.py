import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame()

def show_dashboard():
    st.title("Dashboard")
    st.markdown("Fitness Tracking Overview")
    
    users = load_users()
    
    if users.empty:
        st.info("No user data yet. Add users in User Entry module.")
        return
    
    # Calculate KPIs
    total_users = len(users)
    male_count = len(users[users["gender"].str.lower() == "male"])
    female_count = len(users[users["gender"].str.lower() == "female"])
    weight_loss = len(users[users["goal"].str.lower() == "weight loss"])
    weight_gain = len(users[users["goal"].str.lower() == "weight gain"])
    lean_muscle = len(users[users["goal"].str.lower() == "lean muscle gain"])
    
    users["bmi"] = users["weight"] / ((users["height"] / 100) ** 2)
    avg_bmi = users["bmi"].mean()
    avg_weight = users["weight"].mean()
    avg_height = users["height"].mean()
    
    # Display KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Users", total_users)
    col2.metric("Male Users", male_count)
    col3.metric("Female Users", female_count)
    col4.metric("Average BMI", f"{avg_bmi:.1f}")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Weight Loss", weight_loss)
    col2.metric("Weight Gain", weight_gain)
    col3.metric("Lean Muscle", lean_muscle)
    col4.metric("Avg Weight", f"{avg_weight:.1f} kg")
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Goal Distribution")
        goal_dist = users["goal"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(goal_dist.values, labels=goal_dist.index, autopct="%1.1f%%", startangle=90)
        st.pyplot(fig)
    
    with col2:
        st.subheader("Gender Distribution")
        gender_dist = users["gender"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(gender_dist.index, gender_dist.values, color=["blue", "pink"])
        st.pyplot(fig)
