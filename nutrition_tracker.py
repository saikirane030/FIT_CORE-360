import streamlit as st
import pandas as pd
import os

# Food database
FOOD_DATABASE = {
    "Egg": 155,
    "Rice": 130,
    "Chicken Breast": 165,
    "Milk": 60,
    "Banana": 89,
    "Apple": 52,
    "Bread": 265,
    "Yogurt": 59,
    "Salmon": 206,
    "Broccoli": 34,
    "Sweet Potato": 86,
    "Almonds": 579,
    "Peanut Butter": 588,
    "Orange": 47,
    "Carrot": 41
}

def load_nutrition_log():
    if os.path.exists("nutrition_log.csv"):
        return pd.read_csv("nutrition_log.csv")
    return pd.DataFrame(columns=["food", "quantity", "unit", "calories"])

def save_nutrition_log(df):
    df.to_csv("nutrition_log.csv", index=False)

def show_nutrition_tracker():
    st.title("Nutrition Tracker")
    st.markdown("Track your daily food intake and calories")
    
    tab1, tab2 = st.tabs(["Log Food", "View History"])
    
    with tab1:
        st.subheader("Add Food Item")
        
        col1, col2 = st.columns(2)
        with col1:
            food = st.selectbox("Select Food", list(FOOD_DATABASE.keys()))
        with col2:
            quantity = st.number_input("Quantity", min_value=0.1, value=1.0, step=0.1)
        
        calories_per_unit = FOOD_DATABASE[food]
        total_calories = calories_per_unit * quantity
        
        st.write(f"Calories per 100g: {calories_per_unit} kcal")
        st.write(f"Total Calories: {total_calories:.0f} kcal")
        
        if st.button("Add to Log"):
            log = load_nutrition_log()
            new_entry = pd.DataFrame({
                "food": [food],
                "quantity": [quantity],
                "unit": ["100g"],
                "calories": [total_calories]
            })
            log = pd.concat([log, new_entry], ignore_index=True)
            save_nutrition_log(log)
            st.success("Added to nutrition log!")
    
    with tab2:
        st.subheader("Nutrition Log")
        log = load_nutrition_log()
        
        if log.empty:
            st.info("No food logged yet")
        else:
            st.dataframe(log)
            total_calories = log["calories"].sum()
            st.metric("Total Calories Today", f"{total_calories:.0f} kcal")
