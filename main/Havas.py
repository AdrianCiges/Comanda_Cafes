import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("pages/0_Havas.py", "HAVAS group", "💻"),  
        Page("pages/1_Tu_grupo.py", "NEW group", "⚙️"),  
        Page("pages/2_Mapa.py", "Localizador", "🌍")    
    ]
)
