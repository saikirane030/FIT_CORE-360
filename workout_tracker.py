import pandas as pd
import streamlit as st
from csv_manager import load_csv_data, save_csv_data

# Function to calculate calories based on workout type and duration.
def calculate_calories(workout_name, duration):
    if "cardio" in workout_name.lower():
        return duration * 8
    elif "strength" in workout_name.lower():
        return duration * 6
    elif "yoga" in workout_name.lower():
        return duration * 4
    else:
        return duration * 5

# Workout tracker page with history and filtering.
def show_workout_tracker():
    st.title("Workout Tracking")
    st.markdown("Track workouts and calories burned.")

    members = load_csv_data("members.csv")
    workouts = load_csv_data("workouts.csv")

    member_name = st.selectbox("Select Member", [""] + members["Name"].tolist() if not members.empty else [""])
    workout_name = st.text_input("Workout Name", "Cardio Session")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
    workout_date = st.date_input("Workout Date")

    if st.button("Add Workout"):
        if member_name == "":
            st.error("Please select a member first.")
        else:
            calories = calculate_calories(workout_name, duration)
            next_id = int(workouts["ID"].max()) + 1 if not workouts.empty else 1
            new_row = {
                "ID": next_id,
                "Member": member_name,
                "Workout": workout_name,
                "Duration": duration,
                "Calories": calories,
                "Date": workout_date.strftime("%Y-%m-%d")
            }
            workouts = workouts.append(new_row, ignore_index=True)
            save_csv_data(workouts, "workouts.csv")
            st.success("Workout logged successfully.")

    st.markdown("---")
    st.subheader("Workout History")
    if not workouts.empty:
        search_member = st.text_input("Search history by member")
        if search_member:
            filtered = workouts[workouts["Member"].str.contains(search_member, case=False, na=False)]
            st.dataframe(filtered)
        else:
            st.dataframe(workouts)
    else:
        st.write("No workout history yet.")
