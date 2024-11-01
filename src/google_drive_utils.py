import os
import io
from datetime import datetime
from typing import List, Dict, Optional, Union

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import docx


class GoogleDriveUtility:
    """
    A comprehensive utility class for Google Drive operations.
    """

    # Class constants for scopes and file types
    DRIVE_READONLY_SCOPE = ['https://www.googleapis.com/auth/drive.readonly']
    SUPPORTED_FILE_TYPES = ['google_doc', 'docx', 'txt']

    @staticmethod
    def authenticate_google_drive() -> GoogleDrive:
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
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                gauth.Refresh()
            else:
                gauth.Authorize()

            # Always save the latest credentials
            gauth.SaveCredentialsFile(credentials_path)

            return GoogleDrive(gauth)

        except Exception as e:
            print(f"Authentication error: {e}")
            raise

    @staticmethod
    def list_all_files(folder_id: Optional[str] = None) -> List[Dict[str, str]]:
        """
        List files in a specified Google Drive folder.

        Args:
            folder_id (str, optional): ID of the folder to list files from.
                                       Defaults to None (root folder).

        Returns:
            List[Dict[str, str]]: List of dictionaries containing file information
        """
        try:
            drive = GoogleDriveUtility.authenticate_google_drive()

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

    @classmethod
    def _get_credentials(cls) -> Credentials:
        """
        Manage Google API credentials.

        Returns:
            Credentials: Authenticated credentials
        """
        creds = None
        # Check if token.json exists for cached credentials
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', cls.DRIVE_READONLY_SCOPE)

        # Refresh or re-authenticate if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secrets.json', cls.DRIVE_READONLY_SCOPE)
                creds = flow.run_local_server(port=0)

            # Save the credentials for future runs
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        return creds

    @classmethod
    def read_google_doc(cls, doc_id: str, file_type: str) -> str:
        """
        Downloads a file from Google Drive and reads its content.

        Args:
            doc_id (str): ID of the document
            file_type (str): Type of file to read

        Returns:
            str: Extracted text content of the document
        """
        # Validate file type
        if file_type not in cls.SUPPORTED_FILE_TYPES:
            raise ValueError(f"Unsupported file type. Supported types are {cls.SUPPORTED_FILE_TYPES}")

        # Get credentials and build service
        creds = cls._get_credentials()
        service = build('drive', 'v3', credentials=creds)

        # Prepare download
        fh = io.BytesIO()

        try:
            if file_type == 'google_doc':
                # Export Google Doc as DOCX
                export_mime_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                request = service.files().export_media(fileId=doc_id, mimeType=export_mime_type)
            else:
                # Download other file types directly
                request = service.files().get_media(fileId=doc_id)

            # Download file in chunks
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()

            # Move pointer to beginning of BytesIO object
            fh.seek(0)

            # Process file based on type
            if file_type in ['google_doc', 'docx']:
                document = docx.Document(fh)
                text = [para.text for para in document.paragraphs]
                return "\n".join(text)
            elif file_type == 'txt':
                return fh.read().decode('utf-8')

        except Exception as e:
            print(f"Error reading document: {e}")
            return ""


def main():
    """
    Main function to demonstrate usage of GoogleDriveUtility.
    """
    try:
        # Example of reading a text file
        text_content = GoogleDriveUtility.read_google_doc(
            '1LU16lC4W1BSVSXxFq75CsmtySPrbIggM',
            file_type="txt"
        )
        print("Text Content:", text_content[:500] + "..." if len(text_content) > 500 else text_content)

        # Example of listing files in a folder
        files = GoogleDriveUtility.list_all_files(
            folder_id="1a_6_-TrJe8srDlxPRC3kvQWf1bErR4aN"
        )
        print("\nFiles in folder:")
        for f in files:
            print(f)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()