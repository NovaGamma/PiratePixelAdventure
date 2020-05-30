import pygame
import os
pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
screenx,screeny=1400,700
screendelta_x=screendelta_y=0
path='Graphism/level_editor/'
tools={'move':True,'size':False,'place':False,'cp':False,'spawn':False,'ennemie':False,'finish':False}
toolList=['move','size','place','cp','spawn','ennemie','finish']
bg=pygame.transform.scale(pygame.image.load(path+'bg (1).png'),(screenx,screeny))
plank1=pygame.image.load(path+'plank1.png')
chest_texture=pygame.image.load(path+'chestpoint (1).png')
chest_texture2=pygame.image.load(path+'chestpoint (1)_invi.png')
ennemy_texture=pygame.transform.scale(pygame.image.load(path+'Ennemies/cright0.png'),(2*64,2*64))
ennemy_texture2=pygame.transform.scale(pygame.image.load(path+'Ennemies/Captain_invisible.png'),(2*64,2*64))
spawn=pygame.transform.scale(pygame.image.load(path+'rright0.png'),(2*48,2*64))
spawn2=pygame.transform.scale(pygame.image.load(path+'rright0_invi.png'),(2*48,2*64))
finish=pygame.image.load(path+'Ile.png')
finish2=pygame.image.load(path+'Ile.png')
black=pygame.image.load(path+'black.png')
pointed=pygame.image.load(path+'pointed.png')
arrow_leftup=pygame.transform.scale(pygame.image.load(path+'arrow_leftup.png'),(64,64))
arrow_leftdown=pygame.transform.scale(pygame.image.load(path+'arrow_leftdown.png'),(64,64))
arrow_rightup=pygame.transform.scale(pygame.image.load(path+'arrow_rightup.png'),(64,64))
arrow_rightdown=pygame.transform.scale(pygame.image.load(path+'arrow_rightdown.png'),(64,64))
list=os.listdir(path+'Tools/Tool_10-11')
toolEnemies=[]
for i in range(len(list)):
    toolEnemies.append(pygame.image.load(path+'Tools/Tool_10-11/'+list[i]))
list=os.listdir(path+'Tools')
tool=[]
for i in range(len(list)-1):
    tool.append(pygame.image.load(path+'Tools/'+list[i]))
tool.append(toolEnemies[0])
tool.append(toolEnemies[1])
tool.append(pygame.transform.scale(pygame.image.load(path+'Ile.png'),(64,64)))
tool.append(pygame.transform.scale(pygame.image.load(path+'Ile.png'),(64,64)))
spawn_x,spawn_y=300,350
finish_x,finish_y=800,350
end=False
creating=False
spawning=False
finishing=False
screen_moving=False
ennemy_type=[0,['little','captain','glasses','healer','vice-captain'],False]
entities=[]
ennemies=[]
planks=[]
cps=[]
undo=[]
redo=[]
clipboard=[]
mousepress=[]
mousedelta=[]
mousepos=[]
screen=None
last_loaded=None
last_saved=None
