import streamlit as st
import requests

def get_location_from_ip():
    try:
        response = requests.get("https://ipinfo.io/json?token=83c178d0c646a4")
        data = response.json()
        location = data['loc'].split(',')
        return float(location[0]), float(location[1])
    except:
        return None, None

if st.button("Get my location"):
    lat, lon = get_location_from_ip()
    if lat and lon:
        st.write(f"Your approximate coordinates are: Latitude: {lat}, Longitude: {lon}")
    else:
        st.write("Unable to get your location.")
