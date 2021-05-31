#DISCLAIMER

Disclaimer: These programs, scripts, and compiled executables, should only be used in the lawful and educational purposes only. I assume no responsibility for any direct or indirect damage caused due to the usage of this tool or its code.


# FOR MORE HELP

https://pypi.org/project/Nuitka/0.4.6/
https://askubuntu.com/questions/678277/how-to-install-python3-in-wine


# Download both of these files to ~/Downloads/

Downlaod https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win32/Personal%20Builds/mingw-builds/installer/mingw-w64-install.exe/download
Download https://www.python.org/ftp/python/3.9.5/python-3.9.5.exe


#Setup Wine for cross compiling

WINEPREFIX=~/.wine64 WINARCH=win64 winetricks corefonts win10
WINEPREFIX=~/.wine64 WINARCH=win64 wine ~/Downloads/python-3.9.5.exe 

WINEPREFIX=~/.wine64 WINARCH=win64 wine ~/Downloads/mingw-w64-install.exe

WINEPREFIX=~/.wine64 WINARCH=win64 python -m pip install nuitka SCons
