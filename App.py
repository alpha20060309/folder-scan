import os
import argparse
from folder_scanner import scan_folders_and_create_md
from markdown_utils import get_unique_md_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scan MHTML files and extract information into a markdown file.")
    parser.add_argument("root_folder", help="Path to the root folder to scan.")
    parser.add_argument("output_md", nargs="?", help="Path to save the output markdown file.")
    
    args = parser.parse_args()
    
    # If output path is not provided, use the root folder with default filename
    if args.output_md is None:
        args.output_md = os.path.join(args.root_folder, "README.md")
    
    scan_folders_and_create_md(args.root_folder, args.output_md) 