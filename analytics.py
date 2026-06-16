import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame()

def show_analytics():
    st.title("Fitness Analytics")
    st.markdown("Visual analysis of user fitness data")
    
    users = load_users()
    
    if users.empty:
        st.info("No data available. Add users first.")
        return
    
    users["bmi"] = users["weight"] / ((users["height"] / 100) ** 2)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("BMI Distribution")
        fig, ax = plt.subplots()
        ax.hist(users["bmi"], bins=10, color="blue", edgecolor="black")
        ax.set_xlabel("BMI")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    
    with col2:
        st.subheader("Goal Distribution")
        goal_counts = users["goal"].value_counts()
        fig, ax = plt.subplots()
        ax.pie(goal_counts.values, labels=goal_counts.index, autopct="%1.1f%%")
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Gender Distribution")
        gender_counts = users["gender"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(gender_counts.index, gender_counts.values, color=["blue", "pink", "gray"])
        st.pyplot(fig)
    
    with col2:
        st.subheader("Weight Distribution")
        fig, ax = plt.subplots()
        ax.hist(users["weight"], bins=10, color="green", edgecolor="black")
        ax.set_xlabel("Weight (kg)")
        ax.set_ylabel("Count")
        st.pyplot(fig)
    
    st.subheader("Height Distribution")
    fig, ax = plt.subplots()
    ax.plot(users.index, users["height"].sort_values(), marker="o", linestyle="-", color="red")
    ax.set_xlabel("User")
    ax.set_ylabel("Height (cm)")
    st.pyplot(fig)
