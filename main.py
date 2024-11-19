from src.make_dictionaries import make_dictionaries
from src.google_drive_utils import GoogleDriveUtility
import json
import os

updated_date = "2024-11-19"   # date of current update, None if not updated

flyt_google = "12E8sK7BqYrplpL9UWtXB4I3D6QvvZxDN"
flyt_handbook = "14aOEADB1riPDJXn76n-JobXOeIWBeEbY"

# List all files in the folder
files = GoogleDriveUtility.list_all_files(
        folder_id=flyt_handbook
    )

print(files)

# Create a list of dictionaries for the files
list_of_dictionaries = make_dictionaries(files, updated_date=updated_date)

output_folder = "personal"

if __name__ == "__main__":
    if output_folder:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        for result in list_of_dictionaries:
            json_title = result["title"] + ".json"
            with open(os.path.join(output_folder, json_title), "w", encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=4)



