import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("pags/0_Havas.py", "HAVAS group", "💻"),  
        Page("pags/1_Tu_grupo.py", "NEW group", "⚙️"),  
        Page("pags/2_Mapa.py", "Localizador", "🌍")    
    ]
)
