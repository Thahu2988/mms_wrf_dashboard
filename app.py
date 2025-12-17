import streamlit as st
import os

# 1. Page Configuration
st.set_page_config(page_title="Daily WRF Forecast", layout="wide")

st.title("MMS:WRF Model Dashboard")
st.write("Automatically updated every night at 23:00 hrs.")

# 2. Define the folder where GitHub stores your images
IMAGE_FOLDER = "products"

# 3. Create the list of expected products (pptn-5 to pptn-23)
# This matches the filenames being uploaded from your server
product_list = [f"pptn-{i}.png" for i in range(5, 24)]

# 4. Sidebar Dropdown for selection
with st.sidebar:
    st.header("Settings")
    selected_file = st.selectbox(
        "Select Forecast Hour:",
        options=product_list,
        index=0  # Default to show pptn-5.png
    )

# 5. Display Logic
if os.path.exists(os.path.join(IMAGE_FOLDER, selected_file)):
    # Display the selected plot
    st.subheader(f"Visualizing Product: {selected_file}")
    
    # use_container_width=True makes the image fit the screen perfectly
    st.image(
        os.path.join(IMAGE_FOLDER, selected_file), 
        caption=f"Latest WRF Output - {selected_file}",
        use_container_width=True
    )
else:
    # If the file hasn't uploaded yet, show a friendly message
    st.warning(f"Searching for {selected_file}... If the model is still running, please check back in a few minutes.")

    st.info("Note: The server syncs new data daily at 23:00.")
