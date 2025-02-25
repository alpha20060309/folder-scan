import os
from Modules.file_operations import extract_info_from_mhtml

PRIORITY_FOLDERS = {"@ Bads", "@ Other", "@ Weak", "@ Dead"}  # Use a set for faster membership checking

def scan_folder(folder_path, md_file):
    """Scans a folder for MHTML files and writes to the markdown file."""
    extracted_entries = []  # List to accumulate entries for batch writing
    mhtml_files = []  # List to collect MHTML files for batch processing
    
    # First pass: collect all MHTML files
    for root, dirs, files in os.walk(folder_path):
        # Skip folders containing '- Theory' in their name (both direct and subfolder levels)
        dirs[:] = [d for d in dirs if '- Theory' not in d]

        # Skip the root folder itself if it contains '- Theory'
        if '- Theory' in root:
            print(f"Skipping folder: {root}")
            continue

        # Collect all MHTML files in this directory
        mhtml_files.extend(
            os.path.join(root, filename)
            for filename in files
            if filename.endswith(".mhtml")
        )
    
    # Process files in parallel if we have multiple files
    if mhtml_files:
        print(f"Processing {len(mhtml_files)} files in parallel...")
        results = process_files_in_parallel(mhtml_files)
        
        # Process results and create entries
        for file_path, (url, subject) in zip(mhtml_files, results):
            if url and subject:
                # Check if folder is a priority folder and write its name
                root = os.path.dirname(file_path)
                if any(priority_folder in root for priority_folder in PRIORITY_FOLDERS):
                    folder_name = next(priority_folder for priority_folder in PRIORITY_FOLDERS if priority_folder in root)
                    extracted_entries.append(f"{folder_name}\n")
                extracted_entries.append(f"[{url}] - {subject}\n")
                print(f"Extracted: {url} - {subject}")

    # Write all entries to the markdown file at once
    md_file.writelines(extracted_entries)

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