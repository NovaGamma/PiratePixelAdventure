import pygame
import math
import random
class boat1_part():
    def __init__(self,full_life,img,mask):
        self.full_life=full_life
        self.life=full_life
        self.img=img
        self.mask=mask
        self.damaged=0
        body_parts.append(self)
        body.append(self)
    def draw(self):
        if self.damaged:
            screen.blit(self.img[3],(boat1_x,boat1_y))
            self.damaged-=1
        elif self.life/self.full_life>0.5:
            screen.blit(self.img[0],(boat1_x,boat1_y))
        elif self.life>0:
            screen.blit(self.img[1],(boat1_x,boat1_y))
        else:
            screen.blit(self.img[2],(boat1_x,boat1_y))
class canon():
    def __init__(self,x,y,sort):
        self.x=x
        self.y=y
        self.w=cannon_w
        self.h=cannon_h
        self.sort=sort
        self.cooldown=0
        self.recoil=0
        self.damaged=0
        if sort==1:
            self.life=8
            self.degree=90
            self.next_degree=0
            self.ex_degree=90
            self.cooldown=80
        else:
            self.degree=270
        self.cooldown2=0
    def check(self):
        if not self.sort:
            if mouse_pos[1]<self.y+self.h/2:
                self.degree=math.atan2((mouse_pos[0]-self.x-self.w/2),(mouse_pos[1]-self.y-self.h/2))*180/math.pi+180
            else:
                self.degree=math.atan2((mouse_pos[0]-self.x-self.w/2),0)*180/math.pi+180
            if not blue and not 360>=self.degree>=315:
                if self.degree>=180:
                    self.degree=315
                else:
                    self.degree=0
        else:
            if self.cooldown==79:
                self.next_degree=45+random.randint(-40,45)
            elif not self.cooldown:
                self.ex_degree=self.degree
            elif self.cooldown>38:
                self.degree+=(self.next_degree-self.ex_degree)/40
    def draw(self):
        if blue and not self.sort or self.sort and not self.damaged:
            rotated_cannon=pygame.transform.rotate(cannon,self.degree)
        elif self.sort and self.damaged:
            rotated_cannon=pygame.transform.rotate(white_cannon,self.degree)
            self.damaged-=1
        else:
            rotated_cannon=pygame.transform.rotate(mortar,self.degree)
        cannon_size=rotated_cannon.get_size()
        screen.blit(rotated_cannon,(self.x+(self.w-cannon_size[0])/2,self.y+(self.h-cannon_size[1])/2))
        screen.blit(cannon_wheel,(self.x+2*ratiox,self.y+30*ratioy))
class projectile():
    def __init__(self,sort):
        self.w=20
        self.h=20
        if not sort or sort==2:
            ally_projectiles.append(self)
            self.x=cannon0.x+cannon0.w/2-self.w/2
            self.y=cannon0.y+cannon0.h/2-self.h/2
            if cannon0.degree<=90:
                ratio_x=-cannon0.degree/90
                ratio_y=cannon0.degree/90-1
            else:
                ratio_x=(360-cannon0.degree)/90
                ratio_y=(360-cannon0.degree)/90-1
        else:
            enemy_projectiles.append(self)
            self.x=cannon1.x+cannon1.w/2-self.w/2
            self.y=cannon1.y+cannon1.h/2-self.h/2
            ratio_x=-cannon1.degree/90
            ratio_y=cannon1.degree/90-1
        LOL=23/math.sqrt(ratio_x**2+ratio_y**2)
        self.spd_x_0=LOL*ratio_x
        self.spd_y=LOL*ratio_y
        self.a_y=g/24
        self.sort=sort
    def check(self):
        self.x+=self.spd_x_0
        self.y+=self.spd_y
        self.spd_y+=self.a_y
        if self.x>=screenx or self.x+self.w<0 or self.y>=screeny:
            if self.sort==1:
                enemy_projectiles.remove(self)
            else:
                ally_projectiles.remove(self)
        elif (not self.sort or self.sort==2) and cannon1.life>0 and self.x+self.w>=cannon1.x>=self.x-2*19 and self.y+self.h>=cannon1.y+8*2>=self.y-20*2:
            cannon1.life-=1
            cannon1.damaged=5
            if cannon1.life<1:
                cannon1.cooldown2=300
            ally_projectiles.remove(self)
        elif (not self.sort or self.sort==2) and self.x+self.w>=boat1_x>=self.x-434 and self.y+self.h>=boat1_y>=self.y-280 and boat1_mask.overlap(ball_mask,(int(self.x-boat1_x),int(self.y-boat1_y))):
            for i in body_parts:
                if i.mask.overlap(ball_mask,(int(self.x-boat1_x),int(self.y-boat1_y))):
                    ally_projectiles.remove(self)
                    i.damaged=5
                    if not self.sort:
                        i.life-=1
                    else:
                        i.life-=2
                    if i.life<1:
                        body_parts.remove(i)
        elif self.sort==1 and self.x+self.w>=boat0_x>=self.x-367 and self.y+self.h>=boat0_y>=self.y-280 and boat0_mask.overlap(ball_mask,(int(self.x-boat0_x),int(self.y-boat0_y))):
            enemy_projectiles.remove(self)
            cannon0.damaged=5
            return -1
        return 0
    def draw(self):
        if not self.sort:
            screen.blit(cannon_ball_blue,(self.x,self.y))
        elif self.sort==1:
            screen.blit(cannon_ball_red,(self.x,self.y))
        else:
            screen.blit(cannon_ball,(self.x,self.y))

pygame.init()
pygame.display.set_caption("BOAT FIGHT")
frame=pygame.time.Clock()
g=9.81
screenx,screeny=1400,700
ratiox,ratioy=1.0,1.0
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('bg-1.png').convert(),(screenx,screeny))
bg2=pygame.transform.scale(pygame.image.load('bg10.png').convert_alpha(),(screenx*2,screeny))
bg2_x=0
cannon_w,cannon_h=int(2*19*ratiox),int(2*36*ratioy)
cannon_x,cannon_y=int(270*ratiox),int(480*ratioy)
mortar=pygame.transform.scale(pygame.image.load('19x36mortar.png').convert_alpha(),(cannon_w,cannon_h))
cannon=pygame.transform.scale(pygame.image.load('19x36cannon.png').convert_alpha(),(cannon_w,cannon_h))
white_cannon=pygame.transform.scale(pygame.image.load('19x36white_cannon.png').convert_alpha(),(cannon_w,cannon_h))
cannon_ball=pygame.transform.scale(pygame.image.load('12x12cannon_ball.png').convert_alpha(),(2*10,2*10))
cannon_ball_blue=pygame.transform.scale(pygame.image.load('12x12cannon_ball_blue.png').convert_alpha(),(2*10,2*10))
cannon_ball_red=pygame.transform.scale(pygame.image.load('12x12cannon_ball_red.png').convert_alpha(),(2*10,2*10))
ball_mask=pygame.mask.from_surface(cannon_ball)
boat0=pygame.image.load('367x280ally_boat.png').convert_alpha()
boat0_damaged=pygame.image.load('367x280ally_boat_damaged2.png').convert_alpha()
boat1=pygame.image.load('434x280enemy_boat.png').convert_alpha()
boat1_damaged=pygame.image.load('434x280enemy_boat_damaged.png').convert_alpha()
boat0_mask=pygame.mask.from_surface(pygame.image.load('367x280ally_boat_mask.png').convert_alpha())
boat1_mask=pygame.mask.from_surface(boat1_damaged)
cannon_wheel=pygame.transform.scale(pygame.image.load('17x17cannon_wheel.png').convert_alpha(),(2*15,2*15))
boss_fight=pygame.transform.scale(pygame.image.load('boss_fight.png').convert_alpha(),(95*8,14*8))
ally_projectiles=[]
enemy_projectiles=[]
icons=[pygame.image.load('cannon_ball_blue_icon1.png').convert_alpha(),pygame.image.load('cannon_ball_blue_icon2.png').convert_alpha(),pygame.image.load('cannon_ball_icon1.png').convert_alpha(),pygame.image.load('cannon_ball_icon2.png').convert_alpha()]
reload=[pygame.image.load('reload0.png').convert_alpha(),pygame.image.load('reload1.png').convert_alpha(),pygame.image.load('reload2.png').convert_alpha(),pygame.image.load('reload3.png').convert_alpha(),pygame.image.load('reload4.png').convert_alpha(),pygame.image.load('reload5.png').convert_alpha(),pygame.image.load('reload6.png').convert_alpha(),pygame.image.load('reload7.png').convert_alpha()]
blue=True
body=[]
body_parts=[]
play=True
recoil=0
boat0_x=14
boat0_y=352-40
boat1_x=953+400
boat1_y=339-30 
boat0_full_life=boat0_life=10
f_heart=pygame.transform.scale(pygame.image.load('Full_heart1.png').convert_alpha(),(64,64))
e_heart=pygame.transform.scale(pygame.image.load('Empty_heart.png').convert_alpha(),(64,64))
skip=pygame.transform.scale(pygame.image.load('space_skip.png').convert_alpha(),(274*2,18*2))
box=pygame.transform.scale(pygame.image.load('22x22box.png').convert(),(64,64))
cannon0=canon(cannon_x,cannon_y-40,0)
cannon1=canon(cannon_x+boat1_x-263,cannon_y-50,1)
coque=boat1_part(50,icons,boat1_mask)
cooldown=0
while play:
    frame.tick(60)
    print(frame)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
    mouse_pos=pygame.mouse.get_pos()
    mouse_pressed=pygame.mouse.get_pressed()[0]
    keys=pygame.key.get_pressed()
    screen.blit(bg,(0,0))
    if bg2_x>-screenx:
        bg2_x-=2
    else:
        bg2_x=0
    if boat1_x>953:
        boat1_x-=0.5
        cannon1.x-=0.5
        cannon1.check()
        cannon0.check()
        if keys[pygame.K_SPACE]:
            cannon1.x-=boat1_x-953
            boat1_x=953
    else:
        if keys[pygame.K_1]:
            cannon0.x=cannon_x+boat0_x-14
            blue=True
        elif keys[pygame.K_2]:
            cannon0.x=cannon_x+boat0_x-14
            blue=False
        cannon0.check()
        cannon1.check()
        if mouse_pressed and (blue and not cannon0.cooldown or not blue and not cannon0.cooldown2):
            if blue:
                projectile(0)
                cannon0.cooldown=40
            else:
                projectile(2)
                cannon0.cooldown2=120
            cannon0.recoil=ally_projectiles[len(ally_projectiles)-1].spd_x_0
            cannon0.x-=cannon0.recoil
        if cannon0.cooldown:
            if blue and cannon0.cooldown>20:
                cannon0.x+=cannon0.recoil/20
            cannon0.cooldown-=1
        if cannon0.cooldown2:
            if not blue and cannon0.cooldown2>100:
                cannon0.x+=cannon0.recoil/20
            cannon0.cooldown2-=1
        if not cannon1.cooldown and cannon1.life>0:
            projectile(1)
            cannon1.recoil=enemy_projectiles[len(enemy_projectiles)-1].spd_x_0
            cannon1.x-=cannon1.recoil
            cannon1.cooldown+=80
        elif cannon1.cooldown:
            if cannon1.cooldown>60:
                cannon1.x+=cannon1.recoil/20
            cannon1.cooldown-=1
    if cannon0.damaged:
        screen.blit(boat0_damaged,(boat0_x,boat0_y))
        cannon0.damaged-=1
    else:
        screen.blit(boat0,(boat0_x,boat0_y))
    screen.blit(boat1,(boat1_x,boat1_y))
    for part in body:
        part.draw()
    for proj in ally_projectiles:
        proj.check()
        proj.draw()
    for proj in enemy_projectiles:
        boat0_life+=proj.check()
        proj.draw()
        for i in ally_projectiles:
            if proj.x+proj.w>=i.x>=proj.x-i.w and proj.y+proj.h>=i.y>=proj.y-i.h and proj in enemy_projectiles:
                enemy_projectiles.remove(proj)
                if not i.sort:
                    ally_projectiles.remove(i)
    cannon0.draw()
    cannon1.draw()
    if cannon1.cooldown2:
        cannon1.cooldown2-=1
        if not cannon1.cooldown2:
            cannon1.life=8
        screen.blit(box,(cannon1.x-6,cannon1.y-4))
    screen.blit(bg2,(bg2_x,0))
    if boat1_x<=953:
        heart=0
        for i in range(boat0_life):
            screen.blit(f_heart,(heart,0))
            heart+=70
        for i in range(boat0_full_life-boat0_life):
            screen.blit(e_heart,(heart,0))
            heart+=70
        heart=0
        for i in range(2):
            if blue and i or not blue and not i:
                screen.blit(icons[2*i],(heart,70))
            else:
                screen.blit(icons[2*i+1],(heart,70))
            if not i and cannon0.cooldown:
                screen.blit(reload[int((1-cannon0.cooldown/40)*8)],(heart,70))
            elif i and cannon0.cooldown2:
                screen.blit(reload[int((1-cannon0.cooldown2/120)*8)],(heart,70))
            heart+=70
        if cooldown<100:
            screen.blit(boss_fight,(screenx//2-95*4,screeny//2-100-14*4))
            cooldown+=1
    else:
        screen.blit(skip,(screenx//2-260*ratiox,screeny-70*ratioy))
    if not boat0_life:
        play=False
    elif coque not in body_parts:
        body_parts=[]
        boat1_y+=0.4
        cannon1.y+=0.4
        cannon1.recoil=0
        cannon1.cooldown+=1
        boat0_x+=0.5
        cannon0.x+=0.5
    pygame.draw.rect(screen,100,(0,0,64,64))
    pygame.display.update()
pygame.quit()