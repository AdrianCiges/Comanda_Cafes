import streamlit as st
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json

def get_user_loc():
    loc = get_geolocation()
    return loc['coords']['latitude']}, loc['coords']['longitude']}
