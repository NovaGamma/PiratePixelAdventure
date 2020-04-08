import pygame
import math
pygame.init()
pygame.display.set_caption("BOAT FIGHT")
frame=pygame.time.Clock()
g=9.81
screenx,screeny=1400,700
ratiox,ratioy=1.0,1.0
screen=pygame.display.set_mode((screenx,screeny))
bg=pygame.transform.scale(pygame.image.load('bg.png').convert_alpha(),(screenx,screeny))
canon_w,canon_h=2*19,2*36
canon_x,canon_y=500,300
canon=pygame.transform.scale(pygame.image.load('19x36canon.png').convert_alpha(),(canon_w,canon_h))
canon_ball=pygame.transform.scale(pygame.image.load('12x12canon_ball.png').convert_alpha(),(2*10,2*10))
projectiles=[]
play=True
class projectile():
    def __init__(self,sort,mouse_pos):
        if not sort:
            self.w=20
            self.h=20
            self.x=canon_x+canon_w/2-self.w/2
            self.y=canon_y+canon_h/2-self.h/2
            self.spd_x_0=(mouse_pos[0]-self.x-self.w/2)/6
            self.spd_y_0=(mouse_pos[1]-self.y-self.h/2)/6
            self.spd_y=self.spd_y_0
            self.a_y=g/6
        projectiles.append(self)
    def check(self):
        self.x+=self.spd_x_0
        self.y+=self.spd_y
        self.spd_y+=self.a_y
        if self.x>=screenx or self.x+self.w<0 or self.y>=screeny:
            projectiles.remove(self)
    def draw(self):
        screen.blit(canon_ball,(self.x,self.y))
while play:
    frame.tick(60)
    print(frame)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            play=False
    mouse_pos=pygame.mouse.get_pos()
    mouse_pressed=pygame.mouse.get_pressed()[0]
    screen.blit(bg,(0,0))
    if mouse_pressed:
        projectile(0,mouse_pos)
    for proj in projectiles:
        proj.check()
        proj.draw()
    rotated_canon=pygame.transform.rotate(canon,math.atan2((mouse_pos[0]-canon_x-canon_w/2),(mouse_pos[1]-canon_y-canon_h/2))*180/math.pi+180)
    canon_size=rotated_canon.get_size()
    screen.blit(rotated_canon,(canon_x+(canon_w-canon_size[0])/2,canon_y+(canon_h-canon_size[1])/2))
    pygame.display.update()
pygame.quit()