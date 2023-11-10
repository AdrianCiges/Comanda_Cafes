import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

loc = get_geolocation()
# st.write(f'{loc}')
latitud = loc['coords']['latitude']
longitud = loc['coords']['longitude']
st.write(f'{latitud}, {longitud}')

