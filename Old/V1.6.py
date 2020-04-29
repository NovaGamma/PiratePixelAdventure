import pygame
from pygame.locals import*
import os
import random

class button:
    def __init__(self,height,width,x,y):
        self.height=height
        self.width=width
        self.x=x
        self.y=y

    def collide(self,posX,posY):
        if (posX>=self.x and posX<=self.x+self.width) and (posY>=self.y and posY<=self.y+self.height):
            return 1
        return 0

class text_button(button):
    def __init__(self,width,height,x,y,text,posX=None,posY=None,color=None):#posX and posY are in function of the pos of the button
        self.info=text
        if posX!=None and posY!=None:
            self.textX=posX
            self.textY=posY
        else:
            self.textX='0'
        if color==None:
            self.text=font.render(text,0,(255,255,255))
        else:
            self.text=font.render(text,0,color)
        self.name=text
        self.rect=pygame.Surface((width,height))
        self.rect.fill((115, 54, 0))
        self.rect.set_alpha(180)
        button.__init__(self,height,width,x,y)

    def draw(self,r):
        if r:
            screen.blit(self.rect,(self.x,self.y))
        if self.textX=='0':
            screen.blit(self.text,(self.x,self.y))
        else:
            screen.blit(self.text,(self.x+self.textX,self.y+self.textY))

class image_button(button):
    def __init__(self,width,height,x,y,image):
        self.image=image
        button.__init__(self,height,width,x,y)

    def draw(self):
        screen.blit(self.image,(self.x,self.y))

class control_button(text_button):
    def __init__(self,width,height,x,y,text,posX=None,posY=None,color=None):
        text_button.__init__(self,width,height,x,y,text,posX,posY,color)
        self.control=text

    def controls(self,Id):#control is the control that we are going to change, Id is the id of the key that will be used for that control
        ControlOpt[self.control]=Id
        return ControlOpt

class language_button(button):
    def __init__(self,width,height,x,y,text,image,color_text=None):
        self.rect=pygame.Surface((width,height))
        self.rect.fill((179, 179, 179))
        self.rect.set_alpha(180)
        self.name=text
        self.image=image_button(width,height,x+10,y+(height//3)-10,image)
        button.__init__(self,height,width,x,y)
        self.text=text_button(width,height,x+70,y+(height//3),text,color_text)

    def draw(self):
        screen.blit(self.rect,(self.x,self.y))
        self.image.draw()
        self.text.draw(0)

class platform(object):
    def __init__(self,x,y,height,width,img):
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.img=pygame.transform.scale(img,(self.width,self.height))
        planks.append(self)
    def draw(self):
        if self.x+self.width>=0 and self.x<screenx:
            screen.blit(self.img,(self.x,self.y))
    def check(self):
        for i in entities:
            if self.y+15-i.height>=i.y>=self.y+i.spdy-i.height and self.x-i.width+20<=i.x<=-20+self.x+self.width:
                i.spdy=0
                i.y=self.y-i.height
                i.isground=True
                i.isjump=False

class people(object):
    def __init__(self,x,y,height,width,mass,health,prj=None):
        entities.append(self)
        self.x=x
        self.y=y
        self.mass=mass
        self.height=height
        self.width=width
        self.spdx=0
        self.spdy=0
        self.right=False
        self.left=False
        self.isjump=False
        self.stand=True
        self.isground=False
        self.walkcount=0
        self.info=''
        self.info2=0
        self.jump=60
        self.jumpi=60 #gonna be removed
        self.health=health
        self.life=self.health
        self.spawnpoint=[300,screeny//2]
        self.prj=prj
        self.cooldown=0
        self.turn=False#null
        self.hit=0

    def draw(self,hitbox=False):
        if not self.isground:
            if self.spdy>5:
                self.info2=0
            elif self.spdy>-20:
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
                self.info=walkleft[self.walkcount//2%8]
            else:
                self.info=walkright[self.walkcount//2%8]
        screen.blit(pygame.transform.scale(self.info,(self.width,self.height)),(self.x,self.y))
        if hitbox:
            self.hitbox=(self.x,self.y,self.width,self.height)
            pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
        if self.cooldown>0:
            self.cooldown-=1

    def direction(self):
        if self.right:
            return 'right'
        elif self.left:
            return 'left'
        else:
            return 'None'

class ennemy(people):
    def __init__(self,x,y,height,width,mass,health):
        people.__init__(self,x,y,height,width,mass,health)
        enemies.append(self)

    def move(self):
        pass

    def health_bar(self):
        pygame.draw.rect(screen,(0,0,0), (self.x+self.width/2-26*ratiox,-10+self.y-6*ratioy,52*ratiox,10*ratioy))
        pygame.draw.rect(screen,(255,0,0), (self.x+self.width/2-25*ratiox,-10+self.y-5*ratioy,50*self.life/self.health*ratiox,8*ratioy))

class player(people):
    def __init__(self,x,y,height,width,mass,health,prj):
        self.money=0
        people.__init__(self,x,y,height,width,mass,health,prj)

    def attack(self):
        if self.prj=='axe' and self.cooldown==0:
            throwsound.play()
            if self.left:
                a=projectile(self.x,self.y+self.height//2-self.spdy//2,self.spdx,self.spdy,'axe',-1,'player')
            else:
                a=projectile(self.x,self.y+self.height//2-self.spdy//2,self.spdx,self.spdy,'axe',1,'player')
            prjs.append(a)
            self.cooldown=20
        if self.prj=='knife' and self.cooldown<=10:
            throwsound.play()
            if self.left:
                k=projectile(self.x,self.y+self.height//2-self.spdy//2,self.spdx,self.spdy,'knife',-1,'player')
            else:
                k=projectile(self.x,self.y+self.height//2-self.spdy//2,self.spdx,self.spdy,'knife',1,'player')
            prjs.append(k)
            self.cooldown=20

    def health_draw():
        heart=0
        for i in range(pirate.life):
            screen.blit(f_heart,(heart,0))
            heart+=70
        for i in range(pirate.health-pirate.life):
            screen.blit(e_heart,(heart,0))
            heart+=70

def health_draw():
        heart=0
        for i in range(pirate.life):
            screen.blit(f_heart,(heart,0))
            heart+=70
        for i in range(pirate.health-pirate.life):
            screen.blit(e_heart,(heart,0))
            heart+=70

class cp(object):
    def __init__(self,x,y):
        self.width=128
        self.height=128
        self.x=x
        self.y=y
        self.cpcount=0
        self.cpt=False
        cps.append(self)
    def draw(self):
        if self.x-pirate.width+20<=pirate.x<=self.x+self.width and self.y-self.height<=pirate.y<=self.y+pirate.height and not self.cpt:
            self.cpt=True
            pirate.spawnpoint=[self.x,self.y]
            chestsound.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
            chestsound2.play()
        if self.cpcount<9 and self.cpt:
            self.cpcount+=1
        if self.x+self.width>=0 and self.x<screenx:
            screen.blit(chestpoint[self.cpcount//2],(self.x,self.y))

class projectile(object):
    def __init__(self,x,y,spdx,spdy,typ,direction,owner):
        self.x=x
        self.y=y
        self.width=64#null
        self.height=64#null
        self.aspdx=30+spdx//2*direction
        self.aspdy=-50-spdy//2
        self.kspdx=50+spdx//2*direction
        self.am=0.5
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
                drawn_projectile=laxx[self.count%16//2]
                drawn_hitbox=laxx_hitbox[self.count%16//2]
            else:
                drawn_projectile=raxx[self.count%16//2]
                drawn_hitbox=raxx_hitbox[self.count%16//2]
            screen.blit(drawn_projectile,(self.x,self.y))
            self.hitbox=(self.x+drawn_hitbox[0],self.y+drawn_hitbox[1],drawn_hitbox[2],drawn_hitbox[3])
            pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
        if 0>self.x or self.x>screenx or self.y>screeny:
            prjs.remove(self)
        self.count+=1

def reset_player():
    pirate.life=3
    pirate.spdy=0
    pirate.spdx=0
    pirate.isjump=0
    pirate.isground=1

def SaveOption():
    if not os.path.exists('Config'):
        os.mkdir('Config')
    with open("Config/Game_Option.txt", "w+") as optionFile:
        for key in ScreenOpt.keys():
            temp=key+' '+str(ScreenOpt[key])+'\n'
            optionFile.write(temp)
        optionFile.write('language '+Language["language"])
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
                if not(temp[0]=="language"):
                    print(temp)
                    ScreenOpt[temp[0]]=int(temp[1])
                else:
                    language=temp[1]
        print(ScreenOpt)
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
            print("Error : ",language," not found")
    else:
        print("Error : No Language directory found\nCan't load the language")
    return [ScreenOpt,ControlOpt,Language]
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
                    print(line+" didn't load successully")
            return next_level
    else:
        print("This save file doesn't exists")
    return ''

def load(level,plank1):
    if os.path.exists("Levels/"+level):
        with open("Levels/"+level+'/entities.txt','r') as levelFile:
            print("loading : "+level)
            for line in levelFile:
                parameters=line.split(' ')
                if parameters[0]=='plank':
                        platform(int(parameters[1]),int(parameters[2]),int(parameters[3]),int(parameters[4]),plank1)
                elif parameters[0]=='cp':
                        cp(int(parameters[1]),int(parameters[2]))
                elif parameters[0]=='spawn':
                    pirate.spawnpoint=[int(parameters[1]),int(parameters[2])]
                elif parameters[0]=='ennemy':
                    pass
    else:
        print("Level not found")

def collide(first,second):
    if first.x<=second.x+second.width<=first.x+first.width+second.width and first.y<=second.y+second.height<=first.y+first.height+second.height:
        return 1
    return 0

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
print(ScreenOpt)
print(ControlOpt)
screenx=ScreenOpt['screenX']
screeny=ScreenOpt['screenY']
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
choose_save=False
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
spawnpoint=[300,screeny//2]
pirate=player(300,screeny//2,128,96,1,3,'axe')
for a in range(0,500,50):
    ennemy(350+2*a,screeny//2-50-3*a,128,96,1,2)

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

button_language=text_button(256,128,screenx//2-512,screeny//2+128,Language['language_button'],20,128//3+20,(255,233,0))
french_button=language_button(256,128,screenx//2-512,screeny//2+128,'French',pygame.image.load('Graphism/drapeaux_fr2.PNG').convert_alpha())
english_button=language_button(256,128,screenx//2-512,screeny//2-128,'English',pygame.image.load('Graphism/drapeaux_en2.PNG').convert_alpha())
button_languages=[french_button,english_button]
button_menu=[button_language,button_control]

#load saves
button_save_1=text_button(screenx/3-3*10, screeny-20, 10, 10, 'File 1',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_2=text_button(screenx/3-3*10, screeny-20, 10+screenx/3-2*10, 10, 'File 2',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_3=text_button(screenx/3-3*10, screeny-20, 10+2*(screenx/3-10), 10, 'File 3',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save=[button_save_1,button_save_2,button_save_3]

while not end:
    #main menu
    while not start:
        frame.tick(10)
        screen.fill([100,20, 20])
        screen.blit(pygame.image.load('Graphism/button0.png').convert_alpha(),(screenx//2-128,screeny//2-64))
        button_control.draw(1)
        button_language.draw(1)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=True
                start=True
                play=False
        #button
        pygame.event.get()
        for button in button_menu:
            if button.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0]:
                    if button.name==Language['control_button']:
                        control_setting=True
                    elif button.name==Language['language_button']:
                        language_setting=True
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
            button.draw(1)
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
    while play:
        frame.tick(25)
        #print(frame)
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
            for i in entities:
                i.isground=False
            if pirate.y>screeny//2-pirate.spdy:#gonna be removed (swim)
                pirate.isjump=False
                pirate.jump=20
            else:
                pirate.jump=pirate.jumpi
            if (keys[pygame.K_w] or keys[ControlOpt['up']]) and not pirate.isjump:
                if pirate.y<=screeny//2-pirate.spdy:#gonna be removed (swim)
                    jumpsound.play()
                pirate.isjump=True
                pirate.isground=False
                pirate.spdy=pirate.jump
            for i in entities:
                if not i.isground:
                    i.isjump=True
                    i.spdy-=i.mass*g
                    i.y-=i.spdy

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
                pirate.spdy=0
                pirate.x=pirate.spawnpoint[0]
                pirate.y=pirate.spawnpoint[1]
                pirate.life-=1
                deathsound.play()
            elif pirate.y>screeny:
                play=False
                start=False
                pygame.mixer.stop()
                deathsound.play()
                game_over.play()
            pirate.spdx=0
            if keys[pygame.K_d] or keys[ControlOpt['right']]:
                pirate.stand=False
                pirate.left=False
                pirate.right=True
                pirate.spdx=30
                if pirate.x<screenx-400-pirate.width:
                    pirate.x+=pirate.spdx
                else:
                    for i in planks:
                        i.x-=pirate.spdx
                    for i in cps:
                        i.x-=pirate.spdx
                    for i in prjs:
                        i.x-=pirate.spdx
                    for i in enemies:
                        i.x-=pirate.spdx
                    pirate.spawnpoint[0]-=pirate.spdx
            elif keys[pygame.K_a] or keys[ControlOpt['left']]:
                pirate.stand=False
                pirate.right=False
                pirate.left=True
                pirate.spdx=-30
                if pirate.x>200:
                    pirate.x+=pirate.spdx
                else:
                    for i in planks:
                        i.x-=pirate.spdx
                    for i in cps:
                        i.x-=pirate.spdx
                    for i in prjs:
                        i.x-=pirate.spdx
                    for i in enemies:
                        i.x-=pirate.spdx
                    pirate.spawnpoint[0]-=pirate.spdx
            else:
                pirate.stand=True
            if keys[ControlOpt['shoot']]:
                pirate.attack()
            for i in planks:
                i.check()
                i.draw()
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
                pirate.hit=0
            for i in cps:
                i.draw()
            for i in prjs:
                i.move()
            pirate.draw(hitbox=True)
            for i in enemies:
                i.draw(hitbox=True)
            for i in enemies:
                i.health_bar()
            health_draw()
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
        button_setting.draw()
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
            Button.draw(1)
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
            button.draw()
        if pygame.mouse.get_pressed()[0]:
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            for Button in button_languages:
                if Button.collide(posX,posY):
                    print(Button.name)
                    Language["language"]=Button.name
                    SaveOption()
        pygame.display.update()

pygame.quit()
