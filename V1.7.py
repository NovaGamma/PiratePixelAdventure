import pygame
import os
import random
from Classes.button import*
from level_editor_8 import main
import data_level_editor

class platform(object):#the class used to generate platform
    def __init__(self,x,y,height,width,img):#here just defining the size and the texture of the platfrom
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.img=pygame.transform.scale(img,(self.width,self.height))
        planks.append(self)

    def draw(self):#we draw it only if it is in the view of the player to save ressources
        if self.x+self.width>=0 and self.x<screenx:
            screen.blit(self.img,(self.x,self.y))

    def check(self):#here is the function that check the collision with the enitites
        for i in entities:#the function will go through all the entities  and check if an entity is gonna collide with the current speed that it have
            if i.y+i.height<=self.y<=i.y+i.height+i.spdy and self.x-i.width+20<=i.x<=-20+self.x+self.width:
                i.spdy=self.y-i.y-i.height#here we apply gravity on the entity
                i.isground=True #if it is colliding we the isground parameter to true to indicate that the entity is on the ground, here on a platform

class people(object):#the class used to define the entities such as ennemies or the player but not the projectiles
    def __init__(self,x,y,height,width,mass,health,prj=None):#here we give the position, the height and mass, the health that the entity has adn the type of
    #projectile it will shoot
        entities.append(self)#first we add the entity to the entities list
        self.x=x
        self.y=y
        self.mass=mass
        self.height=height
        self.width=width
        self.spdx=0#we set the speed at 0 for both x and y
        self.spdy=0
        self.right=False #the facing direction isn't set yet, it will depend on the direction the entity is going
        self.left=False
        self.stand=True
        self.isground=False#the parameter indicating if the entity is on the ground or not, used to allow the entity to jump
        self.walkcount=0
        self.info=''
        self.info2=0
        self.jump=-50#the 'force' of the jump
        self.health=health
        self.life=self.health #the current 'health' the entity have, wich will vary, while the self.health will remain constant
        self.spawnpoint=[300,screeny//2] #the spawnpoint of the entity, used to move the camera
        self.prj=prj
        self.cooldown=0#the cooldown for the projectile
        self.hit=0#a parameter that will retain if the entity is being hitted stopping the fact that it would be hitted by the same projectile each frame

    def draw(self,hitbox=False):#the function that display the entity, and if precised the hitbox
        if not self.isground:
            if self.spdy<-5:
                self.info2=0
            elif self.spdy<20:
                self.info2=1
            else:
                self.info2=2
            if self.left:
                self.info=jumpleft[self.info2]
            else:
                self.info=jumpright[self.info2]
        else:
            if self.stand:
                self.walkcount=0
            else:
                self.walkcount+=1
            if self.left:
                self.info=walkleft[self.walkcount//4%8]
            else:
                self.info=walkright[self.walkcount//4%8]
        screen.blit(pygame.transform.scale(self.info,(self.width,self.height)),(self.x,self.y))
        if hitbox:#here we display the hitbox as the border of a rectangle
            self.hitbox=(self.x,self.y,self.width,self.height)
            pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
        if self.cooldown>0:
            self.cooldown-=1

    def direction(self):#a function that return the direction the entity is facing, used for the ejction of the player when hitted by an ennemy
        if self.right:
            return 'right'
        elif self.left:
            return 'left'
        else:
            return 'None'

class ennemy(people):#the class defining ennemies, using the people class
    def __init__(self,x,y,height,width,mass,health,prj):
        people.__init__(self,x,y,height,width,mass,health,prj)
        enemies.append(self)
        self.turn=False#null

    def move(self):#the function that move the ennemy depending of it speed
        self.x+=self.spdx
        self.y+=self.spdy

    def health_bar(self):#function that draw the health bar, drawing a grey bar and then a red bar over , a red bar that might be smaller to let the grey bar be visible behind, making the effect that the ennemy has loose some health
        pygame.draw.rect(screen,(0,0,0), (self.x+self.width/2-26*ratiox,-10+self.y-6*ratioy,52*ratiox,10*ratioy))
        pygame.draw.rect(screen,(255,0,0), (self.x+self.width/2-25*ratiox,-10+self.y-5*ratioy,50*self.life/self.health*ratiox,8*ratioy))

class player(people):#the class of the player entity
    def __init__(self,x,y,height,width,mass,health,prj):
        self.money=0#the player has to keep its money somewhere
        people.__init__(self,x,y,height,width,mass,health,prj)

    def move(self):#the move function is more complicated here because we have to move the camera if the player is going to far in a direction
        if (self.x>200 or self.spdx>0) and (self.x<screenx-400-self.width or self.spdx<0):
            self.x+=self.spdx
        elif self.spdx:
            for i in planks:
                i.x-=self.spdx
            for i in cps:
                i.x-=self.spdx
            for i in enemies:
                i.x-=self.spdx
            for i in prjs:
                i.x-=self.spdx
            self.spawnpoint[0]-=self.spdx
        if (self.y>100 or self.spdy>0) and (self.y<screeny-200-self.height or self.spdy<0 or self.spawnpoint[1]<=0):
            self.y+=self.spdy
        elif self.spdy:
            for i in planks:
                i.y-=self.spdy
            for i in enemies:
                i.y-=self.spdy
            for i in cps:
                i.y-=self.spdy
            for i in prjs:
                i.y-=self.spdy
            self.spawnpoint[1]-=self.spdy

    def attack(self):#the attack function is the function that summon the projectiles thrown by the player
    #depending of the weapon of the player
        if self.prj=='axe' and self.cooldown==0:
            throwsound.play()
            if self.left:
                a=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'axe',-1,'player')
            else:
                a=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'axe',1,'player')
            prjs.append(a)
            self.cooldown=30
        if self.prj=='knife' and self.cooldown<=10:
            throwsound.play()
            if self.left:
                k=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'knife',-1,'player')
            else:
                k=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'knife',1,'player')
            prjs.append(k)
            self.cooldown=30

    def health_draw(self):#the display of the life of the player, at the top left corner of the screen, using the same technic as for the ennemies but whith heart images instead
        heart=0
        for i in range(self.life):
            screen.blit(f_heart,(heart,0))
            heart+=70
        for i in range(self.health-self.life):
            screen.blit(e_heart,(heart,0))
            heart+=70

class cp(object):#the class defining the checkpoints in the game
    def __init__(self,x,y):
        self.width=128
        self.height=128
        self.x=x
        self.y=y
        self.cpcount=0
        self.cpt=False#the state of the cp, if it is activated or not
        cps.append(self)#adding the cp at the list of the cps

    def draw(self):
        if self.x-pirate.width+20<=pirate.x<=self.x+self.width and self.y-self.height<=pirate.y<=self.y+pirate.height and not self.cpt:
            self.cpt=True
            pirate.spawnpoint=[self.x,self.y]#changing the spawn position of the player
            chestsound.play()#playing all the sounds
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
        if self.cpcount<16 and self.cpt:
            self.cpcount+=1
        if self.x+self.width>=0 and self.x<screenx:#still displaying the cp only if it is visible
            screen.blit(chestpoint[self.cpcount//4],(self.x,self.y))

class projectile(object):
    def __init__(self,x,y,spdx,spdy,typ,direction,owner):
        self.x=x
        self.y=y
        self.width=64#null
        self.height=64#null
        self.aspdx=20+spdx//2*direction
        self.aspdy=-40+spdy//2
        self.kspdx=20+spdx//2*direction
        self.am=0.25
        self.typ=typ
        self.direction=direction
        self.count=0
    def move(self):
        if self.typ=='knife':
            self.x+=self.direction*self.kspdx
            if self.direction==-1:
                screen.blit(lniff,(self.x,self.y))
            else:
                screen.blit(rniff,(self.x,self.y))
        elif self.typ=='axe':
            self.x+=self.direction*self.aspdx
            self.aspdy+=self.am*g
            self.y+=self.aspdy
            if self.direction==-1:
                drawn_projectile=laxx[self.count%16//4]
                drawn_hitbox=laxx_hitbox[self.count%16//4]
            else:
                drawn_projectile=raxx[self.count%16//4]
                drawn_hitbox=raxx_hitbox[self.count%16//4]
            screen.blit(drawn_projectile,(self.x,self.y))
            self.hitbox=(self.x+drawn_hitbox[0],self.y+drawn_hitbox[1],drawn_hitbox[2],drawn_hitbox[3])
            pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
        if 0>self.x or self.x>screenx or self.y>screeny:
            prjs.remove(self)
        self.count+=1

def display_levels(plank1):
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    rect=pygame.Surface((325,105))
    rect.fill((179, 179, 179))
    rect.set_alpha(180)
    choosed=False
    lvl_button=[]
    try:
        levels_name = os.listdir("Levels/")
    except:
        os.mkdir('Levels')
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
            button.draw(screen)
        pygame.display.update()
        mousepress=pygame.mouse.get_pressed()
        while mousepress[0]:
            mousepress=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return True
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
        load(levels_name[pos],plank1)

def reset_player():
    pirate.life=3
    pirate.spdy=0
    pirate.spdx=0
    pirate.isground=1

def SaveOption():
    if not os.path.exists('Config'):
        os.mkdir('Config')
    with open("Config/Game_Option.txt", "w+") as optionFile:
        for key in ScreenOpt.keys():
            temp=key+' '+str(ScreenOpt[key])+'\n'
            optionFile.write(temp)
        optionFile.write('language '+Language["language"]+'\n')
        optionFile.write('last_save '+last_save+'\n')
    with open("Config/Controls.txt", "w+") as controlFile:
        for key in ControlOpt.keys():
            temp=key+' '+str(ControlOpt[key])+'\n'
            controlFile.write(temp)

def Init():
    if not(os.path.exists("Saves")):
        os.mkdir("Saves")
    if os.path.exists("Config"):
        with open("Config/Game_Option.txt", "r") as optionFile:
            for line in optionFile:
                temp=line.split(' ')
                print(temp[0])
                if temp[0]=="last_save":
                    last_save=temp[1].rstrip('\n')
                elif temp[0]=="language":
                    language=temp[1].rstrip('\n')
                else:
                    ScreenOpt[temp[0]]=int(temp[1])
        print(ScreenOpt)
        print(language)
        with open("Config/Controls.txt", "r") as controlFile:
            for line in controlFile:
                temp=line.split(' ')
                ControlOpt[temp[0]]=int(temp[1])
    if os.path.exists("Language"):
        if os.path.exists("Language/"+language+'.txt'):
            with open("Language/"+language+'.txt' ,'r') as text:
                Language["language"]=language
                for line in text:
                    temp=line.split(' ')
                    Language[temp[0]]=temp[1].rstrip('\n')
        else:
            raise Exception("Error : ",language," not found")
    else:
        raise Exception("Error : No Language directory found\nCan't load the language")
    return [ScreenOpt,ControlOpt,Language,last_save]
    if not(os.path.exists("Graphism")):
        os.mkdir('Graphism')

def load_save(save_name):
    if os.path.exists("Saves/"+save_name+".txt"):
        with open("Saves/"+save_name+".txt" ,'r') as saveFile:
            for line in saveFile:
                temp=line.split(' ')
                if temp[0]=='level':
                    next_level=temp[1].rstrip("\n")
                elif temp[0]=='money':
                    pirate.money=int(temp[1])
                else:
                    if temp[0]!='level_editor':
                        raise Exception(line+" didn't load successully")
            return next_level
    else:
        raise Exception("Try to open a non-existing save file : "+save_name)
    return ''

def load(level,plank1):
    if os.path.exists("Levels/"+level):
        with open("Levels/"+level+'/entities.txt','r') as levelFile:
            print("loading : "+level)
            for line in levelFile:
                parameters=line.split(' ')
                if parameters[0]=='plank':
                    platform(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),int(float(parameters[3])*screeny),int(float(parameters[4])*screenx),plank1)
                elif parameters[0]=='cp':
                    cp(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny))
                elif parameters[0]=='spawn':
                    pirate.spawnpoint=[int(float(parameters[1])*screenx),int(float(parameters[2])*screeny)]
                    pirate.x=pirate.spawnpoint[0]
                    pirate.y=pirate.spawnpoint[1]
                elif parameters[0]=='ennemy':
                    ennemy(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),128,96,1,2,parameters[3])
    else:
        raise Exception("Level not found")

def collide(first,second):
    if first.x<=second.x+second.width<=first.x+first.width+second.width and first.y<=second.y+second.height<=first.y+first.height+second.height:
        return 1
    return 0

def level_editor_unlocked(last_save):
    print(last_save)
    if os.path.exists("Saves/"+last_save+'.txt'):
        with open("Saves/"+last_save+'.txt','r') as SaveFile:
            for line in SaveFile:
                print(line)
                temp=line.split(' ')
                if temp[0]=='level_editor':
                    if temp[1]=='True':
                        return True
                    else:
                        return False
    else:
        return False



pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
ScreenOpt={}
ControlOpt={}
Language={}
Options=Init()
ScreenOpt=Options[0]
ControlOpt=Options[1]
Language=Options[2]
if Options[3]==None:
    last_save="None"
else:
    last_save=Options[3]
print(ScreenOpt)
print(ControlOpt)
screenx=ScreenOpt['screenX']
screeny=ScreenOpt['screenY']
data_level_editor.screenx=screenx
data_level_editor.screeny=screeny
ratiox=screenx/1400
ratioy=screeny/700
SaveOption()
pygame.display.set_caption(Language["title"])
frame=pygame.time.Clock()
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('Graphism/bg (1).png').convert_alpha(),(screenx,screeny))
play=False
start=False
end=False
settings=False
control_setting=False
language_setting=False
level_editor=False
choose_save=False
load_levels=False
g=9.81
#loading textures
jumpright=[pygame.image.load('Graphism/jumpright0.png').convert_alpha(),pygame.image.load('Graphism/jumpright1.png').convert_alpha(),pygame.image.load('Graphism/jumpright2.png').convert_alpha()]
jumpleft=[pygame.image.load('Graphism/jumpleft0.png').convert_alpha(),pygame.image.load('Graphism/jumpleft1.png').convert_alpha(),pygame.image.load('Graphism/jumpleft2.png').convert_alpha()]
walkright=[]
walkleft=[]
for i in range(8):
    temp='rright'+str(i)+'.png'
    temp2='lleft'+str(i)+'.png'
    walkright.append(pygame.image.load('Graphism/'+temp).convert_alpha())
    walkleft.append(pygame.image.load('Graphism/'+temp2).convert_alpha())
chestpoint=[pygame.image.load('Graphism/chestpoint (1).png').convert_alpha(),pygame.image.load('Graphism/chestpoint (2).png').convert_alpha(),pygame.image.load('Graphism/chestpoint (3).png').convert_alpha(),pygame.image.load('Graphism/chestpoint (4).png').convert_alpha(),pygame.image.load('Graphism/chestpoint (5).png').convert_alpha()]
f_heart=pygame.transform.scale(pygame.image.load('Graphism/Full_heart1.png').convert_alpha(),(64,64))
e_heart=pygame.transform.scale(pygame.image.load('Graphism/Empty_heart.png').convert_alpha(),(64,64))
raxx=[pygame.transform.scale(pygame.image.load('Graphism/raxx0.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx1.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx2.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx3.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx4.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx5.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx6.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx7.png').convert_alpha(),(64,64))]
laxx=[pygame.transform.scale(pygame.image.load('Graphism/laxx0.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx1.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx2.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx3.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx4.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx5.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx6.png').convert_alpha(),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx7.png').convert_alpha(),(64,64))]
raxx_hitbox=[]
laxx_hitbox=[]
for i in range(8):
    raxx_hitbox.append(raxx[i].get_bounding_rect())
    laxx_hitbox.append(laxx[i].get_bounding_rect())
rniff=pygame.image.load('Graphism/rniff.png').convert_alpha()
lniff=pygame.image.load('Graphism/lniff.png').convert_alpha()
parawheel=pygame.image.load('Graphism/parawheel1.png').convert_alpha()
#loading sounds
chestsound=pygame.mixer.Sound("Sounds/grincement.wav")
chestsound2=pygame.mixer.Sound("Sounds/money.wav")
throwsound=pygame.mixer.Sound("Sounds/throwsound.wav")
deathsound=pygame.mixer.Sound("Sounds/deathsound.wav")
game_over=pygame.mixer.Sound("Sounds/game_over.wav")
jumpsound=pygame.mixer.Sound("Sounds/jumpsound.wav")
buttonsound=pygame.mixer.Sound("Sounds/buttonsound.wav")
soundtrack=pygame.mixer.Sound("Sounds/soundtrack.wav")

#creating entities
planks=[]
cps=[]
prjs=[]
enemies=[]
entities=[]
pirate=player(300,screeny//2,128,96,5,3,'axe')

plank_texture=pygame.image.load('Graphism/plank1.png').convert_alpha()
#creating all the buttons
button_setting=image_button(256,128,screenx//2-128,screeny//2-64,pygame.image.load('Graphism/button0.png').convert_alpha())
button_control=text_button(256,128,screenx//2-128,screeny//2+128,Language['control_button'],20,128//3+20,(255,233,0))
button_control_left=control_button(128,64,128,20,Language['left_control_button'],0,0,(255,233,0))
button_control_jump=control_button(128,64,128,2*20+64,Language['jump_control_button'],0,0,(255,233,0))
button_control_right=control_button(128,64,128,3*20+2*64,Language['right_control_button'],0,0,(255,233,0))
button_control_down=control_button(128,64,128,4*20+3*64,Language['down_control_button'],0,0,(255,233,0))
button_control_shoot=control_button(128,64,128,5*20+4*64,Language['shoot_control_button'],0,0,(255,233,0))
button_controls=[button_control_left,button_control_right,button_control_down,button_control_jump,button_control_shoot]

if last_save=='None':
    button_continue=text_button(256,128,screenx//3,0,Language['button_continue'],20,128//3+20,(155,133,0))
else:
    button_continue=text_button(256,128,screenx//3,0,Language['button_continue'],20,128//3+20,(255,233,0))
if level_editor_unlocked(last_save):
    button_level_editor=text_button(256,128,0,0,Language['level_editor_button'],20,128//3+20,(255,233,0))
    button_load_levels=text_button(256,128,0,128,Language['button_load_levels'],20,128//3+20,(255,233,0))
else:
    button_level_editor=image_button(256,128,0,0,pygame.transform.scale(pygame.image.load("Graphism/lock.png").convert_alpha(),(64,64)),96,32,1)
    button_load_levels=text_button()#creating an empty button for the button menu to load it even if we don't wont to display it
button_language=text_button(256,128,screenx//2-512,screeny//2+128,Language['language_button'],20,128//3+20,(255,233,0))
french_button=language_button(256,128,screenx//2-512,screeny//2+128,'French',pygame.image.load('Graphism/drapeaux_fr2.PNG').convert_alpha())
english_button=language_button(256,128,screenx//2-512,screeny//2-128,'English',pygame.image.load('Graphism/drapeaux_en2.PNG').convert_alpha())
button_languages=[french_button,english_button]
button_menu=[button_language,button_control,button_level_editor,button_load_levels,button_continue]

#load saves
button_save_1=text_button(screenx/3-3*10, screeny-20, 10, 10, 'File1',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_2=text_button(screenx/3-3*10, screeny-20, 10+screenx/3-2*10, 10, 'File2',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_3=text_button(screenx/3-3*10, screeny-20, 10+2*(screenx/3-10), 10, 'File3',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save=[button_save_1,button_save_2,button_save_3]

while not end:
    #main menu
    while not start:
        frame.tick(10)
        screen.fill([100,20, 20])
        screen.blit(pygame.image.load('Graphism/button0.png').convert_alpha(),(screenx//2-128,screeny//2-64))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=True
                start=True
                play=False
        #button
        pygame.event.get()
        for button in button_menu:
            button.draw(screen)
            if button.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0]:
                    if button.name==Language['control_button']:
                        control_setting=True
                    elif button.name==Language['language_button']:
                        language_setting=True
                    elif button.name==Language['level_editor_button']:
                        level_editor=True
                    elif button.name==Language['button_load_levels']:
                        load_levels=True
                        display_levels(plank_texture)
                        play=True
                    start=True
        if screenx//2-128<=pygame.mouse.get_pos()[0]<=screenx//2+128 and screeny//2-64<pygame.mouse.get_pos()[1]<screeny//2+64:
            if pygame.mouse.get_pressed()[0]:
                choose_save=True
                start=True
                clicking=True
                screen.blit(pygame.image.load('Graphism/button3.png').convert_alpha(),(screenx//2-128,screeny//2-64))
            else:
                screen.blit(pygame.image.load('Graphism/button2.png').convert_alpha(),(screenx//2-128,screeny//2-64))
        pygame.display.update()

    while choose_save:
        if not(pygame.mouse.get_pressed()[0]):
            clicking=False
        screen.fill([100,20, 20])
        for button in button_save:
            button.draw(screen,1)
            if button.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0] and not(clicking):
                    print("choosed : "+button.info)
                    next_level=load_save(button.info)
                    if next_level!='':
                        planks=[]
                        cps=[]
                        prjs=[]
                        '''enemies=[]
                        entities=[pirate]'''
                        load(next_level,plank_texture)
                        reset_player()
                        pygame.mixer.stop()
                        buttonsound.play()
                        soundtrack.play()
                        play=True
                        choose_save=False
                        print(str(pirate.x)+'   '+str(pirate.y))
                    else:
                        print('Wow such empty')
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                choose_save=False
                end=True
            if event.type==pygame.KEYDOWN and event.key==pygame.K_ESCAPE:
                choose_save=False
                start=False
        pygame.display.update()

    #the game
    frame_per_frame=False
    pause=False
    while play:
        frame.tick(60)
        print(frame)
        if frame_per_frame:
            frame.tick(1)
        if pause:
            while pause:
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        play=False
                        end=True
                        pause=False
                keys=pygame.key.get_pressed()
                if keys[pygame.K_LSHIFT] and keys[pygame.K_o]:
                    pause=False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                play=False
                end=True
                #goto settings
        if pygame.mouse.get_pressed()[0] and screenx-64<=pygame.mouse.get_pos()[0]<=screenx and 0<=pygame.mouse.get_pos()[1]<=64:
            settings=True
            play=False
            pygame.mixer.pause()
        else:
            screen.blit(bg,(0,0))
            keys=pygame.key.get_pressed()
            pirate.spdx=0
            if keys[pygame.K_p] and not(keys[pygame.K_LSHIFT]) and not(frame_per_frame):
                frame_per_frame=True
            elif keys[pygame.K_LSHIFT] and keys[pygame.K_p] and frame_per_frame:
                frame_per_frame=False
            elif keys[pygame.K_o] and not(keys[pygame.K_LSHIFT]) and not(pause):
                pause=True
            elif keys[pygame.K_d] or keys[ControlOpt['right']]:
                pirate.stand=False
                pirate.left=False
                pirate.right=True
                pirate.spdx=15
            elif keys[pygame.K_a] or keys[ControlOpt['left']]:
                pirate.stand=False
                pirate.right=False
                pirate.left=True
                pirate.spdx=-15
            else:
                pirate.stand=True

            for i in entities:
                if not i.isground:
                    i.spdy+=i.mass*g//7
                i.isground=False

            for i in planks:
                i.check()
                i.draw()

            if (keys[pygame.K_w] or keys[ControlOpt['up']]) and pirate.isground and not pirate.spdy:
                jumpsound.play()
                pirate.spdy=pirate.jump

            if pirate.y>screeny and pirate.life>1:
                if pirate.spawnpoint[0]!=300:
                    for i in planks:
                        i.x+=300-pirate.spawnpoint[0]
                    for i in cps:
                        i.x+=300-pirate.spawnpoint[0]
                    for i in prjs:
                        i.x+=300-pirate.spawnpoint[0]
                    for i in enemies:
                        i.x+=300-pirate.spawnpoint[0]
                    pirate.spawnpoint[0]=300
                if pirate.spawnpoint[1]!=350:
                    for i in planks:
                        i.y+=350-pirate.spawnpoint[1]
                    for i in cps:
                        i.y+=350-pirate.spawnpoint[1]
                    for i in prjs:
                        i.y+=350-pirate.spawnpoint[1]
                    for i in enemies:
                        i.y+=350-pirate.spawnpoint[1]
                    pirate.spawnpoint[1]=350
                pirate.spdy=0
                pirate.x=pirate.spawnpoint[0]
                pirate.y=pirate.spawnpoint[1]
                pirate.life-=1
                pirate.isground=True
                deathsound.play()
            elif pirate.y>screeny:
                play=False
                start=False
                pygame.mixer.stop()
                deathsound.play()
                game_over.play()
            if keys[ControlOpt['shoot']]:
                pirate.attack()
            if pirate.hit==1:
                pirate.hit=2
            for i in enemies:
                if i.y>screeny:
                    i.life=0
                    enemies.remove(i)
                    entities.remove(i)
                if i.hit==1:
                    i.hit=2
                for k in prjs:
                    if collide(i,k):
                        if i.hit==0:
                            i.hit=1
                            i.life-=1
                            if i.life==0:
                                pirate.money+=1
                                enemies.remove(i)
                                entities.remove(i)
                        elif i.hit==2:
                            i.hit=1
                if i.hit==2:
                    i.hit=0
                for j in planks:
                    if j.x+i.width-10<=i.x+i.width<=j.x+j.width+10:
                        if not i.turn and i.x+i.width>=j.x+j.width:
                            i.turn=True
                        if i.turn and j.x+i.width>=i.x+i.width:
                            i.turn=False
                        elif i.x-300<pirate.x<i.x and pirate.y-15<i.y<pirate.y+15:
                            i.turn=True
                        elif i.x+300>pirate.x>i.x and pirate.y-15<i.y<pirate.y+15:
                            i.turn=False
                if i.isground and not i.turn:
                    i.x+=10
                    i.stand=False
                    i.right=True
                    i.left=False
                elif i.isground:
                    i.x-=10
                    i.stand=False
                    i.right=False
                    i.left=True
                '''
                if collide(i,pirate):
                    if pirate.hit==0:
                        pirate.life-=1
                        pirate.hit=1
                        if i.direction=='left':
                            pirate.spdx-=10
                        elif i.direction=='right':
                            pirate.spdx+=10
                        pirate.spdy+=10
                    elif pirate.hit==2:
                        pirate.hit=1
            if pirate.hit==2:
                pirate.hit=0'''
            for i in entities:
                i.move()
            for i in prjs:
                i.move()
            for i in planks:
                i.draw()
            for i in cps:
                i.draw()
            for i in entities:
                i.draw(hitbox=True)
            for i in enemies:
                i.health_bar()
            pirate.health_draw()
            screen.blit(parawheel,(screenx-64,0))
            if pirate.life==0:
                play=False
                start=False

        pygame.display.update()

    while settings:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                settings=False
                end=True
        screen.fill([100,20, 20])
        button_setting.draw(screen)
        if pygame.mouse.get_pressed()[0]:
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            if button_setting.collide(posX,posY):
                settings=False
                buttonsound.play()
                pygame.mixer.unpause()
                play=True
        pygame.display.update()

    while control_setting:
        screen.fill([100,20, 20])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                settings=False
                end=True
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            control_setting=False
            start=False
        for Button in button_controls:
            Button.draw(screen,1)
        if pygame.mouse.get_pressed()[0]:
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            for Button in button_controls:
                if Button.collide(posX,posY):
                    getting=True
                    print('getting')
                    while getting:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                getting=False
                            elif event.type == pygame.KEYDOWN:
                                print('get')
                                ControlOpt=Button.controls(event.key)
                                SaveOption()
        pygame.display.update()

    while language_setting:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                settings=False
                end=True
                print("quit")
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            print("exit")
            language_setting=False
            start=False
        for button in button_languages:
            button.draw(screen)
        if pygame.mouse.get_pressed()[0]:
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            for Button in button_languages:
                if Button.collide(posX,posY):
                    print(Button.name)
                    Language["language"]=Button.name
                    SaveOption()
        pygame.display.update()

    if level_editor:
        pygame.display.set_caption("Level Editor")
        print("level editor")
        screen=main(screen)
        level_editor=False
        start=False

pygame.quit()
