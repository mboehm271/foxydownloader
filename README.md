# Foxydownloader

Script to download SGF-Files from Fox Weiqi (fixing the strange Komi format of Fox) and either save them to disk or upload them to OGS.

## Requirements
- python v3.x
- the modules `simple-term-menu`, `pyyaml` and `appdirs`
  ``` 
  pip install simple-term-menu pyyaml appdirs
  ```
  Note that `simple-term-menu` doesn't work in Windows terminals. If you are using Windows it's best to us this script from the Windows Subsystem for Linux (WSL, https://docs.microsoft.com/en-us/windows/wsl/install)

## Installation
It suffices to download the script or clone it to your pc:
``` 
git clone https://github.com/mboehm271/foxydownloader 
```

## Configuration
To make OGS upload work you need to configure an OGS Oauth client id and secret. For this either ask a friend who trusts you or go to https://online-go.com/oauth2/applications/ and register an application with Authorization grant type `Resource owner password-based`. 

Then create the file `~/.config/foxydownloader/config` on linux and WSL or `~/Library/Preferences/foxydownloader/config` on Mac with the following content:
```
ogs-client-id: <your client id>
ogs-client-secret: <your client secret>

```

## Usage 
``` 
python /path/to/foxydownloader.py 
```
As the script saves the files in the currend directory it's useful to make it usable from anywhere. In most linux distributions and in WSL you can do this by creating a file `foxydownloader` in `~/.local/bin` containing
```
#!/bin/sh
python /path/to/foxydownloader.py 
```
and running `chmod +x ~/.local/bin/foxydownloader`. Then you can just call `foxydownloader` from anywhere.

## Thanks
for the people in this thread https://github.com/featurecat/go-dataset/issues/1 whose code was mainly adapted here
