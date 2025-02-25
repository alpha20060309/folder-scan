import re
import os
from multiprocessing import Pool

# Compile regex patterns for better performance
URL_PATTERN = re.compile(r'Content-Location:\s*(https?://[^\s]+)')
SUBJECT_PATTERN = re.compile(r'Subject:\s*(.+)')

# Maximum file size to process (50MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

def extract_info_from_mhtml(file_path):
    """Extracts Content-Location (URL) and Subject from an MHTML file."""
    try:
        # Check file size before processing
        if os.path.getsize(file_path) > MAX_FILE_SIZE:
            print(f"Skipping large file {file_path}: exceeds {MAX_FILE_SIZE/1024/1024:.1f}MB")
            return None, None

        with open(file_path, 'rb') as f:
            # Read only the first 8KB which usually contains the headers
            content = f.read(8192).decode("utf-8", errors="ignore")

        # Extract URL using compiled pattern
        url_match = URL_PATTERN.search(content)
        url = url_match.group(1) if url_match else "Unknown URL"

        # Extract Subject using compiled pattern
        subject_match = SUBJECT_PATTERN.search(content)
        subject = subject_match.group(1).strip() if subject_match else "No Subject"

        return url, subject
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None, None

def process_files_in_parallel(file_paths, num_processes=None):
    """Process multiple files in parallel using multiprocessing."""
    with Pool(processes=num_processes) as pool:
        results = pool.map(extract_info_from_mhtml, file_paths)
    return results 