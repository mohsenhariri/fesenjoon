import fesenjoon

drive = fesenjoon.Drive()

url = "https://drive.google.com/drive/folders/10XArxkv1FwwHgPg-uWePXmDL8EqQMAAS"
depth = 0
out = r"./download"

drive.download(url, depth, out)



