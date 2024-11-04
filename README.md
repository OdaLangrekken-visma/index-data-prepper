# Google Drive Utility Project

This project provides utilities for interacting with Google Drive, including listing files in a folder and reading the content of Google Docs and other file types. It also includes functionality to convert these files into dictionaries for further processing.

## Features

- List all files in a specified Google Drive folder.
- Read the content of Google Docs, DOCX, and TXT files from Google Drive.
- Convert file metadata and content into dictionaries.

## Requirements

- Python 3.7+
- `pip` for managing Python packages

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/google-drive-utility.git
    cd google-drive-utility
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up Google API credentials:
    - Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
    - Enable the Google Drive API for your project.
    - Create OAuth 2.0 credentials and download the `client_secrets.json` file.
    - Place the `client_secrets.json` file in the root directory of the project.

## Usage

### Listing Files

To list all files in a specified Google Drive folder, use the `list_all_files` method from the `GoogleDriveUtility` class.

### Reading Google Docs

To read the content of a Google Doc, DOCX, or TXT file, use the `read_google_doc` method from the `GoogleDriveUtility` class.

### Converting Files to Dictionaries

To convert a list of Google Drive files into dictionaries, use the `make_dictionaries` function.

### Example

Here is an example of how to use the utilities in this project:

```python
from src.make_dictionaries import make_dictionaries
from src.google_drive_utils import GoogleDriveUtility

has_url = False   # is the first line of the document a URL?
updated_date = "2024-11-01"   # date of current update
folder_id = "1a_6_-TrJe8srDlxPRC3kvQWf1bErR4aN" # id of folder in google drive

# List all files in the folder
files = GoogleDriveUtility.list_all_files(folder_id=folder_id)

# Create a list of dictionaries for the files
list_of_dictionaries = make_dictionaries(files, updated_date=updated_date, has_url=True)

print(list_of_dictionaries)
