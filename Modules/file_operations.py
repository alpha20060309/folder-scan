import re

def extract_info_from_mhtml(file_path):
    """Extracts Content-Location (URL) and Subject from an MHTML file."""
    try:
        with open(file_path, 'rb') as f:  # Open in binary mode
            content = f.read().decode("utf-8", errors="ignore")  # Decode to string

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