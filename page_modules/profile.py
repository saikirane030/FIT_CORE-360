import streamlit as st
import pandas as pd
from database.db_setup import save_user, get_all_users

def show():
    st.title("👤 Profile Setup")
    st.markdown("Create your profile — saved to local SQLite database.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("➕ Create New Profile")
        default_name   = st.session_state.get("user_name", "")
        default_age    = st.session_state.get("user_age", 20)
        default_gender = st.session_state.get("user_gender", "Male")
        default_weight = st.session_state.get("user_weight", 70.0)
        default_height = st.session_state.get("user_height", 170.0)
        default_goal   = st.session_state.get("user_goal", "Lose Weight")

        name   = st.text_input("Full Name", placeholder="e.g. Sai Kiran", value=default_name)
        age    = st.number_input("Age", min_value=10, max_value=100, value=int(default_age))
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=["Male", "Female", "Other"].index(default_gender if default_gender in ["Male", "Female", "Other"] else "Male")
        )
        weight = st.number_input("Current Weight (kg)", min_value=20.0, max_value=300.0, value=float(default_weight), step=0.5)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=float(default_height), step=0.5)
        goal   = st.selectbox(
            "Fitness Goal",
            ["Lose Weight", "Gain Muscle", "Maintain Weight", "Improve Stamina", "General Fitness"],
            index=["Lose Weight", "Gain Muscle", "Maintain Weight", "Improve Stamina", "General Fitness"].index(default_goal if default_goal in ["Lose Weight", "Gain Muscle", "Maintain Weight", "Improve Stamina", "General Fitness"] else "Lose Weight")
        )

        if st.button("💾 Save Profile"):
            if name.strip() == "":
                st.error("Please enter your name.")
            else:
                user_id = save_user(name, age, gender, weight, height, goal)
                st.session_state.user_id     = user_id
                st.session_state.user_name   = name
                st.session_state.user_age    = age
                st.session_state.user_gender = gender
                st.session_state.user_weight = weight
                st.session_state.user_height = height
                st.session_state.user_goal   = goal
                st.success(f"✅ Profile saved! Welcome, {name}! (ID: {user_id})")

        if st.session_state.get("user_id"):
            if st.button("Go to BMI Calculator", key="go_to_bmi_after_save"):
                st.session_state.nav_target = "⚖️  BMI Calculator"
                st.experimental_rerun()

    with col2:
        st.subheader("📋 Existing Profiles")
        users = get_all_users()
        if users:
            df = pd.DataFrame(users, columns=[
                "ID", "Name", "Age", "Gender",
                "Weight(kg)", "Height(cm)", "Goal", "Created At"
            ])
            st.dataframe(df[["ID","Name","Age","Gender","Goal"]], use_container_width=True)

            st.markdown("#### 🔄 Load Existing Profile")
            user_names = [f"{u[0]} - {u[1]}" for u in users]
            selected   = st.selectbox("Select profile", user_names)
            if st.button("Load Profile"):
                uid  = int(selected.split(" - ")[0])
                selected_user = next((u for u in users if u[0] == uid), None)
                if selected_user is not None:
                    st.session_state.user_id     = selected_user[0]
                    st.session_state.user_name   = selected_user[1]
                    st.session_state.user_age    = selected_user[2]
                    st.session_state.user_gender = selected_user[3]
                    st.session_state.user_weight = selected_user[4]
                    st.session_state.user_height = selected_user[5]
                    st.session_state.user_goal   = selected_user[6]
                    st.success(f"✅ Loaded profile: {selected_user[1]}")
                else:
                    st.error("Unable to load the selected profile.")

            if st.session_state.get("user_id"):
                if st.button("Go to BMI Calculator", key="go_to_bmi_after_load"):
                    st.session_state.nav_target = "⚖️  BMI Calculator"
                    st.experimental_rerun()

            st.markdown("#### 🗑️ Delete a Profile")
            delete_options = [f"{u[0]} - {u[1]}" for u in users]
            selected_delete = st.selectbox("Select profile to delete", delete_options, key="delete_profile_select")
            if st.button("Delete Selected Profile"):
                uid = int(selected_delete.split(" - ")[0])
                delete_user(uid)
                if st.session_state.get("user_id") == uid:
                    for key in ["user_id", "user_name", "user_age", "user_gender", "user_weight", "user_height", "user_goal"]:
                        if key in st.session_state:
                            del st.session_state[key]
                st.success("✅ Profile and associated history deleted.")
                st.experimental_rerun()
        else:
            st.info("No profiles yet. Create one on the left!")


if __name__ == "__main__":
    show()
