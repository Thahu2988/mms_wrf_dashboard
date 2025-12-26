import streamlit as st
import os
import re
from PIL import Image

st.set_page_config(page_title="WRF Forecast Viewer", layout="wide")

# Custom CSS to make the UI cleaner
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌪️ MMS WRF Dashboard")

PLOT_DIR = "plot"

def natural_sort_key(s):
    """Sorts strings containing numbers in human order (e.g., 2 before 10)"""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

if os.path.exists(PLOT_DIR):
    # Filter for images and sort them numerically
    plot_files = [f for f in os.listdir(PLOT_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    plot_files.sort(key=natural_sort_key)

    if plot_files:
        # Sidebar Navigation
        st.sidebar.header("Navigation Control")
        
        # Method 1: Slider for quick scrubbing through time/frames
        idx = st.sidebar.slider("Timeline Step", 0, len(plot_files) - 1, 0)
        
        # Method 2: Manual Dropdown
        selected_plot = st.sidebar.selectbox("Select Specific Plot", plot_files, index=idx)
        
        # Display the selected image
        image_path = os.path.join(PLOT_DIR, selected_plot)
        
        st.subheader(f"Current Plot: `{selected_plot}`")
        
        # Load and display
        img = Image.open(image_path)
        st.image(img, use_container_width=True, caption=f"WRF Output: {selected_plot}")

        # Metrics/Details (Optional)
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"Total Plots available: {len(plot_files)}")
        with col2:
            st.success(f"File Path: {image_path}")
            
    else:
        st.error("The 'plot' folder is empty.")
else:
    st.error(f"Folder '{PLOT_DIR}' not found. Please check your GitHub repo structure.")
