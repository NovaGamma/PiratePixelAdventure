import pygame
import os

class platform(object):
    def __init__(self,x,y,h,w,img):
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.img=pygame.transform.scale(img,(self.w,self.h))
        self.touched=False
        self.delta=()
        self.right=False
        self.left=False
        self.up=False
        self.right=False
        planks.insert(0,self)
        self.black=pygame.image.load('black.png')
    def draw(self):
        screen.blit(self.img,(self.x,self.y))
        if self==planks[0] or not mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h and (planks[0].x>mousepos[0] or mousepos[0]>planks[0].x+planks[0].w or planks[0].y>mousepos[1] or mousepos[1]>planks[0].y+planks[0].h):
            screen.blit(pygame.transform.scale(self.black,(self.w,4)),(self.x,self.y))
            screen.blit(pygame.transform.scale(self.black,(self.w,4)),(self.x,self.y+self.h-4))
            screen.blit(pygame.transform.scale(self.black,(4,self.h)),(self.x,self.y))
            screen.blit(pygame.transform.scale(self.black,(4,self.h)),(self.x+self.w-4,self.y))
            if size_tool and (self.touched or self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h and (planks[0]==self or planks[0].touched==False and (planks[0].x>mousepos[0] or mousepos[0]>planks[0].x+planks[0].w or planks[0].y>mousepos[1] or mousepos[1]>planks[0].y+planks[0].h))):
                if self.up and self.right:
                    screen.blit(arrow_leftup,(self.x,self.y))
                elif self.up and not self.right:
                    screen.blit(arrow_rightup,(self.x+self.w-64,self.y))
                elif not self.up and not self.right:
                    screen.blit(arrow_rightdown,(self.x+self.w-64,self.y+self.h-64))
                elif not self.up and self.right:
                    screen.blit(arrow_leftdown,(self.x,self.y+self.h-64))
            if move_tool and self==planks[0]:
                screen.blit(pointed,(self.x+self.w//2-8,self.y+self.h//2-8))
    def check(self):
        if self.h==self.w==1 and not mousepress[0]:
            planks.remove(self)
        if size_tool:
            if self.touched or self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h:
                if not self.touched:
                    if self.x<=mousepos[0]<=self.x+self.w/2:
                        self.right=False
                    else:
                        self.right=True
                    if self.y<=mousepos[1]<=self.y+self.h/2:
                        self.up=False
                    else:
                        self.up=True
                if not self.touched and mousepress[0]:
                    self.touched=True
                elif not mousepress[0]:
                    self.touched=False
            if self.touched:
                self.delta=mousedelta
                if self.h+self.delta[1]>0 and self.up:
                    self.h+=self.delta[1]
                elif self.delta[1]<0 or self.h-self.delta[1]>0:
                    self.up=False
                    self.h-=self.delta[1]
                    self.y+=self.delta[1]
                else:
                    self.up=True
                if self.w+self.delta[0]>0 and self.right:
                    self.w+=self.delta[0]
                elif self.delta[0]<0 or self.w-self.delta[0]>0:
                    self.right=False
                    self.w-=self.delta[0]
                    self.x+=self.delta[0]
                else:
                    self.right=True
                self.img=pygame.transform.scale(self.img,(self.w,self.h))
                
        if not self.touched and mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h:
            self.touched=True
        if self.touched and move_tool:
            self.delta=mousedelta
            self.x+=self.delta[0]
            self.y+=self.delta[1]
        if self.touched and not mousepress[0]:
            self.touched=False
def save(planks):
    print("please give the name of the level that your creating (don't put spaces in the name) : \n")
    name=input()
    if not(os.path.exists("Levels")):
        os.mkdir("Levels")
    print("Saving level...")
    with open("Levels/"+name+'.txt','w+') as level:
        for plank in planks:
            level.write(str(plank.x)+' '+str(plank.y)+' '+str(plank.h)+' '+str(plank.w)+' '+'plank1.png\n')
    print("Level saved !")

def load(plank1):
    levels_name = os.listdir("Levels/")
    print('\nAvailable Files :\n')
    for level in levels_name:
        print(level)
    print('')
    print("Please give the name of the level that you want to load (don't forget the .txt at the end)")
    name=input()
    while not('.txt' in name):
        print("Please give the name of the level (don't forget the .txt at the end)")
        name=input()
    pos=-1
    for levels in levels_name:
        if name in levels:
            pos=levels_name.index(levels)
    if pos!=-1:
        planks=[]
        with open("Levels/"+levels_name[pos],'r') as level:
            for line in  level:
                parameters=line.split(' ')
                planks.append(platform(int(parameters[0]),int(parameters[1]),int(parameters[2]),int(parameters[3]),plank1))
        return planks
    return 0

def get_answer():
    try:
        answer=int(input())
        return answer
    except:
        print("Please give an either 0 or 1 as answer")
        answer=get_answer()

pygame.init()
pygame.display.set_caption("Level Editor")
screenx,screeny=1400,700
screen=pygame.display.set_mode((screenx,screeny))
size_tool=False
move_tool=True
place_tool=False
bg=pygame.transform.scale(pygame.image.load('bg (1).png'),(screenx,screeny))
plank1=pygame.image.load('plank1.png')
end=False
pointed=pygame.image.load('pointed.png')
arrow_leftup=pygame.transform.scale(pygame.image.load('arrow_leftup.png'),(64,64))
arrow_leftdown=pygame.transform.scale(pygame.image.load('arrow_leftdown.png'),(64,64))
arrow_rightup=pygame.transform.scale(pygame.image.load('arrow_rightup.png'),(64,64))
arrow_rightdown=pygame.transform.scale(pygame.image.load('arrow_rightdown.png'),(64,64))
tool=[pygame.image.load('edit_tool0.png'),pygame.image.load('edit_tool1.png'),pygame.image.load('edit_tool2.png'),pygame.image.load('edit_tool3.png'),pygame.image.load('edit_tool4.png'),pygame.image.load('edit_tool5.png')]
creating=False
planks=[]
undo=[]
redo=[]
clipboard=[]
del_cooldown=True
undo_cooldown=True
redo_cooldown=True
copy_cooldown=True
paste_cooldown=True
save_cooldown=True
load_cooldown=True
print("\n\n\n\n\n\n\n\n\n\n\n\nControls :\n1, 2 or 3 to select a tool\ntab to select another platform\nsuppr to delete the selected platform\nctr+z to respawn a deleted platform\nctrl+y to delete a respawned platform\nctrl+c to copy a platform, its size and position\nctrl+v to paste the copied platform\nctrl+o to open an existing level\nctrl+s to save your level")
while not end:
    keys=pygame.key.get_pressed()
    mousepress=pygame.mouse.get_pressed()
    mousedelta=pygame.mouse.get_rel()
    mousepos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            end=True
    if keys[pygame.K_2]:
        size_tool=True
        move_tool=False
        place_tool=False
    elif keys[pygame.K_1]:
        size_tool=False
        move_tool=True
        place_tool=False
    elif keys[pygame.K_3]:
        size_tool=False
        move_tool=False
        place_tool=True
    if keys[pygame.K_TAB] and tab_cooldown:
        for i in range(len(planks)-1):
            planks[i],planks[i+1]=planks[i+1],planks[i]
        tab_cooldown=False
    elif not keys[pygame.K_TAB]:
        tab_cooldown=True
    if keys[pygame.K_DELETE] and len(planks)>0 and del_cooldown:
        undo.append(planks[0])
        planks.remove(planks[0])
        redo=[]
        del_cooldown=False
    elif not keys[pygame.K_DELETE]:
        del_cooldown=True
    if keys[pygame.K_w] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and undo_cooldown:
        if len(undo)>0:
            planks.insert(0,undo[len(undo)-1])
            redo.append(undo[len(undo)-1])
            undo.remove(undo[len(undo)-1])
        undo_cooldown=False
    elif not keys[pygame.K_w]:
        undo_cooldown=True
    if keys[pygame.K_y] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and redo_cooldown:
        if len(redo)>0:
            planks.remove(redo[len(redo)-1])
            undo.append(redo[len(redo)-1])
            redo.remove(redo[len(redo)-1])
        redo_cooldown=False
    elif not keys[pygame.K_y]:
        redo_cooldown=True
    if keys[pygame.K_c] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and copy_cooldown:
        if len(planks)>0:
            clipboard=[planks[0].x,planks[0].y,planks[0].h,planks[0].w,planks[0].img]
            copy_cooldown=False
    elif not keys[pygame.K_c]:
        copy_cooldown=True
    if keys[pygame.K_v] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and paste_cooldown:
        if len(clipboard)>0:
            platform(clipboard[0],clipboard[1],clipboard[2],clipboard[3],clipboard[4])
            paste_cooldown=False
    elif not keys[pygame.K_v]:
        paste_cooldown=True
    if keys[pygame.K_o] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and load_cooldown:
        if planks!=[]:
            save(planks)
        planks=load(plank1)
        load_cooldown=False
    elif not keys[pygame.K_o] and not(load_cooldown):
        load_cooldown=True
    if keys[pygame.K_s] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and save_cooldown:
        save(planks)
        save_cooldown=False
    elif not keys[pygame.K_s] and not(save_cooldown):
        save_cooldown=True


    #not getting the keys anymore
    screen.blit(bg,(0,0))
    if place_tool and mousepress[0]:
        platform(mousepos[0],mousepos[1],1,1,plank1)
        place_tool=False
        size_tool=True
        creating=True
    elif creating and not mousepress[0]:
        place_tool=True
        size_tool=False
        creating=False
    only=False
    for i in planks:
        if not only:
            i.check()
        if i.touched==True and i in planks:
            planks.remove(i)
            only=True
            planks.insert(0,i)
    for i in range(len(planks)):
        planks[-i-1].draw()
    for i in range(3):
        if i==1 and not size_tool or i==0 and not move_tool or i==2 and not place_tool:
            screen.blit(tool[i*2],(4+i*(64+4),screeny-64-4))
        if i==1 and size_tool or i==0 and move_tool or i==2 and place_tool:
            screen.blit(tool[i*2+1],(4+i*(64+4),screeny-64-4))
    pygame.display.update()
if planks!=[]:
    print("Have you already saved ? 0/1")
    answer=get_answer()
    while (answer!=0 and answer!=1):
        print("Please give a valid answer (0/1)")
        try:
            answer=int(input())
        except:
            print("Please give an either 0 or 1 as answer")
    if answer==0:
        save(planks)
pygame.quit()