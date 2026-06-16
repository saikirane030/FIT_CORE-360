import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import os

def load_gyms():
    gyms_path = os.path.join("data", "gyms.csv")
    if os.path.exists(gyms_path):
        return pd.read_csv(gyms_path)
    return pd.DataFrame()

def show_gym_map():
    st.title("Gym Finder Map")
    st.markdown("Find nearby gyms on interactive map")
    
    gyms = load_gyms()
    
    if gyms.empty:
        st.error("Gym data not found")
        return
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Filters")
        city = st.selectbox("City", ["All"] + sorted(gyms["city"].unique().tolist()))
        gym_type = st.multiselect("Type", gyms["type"].unique().tolist(),
                                  default=gyms["type"].unique().tolist())
        min_rating = st.slider("Min Rating", 1.0, 5.0, 4.0)
        
        filtered = gyms.copy()
        if city != "All":
            filtered = filtered[filtered["city"] == city]
        filtered = filtered[filtered["type"].isin(gym_type)]
        filtered = filtered[filtered["rating"] >= min_rating]
        
        st.write(f"Found: {len(filtered)} gyms")
        st.dataframe(filtered[["name", "city", "type", "rating"]])
    
    with col2:
        st.subheader("Interactive Map")
        
        if not filtered.empty:
            center_lat = filtered["lat"].mean()
            center_lon = filtered["lon"].mean()
        else:
            center_lat, center_lon = 12.9716, 77.5946
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        colors = {"Premium": "red", "Mid-range": "orange", "Budget": "blue"}
        
        for _, row in filtered.iterrows():
            color = colors.get(row["type"], "gray")
            folium.Marker(
                location=[row["lat"], row["lon"]],
                popup=f"{row['name']} - {row['type']}",
                tooltip=row["name"],
                icon=folium.Icon(color=color)
            ).add_to(m)
        
        st_folium(m, width=700, height=500)
