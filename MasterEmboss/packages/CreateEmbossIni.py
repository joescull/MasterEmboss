"""A script to update the ini file to ensure the correct setting are used for filename emobssing on photos.
adrianschmieder@hieta.biz
Initial development 12-08-2016
"""

import os
import shutil

def EmbossInit():
    IniPath = "C:\\Users\\jscull\\AppData\\Roaming\\IrfanView\\"
    OrigIniPath = IniPath + "i_view64.ini"
    NewIniPath = IniPath + "i_view64New.ini"
    BackupIniPath = IniPath + "i_view64_bk.ini"
    #*************************************************************
    #Check to see if ini file already exists... if so, remove it.
    #*************************************************************
    if os.path.exists(NewIniPath)==1:
        os.remove(NewIniPath)

    OrigIni = open(OrigIniPath,"r")
    NewIni = open(NewIniPath,"a")

    for line in OrigIni.readlines():
        #print line
            
        if line.startswith('AdvCrop='):
             NewIni.write('AdvCrop=0\n')  #Disabling advanced crop

        elif line.startswith('AdvResize='):
             NewIni.write('AdvResize=0\n')  #Disabling advanced resize

        elif line.startswith('AdvResample='):
             NewIni.write('AdvResample=0\n')  #Disabling advanced resample

        elif line.startswith('AdvDPI='):
             NewIni.write('AdvDPI=0\n')

        elif line.startswith('AdvCanvas='):
             NewIni.write('AdvCanvas=0\n')

        elif line.startswith('AdvWatermark='):
             NewIni.write('AdvWatermark=0\n')

        elif line.startswith('AdvAddText='):
             NewIni.write('AdvAddText=1\n')  #Enabling text adition
             
        elif line.startswith('AddText'):
            NewIni.write('AddText=$N\n')

        elif line.startswith('Orientation'):
            NewIni.write('Orientation=0\n')

        elif line.startswith('TranspText'):
            NewIni.write('TranspText=1\n')

        elif line.startswith('SemiTranspText'):
            NewIni.write('SemiTranspText=0\n')

        else:
            NewIni.write(line)

    NewIni.close()

    #Transfering new settings into active initialisation file
    shutil.copyfile(OrigIniPath, BackupIniPath)
    shutil.copyfile(NewIniPath, OrigIniPath)
    
    return 0


