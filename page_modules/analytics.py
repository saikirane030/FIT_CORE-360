import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database.db_setup import get_diet_history, get_weight_log

def show():
    st.title("📊 Analytics Dashboard")
    st.markdown("Visual insights into your fitness journey.")
    st.divider()

    if not st.session_state.get("user_id"):
        st.warning("⚠️ Please set up your profile first to see analytics.")
        return

    uid      = st.session_state.user_id
    diet_df  = get_diet_history(uid)
    weight_df = get_weight_log(uid)

    # ── Weight Trend ──────────────────────────────────────────
    st.subheader("⚖️ Weight Trend")
    if weight_df.empty:
        st.info("No weight data yet. Log your weight in the BMI Calculator page.")
    else:
        fig = px.line(
            weight_df, x="date", y="weight",
            title="Weight Over Time",
            markers=True,
            color_discrete_sequence=["#00b4d8"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,10,30,0.8)",
            font_color="#90e0ef",
            xaxis=dict(gridcolor="#1a1a3e"),
            yaxis=dict(gridcolor="#1a1a3e")
        )
        st.plotly_chart(fig, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Starting Weight", f"{weight_df['weight'].iloc[0]:.1f} kg")
        c2.metric("Current Weight",  f"{weight_df['weight'].iloc[-1]:.1f} kg")
        change = weight_df['weight'].iloc[-1] - weight_df['weight'].iloc[0]
        c3.metric("Change", f"{change:+.1f} kg", delta_color="inverse" if change > 0 else "normal")

    st.divider()

    # ── Calorie Trend ─────────────────────────────────────────
    st.subheader("🔥 Daily Calorie Intake")
    if diet_df.empty:
        st.info("No meal data yet. Log meals in the Nutrition Planner.")
    else:
        daily = diet_df.groupby("date").agg(
            Calories=("calories", "sum"),
            Protein=("protein", "sum"),
            Carbs=("carbs", "sum"),
            Fat=("fat", "sum")
        ).reset_index()

        fig2 = px.bar(
            daily, x="date", y="Calories",
            title="Daily Calories",
            color="Calories",
            color_continuous_scale=["#023e8a", "#00b4d8", "#90e0ef"]
        )
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,10,30,0.8)",
            font_color="#90e0ef",
            xaxis=dict(gridcolor="#1a1a3e"),
            yaxis=dict(gridcolor="#1a1a3e")
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Macro stacked chart
        st.subheader("🍽️ Macro Breakdown Over Time")
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="Protein", x=daily["date"], y=daily["Protein"], marker_color="#00b4d8"))
        fig3.add_trace(go.Bar(name="Carbs",   x=daily["date"], y=daily["Carbs"],   marker_color="#90e0ef"))
        fig3.add_trace(go.Bar(name="Fat",     x=daily["date"], y=daily["Fat"],     marker_color="#0077b6"))
        fig3.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(10,10,30,0.8)",
            font_color="#90e0ef",
            title="Protein / Carbs / Fat per Day",
            xaxis=dict(gridcolor="#1a1a3e"),
            yaxis=dict(gridcolor="#1a1a3e", title="Grams")
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Meal type distribution
        st.subheader("🍴 Meals by Type")
        meal_counts = diet_df.groupby("meal")["calories"].sum().reset_index()
        fig4 = px.pie(
            meal_counts, values="calories", names="meal",
            title="Calorie Share by Meal Type",
            color_discrete_sequence=["#00b4d8","#90e0ef","#0077b6","#023e8a"]
        )
        fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#90e0ef")
        st.plotly_chart(fig4, use_container_width=True)

        # Summary table
        st.subheader("📋 Daily Summary Table")
        st.dataframe(daily.style.format({
            "Calories": "{:.0f} kcal",
            "Protein":  "{:.1f} g",
            "Carbs":    "{:.1f} g",
            "Fat":      "{:.1f} g"
        }), use_container_width=True)


if __name__ == "__main__":
    show()
