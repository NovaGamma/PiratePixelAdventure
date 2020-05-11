import pygame
pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
screenx,screeny=1400,700
screendelta_x=screendelta_y=0
tools={'size':False,'move':True,'place':False,'cp':False,'spawn':False,'ennemie':False}
bg=pygame.transform.scale(pygame.image.load('Graphism/level_editor/bg (1).png'),(screenx,screeny))
plank1=pygame.image.load('Graphism/level_editor/plank1.png')
chest_texture=pygame.image.load('Graphism/level_editor/chestpoint (1).png')
chest_texture2=pygame.image.load('Graphism/level_editor/chestpoint (1)_invi.png')
ennemy_texture=pygame.image.load('Graphism/level_editor/Captain_normal.png')
ennemy_texture=pygame.image.load('Graphism/level_editor/Captain_invisible.png')
spawn=pygame.transform.scale(pygame.image.load('Graphism/level_editor/rright0.png'),(2*48,2*64))
spawn2=pygame.transform.scale(pygame.image.load('Graphism/level_editor/rright0_invi.png'),(2*48,2*64))
black=pygame.image.load('Graphism/level_editor/black.png')
pointed=pygame.image.load('Graphism/level_editor/pointed.png')
arrow_leftup=pygame.transform.scale(pygame.image.load('Graphism/level_editor/arrow_leftup.png'),(64,64))
arrow_leftdown=pygame.transform.scale(pygame.image.load('Graphism/level_editor/arrow_leftdown.png'),(64,64))
arrow_rightup=pygame.transform.scale(pygame.image.load('Graphism/level_editor/arrow_rightup.png'),(64,64))
arrow_rightdown=pygame.transform.scale(pygame.image.load('Graphism/level_editor/arrow_rightdown.png'),(64,64))
tool=[pygame.image.load('Graphism/level_editor/edit_tool0.png'),pygame.image.load('Graphism/level_editor/edit_tool1.png'),pygame.image.load('Graphism/level_editor/edit_tool2.png'),pygame.image.load('Graphism/level_editor/edit_tool3.png'),pygame.image.load('Graphism/level_editor/edit_tool4.png'),pygame.image.load('Graphism/level_editor/edit_tool5.png'),pygame.image.load('Graphism/level_editor/edit_tool6.png'),pygame.image.load('Graphism/level_editor/edit_tool7.png'),pygame.image.load('Graphism/level_editor/edit_tool8.png'),pygame.image.load('Graphism/level_editor/edit_tool9.png'),pygame.image.load('Graphism/level_editor/edit_tool10.png'),pygame.image.load('Graphism/level_editor/edit_tool11.png')]
spawn_x,spawn_y=300,350
end=False
creating=False
spawning=False
screen_moving=False
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
