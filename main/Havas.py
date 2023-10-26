import streamlit as st
from st_pages import Page, show_pages, add_page_title
from collections import Counter
from PIL import Image
import base64
import io
import datetime
from datetime import datetime, time, timedelta
import re
import streamlit.components.v1 as components
import time as timee
import os
#import pywhatkit

st.set_page_config(layout="wide", page_title="Ruta del Café", page_icon="./img/cafe5.png")

show_pages(
    [
        Page(Havas_group, "HAVAS group", "💻"),  
        Page("pags/1_Tu_grupo.py", "NEW group", "⚙️"),  
        Page("pags/2_Mapa.py", "Localizador", "🌍")    
    ]
)
