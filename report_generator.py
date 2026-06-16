import streamlit as st
import pandas as pd
import os

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame()

def load_nutrition_log():
    if os.path.exists("nutrition_log.csv"):
        return pd.read_csv("nutrition_log.csv")
    return pd.DataFrame()

def generate_user_report(user_name):
    users = load_users()
    user = users[users["name"].str.lower() == user_name.lower()]
    
    if user.empty:
        return None
    
    user = user.iloc[0]
    bmi = user["weight"] / ((user["height"] / 100) ** 2)
    
    if bmi < 18.5:
        bmi_category = "Underweight"
    elif bmi < 25:
        bmi_category = "Normal"
    elif bmi < 30:
        bmi_category = "Overweight"
    else:
        bmi_category = "Obese"
    
    nutrition = load_nutrition_log()
    consumed_calories = nutrition["calories"].sum() if not nutrition.empty else 0
    
    report = {
        "Name": user["name"],
        "Age": user["age"],
        "Gender": user["gender"],
        "Height (cm)": user["height"],
        "Weight (kg)": user["weight"],
        "BMI": round(bmi, 2),
        "BMI Category": bmi_category,
        "Goal": user["goal"],
        "Total Consumed Calories": consumed_calories
    }
    return report

def show_report_generator():
    st.title("Report Generator")
    st.markdown("Generate fitness reports for users")
    
    users = load_users()
    
    if users.empty:
        st.info("No users found")
        return
    
    user_name = st.selectbox("Select User", users["name"].tolist())
    
    if st.button("Generate Report"):
        report = generate_user_report(user_name)
        
        if report:
            st.subheader("Fitness Report")
            
            for key, value in report.items():
                st.write(f"**{key}:** {value}")
            
            st.divider()
            
            report_df = pd.DataFrame([report])
            csv = report_df.to_csv(index=False)
            
            st.download_button(
                label="Download Report as CSV",
                data=csv,
                file_name=f"{user_name}_report.csv",
                mime="text/csv"
            )
