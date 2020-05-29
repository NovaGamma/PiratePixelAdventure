import pygame
import math
import random
pygame.init()
pygame.display.set_caption("BOAT FIGHT")
frame=pygame.time.Clock()
g=9.81
screenx,screeny=1400,700
ratiox,ratioy=1.0,1.0
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('bg.png').convert(),(screenx,screeny))
cannon_w,cannon_h=int(2*19*ratiox),int(2*36*ratioy)
cannon_x,cannon_y=int(270*ratiox),int(480*ratioy)
cannon=pygame.transform.scale(pygame.image.load('19x36cannon.png').convert_alpha(),(cannon_w,cannon_h))
cannon_ball=pygame.transform.scale(pygame.image.load('12x12cannon_ball.png').convert_alpha(),(2*10,2*10))
cannon_ball_red=pygame.transform.scale(pygame.image.load('12x12cannon_ball_red.png').convert_alpha(),(2*10,2*10))
cannon_wheel=pygame.transform.scale(pygame.image.load('17x17cannon_wheel.png').convert_alpha(),(2*15,2*15))
ally_projectiles=[]
enemy_projectiles=[]
play=True
recoil=0
class canon():
    def __init__(self,x,y,sort):
        self.x=x
        self.y=y
        self.w=cannon_w
        self.h=cannon_h
        self.sort=sort
        self.cooldown=0
        self.recoil=0
        if sort==1:
            self.degree=90
            self.next_degree=0
            self.ex_degree=90
            self.cooldown=80
    def draw(self):
        if not self.sort:
            if mouse_pos[1]<self.y+self.h/2:
                rotated_cannon=pygame.transform.rotate(cannon,math.atan2((mouse_pos[0]-self.x-self.w/2),(mouse_pos[1]-self.y-self.h/2))*180/math.pi+180)
            else:
                rotated_cannon=pygame.transform.rotate(cannon,math.atan2((mouse_pos[0]-self.x-self.w/2),0)*180/math.pi+180)
        else:
            if self.cooldown==79:
                self.next_degree=45+random.randint(-30,45)
            elif not self.cooldown:
                self.ex_degree=self.degree
            elif self.cooldown>38:
                self.degree+=(self.next_degree-self.ex_degree)/40
            rotated_cannon=pygame.transform.rotate(cannon,self.degree)
        cannon_size=rotated_cannon.get_size()
        screen.blit(rotated_cannon,(self.x+(self.w-cannon_size[0])/2,self.y+(self.h-cannon_size[1])/2))
        screen.blit(cannon_wheel,(self.x+2*ratiox,self.y+30*ratioy))
class projectile():
    def __init__(self,sort):
        if not sort:
            ally_projectiles.append(self)
            self.w=20
            self.h=20
            self.x=cannon0.x+cannon0.w/2-self.w/2
            self.y=cannon0.y+cannon0.h/2-self.h/2
            if mouse_pos[1]<cannon0.y+cannon0.h/2:
                ratio_y=mouse_pos[1]-self.y-self.h/2
            else:
                ratio_y=0
            ratio_x=mouse_pos[0]-self.x-self.w/2
        elif sort==1:
            enemy_projectiles.append(self)
            self.w=20
            self.h=20
            self.x=cannon1.x+cannon1.w/2-self.w/2
            self.y=cannon1.y+cannon1.h/2-self.h/2
            ratio_x=-cannon1.degree/90
            ratio_y=cannon1.degree/90-1
        LOL=23/math.sqrt(ratio_x**2+ratio_y**2)
        self.spd_x_0=LOL*ratio_x
        self.spd_y=LOL*ratio_y
        self.a_y=g/20
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
    def draw(self):
        if not self.sort:
            screen.blit(cannon_ball,(self.x,self.y))
        elif self.sort==1:
            screen.blit(cannon_ball_red,(self.x,self.y))
cannon0=canon(cannon_x,cannon_y,0)
cannon1=canon(cannon_x+690,cannon_y-20,1)
while play:
    frame.tick(60)
    print(frame)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
    mouse_pos=pygame.mouse.get_pos()
    mouse_pressed=pygame.mouse.get_pressed()[0]
    screen.blit(bg,(0,0))
    if mouse_pressed and not cannon0.cooldown:
        projectile(0)
        cannon0.recoil=ally_projectiles[len(ally_projectiles)-1].spd_x_0
        cannon0.x-=cannon0.recoil
        cannon0.cooldown+=40
    if cannon0.cooldown:
        if cannon0.cooldown>20:
            cannon0.x+=cannon0.recoil/20
        cannon0.cooldown-=1
    if not cannon1.cooldown:
        projectile(1)
        cannon1.recoil=enemy_projectiles[len(enemy_projectiles)-1].spd_x_0
        cannon1.x-=cannon1.recoil
        cannon1.cooldown+=80
    elif cannon1.cooldown:
        if cannon1.cooldown>60:
            cannon1.x+=cannon1.recoil/20
        cannon1.cooldown-=1
    for proj in ally_projectiles:
        proj.check()
        proj.draw()
    for proj in enemy_projectiles:
        proj.check()
        if proj in enemy_projectiles:
            proj.draw()
            for i in ally_projectiles:
                if proj.x+proj.w>=i.x>=proj.x-i.w and proj.y+proj.h>=i.y>=proj.y-i.h:
                    enemy_projectiles.remove(proj)
                    ally_projectiles.remove(i)
    cannon0.draw()
    cannon1.draw()
    pygame.display.update()
pygame.quit()