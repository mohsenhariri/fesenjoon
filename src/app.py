"""
DocString
"""
import os.path
import pickle
from urllib.parse import urlparse
from pprint import pprint as print
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
        if os.path.exists(".token"):
            with open(".token", "rb") as token_file:
                try:
                    creds = pickle.load(token_file)
                except Exception as err:
                    print(".token file exists, but it damaged.", err)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(".credentials", SCOPES)
                creds = flow.run_local_server(port=0)

            with open(".token", "wb") as token_file:
                pickle.dump(creds, token_file)

        try:
            self.service = build("drive", "v3", credentials=creds)
        except HttpError as err:
            print("Can not stablish the connection.", err)

    def id_parser(self, url):
        parse = urlparse(url).path.split("/")
        type = parse[1]
        id = parse[3]
        return type, id

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

        with open(f"./here/{file_name}", "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request)
            print(downloader.__dict__)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100))

    def upload_file():
        pass

    def files_folder(self, url):
        _, folder_id = self.id_parser(url)

        # end_nest = False
        # structure=[]
        # while True:

        page_token = None
        while True:
            # application/vnd.google-apps.folder
            # https://developers.google.com/drive/api/guides/search-files
            response = (
                self.service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    pageSize=10,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType, parents)",
                    pageToken=page_token,
                )
                .execute()
            )

            items = response.get("files", [])
            page_token = response.get("nextPageToken", None)
            print(items)
            print("next")

            if page_token is None:
                break
            # if not items:
            # break

        if not items:
            print("No files found.")
            return None

        return items

    def download_folder(self, folder_id):
        page_token = None
        while True:
            # Call the Drive v3 API
            results = (
                self.service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    pageSize=10,
                    fields="nextPageToken, files(id, name)",
                    pageToken=page_token,
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

                    with open(item["name"], "wb") as fh:
                        downloader = MediaIoBaseDownload(fh, request)
                        done = False
                        while done is False:
                            status, done = downloader.next_chunk()
                            print("Download %d%%." % int(status.progress() * 100))

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break


# folder_id = "1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"
drive = Drive()


# print(
#     drive.id_parser(
#         "https://drive.google.com/drive/folders/1oEdQ6XNZ6wbn6dY98vFcf2ofOrY5GX-r?usp=sharing"
#     )
# )

# print(
#     drive.id_parser(
#         "https://drive.google.com/file/d/1sRTNDHiowo7vhhxzg-8IvVTbVI96QDIz/view?usp=sharing"
#     )
# )

# drive.files_list()
# drive.download_file('19XDepgl7JF0VkSGfqpn64W_uwAw7tmJG','fsd.png')
# print(drive.files_folder("1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"))
# print(
#     drive.files_folder(
#         "https://drive.google.com/drive/folders/1oEdQ6XNZ6wbn6dY98vFcf2ofOrY5GX-r"
#     )
# )

print(
    drive.files_folder(
        "https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"
    )
)

# drive.download_folder(folder_id)
