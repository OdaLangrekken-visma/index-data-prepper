from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime


def authenticate_google_drive():
    """
    Handle Google Drive authentication and credential management.

    Returns:
        GoogleDrive: Authenticated Google Drive client
    """
    gauth = GoogleAuth()
    credentials_path = "credentials.txt"

    try:
        # Try to load existing credentials
        gauth.LoadCredentialsFile(credentials_path)

        if gauth.credentials is None:
            # No saved credentials, perform web authentication
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh expired credentials
            gauth.Refresh()
        else:
            # Use existing valid credentials
            gauth.Authorize()

        # Always save the latest credentials
        gauth.SaveCredentialsFile(credentials_path)

        return GoogleDrive(gauth)

    except Exception as e:
        print(f"Authentication error: {e}")
        raise


def list_all_files(folder_id=None):
    """
    List files in a specified Google Drive folder.

    Args:
        folder_id (str, optional): ID of the folder to list files from.
                                   Defaults to None (root folder).

    Returns:
        list: List of dictionaries containing file information
    """
    try:
        drive = authenticate_google_drive()

        # Build query to list files in the specified folder
        query = f"'{folder_id}' in parents and trashed=false" if folder_id else "trashed=false"

        # Retrieve file list
        file_list = drive.ListFile({'q': query}).GetList()

        # Transform file information
        all_files = []
        for file in file_list:
            try:
                # Parse modification date, handle potential parsing errors
                modified_date = datetime.strptime(
                    file.get("modifiedDate", ""),
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                ).date()
            except (ValueError, TypeError):
                modified_date = None

            all_files.append({
                "title": file.get('title', 'Untitled'),
                "id": file.get('id', ''),
                "modified": str(modified_date) if modified_date else 'Unknown'
            })

        return all_files

    except Exception as e:
        print(f"Error listing files: {e}")
        return []


if __name__ == '__main__':
    files = list_all_files(folder_id="1a_6_-TrJe8srDlxPRC3kvQWf1bErR4aN")
    for f in files:
        print(f)