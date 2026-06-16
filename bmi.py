import streamlit as st

# BMI calculator page using simple formula.
def show_bmi():
    st.title("BMI Calculator")
    st.markdown("Enter height and weight to calculate BMI.")

    height = st.number_input("Height (meters)", min_value=0.5, max_value=2.5, value=1.7)
    weight = st.number_input("Weight (kilograms)", min_value=20.0, max_value=200.0, value=70.0)

    if st.button("Calculate BMI"):
        bmi = weight / (height ** 2)
        category = ""
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"

        st.metric("BMI", f"{bmi:.2f}")
        st.write(f"BMI Category: {category}")
