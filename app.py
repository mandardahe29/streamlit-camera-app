import streamlit as st
import os
import datetime
from pathlib import Path
from PIL import Image

def save_image(image, folder_path):
    """Save the uploaded image to the specified folder with a timestamped filename."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.png"
    save_path = Path(folder_path) / filename
    with open(save_path, "wb") as f:
        f.write(image.getbuffer())
    return save_path

def list_image_files(folder):
    """Return a list of image filenames in the given folder."""
    if os.path.exists(folder):
        files = os.listdir(folder)
        image_files = [
            file for file in files
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        return image_files
    return []

def list_subfolders(base="."):
    """
    Return a list of subfolders in the given base directory.
    Skips hidden folders (those starting with '.').
    """
    if not os.path.exists(base):
        return []
    return [
        f for f in os.listdir(base)
        if os.path.isdir(f) and not f.startswith(".")
    ]

def capture_page(folder):
    """Page to capture images using the camera and save them to `folder`."""
    st.header("Capture Image")
    st.write(f"Images will be saved in: **{folder}**")
    
    # Ensure the folder exists.
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        st.info(f"Created folder: {folder}")
    
    # Camera input widget.
    image = st.camera_input("Take a picture")
    
    if image is not None:
        saved_path = save_image(image, folder)
        st.success(f"Image saved at: {saved_path}")
        st.image(str(saved_path), caption="Saved Image", use_column_width=True)

def gallery_page():
    """Page to view images in any subfolder of the current directory."""
    st.header("Gallery")

    # List all subfolders in the current directory
    folders = list_subfolders(".")
    
    if not folders:
        st.write("No folders found. Try capturing an image first!")
        return
    
    # Let the user pick which folder to view
    selected_folder = st.selectbox("Select a folder to view images:", folders)
    
    # Show the images in the selected folder
    image_files = list_image_files(selected_folder)
    if image_files:
        st.write(f"Showing images in **{selected_folder}**:")
        for img_file in image_files:
            full_path = Path(selected_folder) / img_file
            st.image(str(full_path), caption=img_file, use_column_width=True)
    else:
        st.write(f"No images found in **{selected_folder}**.")

def main():
    st.title("Camera App with Dynamic Folder & Gallery")

    # Sidebar: Custom folder name
    st.sidebar.header("Settings")
    folder = st.sidebar.text_input("Enter custom folder name:", value="Folder1")

    # Sidebar navigation
    nav_options = ["Capture", "Gallery"]
    selection = st.sidebar.radio("Navigation", nav_options)
    
    if selection == "Capture":
        capture_page(folder)
    elif selection == "Gallery":
        gallery_page()

if __name__ == "__main__":
    main()
