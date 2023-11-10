import streamlit as st

from streamlit_js_eval import streamlit_js_eval


width = streamlit_js_eval(js_expressions='screen.width', want_output = True, key = 'SCR')


def disp_width():
    to_display = f"Screen width is _{width}_"
    
    print(to_display)


st.button("Display Screen Width", on_click=disp_width)
disp_width()
