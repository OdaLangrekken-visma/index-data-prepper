from typing import List, Dict, Optional
from google_drive_utils import GoogleDriveUtility


def make_dictionaries(
        files: List[Dict],
        updated_date: str,
        has_url: bool = False
) -> List[Dict]:
    """
    Convert a list of Google Drive files into a list of dictionaries.

    Args:
        files: List of file metadata dictionaries
        updated_date: Date of last update
        has_url: Whether to extract a URL from the first line of the document

    Returns:
        List of processed file dictionaries
    """
    list_of_dictionaries = []

    for file in files:
        try:
            # Sanitize file title
            file_title = _sanitize_filename(file["title"])

            # Determine file type and read content
            file_text = _read_file_content(file, file_title)

            # Process URL if requested
            url, file_text = _extract_url(file_text) if has_url else ("", file_text)

            # Create file dictionary
            file_dict = {
                "title": file_title,
                "body": file_text,
                "LAST UPDATED": updated_date,
                "URL": url
            }

            list_of_dictionaries.append(file_dict)

        except Exception as e:
            print(f"Error processing file {file.get('title', 'Unknown')}: {e}")
            continue

    return list_of_dictionaries


def _sanitize_filename(filename: str) -> str:
    """
    Remove or replace problematic characters from filename.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    return filename.replace("?", "_").replace("/", "_")


def _read_file_content(
        file: Dict,
        file_title: str
) -> str:
    """
    Read file content based on file type.

    Args:
        file: File metadata dictionary
        file_title: Sanitized filename

    Returns:
        File content as a string
    """
    if ".docx" in file_title:
        return GoogleDriveUtility.read_google_doc(file["id"], file_type="docx")
    elif ".txt" in file_title:
        return GoogleDriveUtility.read_google_doc(file["id"], file_type="txt")
    else:
        return GoogleDriveUtility.read_google_doc(file["id"], is_docx="google_doc")


def _extract_url(
        file_text: str
) -> tuple[str, str]:
    """
    Extract URL from the first line of the document if present.

    Args:
        file_text: Full document text

    Returns:
        Tuple of (URL, document text without URL)
    """
    # Remove potential BOM (Byte Order Mark)
    lines = file_text.split("\n")
    url = lines[0].replace("\ufeff", "").strip()

    # Return URL and the rest of the document
    return url, " ".join(lines[1:])

files = GoogleDriveUtility.list_all_files(
        folder_id="1a_6_-TrJe8srDlxPRC3kvQWf1bErR4aN"
)

print(make_dictionaries(files, updated_date="2024-11-01", has_url=True))