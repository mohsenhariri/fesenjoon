"""
DocString
https://docs.python.org/3/library/io.html
"""
import json
import pickle
from os import getenv
from pathlib import Path
from pprint import pprint as print
from urllib.parse import urlparse

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload


class Drive:
    global SCOPES
    SCOPES = [
        "https://www.googleapis.com/auth/drive.metadata.readonly",
        "https://www.googleapis.com/auth/drive",
    ]

    def __init__(self) -> None:
        creds = None

        path_token = Path(getenv("PATH_TOKEN"))

        if path_token.exists():
            with open(".token", "rb") as fp:
                try:
                    creds = pickle.load(fp)
                except Exception as err:
                    print(".token file exists, but it damaged.", err)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(".credentials", SCOPES)
                creds = flow.run_local_server(port=0)

            with open(".token", "wb") as fp:
                pickle.dump(creds, fp)

        try:
            self.service = build("drive", "v3", credentials=creds)
        except HttpError as err:
            print("Can not stablish the connection.", err)

    def id_parser(self, url):
        parse = urlparse(url).path.split("/")
        type = parse[1]
        id = parse[3]
        return type, id

    def sanitizer(self, name: str) -> str:
        file_name = name.replace("/", "_")  # replace illegal characters
        return file_name

    def files_list(self):
        results = (
            self.service.files().list(pageSize=100, fields="files(id, name)").execute()
        )
        items = results.get("files", [])

        # print a list of files

        print("Here's a list of files: \n")
        print(*items, sep="\n", end="\n\n")

    def download_file(self, file_id, file_name):

        request = self.service.files().get_media(fileId=file_id)

        with open(f"./download/{file_name}", "wb") as fd:
            downloader = MediaIoBaseDownload(fd, request)
            print(downloader.__dict__)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

    def download_google_files(self, url, export):
        # https://developers.google.com/drive/api/guides/folder
        _, id = self.id_parser(url)
        mimeType = None
        if export == "csv":
            mimeType = "text/csv"
        if export == "pdf":
            mimeType = "application/pdf"

        # print(id)
        # mimeTypeMatchup = {
        #     "application/vnd.google-apps.document": {
        #         "exportType": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        #         "docExt": "docx",
        #     }
        # }
        # res = self.service.files().get(fileId=id).execute()
        # print(res)
        try:
            # request = self.service.files().export(fileId=id, mimeType="application/pdf")
            request_metadata = self.service.files().get(fileId=id).execute()

            name = self.sanitizer(request_metadata["name"])

            request = self.service.files().export(fileId=id, mimeType=mimeType)

            # exit()
            with open(f"./download/{name}.{export}", "wb") as fd:
                downloader = MediaIoBaseDownload(fd, request)
                # print(downloader.__dict__)
                # print(request.__dict__)

                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print("Download %d%%." % int(status.progress() * 100))

            # exportMimeType =mimeTypeMatchup[docMimeType]['exportType']

            # request = self.service.files().export_media(fileId=id,mimeType=exportMimeType)
        except HttpError as error:
            print(f"An error occurred: {error}")
        except Exception as error:
            print(f"An Exception occurred: {error}")

    def upload_file():
        pass

    def directory_structure(self, url):  # fin
        """
        finish

        all files and folders in the given url
        """

        _, id = self.id_parser(url)

        def traverse(id, path_parent):

            files_and_folders = self.files_folder(id)

            for file in files_and_folders:

                path_directory = Path(rf'{path_parent}/{file["name"]}')
                file["path"] = str(path_directory)

                if file["mimeType"] == "application/vnd.google-apps.folder":
                    file["inside"] = traverse(id=file["id"], path_parent=path_directory)

            with open("save.json", "w") as fp:
                json.dump(files_and_folders, fp)
            return files_and_folders

        return traverse(id, path_parent="./")

    def down_all(self, url):

        """
        Finish
        Download all files in parent and all sub directories
        """
        path_download = Path(getenv("PATH_DOWNLOAD"))
        if not path_download.exists():
            raise Exception("Download path doesn't exist.")

        _, id = self.id_parser(url)

        def traverse(id, path_parent):

            files_and_folders = self.files_folder(id)

            for file in files_and_folders:
                if file["mimeType"] == "application/vnd.google-apps.folder":

                    path_directory = Path(rf'{path_parent}/{file["name"]}')
                    path_directory.mkdir(parents=True, exist_ok=True)
                    file["inside"] = traverse(id=file["id"], path_parent=path_directory)

                else:
                    self.down_file(file, path_parent)

            return files_and_folders

        return traverse(id, path_download)

    def down_file(self, item, path_parent):
        """
        finish
        """
        file_id = item["id"]

        request = self.service.files().get_media(fileId=file_id)

        file_name = item["name"].replace("/", "_")  # replace illegal characters

        path_file = Path(rf"{path_parent}/{file_name}")

        if path_file.exists():
            print(f"{path_file} already exists.")

        with open(path_file, "wb") as fd:
            downloader = MediaIoBaseDownload(fd, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f"{path_file} is downloading {int(status.progress() * 100)}")

    def files_folder(self, folder_id, pageSize=10):

        page_token = None
        while True:
            """
            application/vnd.google-apps.folder
            https://developers.google.com/drive/api/guides/search-files
            https://developers.google.com/drive/api/v3/reference/files/list

            """
            response = (
                self.service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    pageSize=pageSize,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType, parents)",
                    pageToken=page_token,
                )
                .execute()
            )

            items = response.get("files", [])
            page_token = response.get("nextPageToken", None)

            print("next")

            if page_token is None:
                break

        if not items:
            print("No files found.")

        return items

    def download_folder(self, folder_id):
        page_token = None
        while True:
            # Call the Drive v3 API
            results = (
                self.service.files()
                .list(
                    # q=f"'{folder_id}' in parents",
                    pageSize=30,
                    # supportsAllDrives = True,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
                    # driveId =  "0AIyERKEAMNpHUk9PVA",
                    fileId=file_id,
                )
                .execute()
            )
            items = results.get("files", [])

            if not items:
                print("No files found.")
            else:
                for item in items:
                    print("{0} ({1})".format(item["name"], item["id"]))

                    file_id = item["id"]
                    request = self.service.files().get_media(fileId=file_id)

                    with open(item["name"], "wb") as fd:
                        downloader = MediaIoBaseDownload(fd, request)

                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print("Download %d%%." % int(status.progress() * 100))

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break
