import streamlit as st
from st_pages import Page, show_pages, add_page_title

show_pages(
    [
        Page("Havas.py", "HAVAS group", "💻"),  
        Page("../main/pages/1_Tu_grupo.py", "NEW group", "⚙️"),  
        Page("../main/pages/2_Mapa.py", "Localizador", "🌍")    
    ]
)
