from src.make_dictionaries import make_dictionaries
from src.google_drive_utils import GoogleDriveUtility

has_url = False   # is the first line of the document a URL?
updated_date = None   # date of current update, None if not updated
folder_id = "1a_6_-TrJe8srDlxPRC3kvQWf1bErR4aN" # id of folder in google drive

# List all files in the folder
files = GoogleDriveUtility.list_all_files(
        folder_id=folder_id
    )

# Create a list of dictionaries for the files
list_of_dictionaries = make_dictionaries(files, updated_date="2024-11-01")

if __name__ == "__main__":
    print(list_of_dictionaries)
