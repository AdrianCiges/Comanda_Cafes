import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

if st.checkbox("Check my location"):
    loc = get_geolocation()
    st.write(f"Your coordinates are {loc}")
