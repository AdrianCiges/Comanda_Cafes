import streamlit as st
import pandas as pd
from collections import Counter
from PIL import Image
import base64
import io
import datetime
from datetime import datetime, time, timedelta
import re
import streamlit.components.v1 as components
import time as timee

# Coordinates of Madrid
data = pd.DataFrame({
    'lat': [40.4168],
    'lon': [-3.7038]
})

# Create a map centered around coordinates
st.map(data, zoom=12)
