import streamlit as st

def show():
    st.title("💪 Welcome to FitCore 360")
    st.markdown("#### Your All-in-One Health & Fitness Platform")
    st.divider()

    # Feature cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>⚖️</h2>
            <h4 style='color:#90e0ef'>BMI Calculator</h4>
            <p style='color:#caf0f8;font-size:13px'>Calculate your Body Mass Index and know your health status instantly</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>🥗</h2>
            <h4 style='color:#90e0ef'>Nutrition Planner</h4>
            <p style='color:#caf0f8;font-size:13px'>Log meals, track calories, protein, carbs & fat from our food database</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>📊</h2>
            <h4 style='color:#90e0ef'>Analytics</h4>
            <p style='color:#caf0f8;font-size:13px'>Visual charts for weight trends, calorie history, and macro breakdown</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>🗺️</h2>
            <h4 style='color:#90e0ef'>Gym Finder</h4>
            <p style='color:#caf0f8;font-size:13px'>Find gyms near you on an interactive map with ratings and details</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>👤</h2>
            <h4 style='color:#90e0ef'>Profile Setup</h4>
            <p style='color:#caf0f8;font-size:13px'>Save your profile to SQLite DB and track your fitness journey over time</p>
        </div>
        """, unsafe_allow_html=True)
    with col6:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#1a1a2e,#16213e);
                    border:1px solid #00b4d8;border-radius:12px;padding:20px;text-align:center'>
            <h2>💾</h2>
            <h4 style='color:#90e0ef'>Data Storage</h4>
            <p style='color:#caf0f8;font-size:13px'>All data saved to local SQLite database — no internet required</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.info("👈 Start by going to **Profile Setup** in the sidebar to create your account!")

    # Quick stats
    st.markdown("### 📈 Quick Stats")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Features", "6", "Modules")
    m2.metric("Food Items", "35+", "In Database")
    m3.metric("Gyms Listed", "12", "Cities")
    m4.metric("Storage", "SQLite", "Local DB")


if __name__ == "__main__":
    show()
