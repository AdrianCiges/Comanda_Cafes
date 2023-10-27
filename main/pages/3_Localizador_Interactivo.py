import streamlit as st
import streamlit_js_eval

# Returns user's location after asking for permission when the user clicks the generated link with the given text
location = get_geolocation()
# The URL parts of the page
location_json = get_page_location()
