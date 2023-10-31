import streamlit as st
import geocoder
g = geocoder.ip('me')
st.write(g.latlng)
