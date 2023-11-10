import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

loc = get_geolocation()
st.write(f'{loc}')

location = [loc]
st.write(location)



# latitud = list(loc['coords']['latitude'])[0]
# longitud = list(loc['coords']['longitude'])[0]
# st.write(f'{latitud}, {longitud}')



