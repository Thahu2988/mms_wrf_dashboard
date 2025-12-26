import streamlit as st
import os
import re
from PIL import Image

st.set_page_config(page_title="WRF Dashboard", layout="wide")

# 1. FIX: Force Streamlit to re-scan the folder by clearing cache
if st.sidebar.button("🔄 Refresh Plots"):
    st.cache_data.clear()

st.title("🌪️ MMS WRF Dashboard")

# 2. Path Setup
# Using os.getcwd() ensures we are looking in the root of the deployed app
PLOT_DIR = os.path.join(os.getcwd(), "plot")

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# 3. Enhanced File Search
if os.path.exists(PLOT_DIR):
    # This grabs ALL images, even if they have different extensions
    plot_files = [
        f for f in os.listdir(PLOT_DIR) 
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))
    ]
    plot_files.sort(key=natural_sort_key)

    if plot_files:
        st.sidebar.success(f"✅ Found {len(plot_files)} plots")
        
        # Selection UI
        selected_plot = st.sidebar.select_slider(
            "Move through timeline", 
            options=plot_files
        )
        
        # Display
        image_path = os.path.join(PLOT_DIR, selected_plot)
        img = Image.open(image_path)
        
        st.subheader(f"Current Plot: `{selected_plot}`")
        st.image(img, use_container_width=True)
        
    else:
        st.error("The folder was found, but it appears empty. Check your file extensions.")
else:
    st.error(f"Cannot find folder: {PLOT_DIR}")
    # Show what folders DO exist to help debug
    st.write("Available folders:", os.listdir("."))
