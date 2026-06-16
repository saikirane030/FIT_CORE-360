import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

GYMS_CSV = os.path.join(os.path.dirname(__file__), "..", "data", "gyms.csv")

@st.cache_data
def load_gyms():
    return pd.read_csv(GYMS_CSV)

def show():
    st.title("🗺️ Gym Finder")
    st.markdown("Find gyms near you on an interactive map.")
    st.divider()

    gyms_df = load_gyms()

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔍 Filter Gyms")
        city = st.selectbox("Select City", ["All"] + sorted(gyms_df["city"].unique().tolist()))
        gym_type = st.multiselect("Gym Type", gyms_df["type"].unique().tolist(),
                                  default=gyms_df["type"].unique().tolist())
        min_rating = st.slider("Minimum Rating", 1.0, 5.0, 4.0, 0.1)

        # Filter
        filtered = gyms_df.copy()
        if city != "All":
            filtered = filtered[filtered["city"] == city]
        filtered = filtered[filtered["type"].isin(gym_type)]
        filtered = filtered[filtered["rating"] >= min_rating]

        st.markdown(f"**{len(filtered)} gyms found**")
        st.dataframe(
            filtered[["name","city","type","rating"]].reset_index(drop=True),
            use_container_width=True
        )

    with col2:
        st.subheader("🗺️ Interactive Map")

        # Center map
        if city != "All" and not filtered.empty:
            center_lat = filtered["lat"].mean()
            center_lon = filtered["lon"].mean()
            zoom = 12
        else:
            center_lat, center_lon, zoom = 20.5937, 78.9629, 5  # India center

        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom,
                       tiles="CartoDB dark_matter")

        # Color by type
        type_colors = {"Premium": "red", "Mid-range": "orange", "Budget": "blue"}

        for _, row in filtered.iterrows():
            color = type_colors.get(row["type"], "gray")
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=folium.Popup(
                    f"""<b>{row['name']}</b><br>
                    📍 {row['address']}<br>
                    ⭐ Rating: {row['rating']}<br>
                    🏷️ Type: {row['type']}""",
                    max_width=200
                ),
                tooltip=row["name"],
                icon=folium.Icon(color=color, icon="heart", prefix="fa")
            ).add_to(m)

        st_folium(m, width=650, height=480)

        # Legend
        st.markdown("""
        **Map Legend:**
        🔴 Premium &nbsp;&nbsp; 🟠 Mid-range &nbsp;&nbsp; 🔵 Budget
        """)
