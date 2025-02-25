import os
import re
import argparse

PRIORITY_FOLDERS = ["@ Bads", "@ Other", "@ Weak", "@ Dead"]  # Folders to scan first
IGNORE_FOLDERS = ["- Theory"]  # Folders to ignore

def extract_info_from_mhtml(file_path):
    """Extracts Content-Location (URL) and Subject from an MHTML file."""
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Extract Content-Location (URL)
        url_match = re.search(r'Content-Location:\s*(https?://[^\s]+)', content)
        url = url_match.group(1) if url_match else "Unknown URL"

        # Extract Subject
        subject_match = re.search(r'Subject:\s*(.+)', content)
        subject = subject_match.group(1).strip() if subject_match else "No Subject"

        return url, subject
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def scan_folder(folder_path, md_file):
    """Scans a folder for MHTML files and writes to the markdown file."""
    for root, dirs, files in os.walk(folder_path):
        # Skip folders containing '- Theory' in their name (both direct and subfolder levels)
        dirs[:] = [d for d in dirs if '- Theory' not in d]

        # Skip the root folder itself if it contains '- Theory'
        if '- Theory' in root:
            print(f"Skipping folder: {root}")
            continue

        for filename in files:
            if filename.endswith(".mhtml"):
                file_path = os.path.join(root, filename)
                url, subject = extract_info_from_mhtml(file_path)
                if url and subject:
                    # Check if folder is a priority folder and write its name
                    if any(priority_folder in root for priority_folder in PRIORITY_FOLDERS):
                        folder_name = next(priority_folder for priority_folder in PRIORITY_FOLDERS if priority_folder in root)
                        md_file.write(f"{folder_name}\n")
                    md_file.write(f"[{url}] - {subject}\n")
                    print(f"Extracted: {url} - {subject}")

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

def scan_folders_and_create_md(root_folder, output_md_path):
    """Scans subfolders, prioritizes certain folders, and creates a Markdown file."""
    
    with open(output_md_path, "w", encoding="utf-8") as md_file:
        # Scan non-priority folders first
        for foldername in sorted(os.listdir(root_folder)):  # Sort for consistency
            folder_path = os.path.join(root_folder, foldername)
            if os.path.isdir(folder_path) and foldername not in PRIORITY_FOLDERS:
                print(f"Scanning: {folder_path}")
                scan_folder(folder_path, md_file)

        # Scan priority folders last
        for folder in PRIORITY_FOLDERS:
            folder_path = os.path.join(root_folder, folder)
            if os.path.isdir(folder_path):
                print(f"Scanning priority folder: {folder_path}")
                scan_folder(folder_path, md_file)

    print(f"Markdown file saved at: {output_md_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan MHTML files and extract information into a markdown file.")
    parser.add_argument("root_folder", help="Path to the root folder to scan.")
    parser.add_argument("output_md", nargs="?", help="Path to save the output markdown file.")
    
    args = parser.parse_args()
    
    # If output path is not provided, use the root folder with default filename
    if args.output_md is None:
        args.output_md = os.path.join(args.root_folder, "README.md")
    
    scan_folders_and_create_md(args.root_folder, args.output_md)