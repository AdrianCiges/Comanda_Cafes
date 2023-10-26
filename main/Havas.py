import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("pags/Havas.py", "HAVAS group", "💻"),  
        Page("pags/Tu_grupo.py", "NEW group", "⚙️"),  
        Page("pags/Mapa.py", "Localizador", "🌍")    
    ]
)
