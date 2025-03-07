import streamlit as st
import os
import datetime
from pathlib import Path

def save_image(image, folder_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.png"
    save_path = Path(folder_path) / filename
    with open(save_path, "wb") as f:
        f.write(image.getbuffer())
    return save_path

def main():
    st.title("Mobile Camera Capture & Save")

    st.markdown("""
    **Instructions:**
    - This app allows you to capture an image using your phone’s camera and save it.
    - **Note:** When hosted on Streamlit Community Cloud, the saved images reside on the cloud's ephemeral storage.
    """)

    # Predefined folder options (ephemeral, within the container)
    folder_options = ["Folder1", "Folder2", "Folder3"]
    default_folder = "Folder1"
    
    folder = st.selectbox("Select a folder to save images", options=folder_options)
    
    # Create folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
        st.info(f"Created folder: {folder}")
    
    # Allow override with custom folder name
    custom_folder = st.text_input("Or enter a custom folder name:", value=folder)
    if custom_folder:
        folder = custom_folder
        if not os.path.exists(folder):
            os.makedirs(folder)
            st.info(f"Created folder: {folder}")
    
    # Use the camera input widget.
    image = st.camera_input("Take a picture")

    if image is not None:
        saved_path = save_image(image, folder)
        st.success(f"Image saved at: {saved_path}")
        st.image(saved_path, caption="Saved Image", use_column_width=True)
    
    if os.path.exists("Folder1"):
        st.write("Files in Folder1:", os.listdir("Folder1"))

if __name__ == "__main__":
    main()
