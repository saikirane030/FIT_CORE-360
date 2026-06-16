import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from csv_manager import load_csv_data

# Progress analysis using Matplotlib charts.
def show_progress():
    st.title("Progress Analysis")
    st.markdown("Visualize workout and nutrition progress using charts.")

    workouts = load_csv_data("workouts.csv")
    nutrition = load_csv_data("nutrition.csv")

    if not workouts.empty:
        st.subheader("Weight Progress Chart")
        workout_counts = workouts["Workout"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.bar(workout_counts.index, workout_counts.values)
        ax1.set_xlabel("Workout")
        ax1.set_ylabel("Count")
        st.pyplot(fig1)

        st.subheader("Workout Calories Pie Chart")
        calories_by_workout = workouts.groupby("Workout")["Calories"].sum()
        fig2, ax2 = plt.subplots()
        ax2.pie(calories_by_workout, labels=calories_by_workout.index, autopct="%.1f%%")
        ax2.axis("equal")
        st.pyplot(fig2)
    else:
        st.write("No workout data available for charts.")

    if not nutrition.empty:
        st.subheader("Nutrition Calories Line Chart")
        nutrition_by_date = nutrition.groupby("Date")["Calories"].sum().reset_index()
        fig3, ax3 = plt.subplots()
        ax3.plot(nutrition_by_date["Date"], nutrition_by_date["Calories"], marker="o")
        ax3.set_xlabel("Date")
        ax3.set_ylabel("Calories")
        st.pyplot(fig3)
    else:
        st.write("No nutrition data available for charts.")
