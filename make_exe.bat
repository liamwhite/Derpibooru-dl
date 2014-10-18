REM This is just to build a .exe with pyinstaller.
REM Folders for python and pyinstaller must be in PATH environment variable for this to work.
pyinstaller derpibooru_dl.py
REM Clean up temporary files used by pyinstaller
REM "derpibooru_dl.spec"
del derpibooru_dl.spec
REM "build\"
IF EXIST "build" (
    rmdir "build" /s /q
)