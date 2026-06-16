import streamlit as st
import pandas as pd
import os

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame(columns=["name", "age", "gender", "height", "weight", "goal"])

def save_users(df):
    df.to_csv("users.csv", index=False)

def show_user_entry():
    st.title("User Entry")
    st.markdown("Add new user data manually or via CSV")
    
    entry_type = st.radio("Select Entry Type", ["Individual Entry", "CSV Upload"])
    
    if entry_type == "Individual Entry":
        st.subheader("Enter User Details")
        
        name = st.text_input("Name", placeholder="John Doe")
        col1, col2 = st.columns(2)
        with col1:
            age = st.number_input("Age", min_value=10, max_value=100, value=25)
        with col2:
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        
        col1, col2 = st.columns(2)
        with col1:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=170)
        with col2:
            weight = st.number_input("Weight (kg)", min_value=30, max_value=200, value=70)
        
        goal = st.selectbox("Fitness Goal", ["Weight Loss", "Weight Gain", "Lean Muscle Gain"])
        
        if st.button("Add User"):
            if name.strip():
                users = load_users()
                new_user = {
                    "name": name,
                    "age": age,
                    "gender": gender,
                    "height": height,
                    "weight": weight,
                    "goal": goal
                }
                users = pd.concat([users, pd.DataFrame([new_user])], ignore_index=True)
                save_users(users)
                st.success(f"User {name} added successfully!")
            else:
                st.error("Please enter a name")
    
    else:
        st.subheader("Upload CSV File")
        uploaded_file = st.file_uploader("Choose CSV file", type=["csv"])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df.head())
            
            if st.button("Import Data"):
                users = load_users()
                users = pd.concat([users, df], ignore_index=True)
                save_users(users)
                st.success(f"{len(df)} users imported successfully!")
