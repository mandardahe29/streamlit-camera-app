import streamlit as st
import os
import datetime
from pathlib import Path
from PIL import Image

# ------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------
def list_subfolders(base="."):
    """
    Return a list of subfolders in the given base directory,
    skipping hidden folders (those starting with '.').
    """
    if not os.path.exists(base):
        return []
    return [
        f for f in os.listdir(base)
        if os.path.isdir(os.path.join(base, f)) and not f.startswith(".")
    ]

def save_image(image, folder_path):
    """
    Save the uploaded image to the specified folder with a timestamped filename.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_{timestamp}.png"
    save_path = Path(folder_path) / filename
    with open(save_path, "wb") as f:
        f.write(image.getbuffer())
    return save_path

def list_image_files(folder):
    """
    Return a list of image filenames in the given folder.
    """
    if os.path.exists(folder):
        files = os.listdir(folder)
        image_files = [
            file for file in files
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))
        ]
        return image_files
    return []

# ------------------------------------------------------------------------
# Page: Capture
# ------------------------------------------------------------------------
def capture_page(folder):
    """
    Page to capture multiple images using the camera
    and save them to `folder`.
    """
    st.header("Capture Images")
    st.write(f"Images will be saved in: **{folder}**")

    # Ensure the folder exists.
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
        st.info(f"Created folder: {folder}")

    # Keep track of all captured images this session in st.session_state
    if "captured_images" not in st.session_state:
        st.session_state["captured_images"] = []

    # Camera input widget (always visible so you can take multiple shots).
    image = st.camera_input("Take a picture")

    if image is not None:
        # Save the image to the folder
        saved_path = save_image(image, folder)
        st.session_state["captured_images"].append(str(saved_path))
        st.success(f"Image saved at: {saved_path}")

    # Display all images captured in this session
    if st.session_state["captured_images"]:
        st.write("Photos captured **this session**:")
        for i, path in enumerate(st.session_state["captured_images"], start=1):
            st.image(path, caption=f"Photo {i}", use_column_width=True)

# ------------------------------------------------------------------------
# Page: Gallery
# ------------------------------------------------------------------------
def gallery_page():
    """
    Page to view images in any subfolder of the current directory.
    """
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

# ------------------------------------------------------------------------
# Main app
# ------------------------------------------------------------------------
def main():
    st.title("Camera App with Advanced Folder & Multiple Photos")

    # --- Sidebar: Folder selection and navigation ---
    st.sidebar.header("Folder Settings")
    
    # 1) List existing folders
    existing_folders = list_subfolders(".")
    
    # 2) Dropdown to pick an existing folder
    selected_existing = ""
    if existing_folders:
        selected_existing = st.sidebar.selectbox(
            "Select an existing folder:", 
            options=["(None)"] + existing_folders,  # let user pick or skip
            index=0
        )
        if selected_existing == "(None)":
            selected_existing = ""  # means user hasn't chosen from existing
    
    # 3) Text input to type a custom folder name
    custom_folder = st.sidebar.text_input(
        "Or type a custom folder name (leave blank to use existing):", 
        value=""
    )

    # Decide which folder to use
    if custom_folder.strip():
        folder = custom_folder.strip()
        if folder in existing_folders:
            st.sidebar.info(f"Folder '{folder}' already exists.")
        else:
            st.sidebar.warning(f"Folder '{folder}' does not exist yet; it will be created.")
    else:
        # If no custom folder typed, use the one from the dropdown (if any)
        folder = selected_existing
    
    if not folder:
        folder = "Folder1"  # Fallback if user hasn't selected or typed anything

    # --- Sidebar: Navigation ---
    nav_options = ["Capture", "Gallery"]
    selection = st.sidebar.radio("Navigation", nav_options)
    
    if selection == "Capture":
        capture_page(folder)
    elif selection == "Gallery":
        gallery_page()

if __name__ == "__main__":
    main()
