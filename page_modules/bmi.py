import streamlit as st
import plotly.graph_objects as go
from database.db_setup import save_weight_log
from datetime import date

def show():
    st.title("⚖️ BMI Calculator")
    st.markdown("Calculate your Body Mass Index and get health recommendations.")
    st.divider()

    default_age = st.session_state.get("user_age", 20)
    default_gender = st.session_state.get("user_gender", "Male")
    default_weight = st.session_state.get("user_weight", 70.0)
    default_height = st.session_state.get("user_height", 170.0)

    if st.session_state.get("user_id"):
        st.info("Using your saved profile values. Update them below if needed.")
    else:
        st.info("No profile loaded. Enter your measurements or go to Profile Setup to save them.")
        if st.button("Go to Profile Setup"):
            st.session_state.nav_target = "👤  Profile Setup"
            st.experimental_rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Your Measurements")
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=float(default_weight), step=0.5)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=float(default_height), step=0.5)
        age    = st.number_input("Age", min_value=10, max_value=100, value=int(default_age))
        gender = st.selectbox("Gender", ["Male", "Female"], index=["Male", "Female"].index(default_gender if default_gender in ["Male", "Female"] else "Male"))

        calculate = st.button("⚡ Calculate BMI")

    with col2:
        if calculate:
            h_m  = height / 100
            bmi  = weight / (h_m ** 2)
            bmr  = (10 * weight + 6.25 * height - 5 * age + (5 if gender == "Male" else -161))

            # Status
            if bmi < 18.5:
                status, color, advice = "Underweight 🔵", "#48cae4", "Eat more calorie-dense foods. Focus on proteins and healthy fats."
            elif bmi < 25:
                status, color, advice = "Normal ✅", "#52b788", "Great! Maintain your current diet and exercise routine."
            elif bmi < 30:
                status, color, advice = "Overweight 🟡", "#f4a261", "Reduce processed foods. Add 30 mins cardio daily."
            else:
                status, color, advice = "Obese 🔴", "#e63946", "Consult a doctor. Start with low-impact exercises and a calorie deficit."

            st.metric("Your BMI", f"{bmi:.1f}", status)
            st.metric("BMR (Base Metabolic Rate)", f"{bmr:.0f} kcal/day")

            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=bmi,
                title={"text": "BMI Gauge", "font": {"color": "#90e0ef"}},
                number={"font": {"color": "#00b4d8"}},
                gauge={
                    "axis": {"range": [10, 40], "tickcolor": "#90e0ef"},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [10, 18.5], "color": "#023e8a"},
                        {"range": [18.5, 25], "color": "#1b4332"},
                        {"range": [25, 30],   "color": "#7f4f24"},
                        {"range": [30, 40],   "color": "#6b0000"},
                    ],
                    "threshold": {"line": {"color": "white", "width": 3}, "value": bmi}
                }
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font_color="#90e0ef",
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)

            st.info(f"💡 **Advice:** {advice}")

            # Log weight if user logged in
            if st.session_state.get("user_id"):
                if st.button("📥 Save Weight to Log"):
                    save_weight_log(st.session_state.user_id, str(date.today()), weight)
                    st.success("Weight saved to your history!")

    # BMI Table reference
    st.divider()
    st.subheader("📋 BMI Reference Table")
    import pandas as pd
    ref = pd.DataFrame({
        "Category":   ["Underweight", "Normal", "Overweight", "Obese"],
        "BMI Range":  ["< 18.5", "18.5 – 24.9", "25 – 29.9", "≥ 30"],
        "Risk Level": ["Low (but health risks)", "Lowest risk", "Moderate risk", "High risk"]
    })
    st.table(ref)


if __name__ == "__main__":
    show()
