import streamlit as st
import os
import datetime
from pathlib import Path
from PIL import Image

def save_image(image, folder_path):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.png"
    save_path = Path(folder_path) / filename
    with open(save_path, "wb") as f:
        f.write(image.getbuffer())
    return save_path

def list_folder_contents(folder):
    if os.path.exists(folder):
        # Only list common image types.
        files = os.listdir(folder)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return image_files
    return []

def capture_page(folder):
    st.header("Capture Image")
    st.write(f"Images will be saved in: **{folder}**")
    
    # Ensure the folder exists.
    if not os.path.exists(folder):
        os.makedirs(folder)
        st.info(f"Created folder: {folder}")
    
    # Camera input widget.
    image = st.camera_input("Take a picture")
    
    if image is not None:
        saved_path = save_image(image, folder)
        st.success(f"Image saved at: {saved_path}")
        st.image(str(saved_path), caption="Saved Image", use_column_width=True)

def gallery_page(folder):
    st.header(f"Gallery for folder: {folder}")
    
    if not os.path.exists(folder):
        st.write("Folder does not exist yet. Capture an image first!")
    else:
        image_files = list_folder_contents(folder)
        if image_files:
            for img_file in image_files:
                full_path = Path(folder) / img_file
                st.image(str(full_path), caption=img_file, use_column_width=True)
        else:
            st.write("No images found in this folder.")

def main():
    st.title("Camera App with Dynamic Folder Selection")
    
    # Sidebar: Custom folder name and navigation.
    st.sidebar.header("Settings")
    # Enter a custom folder name; default is 'Folder1'
    folder = st.sidebar.text_input("Enter custom folder name:", value="Folder1")
    # Auto-create the folder if it doesn't exist.
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        st.sidebar.info(f"Created folder: {folder}")
    
    # Sidebar navigation.
    nav_options = ["Capture", "Gallery"]
    selection = st.sidebar.radio("Navigation", nav_options)
    
    # Show the appropriate page.
    if selection == "Capture":
        capture_page(folder)
    elif selection == "Gallery":
        gallery_page(folder)

if __name__ == "__main__":
    main()
