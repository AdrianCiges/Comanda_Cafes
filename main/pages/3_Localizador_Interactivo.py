import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

loc = get_geolocation()
st.write(f'{loc})
st.write(f'{loc['coords']['latitude']}, {loc['coords']['longitude']}]

