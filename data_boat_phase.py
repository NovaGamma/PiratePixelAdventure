import os
import pygame
from screen import screen,screenx,screeny

pygame.init() #initialization of pygame
frame=pygame.time.Clock() #function to cap the frame rate with frame.tick(...) that we used below
g=9.81 #Earth's gravity constant used to add gravity for the cannon balls
bg=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/bg-1.png').convert(),(screenx,screeny))
bg2=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/bg10.png').convert_alpha(),(screenx*2,screeny))
bg2_x=0
cannon_w,cannon_h=2*19,2*36
cannon_x,cannon_y=270,480
mortar=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/19x36mortar.png').convert_alpha(),(cannon_w,cannon_h))
cannon=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/19x36cannon.png').convert_alpha(),(cannon_w,cannon_h))
white_cannon=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/19x36white_cannon.png').convert_alpha(),(cannon_w,cannon_h))
cannon_ball=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/12x12cannon_ball.png').convert_alpha(),(2*10,2*10))
cannon_ball_blue=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/12x12cannon_ball_blue.png').convert_alpha(),(2*10,2*10))
cannon_ball_red=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/12x12cannon_ball_red.png').convert_alpha(),(2*10,2*10))
ball_mask=pygame.mask.from_surface(cannon_ball)
boat0=pygame.image.load('Graphism/boat_phase/367x280ally_boat.png').convert_alpha()
boat0_damaged=pygame.image.load('Graphism/boat_phase/367x280ally_boat_damaged2.png').convert_alpha()
boat0_mask=pygame.mask.from_surface(pygame.image.load('Graphism/boat_phase/367x280ally_boat_mask.png').convert_alpha())
boat1_mask=pygame.mask.from_surface(pygame.image.load('Graphism/boat_phase/434x280enemy_boat_damaged.png').convert_alpha())
cannon_wheel=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/17x17cannon_wheel.png').convert_alpha(),(2*15,2*15))
boss_fight=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/boss_fight.png').convert_alpha(),(95*8,14*8))
ally_projectiles=[]
enemy_projectiles=[]
icons=[pygame.image.load('Graphism/boat_phase/cannon_ball_blue_icon1.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/cannon_ball_blue_icon2.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/cannon_ball_icon1.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/cannon_ball_icon2.png').convert_alpha()]
reload=[pygame.image.load('Graphism/boat_phase/reload0.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload1.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload2.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload3.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload4.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload5.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload6.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/reload7.png').convert_alpha()]
blue=True
body=[]
body_parts=[]
play=True
boat0_x=14
boat0_y=352-40
boat1_x=953+400
boat1_y=339-30
boat0_full_life=boat0_life=10
f_heart=pygame.transform.scale(pygame.image.load('Graphism/Full_heart1.png').convert_alpha(),(64,64))
e_heart=pygame.transform.scale(pygame.image.load('Graphism/Empty_heart.png').convert_alpha(),(64,64))
skip=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/space_skip.png').convert_alpha(),(274*2,18*2))
box=pygame.transform.scale(pygame.image.load('Graphism/boat_phase/22x22box.png').convert(),(64,64))
enemy_coque=[pygame.image.load('Graphism/boat_phase/434x280enemy_coque0.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_coque1.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_coque2.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_coque3.png').convert_alpha()]
coque_mask=pygame.mask.from_surface(enemy_coque[3])
enemy_flag1=[pygame.image.load('Graphism/boat_phase/434x280enemy_flag10.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag11.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag12.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag13.png').convert_alpha()]
flag1_mask=pygame.mask.from_surface(enemy_flag1[3])
enemy_flag2=[pygame.image.load('Graphism/boat_phase/434x280enemy_flag20.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag21.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag22.png').convert_alpha(),pygame.image.load('Graphism/boat_phase/434x280enemy_flag23.png').convert_alpha()]
flag2_mask=pygame.mask.from_surface(enemy_flag2[3])
cooldown=0
boat1_full_life=0
boat1_life=1
