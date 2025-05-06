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

def cleanup_static_folders():
    static_dirs = ['static/result', 'static/tmp']
    for directory in static_dirs:
        folder_path = os.path.join(os.getcwd(), directory)
        if os.path.exists(folder_path):
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Deleted {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
