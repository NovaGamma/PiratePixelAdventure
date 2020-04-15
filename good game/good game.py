import pygame

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
            if i.y+i.height<=self.y<=i.y+i.height+i.spdy and self.x-i.width+20<=i.x<=-20+self.x+self.width:
                i.spdy=self.y-i.y-i.height
                i.isground=True
class people(object):
    def __init__(self,x,y,height,width,mass,health,prj=None):
        self.x=x
        self.y=y
        self.mass=mass
        self.height=height
        self.width=width
        self.spdx=0
        self.spdy=0
        self.right=False
        self.left=False
        self.stand=True
        self.isground=False
        self.walkcount=0
        self.info=''
        self.info2=0
        self.jump=-50
        self.health=health
        self.life=self.health
        self.spawnpoint=[300,screeny//2]
        self.prj=prj
        self.cooldown=0
        self.turn=False#null
        self.hit=0

    def draw(self,hitbox=False):
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
        if hitbox:
            self.hitbox=(self.x,self.y,self.width,self.height)
            pygame.draw.rect(screen,(255,0,0),self.hitbox,2)
        if self.cooldown>0:
            self.cooldown-=1

class ennemy(people):
    def __init__(self,x,y,height,width,mass,health):
        people.__init__(self,x,y,height,width,mass,health)

    def move(self):
        self.x+=self.spdx
        self.y+=self.spdy
    def health_bar(self):
        pygame.draw.rect(screen,(0,0,0), (self.x+self.width/2-26*ratiox,-10+self.y-6*ratioy,52*ratiox,10*ratioy))
        pygame.draw.rect(screen,(255,0,0), (self.x+self.width/2-25*ratiox,-10+self.y-5*ratioy,50*self.life/self.health*ratiox,8*ratioy))

class player(people):
    def __init__(self,x,y,height,width,mass,health,prj):
        self.money=0
        people.__init__(self,x,y,height,width,mass,health,prj)
    
    def move(self):
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
        if (self.y>100 or self.spdy>0) and (self.y<screeny-200-self.height or self.spdy<0):
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

pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
screenx=1400
screeny=700
ratiox=screenx/1400
ratioy=screeny/700
frame=pygame.time.Clock()
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('Graphism/bg (1).png').convert_alpha(),(screenx,screeny))
g=9.81
jumpright=[pygame.image.load('Graphism/jumpright0.png').convert_alpha(),pygame.image.load('Graphism/jumpright1.png').convert_alpha(),pygame.image.load('Graphism/jumpright2.png').convert_alpha()]
jumpleft=[pygame.image.load('Graphism/jumpleft0.png').convert_alpha(),pygame.image.load('Graphism/jumpleft1.png').convert_alpha(),pygame.image.load('Graphism/jumpleft2.png').convert_alpha()]
walkright=[]
walkleft=[]
plank_texture=pygame.image.load('Graphism/plank1.png').convert_alpha()
for i in range(8):
    temp='rright'+str(i)+'.png'
    temp2='lleft'+str(i)+'.png'
    walkright.append(pygame.image.load('Graphism/'+temp).convert_alpha())
    walkleft.append(pygame.image.load('Graphism/'+temp2).convert_alpha())
f_heart=pygame.transform.scale(pygame.image.load('Graphism/Full_heart1.png').convert_alpha(),(64,64))
e_heart=pygame.transform.scale(pygame.image.load('Graphism/Empty_heart.png').convert_alpha(),(64,64))
parawheel=pygame.image.load('Graphism/parawheel1.png').convert_alpha()

#creating entities
planks=[]
platform(100,500,50,3000,plank_texture)
platform(100,300,50,3000,plank_texture)
platform(100,100,50,3000,plank_texture)
cps=[]
prjs=[]
enemies=[]
entities=[]
spawnpoint=[300,screeny//2]
pirate=player(300,350,128,96,1,3,'axe')
entities.append(pirate)
for a in range(0,500,50):
    enemies.append(ennemy(350+2*a,screeny//2-50-3*a,128,96,1,2))
    entities.append(enemies[-1])
play=True
while play:
    frame.tick(60)
    print(frame)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
            #goto settings
    screen.blit(bg,(0,0))
    keys=pygame.key.get_pressed()
    if pirate.y>screeny:
        play=False
    pirate.spdx=0
    if keys[pygame.K_d]:
        pirate.stand=False
        pirate.left=False
        pirate.right=True
        pirate.spdx=20
    elif keys[pygame.K_a]:
        pirate.stand=False
        pirate.right=False
        pirate.left=True
        pirate.spdx=-20
    else:
        pirate.stand=True
    
    for i in enemies:
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
            i.spdx=5
            i.stand=False
            i.right=True
            i.left=False
        elif i.isground:
            i.spdx=-5
            i.stand=False
            i.right=False
            i.left=True

    for i in entities:
        if not i.isground:
            i.spdy+=i.mass*g//3
        i.isground=False

    
    for i in planks:
        i.check()

    

    if keys[pygame.K_w] and pirate.isground and not pirate.spdy:
        pirate.isground=False
        pirate.spdy=pirate.jump

    for i in entities:
        i.move()
    
    for i in planks:
        i.draw()
    for i in cps:
        i.draw()
    for i in entities:
        i.draw(True)
    for i in enemies:
        i.health_bar()
    pygame.display.update()
pygame.quit()