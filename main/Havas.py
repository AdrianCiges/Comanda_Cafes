import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("pages/Havas.py", "HAVAS group", "💻"),  
        Page("pages/Tu_grupo.py", "NEW group", "⚙️"),  
        Page("pages/Mapa.py", "Localizador", "🌍")    
    ]
)
