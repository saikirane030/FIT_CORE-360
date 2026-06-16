import streamlit as st
import pandas as pd

def calculate_bmi(height_cm, weight_kg):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def get_health_message(category):
    messages = {
        "Underweight": "You are underweight. Consult a doctor for guidance.",
        "Normal": "Great! You have a healthy weight. Maintain it!",
        "Overweight": "You are overweight. Consider a balanced diet and exercise.",
        "Obese": "You are obese. Consult a healthcare professional immediately."
    }
    return messages.get(category, "")

def show_bmi_calculator():
    st.title("BMI Calculator")
    st.markdown("Calculate your Body Mass Index")
    
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
    with col2:
        weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
    
    if st.button("Calculate BMI"):
        bmi = calculate_bmi(height, weight)
        category = get_bmi_category(bmi)
        message = get_health_message(category)
        
        st.metric("Your BMI", f"{bmi:.2f}")
        st.subheader(f"Category: {category}")
        st.info(message)
        
        st.divider()
        st.subheader("BMI Categories")
        categories = pd.DataFrame({
            "Category": ["Underweight", "Normal", "Overweight", "Obese"],
            "BMI Range": ["< 18.5", "18.5 - 24.9", "25 - 29.9", ">= 30"],
            "Status": ["Underweight", "Healthy", "At Risk", "High Risk"]
        })
        st.table(categories)
