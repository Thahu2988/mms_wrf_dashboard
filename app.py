import streamlit as st
import os
import re
from PIL import Image

st.set_page_config(page_title="WRF Plot Viewer", layout="wide")

st.title("🌪️ MMS WRF Dashboard")

# 1. Folder Path
PLOT_DIR = "plot"

def natural_sort_key(s):
    """Ensures 03.png comes before 10_wind.png"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

if os.path.exists(PLOT_DIR):
    # 2. Get all images and sort them
    all_files = os.listdir(PLOT_DIR)
    plot_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    plot_files.sort(key=natural_sort_key)

    if plot_files:
        # 3. Sidebar Dropdown Menu
        st.sidebar.header("Controls")
        selected_plot = st.sidebar.selectbox(
            "Choose a Plot:", 
            options=plot_files,
            index=0  # Defaults to the first plot
        )

        # 4. Display Logic
        st.subheader(f"Showing: {selected_plot}")
        image_path = os.path.join(PLOT_DIR, selected_plot)
        
        try:
            img = Image.open(image_path)
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")

        # --- DEBUG SECTION ---
        # This helps us find why only 4 are visible
        with st.expander("🛠️ Debug: See all files found"):
            st.write(f"Total files in folder: {len(all_files)}")
            st.write(f"Valid images found: {len(plot_files)}")
            st.write("List of all files discovered:", all_files)
            
    else:
        st.error(f"No .png or .jpg files found in /{PLOT_DIR}")
        st.write("Files actually present:", all_files)
else:
    st.error(f"Folder '{PLOT_DIR}' not found. Please check your GitHub structure.")
