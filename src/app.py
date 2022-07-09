import argparse
from lib2to3.pgen2.driver import Driver

from Drive import Drive

parser = argparse.ArgumentParser(description="URL of file or folder")

parser.add_argument("-url", type=str, default=None, metavar="N", help="URL")
u = parser.parse_args().url


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

# url =   "https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"
# url = "https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"
# url = "https://drive.google.com/drive/folders/0ABMmE9OGuOAaUk9PVA"
# url = "https://drive.google.com/drive/folders/16oxBwnA9vchagtijZGtwjXSy0yni8C5r"
# url = u

# url = "https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"

# url = "https://drive.google.com/drive/folders/10XArxkv1FwwHgPg-uWePXmDL8EqQMAAS"

# drive.files_folder(url)

# drive.download_folder(folder_id)

url = "https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK"


# url = "https://drive.google.com/drive/folders/1xbMsmuiFXgNDC1YPX9-e61jUXLMSbroC"
# url = "https://drive.google.com/drive/folders/118iMdI-X9S5o5-1sGrVK1P4_o6HzN4zr"


# url = "https://drive.google.com/drive/folders/1k7ZJYxJQF9APBsFgP9Q2BHGk_Rjn4iPY"
# drive.down_all(url)

# print(drive.directory_structure(url))


# drive.download_all(url)


# url = "https://drive.google.com/drive/folders/10siyKtClyXCLAK3KVfbFHHL4RoCtjgK2"

# print(drive.id_parser(url))
# print(drive.directory_structure(url))

url = "https://docs.google.com/spreadsheets/d/1P9HnkojMJnMRA---HfoEKrMH6bJyUCi7YXkXF_UhAWY/edit?usp=sharing"

# print(drive.id_parser(url))
drive.download_google_files(url, "pdf")
drive.download_google_files(url, "csv")
