import streamlit as st
import pandas as pd
import os

def get_base_calories(bmi_category):
    base_calories = {
        "Underweight": 2500,
        "Normal": 2200,
        "Overweight": 1800,
        "Obese": 1500
    }
    return base_calories.get(bmi_category, 2200)

def get_goal_adjustment(goal):
    adjustments = {
        "Weight Loss": -300,
        "Weight Gain": 300,
        "Lean Muscle Gain": 500
    }
    return adjustments.get(goal, 0)

def calculate_recommended_calories(bmi_category, goal):
    base = get_base_calories(bmi_category)
    adjustment = get_goal_adjustment(goal)
    return base + adjustment

def show_calorie_recommendation():
    st.title("Calorie Recommendation System")
    st.markdown("Get personalized daily calorie recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    with col2:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    
    goal = st.selectbox("Fitness Goal", ["Weight Loss", "Weight Gain", "Lean Muscle Gain"])
    
    if st.button("Get Recommendation"):
        bmi = weight / ((height / 100) ** 2)
        
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        
        recommended = calculate_recommended_calories(category, goal)
        
        st.metric("BMI Category", category)
        st.metric("Recommended Daily Calories", f"{recommended} kcal")
        
        col1, col2, col3 = st.columns(3)
        col1.write(f"**Base:** 2200 kcal")
        col2.write(f"**Goal Adjustment:** {get_goal_adjustment(goal):+d} kcal")
        col3.write(f"**Total:** {recommended} kcal")
        
        st.divider()
        st.subheader("Base Calorie by BMI Category")
        df = pd.DataFrame({
            "Category": ["Underweight", "Normal", "Overweight", "Obese"],
            "Base Calories": [2500, 2200, 1800, 1500]
        })
        st.table(df)
