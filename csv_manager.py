import streamlit as st
import pandas as pd
import os

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame()

def save_users(df):
    df.to_csv("users.csv", index=False)

def show_csv_manager():
    st.title("CSV Data Management")
    st.markdown("Upload, validate, and manage CSV data")
    
    action = st.selectbox("Select Action", ["View Data", "Upload CSV", "Download CSV"])
    
    if action == "View Data":
        st.subheader("Current User Data")
        users = load_users()
        
        if users.empty:
            st.info("No users found")
        else:
            st.dataframe(users)
            st.write(f"Total Records: {len(users)}")
    
    elif action == "Upload CSV":
        st.subheader("Upload CSV File")
        uploaded_file = st.file_uploader("Choose CSV", type=["csv"])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            required_cols = ["name", "age", "gender", "height", "weight", "goal"]
            
            if all(col in df.columns for col in required_cols):
                st.success("CSV has all required columns")
                st.dataframe(df.head())
                
                if st.button("Import CSV"):
                    users = load_users()
                    users = pd.concat([users, df], ignore_index=True)
                    save_users(users)
                    st.success(f"Imported {len(df)} records successfully!")
            else:
                st.error(f"Missing columns. Required: {required_cols}")
    
    elif action == "Download CSV":
        st.subheader("Download User Data")
        users = load_users()
        
        if not users.empty:
            csv_data = users.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="users.csv",
                mime="text/csv"
            )
        else:
            st.info("No data to download")
