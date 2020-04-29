import os
if os.path.exists("entities.txt"):
    print("existe")
    levelFile = open("entities.txt",'r')
    txt=[]
    for line in levelFile:
        temp=line.split(' ')
        if temp[0]=='plank':
            txt.append(temp[0]+' '+str(int(float(temp[1])*1400))+' '+str(int(float(temp[2])*700))+' '+str(int(float(temp[3])*700))+' '+str(int(float(temp[4])*1400))+'\n')
        else:
            txt.append(temp[0]+' '+str(int(float(temp[1])*1400))+' '+str(int(float(temp[2])*700))+'\n')
    levelFile.close()
    levelFile = open("entities.txt",'w')
    for line in txt:
        levelFile.write(line)
    levelFile.close()
