from typing import List, Dict, Optional

from pygments.lexers.webassembly import keywords

from .google_drive_utils import GoogleDriveUtility
from .keywords import extract_keywords


def make_dictionaries(
        files: List[Dict],
        updated_date: str,
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
            file_title = file["title"]
            file_title_clean = _sanitize_filename(file_title)

            # Check if file is for leaders only
            if "KUN FOR LEDER" in file_title:
                forLeaders = True
                file_title = file_title.replace("- KUN FOR LEDERE", "").replace("- KUN FOR LEDER", "").strip()
            else:
                forLeaders = False

            # Determine file type and read content
            file_text = _read_file_content(file, file_title)

            # Process URL if requested
            url, file_text = _extract_url(file_text)

            # Get keywords from the document text
            keywords = _create_keywords(file_text)

            # Create file dictionary
            file_dict = {
                "title": file_title_clean,
                "body": file_text,
                "LAST UPDATED": updated_date,
                "URL": url,
                "tags": keywords,
                "forLeaders": forLeaders
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
    # Replace problematic characters
    filename_clean = filename.replace("?", "_").replace("/", "_")
    # Remove extensions
    filename_clean = filename_clean.replace(".docx", "").replace(".txt", "")
    # Remove whitespace
    filename_clean = filename_clean.strip()
    return filename_clean


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
    file_type = file["file_type"]
    return GoogleDriveUtility.read_google_doc(file["id"], file_type=file_type)


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
    # Check if first line is URL
    if "https" in lines[0]:
        url = (lines[0].replace("\ufeff", ""))
        url = url.replace('Dokument URL:', "")
        url = url.strip()
    else:
        url = ""

    # Return URL and the rest of the document
    return url, " ".join(lines[1:])

def _create_keywords(file_text: str) -> List[str]:
    """
    Extract keywords from the document text.

    Args:
        file_text: Full document text

    Returns:
        List of extracted keywords
    """
    # Split text into words
    keywords = extract_keywords(file_text)
    return keywords

if __name__ == "__main__":
    files = GoogleDriveUtility.list_all_files(
        folder_id="12E8sK7BqYrplpL9UWtXB4I3D6QvvZxDN"
    )

    print(make_dictionaries(files, updated_date="2024-11-01", has_url=True))