# Foxydownloader

Script to download SGF-Files from Fox Weiqi (fixing the strange Komi format of Fox) and either save them to disk or upload them to OGS.

## Requirements
- python v3.x
- the module `simple-term-menu`
  ``` 
  pip install simple-term-menu 
  ```
  Note that this module doesn't work in Windows terminals. If you are using Windows it's best to us this script from the Windows Subsystem for Linux (WSL, https://docs.microsoft.com/en-us/windows/wsl/install)

## Installation
It suffices to download the script or clone it to your pc:
``` 
git clone https://github.com/mboehm271/foxydownloader 
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
