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
        # Filter only image files
        files = os.listdir(folder)
        image_files = [file for file in files if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        return image_files
    return []

def capture_page():
    st.header("Capture Image")
    # Choose a folder (or enter a custom folder name)
    folder_options = ["Folder1", "Folder2", "Folder3"]
    folder = st.selectbox("Select a folder to save images", options=folder_options)
    custom_folder = st.text_input("Or enter a custom folder name:", value=folder)
    if custom_folder:
        folder = custom_folder

    # Create the folder if it doesn't exist.
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
    st.header(f"Gallery - {folder}")
    if not os.path.exists(folder):
        st.write("Folder does not exist. No images to display.")
    else:
        image_files = list_folder_contents(folder)
        if image_files:
            for img_file in image_files:
                full_path = Path(folder) / img_file
                st.image(str(full_path), caption=img_file, use_column_width=True)
        else:
            st.write("No images found in this folder.")

def main():
    st.title("Camera App with Folder Gallery")
    
    # Sidebar toolbar for navigation.
    nav_options = ["Capture", "Gallery: Folder1", "Gallery: Folder2", "Gallery: Folder3"]
    selection = st.sidebar.radio("Navigation", nav_options)
    
    if selection == "Capture":
        capture_page()
    elif selection == "Gallery: Folder1":
        gallery_page("Folder1")
    elif selection == "Gallery: Folder2":
        gallery_page("Folder2")
    elif selection == "Gallery: Folder3":
        gallery_page("Folder3")

if __name__ == "__main__":
    main()
