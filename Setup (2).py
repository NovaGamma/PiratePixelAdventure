import os
import shutil

if not(os.path.exists("Config")):
    os.mkdir("Config")
if not(os.path.exists("Graphism")):
    os.mkdir("Graphism")
if not(os.path.exists("Sounds")):
    os.mkdir("Sounds")
if not(os.path.exists("Levels")):
    os.mkdir("Levels")
if not(os.path.exists("Language")):
    os.mkdir("Language")
#creating documents
if not(os.path.exists("Config/controls.txt")):
    with open("Config/controls.txt",'w+') as controlsFile:
        controlsFile.write("up 273\ndown 274\nright 275\nleft 276\nshoot 32\n")
if not(os.path.exists("Config/Game_Option.txt")):
    with open("Config/Game_Option.txt",'w+') as screenFile:
        screenFile.write("screenX 1400\nscreenY 700\nlanguage English")
if os.path.exists("Data"):
    path='Data/'
    names = os.listdir(path)
    for name in names:
        srcname = os.path.join(path, name)
        if '.wav' in name:
            dstname = os.path.join("Sounds/", name)
        elif '.png' in name:
            dstname = os.path.join("Graphism/", name)
        elif '.txt' in name:
            dstname = os.path.join("Language/", name)
        elif '.py' in name:
            dstname = name
        elif name=='level editor':
            dstname = name
        else:
            dstname = os.path.join("Levels/", name)
        if not(os.path.exists(dstname)):
            shutil.move(srcname, dstname)
        else:
            os.remove(srcname)
    os.rmdir("Data")
