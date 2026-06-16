import streamlit as st
import pandas as pd
import plotly.express as px
from database.db_setup import save_diet_entry, get_diet_history, delete_diet_entry
from datetime import date
import os

FOOD_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "food_database.csv")

@st.cache_data
def load_food_db():
    return pd.read_csv(FOOD_CSV)

def show():
    st.title("🥗 Nutrition Planner")
    st.markdown("Log your meals and track your daily nutrition intake.")
    st.divider()

    food_df = load_food_db()

    st.subheader("➕ Log a Meal")

    col1, col2 = st.columns(2)
    with col1:
        meal_date  = st.date_input("Date", value=date.today())
        meal_type  = st.selectbox("Meal", ["Breakfast", "Lunch", "Dinner", "Snack"])
        category   = st.selectbox("Food Category", ["All"] + sorted(food_df["category"].unique().tolist()))

    with col2:
        if category == "All":
            filtered = food_df
        else:
            filtered = food_df[food_df["category"] == category]

        food_item = st.selectbox("Select Food", filtered["food_item"].tolist())
        selected  = filtered[filtered["food_item"] == food_item].iloc[0]

        st.markdown(f"""
        **Nutritional Info (per serving):**
        - 🔥 Calories: `{selected['calories']} kcal`
        - 💪 Protein: `{selected['protein']} g`
        - 🍞 Carbs: `{selected['carbs']} g`
        - 🧈 Fat: `{selected['fat']} g`
        """, unsafe_allow_html=True)

    servings = st.slider("Number of servings", 0.5, 5.0, 1.0, 0.5)

    if st.button("➕ Add to Log"):
        if not st.session_state.get("user_id"):
            st.error("⚠️ Please set up your profile first (go to Profile Setup).")
        else:
            added_calories = round(selected["calories"] * servings, 1)
            save_diet_entry(
                st.session_state.user_id,
                str(meal_date), meal_type, food_item,
                added_calories,
                round(selected["protein"]  * servings, 1),
                round(selected["carbs"]    * servings, 1),
                round(selected["fat"]      * servings, 1)
            )
            df_user = get_diet_history(st.session_state.user_id)
            total_today = df_user[df_user["date"] == str(meal_date)]["calories"].sum()
            total_logged = df_user["calories"].sum()
            st.success(f"✅ {food_item} added to {meal_type}!")
            st.info(
                f"Added **{added_calories:.1f} kcal** to the log. "
                f"Total for {meal_date}: **{total_today:.1f} kcal**. "
                f"Total logged so far: **{total_logged:.1f} kcal**."
            )

    st.divider()
    st.subheader("📋 Meal History")
    if not st.session_state.get("user_id"):
        st.warning("Please set up your profile to see history.")
    else:
        df = get_diet_history(st.session_state.user_id)
        if df.empty:
            st.info("No meals logged yet. Start logging in the log section above!")
        else:
            # Today summary
            today_str = str(date.today())
            today_df  = df[df["date"] == today_str]
            if not today_df.empty:
                st.markdown("#### 📅 Today's Summary")
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Calories",  f"{today_df['calories'].sum():.0f} kcal")
                c2.metric("Protein",   f"{today_df['protein'].sum():.1f} g")
                c3.metric("Carbs",     f"{today_df['carbs'].sum():.1f} g")
                c4.metric("Fat",       f"{today_df['fat'].sum():.1f} g")

                # Macro pie
                macro = {
                    "Protein": today_df["protein"].sum(),
                    "Carbs":   today_df["carbs"].sum(),
                    "Fat":     today_df["fat"].sum()
                }
                fig = px.pie(
                    values=list(macro.values()),
                    names=list(macro.keys()),
                    title="Today's Macro Split",
                    color_discrete_sequence=["#00b4d8", "#90e0ef", "#0077b6"]
                )
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#90e0ef")
                st.plotly_chart(fig, use_container_width=True)

            st.markdown("#### 📋 Full History")
            st.dataframe(df[["date","meal","food_item","calories","protein","carbs","fat"]],
                         use_container_width=True)

            st.markdown("#### 🗑️ Delete a Logged Meal")
            delete_options = [
                f"{row['id']} - {row['date']} | {row['meal']} | {row['food_item']} | {row['calories']} kcal"
                for _, row in df.iterrows()
            ]
            selected_delete = st.selectbox("Select an entry to delete", delete_options)
            if st.button("Delete Selected Entry"):
                delete_id = int(selected_delete.split(" - ")[0])
                delete_diet_entry(delete_id)
                st.success("✅ Meal entry deleted from your log.")
                df = get_diet_history(st.session_state.user_id)
                if df.empty:
                    st.info("No meals left in your history.")
                else:
                    st.dataframe(df[["date","meal","food_item","calories","protein","carbs","fat"]],
                                 use_container_width=True)

    st.divider()
    st.subheader("🍽️ Suggested Meal Plan")
    goal = st.selectbox("Select Goal", ["Lose Weight", "Gain Muscle", "Maintenance"])

    plans = {
        "Lose Weight": {
            "Breakfast": "Oats (1 cup) + Apple + Green Tea → ~350 kcal",
            "Lunch":     "Salad + Grilled Chicken (100g) + Brown Rice → ~480 kcal",
            "Snack":     "Almonds (10) + Orange → ~140 kcal",
            "Dinner":    "Dal (1 cup) + 2 Chapati + Cucumber → ~450 kcal",
            "Total":     "~1420 kcal | High Protein, Low Fat"
        },
        "Gain Muscle": {
            "Breakfast": "4 Eggs + 2 Toast + Milk (1 cup) → ~620 kcal",
            "Lunch":     "Rice (2 cups) + Chicken (150g) + Dal → ~900 kcal",
            "Snack":     "Banana + Mixed Nuts + Curd → ~380 kcal",
            "Dinner":    "Paneer (100g) + 3 Roti + Sabzi → ~700 kcal",
            "Total":     "~2600 kcal | Very High Protein"
        },
        "Maintenance": {
            "Breakfast": "Idli (2) + Sambar + Curd → ~380 kcal",
            "Lunch":     "Rice + Dal + Sabzi + Salad → ~550 kcal",
            "Snack":     "Fruits + Peanuts → ~200 kcal",
            "Dinner":    "2 Chapati + Dal + Vegetables → ~480 kcal",
            "Total":     "~1610 kcal | Balanced"
        }
    }

    plan = plans[goal]
    for meal, desc in plan.items():
        if meal == "Total":
            st.success(f"🏁 **Total:** {desc}")
        else:
            st.markdown(f"**{meal}:** {desc}")


if __name__ == "__main__":
    show()
