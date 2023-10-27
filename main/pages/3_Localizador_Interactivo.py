import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
from geopy.distance import geodesic

# Supongamos que tienes el siguiente DataFrame como ejemplo
df = pd.DataFrame({
    'latitude': [40.4168, 40.4070, 40.3999, 40.3920, 40.3840, 40.3760, 40.3680, 40.3600, 40.3520, 40.3440, 40.3360],
    'longitude': [-3.7038, -3.6950, -3.6860, -3.6770, -3.6680, -3.6590, -3.6500, -3.6410, -3.6320, -3.6230, -3.6140]
})

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=False, minimap_control=True)
    m.add_basemap(basemap)

    # Captura las coordenadas del punto seleccionado
    location = m.click_latlon()
    if location:
        lat, lon = location
        st.write(f"Selected coordinates: Latitude: {lat}, Longitude: {lon}")
        
        # Calcular distancias y seleccionar las 10 ubicaciones más cercanas
        df['distance'] = df.apply(lambda row: geodesic((lat, lon), (row['latitude'], row['longitude'])).km, axis=1)
        closest_points = df.nsmallest(10, 'distance')
        
        # Añadir marcadores para las 10 ubicaciones más cercanas
        for idx, row in closest_points.iterrows():
            folium.Marker([row['latitude'], row['longitude']], popup=f"Distance: {row['distance']:.2f} km").add_to(m)
    
    m.to_streamlit(height=700)
