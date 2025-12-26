import streamlit as st
import os
import re
from PIL import Image

# Page config
st.set_page_config(page_title="WRF Plot Viewer", layout="wide")

st.title("📊 MMS WRF Dashboard")

# Define the directory
PLOT_DIR = "plot"

def natural_sort_key(s):
    """Sorts strings containing numbers in human order (1, 2, 10 instead of 1, 10, 2)"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

# 1. Check if folder exists
if os.path.exists(PLOT_DIR):
    # 2. Get all images and sort them correctly
    all_files = os.listdir(PLOT_DIR)
    plot_files = [f for f in all_files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    plot_files.sort(key=natural_sort_key)

    if plot_files:
        # 3. Sidebar Dropdown Menu
        st.sidebar.header("Navigation")
        selected_plot = st.sidebar.selectbox(
            "Select Plot File:", 
            options=plot_files
        )

        # 4. Main Display Area
        st.subheader(f"Current View: {selected_plot}")
        
        image_path = os.path.join(PLOT_DIR, selected_plot)
        img = Image.open(image_path)
        
        # Display the image
        st.image(img, use_container_width=True)
        
        # Optional: File info
        st.caption(f"File location: {image_path} | Total plots: {len(plot_files)}")

    else:
        st.error("No images found in the 'plot' folder. Please check your file extensions (.png, .jpg).")
else:
    st.error(f"Directory '{PLOT_DIR}' not found. Ensure the folder is in your GitHub repo.")

# --- Troubleshooting Helper ---
with st.expander("Debug: See all files in folder"):
    st.write(os.listdir(PLOT_DIR) if os.path.exists(PLOT_DIR) else "Folder not found")
