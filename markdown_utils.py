import os

def get_unique_md_path(output_md_path):
    """Generates a unique markdown file path if the file already exists."""
    if not os.path.exists(output_md_path):
        return output_md_path
    
    base, ext = os.path.splitext(output_md_path)
    counter = 1
    new_output_md_path = f"{base}_{counter}{ext}"
    
    while os.path.exists(new_output_md_path):
        counter += 1
        new_output_md_path = f"{base}_{counter}{ext}"
    
    return new_output_md_path 