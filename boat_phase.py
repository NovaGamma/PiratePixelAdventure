import pygame
import math
import random
from data_boat_phase import*

class boat1_part(): #this is the class used for the enemy boat parts
    def __init__(self,full_life,img,mask):
        self.full_life=full_life #the max health of the part of the boat
        self.life=full_life #the remaining health
        self.img=img #an array containing all the needed images of a part
        self.mask=mask #the mask is used for pixel perfect collisions, it is the hitbox
        self.damaged=0 #this will be the time (in frames) for which we will display that the part has been damaged
        body_parts.append(self) #this is an array containing the parts of the boat that still have health so that we keep the collision detection
        body.append(self) #this is an array containing all the parts of the boat
    def draw(self):
        if self.damaged: #as said above, while self.damaged!=0, we display a white version of the boat part to show the player he touched it, and we reduce the variable by one so that it takes a certain number of frames long
            screen.blit(self.img[3],(boat1_x,boat1_y))
            self.damaged-=1
        elif self.life/self.full_life>0.5: #here, we display the clean and undamaged version of the boat part, as long as its health stays above the half of its maximum health
            screen.blit(self.img[0],(boat1_x,boat1_y))
        elif self.life>0: #here, we display the damaged version
            screen.blit(self.img[1],(boat1_x,boat1_y))
        else: #here we display the "dead" version
            screen.blit(self.img[2],(boat1_x,boat1_y))
class canon(): #this is the class used for the cannons
    def __init__(self,x,y,sort):
        self.x=x
        self.y=y
        self.width=cannon_w #w means weight
        self.height=cannon_h #h means height
        self.sort=sort #sort is a variable depending on which cannon it is, 0 for the player's cannons, 1 for the enemy cannon
        self.cooldown=0 #this is the minimum cooldown between two consecutive shots
        self.recoil=0 #this is the recoil the cannon gets when it shoots. Real physics formulae weren't used, it is only aesthetic
        self.damaged=0 #as for the boat parts, it is to show when the enemy cannon has been damaged, or to show when the player's boat has been damaged. We used this variable for the boat because it is global (not local) and unused for the player's cannon that cannot be shot
        if sort==1: #enemy cannon
            self.life=8 #cannon's life before it needs to be repaired
            self.degree=90 #cannon's degree
            self.next_degree=0 #cannon's future degree, that it is trying to reach, where it is going to shoot
            self.ex_degree=90 #past cannon's degree from the last time it shot
            self.cooldown=80 #we change the cooldown so that the cannon takes a bit of time before shooting at the player
        else: #player's cannons
            self.degree=270 #cannon's degree
        self.cooldown2=0 #this cooldown is used for the enemy cannon as the repair time, and for the player's cannon as the second cooldown, for the second cannon
    def check(self): #this function checks what angle the cannon should have
        if not self.sort: #player's cannon
            if mouse_pos[1]<self.y+self.height/2: #if the mouse is above the cannon (because we don't want the player to be able to shoot downwards)
                self.degree=math.atan2((mouse_pos[0]-self.x-self.width/2),(mouse_pos[1]-self.y-self.height/2))*180/math.pi+180 #using the arctangent function from the math library, we obtain the degree
            else: #if the mouse is below the cannon
                self.degree=math.atan2((mouse_pos[0]-self.x-self.width/2),0)*180/math.pi+180 # the degree is 90 if the mouse is at the left of the cannon and -90 if the mouse is at the right
            if not blue and not 360>=self.degree>=315:#player's second cannon, blue being the first cannon (the second cannon has more restrictions and can only shoot "en cloche")
                if self.degree>=180:#different method for the mouse at the left or right of the cannon
                    self.degree=315
                else:
                    self.degree=0
        else:#enemy cannon
            if self.cooldown==79:#the cannon just shot
                self.next_degree=random.randint(5,90)#we randomly calculate an angle for the next shot (from 5 to 90 so that it doesn't shoot on its own ship and doesn't shoot downwards) with this range, the enemy won't touch the player's boat each time
            elif not self.cooldown:#the cannon is going to shoot
                self.ex_degree=self.degree #we save where the cannon last shot because we will need that variable
            elif self.cooldown>38:#the first half of the cooldown where the cannon don't shoot
                self.degree+=(self.next_degree-self.ex_degree)/40 #here, for the 40 first frames after the enemy cannon shot, we will rotate the cannon a 40th of the difference between the next and previous shots angles, for it to reach the wanted angle. This way, the player can check the pattern and understand a bit where and when it is going to shoot and can prevent a damage
    def draw(self): #this function displays the cannons
        if blue and not self.sort or self.sort and not self.damaged: #this concerns the first player's cannon and the enemy cannon when it is not damaged
            rotated_cannon=pygame.transform.rotate(cannon,self.degree) #this function allows us to rotate an image with the image and the degree in parameters
        elif self.sort and self.damaged: #this concerns the enemy cannon when it took damage (in white to show the player he shot the cannon)
            rotated_cannon=pygame.transform.rotate(white_cannon,self.degree)
            self.damaged-=1
        else: #this concerns the second player's cannon
            rotated_cannon=pygame.transform.rotate(mortar,self.degree)
        cannon_size=rotated_cannon.get_size() #this takes the newly saved image and check its size because rotating an image doesn't change its position but its size, so we need to manually move the image correctly
        screen.blit(rotated_cannon,(self.x+(self.width-cannon_size[0])/2,self.y+(self.height-cannon_size[1])/2)) #we display the cannons, moving their position a bit to recenter the rotated image
        screen.blit(cannon_wheel,(self.x+2,self.y+30)) #we display the wheel of the cannons (the cannon havin to rotate, we can't fix the wheel to the cannon, so we just display it right after)
class projectile(): #this class is used for the cannon balls
    def __init__(self,sort):
        self.width=20 #w is the weight
        self.height=20 #h is the height
        if not sort or sort==2: #this concerns the player's balls ; sort==0 is for the player's first balls, sort==1 is for the enemy's balls and sort==2 is for the player's second balls (from the second cannon)
            ally_projectiles.append(self) #this array contains all the ally cannon balls
            self.x=cannon0.x+cannon0.width/2-self.width/2 #the cannon ball has its starting position in the cannon
            self.y=cannon0.y+cannon0.height/2-self.height/2
            if cannon0.degree<=90: #having the cannon's angle, we get the ratio on x and on y of the angle
                ratio_x=-cannon0.degree/90
                ratio_y=cannon0.degree/90-1
            else:
                ratio_x=(360-cannon0.degree)/90
                ratio_y=(360-cannon0.degree)/90-1
        else: #this concern the enemy cannon balls. In it, it is the same thing as above, but with the other cannon
            enemy_projectiles.append(self)
            self.x=cannon1.x+cannon1.width/2-self.width/2
            self.y=cannon1.y+cannon1.height/2-self.height/2
            ratio_x=-cannon1.degree/90
            ratio_y=cannon1.degree/90-1
        velocity=23/math.sqrt(ratio_x**2+ratio_y**2) #23 is the hypothenus, it is the power we chose for the cannons
        self.spd_x_0=velocity*ratio_x #because of the weird angles in pygame, it was easier to do that than to use trygonometrical functions
        self.spd_y=velocity*ratio_y
        self.a_y=g/24 #this is the acceleration of the ball (g=9.81 over 24) 24 being a chosen integer to have a good feeling of the gravity
        self.sort=sort
    def check(self): #here we set the new position of the ball
        self.x+=self.spd_x_0 #we add the speed to the postion every frame (x=x0+v*t)
        self.y+=self.spd_y
        self.spd_y+=self.a_y #we add the acceleration to the y-speed  every frame too (v=v0+a*t)
        if self.x>=screenx or self.x+self.width<0 or self.y>=screeny: #the ball gets out of the screen
            if self.sort==1: #it is "deleted" -> We remove it from the array we use to call its functions
                enemy_projectiles.remove(self)
            else:
                ally_projectiles.remove(self)
        elif (not self.sort or self.sort==2) and cannon1.life>0 and self.x+self.width>=cannon1.x>=self.x-2*19 and self.y+self.height>=cannon1.y+8*2>=self.y-20*2: #a player's ball touch the enemy cannon
            if not self.sort: #first cannon
                cannon1.life-=1 #removing 1 from the remaining life of the enemy cannon
            else: #second cannon dealing 2 damage points instead of 1
                cannon1.life-=2
            cannon1.damaged=5 #number of frames the white image indicating the cannon got touched is displayed
            if cannon1.life<1: #if the enemy cannon is dead, we start the repair cooldown, of 300 frames
                cannon1.cooldown2=300
            ally_projectiles.remove(self) #because the player's ball touched the cannon, it is now "deleted"
        elif (not self.sort or self.sort==2) and self.x+self.width>=boat1_x>=self.x-434 and self.y+self.height>=boat1_y>=self.y-280 and boat1_mask.overlap(ball_mask,(int(self.x-boat1_x),int(self.y-boat1_y))): #a player's ball touched the boat
            for i in body_parts: #enemy boat's parts with health remaining. Because the boat has been touched, we check each part to see which one has been touched
                if self in ally_projectiles and i.mask.overlap(ball_mask,(int(self.x-boat1_x),int(self.y-boat1_y))): #the mask overlap function checks every pixel of two masks (images but with bits=1 when there is a colour and equal to 0 when there is no colour on a pixel) to see if they are overlapping, which means they are colliding
                    ally_projectiles.remove(self) #the cannon hit something so we "delete" it
                    i.damaged=5 #cooldown of the damaged display (white image)
                    if not self.sort: #first cannon ball
                        i.life-=1
                    else: #second more powerful cannon ball
                        i.life-=2
                    if i.life<1: #the body part has no remaining health left
                        body_parts.remove(i) #we remove it from the array checking for collisions
        elif self.sort==1 and self.x+self.width>=boat0_x>=self.x-367 and self.y+self.height>=boat0_y>=self.y-280 and boat0_mask.overlap(ball_mask,(int(self.x-boat0_x),int(self.y-boat0_y))): #the enemy ball touches  the player's boat
            enemy_projectiles.remove(self) #the enemy ball is "deleted"
            cannon0.damaged=5 #number of frames for which the player's boat will be white so that the player understand he got damaged
            return -1 #number of health we remove to the player's life
        return 0
    def draw(self): #display of the cannon balls
        if not self.sort: #player's first cannon ball
            screen.blit(cannon_ball_blue,(self.x,self.y))
        elif self.sort==1: #enemy cannon ball
            screen.blit(cannon_ball_red,(self.x,self.y))
        else: #player's second cannon ball
            screen.blit(cannon_ball,(self.x,self.y))

def main_boat():
    global boat1_x,boat1_full_life,play,bg2_x,mouse_pos,boat0_x,boat1_life,boat0_life,blue,cooldown,cannon1,cannon0,boat1_y
    coque=boat1_part(50,enemy_coque,coque_mask)
    flag1=boat1_part(15,enemy_flag1,flag1_mask)
    flag2=boat1_part(15,enemy_flag2,flag2_mask)
    cannon0=canon(cannon_x,cannon_y-40,0)
    cannon1=canon(cannon_x+boat1_x-263,cannon_y-50,1)
    for part in body:
        boat1_full_life+=part.full_life
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
        for part in body:
            part.draw()
        for proj in ally_projectiles:
            proj.check()
            proj.draw()
        for proj in enemy_projectiles:
            boat0_life+=proj.check()
            proj.draw()
            for i in ally_projectiles:
                if proj.x+proj.width>=i.x>=proj.x-i.width and proj.y+proj.height>=i.y>=proj.y-i.height and proj in enemy_projectiles:
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
            boat1_life=0
            for part in body_parts:
                boat1_life+=part.life
            pygame.draw.rect(screen,(0,0,0), (screenx//2-274,screeny-50,274*2,18*2))
            pygame.draw.rect(screen,(255,0,0), (screenx//2-272,screeny-48,272*2*boat1_life/boat1_full_life,16*2))
        else:
            screen.blit(skip,(screenx//2-274,screeny-70))
        if not boat1_life:
            boat1_y+=0.4
            cannon1.y+=0.4
            cannon1.recoil=0
            cannon1.cooldown+=1
            boat0_x+=0.5
            cannon0.x+=0.5
        elif not boat0_life:
            return
        pygame.display.update()
