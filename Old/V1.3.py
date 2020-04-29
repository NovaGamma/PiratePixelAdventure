import pygame
from pygame.locals import*
import os

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

class platform(object):
    def __init__(self,x,y,h,w,img):
        self.x=x
        self.y=y+pirate.h
        self.h=h
        self.w=w
        self.img=pygame.transform.scale(img,(self.w,self.h))
        planks.append(self)
    def draw(self):
        if self.x+self.w>=0 and self.x<screenx:
            screen.blit(self.img,(self.x,self.y))
    def check(self):
        if self.y+15-pirate.h>=pirate.y>=self.y+pirate.spdy-pirate.h and self.x-pirate.w+20<=pirate.x<=-20+self.x+self.w:
            pirate.spdy=0
            pirate.y=self.y-pirate.h
            pirate.isground=True
            pirate.isjump=False

class player(object):
    def __init__(self,x,y,h,w,m,health,prj):
        self.x=x
        self.y=y
        self.m=m
        self.h=h
        self.w=w
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
        self.attack=False
        self.cooldown=0
    def draw(self):
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
        screen.blit(pygame.transform.scale(self.info,(self.w,self.h)),(self.x,self.y))
        heart=0
        for i in range(self.life):
            screen.blit(f_heart,(heart,0))
            heart+=70
        for i in range(self.health-self.life):
            screen.blit(e_heart,(heart,0))
            heart+=70
        if self.cooldown>0:
            self.cooldown-=1
        if self.attack:
            if self.prj=='axe' and self.cooldown==0:
                throwsound.play()
                if self.left:
                    a=projectile(self.x,self.y+self.h//2-self.spdy//2,self.spdx,self.spdy,'axe',-1)
                else:
                    a=projectile(self.x,self.y+self.h//2-self.spdy//2,self.spdx,self.spdy,'axe',1)
                prjs.append(a)
                self.cooldown=20
            if self.prj=='knife' and self.cooldown<=10:
                throwsound.play()
                if self.left:
                    k=projectile(self.x,self.y+self.h//2-self.spdy//2,self.spdx,self.spdy,'knife',-1)
                else:
                    k=projectile(self.x,self.y+self.h//2-self.spdy//2,self.spdx,self.spdy,'knife',1)
                prjs.append(k)
                self.cooldown=20

class cp(object):
    def __init__(self,x,y):
        self.w=128
        self.h=128
        self.x=x
        self.y=y
        self.cpcount=0
        self.cpt=False
        cps.append(self)
    def draw(self):
        if self.x-pirate.w+20<=pirate.x<=self.x+self.w and self.y-self.h<=pirate.y<=self.y+pirate.h and not self.cpt:
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
        if self.x+self.w>=0 and self.x<screenx:
            screen.blit(chestpoint[self.cpcount//2],(self.x,self.y))

class projectile(object):
    def __init__(self,x,y,spdx,spdy,typ,direction):
        self.x=x
        self.y=y
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
                screen.blit(laxx[self.count%16//2],(self.x,self.y))
            else:
                screen.blit(raxx[self.count%16//2],(self.x,self.y))
        if 0>self.x or self.x>screenx or self.y>screeny:
            prjs.remove(self)
        self.count+=1

def load_lvl1():
    #set pos of pirate
    pirate.life=3
    pirate.x=300
    pirate.y=screeny//2
    pirate.spdy=0
    pirate.spdx=0
    pirate.isjump=0
    pirate.isground=1
    pirate.spawnpoint=[300,screeny//2]

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
            work=True
            while work:
                try:
                    line=controlFile.readline()
                    print(line)
                    temp=line.split(':')
                    ControlOpt[temp[0]]=int(temp[1])
                except:
                    work=False
    if os.path.exists("Language"):
        with open("Language/"+language+'.txt') as text:
            Language["language"]=language
            for line in text:
                temp=line.split(' ')
                Language[temp[0]]=temp[1].rstrip('\n')
    else:
        print("Error : No Language directory found\nCan't load the language")
    return [ScreenOpt,ControlOpt,Language]
    if not(os.path.exists("Graphism")):
        os.mkdir('Graphism')

def load(level,plank1):
    levels_name = os.listdir("Levels/")
    name=level
    pos=-1
    for levels in levels_name:
        if name==levels:
            pos=levels_name.index(levels)
    if pos!=-1:
        planks=[]
        cps=[]
        with open("Levels/"+levels_name[pos]+'/entities.txt','r') as level:
            for line in level:
                parameters=line.split(' ')
                if parameters[0]=='plank':
                    planks.append(platform(int(parameters[1]),int(parameters[2]),int(parameters[3]),int(parameters[4]),plank1))    
                elif parameters[0]=='cp':
                    cps.append(cp(int(parameters[1]),int(parameters[2])))
                elif parameters[0]=='spawn':
                    pirate.spawnpoint=[parameters[1],parameters[2]]

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
SaveOption()
pygame.display.set_caption(Language["title"])
frame=pygame.time.Clock()
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('Graphism/bg (1).png'),(screenx,screeny))
play=False
start=False
end=False
settings=False
control_setting=False
language_setting=False
g=9.81
#loading textures
jumpright=[pygame.image.load('Graphism/jumpright0.png'),pygame.image.load('Graphism/jumpright1.png'),pygame.image.load('Graphism/jumpright2.png')]
jumpleft=[pygame.image.load('Graphism/jumpleft0.png'),pygame.image.load('Graphism/jumpleft1.png'),pygame.image.load('Graphism/jumpleft2.png')]
walkright=[]
walkleft=[]
for i in range(8):
    temp='rright'+str(i)+'.png'
    temp2='lleft'+str(i)+'.png'
    walkright.append(pygame.image.load('Graphism/'+temp))
    walkleft.append(pygame.image.load('Graphism/'+temp2))
chestpoint=[pygame.image.load('Graphism/chestpoint (1).png'),pygame.image.load('Graphism/chestpoint (2).png'),pygame.image.load('Graphism/chestpoint (3).png'),pygame.image.load('Graphism/chestpoint (4).png'),pygame.image.load('Graphism/chestpoint (5).png')]
f_heart=pygame.transform.scale(pygame.image.load('Graphism/Full_heart1.png'),(64,64))
e_heart=pygame.transform.scale(pygame.image.load('Graphism/Empty_heart.png'),(64,64))
raxx=[pygame.transform.scale(pygame.image.load('Graphism/raxx0.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx1.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx2.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx3.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx4.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx5.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx6.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/raxx7.png'),(64,64))]
laxx=[pygame.transform.scale(pygame.image.load('Graphism/laxx0.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx1.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx2.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx3.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx4.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx5.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx6.png'),(64,64)),pygame.transform.scale(pygame.image.load('Graphism/laxx7.png'),(64,64))]
rniff=pygame.image.load('Graphism/rniff.png')
lniff=pygame.image.load('Graphism/lniff.png')
parawheel=pygame.image.load('Graphism/parawheel1.png')
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
spawnpoint=[300,screeny//2]
pirate=player(300,screeny//2,128,96,1,3,'axe')
plank_texture=pygame.image.load('Graphism/plank1.png')
load('level',plank_texture)
#creating all the buttons
button_setting=image_button(256,128,screenx//2-128,screeny//2-64,pygame.image.load('Graphism/button0.png'))
button_control=text_button(256,128,screenx//2-128,screeny//2+128,Language['control_button'],20,128//3+20,(255,233,0))
button_control_left=control_button(128,64,128,20,Language['left_control_button'],0,0,(255,233,0))
button_control_jump=control_button(128,64,128,2*20+64,Language['jump_control_button'],0,0,(255,233,0))
button_control_right=control_button(128,64,128,3*20+2*64,Language['right_control_button'],0,0,(255,233,0))
button_control_down=control_button(128,64,128,4*20+3*64,Language['down_control_button'],0,0,(255,233,0))
button_control_shoot=control_button(128,64,128,5*20+4*64,Language['shoot_control_button'],0,0,(255,233,0))
button_controls=[button_control_left,button_control_right,button_control_down,button_control_jump,button_control_shoot]

button_language=text_button(256,128,screenx//2-512,screeny//2+128,Language['language_button'],20,128//3+20,(255,233,0))

button_menu=[button_language,button_control]
while not end:
    #main menu
    while not start:
        frame.tick(10)
        screen.fill([100,20, 20])
        screen.blit(pygame.image.load('Graphism/button0.png'),(screenx//2-128,screeny//2-64))
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
            if button_control.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0]:
                    if button.name==Language['control_button']:
                        control_setting=True
                    elif button.name==Language['language_button']:
                        language_setting=True
                    start=True
        if screenx//2-128<=pygame.mouse.get_pos()[0]<=screenx//2+128 and screeny//2-64<pygame.mouse.get_pos()[1]<screeny//2+64:
            if pygame.mouse.get_pressed()[0]:
                load_lvl1()
                pygame.mixer.stop()
                buttonsound.play()
                soundtrack.play()
                start=True
                play=True
                screen.blit(pygame.image.load('Graphism/button3.png'),(screenx//2-128,screeny//2-64))
            else:
                screen.blit(pygame.image.load('Graphism/button2.png'),(screenx//2-128,screeny//2-64))
        pygame.display.update()
    #the game
    while play:
        frame.tick(25)
        print(frame)
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
            pirate.isground=False
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
            if not pirate.isground:
                pirate.isjump=True
                pirate.spdy-=pirate.m*g
                pirate.y-=pirate.spdy
                
            if pirate.y>screeny and pirate.life>1:
                if pirate.spawnpoint[0]!=300:
                    for i in planks:
                        i.x+=300-pirate.spawnpoint[0]
                    for i in cps:
                        i.x+=300-pirate.spawnpoint[0]
                    for i in prjs:
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
                if pirate.x<screenx-400-pirate.w:
                    pirate.x+=pirate.spdx
                else:
                    for i in planks:
                        i.x-=pirate.spdx
                    for i in cps:
                        i.x-=pirate.spdx
                    for i in prjs:
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
                    pirate.spawnpoint[0]-=pirate.spdx
            else:
                pirate.stand=True
            pirate.attack=False
            if keys[ControlOpt['shoot']] and not pirate.attack:
                pirate.attack=True
            for i in planks:
                i.check()
                i.draw()
            for i in cps:
                i.draw()
            for i in prjs:
                i.move()
            pirate.draw()
            screen.blit(parawheel,(screenx-64,0))
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
                                SaveOption(ScreenOpt,ControlOpt)
        pygame.display.update()

        while language_setting:
            pass

pygame.quit()