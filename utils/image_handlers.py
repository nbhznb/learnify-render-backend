# utils/image_handlers.py
import os

def delete_images(*filepaths):
    static_dir = os.path.join(os.getcwd(), 'static')
    for filepath in filepaths:
        full_path = os.path.join(static_dir, filepath)
        try:
            if os.path.exists(full_path):
                os.remove(full_path)
                print(f"Deleted {filepath}")
            else:
                print(f"File already deleted or does not exist: {filepath}")
        except Exception as e:
            print(f"Error deleting {filepath}: {e}")

def ensure_static_folders():
    """
    Ensure that the necessary static folders exist.
    This should be called at startup.
    """
    static_dirs = ['static', 'static/result', 'static/tmp', 'static/data']
    for directory in static_dirs:
        folder_path = os.path.join(os.getcwd(), directory)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Ensured directory exists: {folder_path}")

def cleanup_static_folders():
    """
    Clean up temporary files in static folders.
    This should be called at startup.
    """
    # First ensure the directories exist
    ensure_static_folders()
    
    # Then clean up files in these directories
    static_dirs = ['static/result', 'static/tmp']
    for directory in static_dirs:
        folder_path = os.path.join(os.getcwd(), directory)
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
