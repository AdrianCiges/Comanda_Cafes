import streamlit as st

st.write(f"Screen width is {streamlit_js_eval(js_expressions='screen.width', key = 'SCR')}")
location = get_geolocation()
