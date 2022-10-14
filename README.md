# Fesenjoon


## Install

```
    pip install fesenjoon
```

## API call

```
    import fesenjoon

    drive = fesenjoon.Drive()
```

```
    from fesenjoon import Drive
    drive = Drive()
```


## Command Line

```
    fesenjoon -u https://drive.google.com/drive/folders/1Eu2e4m3nH4Mwh8Jc6r_ULJ4U2y1nK6jK
```


### Install packages

```
    pylint
    black
    google-api-python-client
    google-auth-oauthlib
```

https://github.com/googleapis/google-api-python-client

https://github.com/googleapis/google-auth-library-python-oauthlib

https://developers.google.com/drive/api/guides/about-sdk

![photo](https://developers.google.com/drive/images/drive-intro.png)

https://developers.google.com/workspace/guides/auth-overview
![image](https://developers.google.com/workspace/images/auth-overview.png)

## Features

- Linter: Pylint
- Formatter: Black
- CI: GitHub Actions

1.
--url
-u 
2.
depth
default = 0 (just current directory)
int
string all

3.
default binary files
--mimetype-includes
--mimetype-excludes

4.
-out



# Setup

git clone git@github.com:mohsenhariri/fesenjoon.git

python3 -m venv env

make pia

go to https://console.cloud.google.com/ and download your token (OAuth Client ID)

copy token in the root path

rename token with .credentials

finish

make app