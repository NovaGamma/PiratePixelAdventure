import os
if os.path.exists("entities.txt"):
    print("existe")
    levelFile = open("entities.txt",'r')
    txt=[]
    for line in levelFile:
        temp=line.split(' ')
        if temp[0]=='plank':
            txt.append(temp[0]+' '+str(float(int(temp[1])/1400))+' '+str(float(int(temp[2])/700))+' '+str(float(int(temp[3])/700))+' '+str(float(int(temp[4])/1400))+'\n')
        elif temp[0]=='ennemy':
            txt.append(temp[0]+' '+str(float(int(temp[1])/1400))+' '+str(float(int(temp[2])/700))+temp[3]+'\n')
        else:
            txt.append(temp[0]+' '+str(float(int(temp[1])/1400))+' '+str(float(int(temp[2])/700))+'\n')
    levelFile.close()
    levelFile = open("entities.txt",'w')
    for line in txt:
        levelFile.write(line)
    levelFile.close()
