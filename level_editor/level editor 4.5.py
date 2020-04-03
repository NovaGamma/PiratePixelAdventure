import pygame
import os

class platform(object):#defining the class to create platforms
    def __init__(self,x,y,h,w,img):#init method to get all the requirement such as the position x and y the size (height and width) and the texture of the platforms
        self.x=x#getting x
        self.y=y#getting y
        self.h=h#getting the height
        self.w=w#getting the width
        self.img=pygame.transform.scale(img,(self.w,self.h))#rescaling the texture according to the size of the platform
        self.touched=False
        self.right=False
        self.left=False
        self.up=False
        self.right=False
        planks.append(self)#adding the platform to the list of all platforms
        entities.insert(0,self)#adding the platform to the list of all entities at the first pos to know that this is the last one that we added
    def draw(self):#defining the draw method of the class
        screen.blit(self.img,(self.x,self.y))
        if self==entities[0] or not mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h):
            screen.blit(pygame.transform.scale(black,(self.w,4)),(self.x,self.y))
            screen.blit(pygame.transform.scale(black,(self.w,4)),(self.x,self.y+self.h-4))
            screen.blit(pygame.transform.scale(black,(4,self.h)),(self.x,self.y))
            screen.blit(pygame.transform.scale(black,(4,self.h)),(self.x+self.w-4,self.y))
            if size_tool and (self.touched or self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h and (entities[0]==self or entities[0].touched==False and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h))):
                if self.up and self.right:
                    screen.blit(arrow_leftup,(self.x,self.y))
                elif self.up and not self.right:
                    screen.blit(arrow_rightup,(self.x+self.w-64,self.y))
                elif not self.up and not self.right:
                    screen.blit(arrow_rightdown,(self.x+self.w-64,self.y+self.h-64))
                elif not self.up and self.right:
                    screen.blit(arrow_leftdown,(self.x,self.y+self.h-64))
            if move_tool and self==entities[0]:
                screen.blit(pointed,(self.x+self.w//2-8,self.y+self.h//2-8))
    def check(self):
        if self.h==self.w==1 and not mousepress[0]:
            planks.remove(self)
            entities.remove(self)
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
                if self.h+mousedelta[1]>0 and self.up:
                    self.h+=mousedelta[1]
                elif mousedelta[1]<0 or self.h-mousedelta[1]>0:
                    self.up=False
                    self.h-=mousedelta[1]
                    self.y+=mousedelta[1]
                else:
                    self.up=True
                if self.w+mousedelta[0]>0 and self.right:
                    self.w+=mousedelta[0]
                elif mousedelta[0]<0 or self.w-mousedelta[0]>0:
                    self.right=False
                    self.w-=mousedelta[0]
                    self.x+=mousedelta[0]
                else:
                    self.right=True
                self.img=pygame.transform.scale(self.img,(self.w,self.h))

        if not self.touched and mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h:
            self.touched=True
        if self.touched and move_tool:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

class chestpoint(object):
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.w=128
        self.h=128
        self.touched=False
        self.img=chest_texture
        entities.insert(0,self)
        cps.append(self)
    def draw(self):
        print(self.img,self.x,self.y)
        screen.blit(self.img,(self.x,self.y))
        if self==entities[0] or not mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h):
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x,self.y))
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x,self.y+128-4))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x,self.y))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+128-4,self.y))
        if move_tool and self==entities[0]:
                screen.blit(pointed,(self.x+self.w//2-8,self.y+self.h//2-8))
    def check(self):
        if not self.touched and mousepress[0] and self.x<=mousepos[0]<=self.x+self.w and self.y<=mousepos[1]<=self.y+self.h:
            self.touched=True
        if self.touched and move_tool:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

class button:
    def __init__(self,height,width):
        self.height=height
        self.width=width
        self.x=0
        self.y=0

    def pos(self,x,y):
        self.x=x
        self.y=y

    def collide(self,posX,posY):
        if (posX>=self.x and posX<=self.x+self.width) and (posY>=self.y and posY<=self.y+self.height):
            return 1
        return 0

class level_button(button):
    def __init__(self,width,height,x,y,text,image=None):
        self.name=text
        if image!=None:
            self.image=image
        self.text=font.render(text,0,(255,255,255))
        button.__init__(self,height,width)
        self.x=x
        self.y=y

    def draw(self,rect):
        screen.blit(rect,(self.x,self.y))
        try:
            screen.blit(self.image,(self.x+10,self.y+(self.height//3)-10))
        except:
            pass
        screen.blit(self.text,(self.x+70,self.y+(self.height//3)))    

def save():
    print("please give the name of the level that your creating (don't put spaces in the name) :")
    name=input()
    if not(os.path.exists("Levels")):
        os.mkdir("Levels")
    print("Saving level...")
    if not(os.path.exists('Levels/'+name)):
        os.mkdir('Levels/'+name)
    with open("Levels/"+name+'/'+'entities.txt','w+') as level:
        for plank in planks:
            level.write('plank '+str(plank.x)+' '+str(plank.y)+' '+str(plank.h)+' '+str(plank.w)+'\n')
        for cp in cps:
            level.write('cp '+str(cp.x)+' '+str(cp.y)+'\n')
    #re-blitting the entities and the bg but without the tools to have a clean preview
    screen.blit(bg,(0,0))
    for i in range(len(entities)):
        entities[-i-1].draw()
    pygame.display.flip()#updating the screen
    pygame.image.save(screen,'Levels/'+name+'/level_preview.PNG')#saving the preview
    print("Level saved !")

def load(plank1):
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    rect=pygame.Surface((325,105))
    rect.fill((179, 179, 179))
    rect.set_alpha(180)
    choosed=False
    lvl_button=[]
    levels_name = os.listdir("Levels/")
    i=0
    j=0
    screen.blit(fond, (0,0))
    if len(levels_name)!=0:
        for level in levels_name:
            lvl_button.append(level_button(325,105,30+i*(325+15),30+j*(105+25),level,pygame.transform.scale(pygame.image.load("Levels/"+level+'/level_preview.PNG'),(50,50))))
            i+=1
            if i==4:
                j+=1
                i=0
        for button in lvl_button:
            button.draw(rect)
        pygame.display.update()
        while not(choosed):
            mousepress=pygame.mouse.get_pressed()
            mousepos=pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return True
                if mousepress[0]:
                    for button in lvl_button:
                        if button.collide(mousepos[0],mousepos[1]):
                            name=button.name
                            print(name)
                            choosed=True
    else:
        txt=font.render('NO LEVEL FOUND',0,(255,255,255))
        screen.blit(txt,(2*(screenx//5),screeny//2))
        pygame.display.update()
        mouse=pygame.mouse.get_pressed()
        mousepress=False
        while not(mousepress):
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse=pygame.mouse.get_pressed()
                if event.type == pygame.QUIT:
                    return True
            if mouse[0] or mouse[1]:
                mousepress=True
    pos=-1
    for levels in levels_name:
        if name==levels:
            pos=levels_name.index(levels)
    if pos!=-1:
        with open("Levels/"+levels_name[pos]+'/'+'entities.txt','r') as level:
            for line in  level:
                parameters=line.split(' ')
                if parameters[0]=='cp':
                    chestpoint(int(parameters[1]),int(parameters[2]))
                elif parameters[0]=='plank':
                    platform(int(parameters[1]),int(parameters[2]),int(parameters[3]),int(parameters[4]),plank1)

def blit_tools():
    for i in range(4):
        if i==1 and not size_tool or i==0 and not move_tool or i==2 and not place_tool or i==3 and not cp_tool:
            screen.blit(tool[i*2],(4+i*(64+4),screeny-64-4))
        elif i==1 and size_tool or i==0 and move_tool or i==2 and place_tool or i==3 and cp_tool:
            screen.blit(tool[i*2+1],(4+i*(64+4),screeny-64-4))

def ask():
    rect=pygame.Surface((325,105))#surface for the buttons
    rect2=pygame.Surface((675,105))#surface for the question
    rect.fill((179, 179, 179))#filling the surface with grey
    rect.set_alpha(180)#setting the "transparency" of the surface
    rect2.fill((179, 179, 179))#filling the surface with grey
    rect2.set_alpha(180)#setting the "transparency" of the surface
    yes=level_button(325,105,350,320,"YES")#creating the button for the Yes answer
    no=level_button(325,105,700,320,"NO")#creating the button for the No answer
    choosed=False
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    screen.blit(fond,(0,0))
    question=font.render("DO YOU WANT TO SAVE ?",0,(255,255,255))
    screen.blit(rect2,(350,150))
    screen.blit(question,(360,150+35))
    yes.draw(rect)
    no.draw(rect)
    pygame.display.update()
    mousepos=pygame.mouse.get_pos()
    while not(choosed):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousepos=pygame.mouse.get_pos()
        mousepress=pygame.mouse.get_pressed()
        if mousepress[0]:
            if yes.collide(mousepos[0],mousepos[1]):
                return 1
            elif no.collide(mousepos[0],mousepos[1]):
                return 0
        pygame.display.update()

pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
pygame.display.set_caption("Level Editor")
screenx,screeny=1400,700
screen=pygame.display.set_mode((screenx,screeny))
size_tool=False
move_tool=True
place_tool=False
cp_tool=False
bg=pygame.transform.scale(pygame.image.load('bg (1).png'),(screenx,screeny))
plank1=pygame.image.load('plank1.png')
chest_texture=pygame.image.load('chestpoint (1).png')
end=False
black=pygame.image.load('black.png')
pointed=pygame.image.load('pointed.png')
arrow_leftup=pygame.transform.scale(pygame.image.load('arrow_leftup.png'),(64,64))
arrow_leftdown=pygame.transform.scale(pygame.image.load('arrow_leftdown.png'),(64,64))
arrow_rightup=pygame.transform.scale(pygame.image.load('arrow_rightup.png'),(64,64))
arrow_rightdown=pygame.transform.scale(pygame.image.load('arrow_rightdown.png'),(64,64))
tool=[pygame.image.load('edit_tool0.png'),pygame.image.load('edit_tool1.png'),pygame.image.load('edit_tool2.png'),pygame.image.load('edit_tool3.png'),pygame.image.load('edit_tool4.png'),pygame.image.load('edit_tool5.png'),pygame.image.load('edit_tool6.png'),pygame.image.load('edit_tool7.png')]
creating=False
entities=[]
planks=[]
cps=[]
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
print("\n\n\n\n\n\n\n\n\n\n\n\nControls :\n\n1, 2, 3 or 4 to select a tool\ntab to select another platform\nsuppr to delete the selected platform\nctr+z to respawn a deleted platform\nctrl+y to delete a respawned platform\nctrl+c to copy a platform, its size and position\nctrl+v to paste the copied platform\nctrl+o to open an existing level\nctrl+s to save your level")

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
        cp_tool=False
    elif keys[pygame.K_1]:
        size_tool=False
        move_tool=True
        place_tool=False
        cp_tool=False
    elif keys[pygame.K_3]:
        size_tool=False
        move_tool=False
        place_tool=True
        cp_tool=False
    elif keys[pygame.K_4]:
        size_tool=False
        move_tool=False
        place_tool=False
        cp_tool=True
    if keys[pygame.K_TAB] and tab_cooldown:
        for i in range(len(entities)-1):
            entities[i],entities[i+1]=entities[i+1],entities[i]
        tab_cooldown=False
    elif not keys[pygame.K_TAB]:
        tab_cooldown=True
    if keys[pygame.K_DELETE] and len(entities)>0 and del_cooldown:
        undo.append(entities[0])
        if entities[0] in planks:
            planks.remove(entities[0])
        elif entities[0] in cps:
            cps.remove(entities[0])
        entities.remove(entities[0])
        redo=[]
        del_cooldown=False
    elif not keys[pygame.K_DELETE]:
        del_cooldown=True
    if keys[pygame.K_w] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and undo_cooldown:
        if len(undo)>0:
            entities.insert(0,undo[len(undo)-1])
            redo.append(undo[len(undo)-1])
            undo.remove(undo[len(undo)-1])
        undo_cooldown=False
    elif not keys[pygame.K_w]:
        undo_cooldown=True
    if keys[pygame.K_y] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and redo_cooldown:
        if len(redo)>0:
            if redo[len(redo)-1] in planks:
                planks.remove(redo[len(redo)-1])
            elif redo[len(redo)-1] in cps:
                cps.remove(redo[len(redo)-1])
            entities.remove(redo[len(redo)-1])
            undo.append(redo[len(redo)-1])
            redo.remove(redo[len(redo)-1])
        redo_cooldown=False
    elif not keys[pygame.K_y]:
        redo_cooldown=True
    if keys[pygame.K_c] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and copy_cooldown:
        if len(entities)>0:
            clipboard=[entities[0].x,entities[0].y,entities[0].h,entities[0].w,entities[0].img]
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
        if entities!=[]:
            answer=ask()
            if answer==0:
                save()
        #clearing the space
        cps=[]
        planks=[]
        entities=[]
        end=load(plank1)
        load_cooldown=False
    elif not keys[pygame.K_o] and not(load_cooldown):
        load_cooldown=True
    if keys[pygame.K_s] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and save_cooldown:
        save()
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
    elif size_tool and creating and not mousepress[0]:
        place_tool=True
        size_tool=False
        creating=False
    if cp_tool and mousepress[0] and not creating:
        chestpoint(mousepos[0]-64,mousepos[1]-64)
        creating=True
    elif creating and not mousepress[0]:
        creating=False
    only=False
    for i in entities:
        if not only:
            i.check()
        if i.touched==True and i in entities:
            entities.remove(i)
            only=True
            entities.insert(0,i)
    #blitting the entities
    for i in range(len(entities)):
        entities[-i-1].draw()
    if cp_tool:
        screen.blit(chest_texture,(mousepos[0]-64,mousepos[1]-64))
    #blitting the tools (optionnal and unwanted for the preview of levels)
    blit_tools()
    pygame.display.update()#updating the display to show the new elements
if entities!=[]:#asking to save only if the level isn't empty
    answer=ask()
    if answer==0:
        save()#saving
pygame.quit()#closing pygame and ending the process