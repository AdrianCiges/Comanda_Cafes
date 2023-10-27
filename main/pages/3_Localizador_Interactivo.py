import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
from geopy.distance import geodesic

# Suponemos el siguiente DataFrame de ejemplo
df = pd.DataFrame({
    'latitude': [40.4168, 40.4070, 40.3999, 40.3920, 40.3840, 40.3760, 40.3680, 40.3600, 40.3520, 40.3440, 40.3360],
    'longitude': [-3.7038, -3.6950, -3.6860, -3.6770, -3.6680, -3.6590, -3.6500, -3.6410, -3.6320, -3.6230, -3.6140]
})

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

click_coords = st.session_state.get("click_coords", None)

m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)

if click_coords:
    lat, lon = click_coords
    st.write(f"Selected coordinates: Latitude: {lat}, Longitude: {lon}")

    # Calculate distances and select the 10 closest locations
    df['distance'] = df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km, axis=1)
    closest_points = df.nsmallest(10, 'distance')

    # Add markers for the 10 closest locations
    for idx, row in closest_points.iterrows():
        folium.Marker([row['latitude'], row['longitude']], popup=f"Distance: {row['distance']:.2f} km").add_to(m)

m.add_child(folium.ClickForMarker(popup="Selected Location"))

folium_static(m)
