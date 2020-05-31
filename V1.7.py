import pygame
import os
from Classes.button import*#importing the button classes
from level_editor_8 import main#importing the main function from the level editor, used to run it
from boat_phase import main_boat
from screen import*

class platform(object):#the class used to generate platform
    def __init__(self,x,y,height,width,img):#here just defining the size and the texture of the platfrom
        self.x=x
        self.y=y
        self.height=height
        self.width=width
        self.img=pygame.transform.scale(img,(self.width,self.height)) # we make sure to rescale the base texture tp the size of the wanted platform
        planks.append(self)#and we add it to the list containing the platforms

    def draw(self):#we draw it only if it is in the view of the player to save ressources
        if self.x+self.width>=0 and self.x<screenx:
            screen.blit(self.img,(self.x,self.y))

    def check(self):#here is the function that check the collision with the enitites
        for i in entities:#the function will go through all the entities  and check if an entity is gonna collide with the current speed that it have
            if i.y+i.height<=self.y<=i.y+i.height+i.spdy and self.x-i.width+20<=i.x<=-20+self.x+self.width:
                i.spdy=self.y-i.y-i.height#here we apply gravity on the entity
                i.isground=True #if it is colliding we the isground parameter to true to indicate that the entity is on the ground, here on a platform

class people(object):#the class used to define the entities such as ennemies or the player but not the projectiles
    def __init__(self,x,y,mass,health,Type=5):#here we give the position, the height and mass, the health that the entity has adn the Type of
    #projectile it will shoot
        entities.append(self)#first we add the entity to the entities list
        self.x=x
        self.y=y
        self.mass=mass
        self.Type=Type
        self.height=walkright[self.Type][0].get_size()[1]*2#in order to get the height and width, we use the get_size method from pygame
        self.width=walkright[self.Type][0].get_size()[0]*2#to get the size of the texture, which here is the first frame of the walk animation
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
        self.cooldown=0#the cooldown for the projectile
        self.hit=0#a parameter that will retain if the entity is being hitted stopping the fact that it would be hitted by the same projectile each frame


    def draw(self,hitbox=False):#the function that display the entity, and if precised the hitbox
        if not self.isground and self.Type>4:#for the jump animation, we check if the player is not on the ground, and that it's type is 5 or 6 which correspond to the player types
            if self.left:#then we change the animation either to the left or right depending of the parameters
                self.info=jumpleft[self.Type-5]
            else:
                self.info=jumpright[self.Type-5]
        else:
            if self.stand:#stand is active if the entity doesn't move
                self.walkcount=0
            else:
                self.walkcount+=1
            if self.left:
                self.info=walkleft[self.Type][self.walkcount//4%4]#here, as below, we get the frame of the walk animation, depending of the direction and the number of frames taht elapsed
            else:
                self.info=walkright[self.Type][self.walkcount//4%4]
        screen.blit(pygame.transform.scale(self.info,(self.width,self.height)),(self.x,self.y))#we display the entity rescaled by twice the size of the original image
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
    def __init__(self,x,y,mass,health,Type=1):
        people.__init__(self,x,y,mass,health,Type)
        enemies.append(self)
        self.turn=False#null

    def move(self):#the function that move the ennemy depending of it speed
        self.x+=self.spdx
        self.y+=self.spdy

    def health_bar(self):#function that draw the health bar, drawing a grey bar and then a red bar over , a red bar that might be smaller to let the grey bar be visible behind, making the effect that the ennemy has loose some health
        pygame.draw.rect(screen,(0,0,0), (self.x+self.width/2-26*ratiox,-10+self.y-6*ratioy,52*ratiox,10*ratioy))
        pygame.draw.rect(screen,(255,0,0), (self.x+self.width/2-25*ratiox,-10+self.y-5*ratioy,50*self.life/self.health*ratiox,8*ratioy))

class player(people):#the class of the player entity
    def __init__(self,x,y,mass,health,Type=5):
        self.finish=[0,0]
        self.y_spawnpoint=0
        people.__init__(self,x,y,mass,health,Type)

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
            self.finish[0]-=self.spdx
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
            self.finish[1]-=self.spdy
            self.spawnpoint[1]-=self.spdy

    def attack(self):#the attack function is the function that summon the projectiles thrown by the player
    #depending of the weapon of the player which is defined by it's type
        if self.Type==5 and self.cooldown==0:
            throwsound.play()
            if self.left:
                a=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'axe',-1,'player')
            else:
                a=projectile(self.x,self.y+self.height//2+self.spdy,self.spdx,self.spdy,'axe',1,'player')
            prjs.append(a)
            self.cooldown=30
        if self.Type==6 and self.cooldown<=10:
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
        if self.x-player.width+20<=player.x<=self.x+self.width and self.y-self.height<=player.y<=self.y+player.height and not self.cpt:
            self.cpt=True
            player.y_spawnpoint+=player.spawnpoint[1]-350
            player.spawnpoint=[self.x,self.y]#changing the spawn position of the player
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

class projectile(object):#the class handling the projectiles
    def __init__(self,x,y,spdx,spdy,Type,direction,owner):
        self.x=x
        self.y=y
        self.width=64#null
        self.height=64#null
        self.aspdx=20+spdx//2*direction#here it's the acceleration of the speed in the x direction
        self.aspdy=-40+spdy//2
        self.kspdx=20+spdx//2*direction
        self.am=0.25
        self.Type=Type
        self.direction=direction
        self.count=0
    def move(self):
        if self.Type=='knife':
            self.x+=self.direction*self.kspdx
            if self.direction==-1:
                screen.blit(lniff,(self.x,self.y))
            else:
                screen.blit(rniff,(self.x,self.y))
        elif self.Type=='axe':
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

def display_levels(plank1):#here we will display all the available levels
    fond=pygame.Surface((screenx,screeny))#first we setup the semi-transparent background
    fond.fill((102,0,0))
    fond.set_alpha(150)
    rect=pygame.Surface((325,105))
    rect.fill((179, 179, 179))
    rect.set_alpha(180)
    choosed=False
    lvl_button=[]#then we get the different levels from the Levels directory
    try:
        levels_name = os.listdir("Levels/")
    except:
        os.mkdir('Levels')
        levels_name = os.listdir("Levels/")
    i=0
    j=0
    screen.blit(fond, (0,0))
    if len(levels_name)!=0:#and we display all the levels using the lvl_button, that display both the name and the preview
        for level in levels_name:
            lvl_button.append(level_button(325,105,30+i*(325+15),30+j*(105+25),level,pygame.transform.scale(pygame.image.load("Levels/"+level+'/level_preview.PNG'),(50,50))))
            i+=1#here we make sure to display 4 per line
            if i==4:
                j+=1
                i=0
        for button in lvl_button:#here we wait until the user chooses the level that he want to load using the collide function from the button class
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
            keys=pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                return ''
            if mousepress[0]:
                for button in lvl_button:
                    if button.collide(mousepos[0],mousepos[1]):
                        name=button.name
                        choosed=True
    else: #if the Levels directory was empty, we inform the user and wait until he click to go back to the menu
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
    pos=-1 #when the user has choosed the wanted level, we get its index in the list
    for levels in levels_name:
        if name==levels:
            pos=levels_name.index(levels)
    if pos!=-1:
        load(levels_name[pos],plank1)#and then we load it using the load function

def reset_player():#to reset the parameters of the player, we just heal it, and reset it's speed and put it on the ground
    player.life=3
    player.spdy=0
    player.spdx=0
    player.isground=1

def SaveOption():#the function used to save the option such as the size of the screen, that you can manually changed from the Game_Option file aswell as for the controls and languages
    if not os.path.exists('Config'):#So we check if the directory exist, if not we create it
        os.mkdir('Config')
    with open("Config/Game_Option.txt", "w+") as optionFile:#then we open the Game_Option file
        for key in ScreenOpt.keys():#and go through all the keys of the ScreenOpt dictionnary, keeping the size of the screen
            temp=key+' '+str(ScreenOpt[key])+'\n'
            optionFile.write(temp)#and so we write these value in the txt file
        optionFile.write('language '+Language["language"]+'\n')#we do the same for the language currently used, info that will be used by the Init function to load the languages
        optionFile.write('last_save '+last_save+'\n')#same for the last save file used
    with open("Config/Controls.txt", "w+") as controlFile:#then we open the Controls file
        for key in ControlOpt.keys():#and we put all the controls with their corresponding key
            temp=key+' '+str(ControlOpt[key])+'\n'
            controlFile.write(temp)

def Init():#the function that import the main assets of the game
    if not(os.path.exists("Saves")):#first we check if the Saves directory exists; if not we create it
        os.mkdir("Saves")
    if os.path.exists("Config"):#same thing for the Config directory
        with open("Config/Game_Option.txt", "r") as optionFile:#if it exist, we will fo through the Game_Option and Controls file to get the screen size, last save used, and last language used
            for line in optionFile:#so here we read each line, and split it from the space characters
                temp=line.split(' ')
                print(temp[0])#and we get the values/names for the last_save and language aswell as for the screen size, saved in ScreenOpt dictionnary
                if temp[0]=="last_save":
                    last_save=temp[1].rstrip('\n')
                elif temp[0]=="language":
                    language=temp[1].rstrip('\n')
                else:
                    ScreenOpt[temp[0]]=int(temp[1])
        print(ScreenOpt)
        print(language)
        with open("Config/Controls.txt", "r") as controlFile:#we do the same thing for the controls
            for line in controlFile:
                temp=line.split(' ')
                ControlOpt[temp[0]]=int(temp[1])
    if os.path.exists("Language"):#and then for the language, we associate each part to it's key in the dictionnary, which will be the same for the different languages
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
    return [ScreenOpt,ControlOpt,Language,last_save]#and lastly we return all these values to the main part

def load_save(save_name):#the function that laod the given save file
    if os.path.exists("Saves/"+save_name+".txt"):#first as we always do, we check if the file exist
        with open("Saves/"+save_name+".txt" ,'r') as saveFile:#if yes we open it
            for line in saveFile:#and then go through each line getting
                temp=line.split(' ')
                if temp[0]=='level':#and get the level which the player was, the last time he used this save file
                    nLevel=int(temp[1])
                elif temp[0]=='player':#aswell as the type of the player, i-e the Boy or the Girl (type 5 or 6)
                    print(int(temp[1]))
                    player.Type=int(temp[1])
            return nLevel#and we return the level to load to the main part
    else:
        raise Exception("Try to open a non-existing save file : "+save_name)#we raise an Exception if the programm tried to open a non existing file
    return -1

def load(level,plank1):#here one of the most important function, that load a level, from the level editor,
    if os.path.exists("Levels/"+level):
        with open("Levels/"+level+'/entities.txt','r') as levelFile:
            print("loading : "+level)
            for line in levelFile:#going through the file
                parameters=line.split(' ')
                if parameters[0]=='plank':#if there is a plank/platform to load we call the platform function, converting the values that are the relative position to the screen into the position in the screen, depending of the current size of the screen
                    platform(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),int(float(parameters[3])*screeny),int(float(parameters[4])*screenx),plank1)
                elif parameters[0]=='cp':#same thing for the checkpoints
                    cp(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny))
                elif parameters[0]=='spawn':#here we just modify the base values for the player, getting the new values
                    player.spawnpoint=[int(float(parameters[1])*screenx),int(float(parameters[2])*screeny)]
                    player.x=player.spawnpoint[0]
                    player.y=player.spawnpoint[1]
                elif parameters[0]=='ennemy':#and here the same, just creating an ennemy, and giving it's type
                    ennemy(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),1,2,int(parameters[3]))
                elif parameters[0]=='finish':
                    player.finish=[int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),finish_line]
    else:
        raise Exception("Level not found")

def collide(first,second):#function used to check if two object collides using the position and sizes of both of them
    if first.x<=second.x+second.width<=first.x+first.width+second.width and first.y<=second.y+second.height<=first.y+first.height+second.height:
        return 1#returning 1 if they collide and 0 if not
    return 0

def level_editor_unlocked(last_save):#function used, to know if the player has unlocked the level editor, in his save file
    if os.path.exists("Saves/"+last_save+'.txt'):
        with open("Saves/"+last_save+'.txt','r') as SaveFile:#so here we just go through the file, and check for the level_editor line, and get if it is True (activate) or false
            for line in SaveFile:
                print(line)
                temp=line.split(' ')
                if temp[0]=='level_editor':
                    if temp[1].rstrip('\n')=='True':
                        return True
                    else:
                        return False
    else:
        return False

def save_save(save_name):
    if os.path.exists("Saves/"+save_name+".txt"):#first as we always do, we check if the file exist
        with open("Saves/"+save_name+".txt" ,'w+') as saveFile:#if yes we open it
            saveFile.write('level '+str(nLevel)+'\n')
            if nLevel==3:
                saveFile.write('level_editor True\n')
            else:
                saveFile.write('level_editor False\n')
            saveFile.write('player '+str(player.Type))
#beginning of the execution
#initialysing and loading all the variables/texures/buttons/lists
pygame.init()
pygame.font.init()
font=pygame.font.Font(None,50)
ControlOpt={}
Language={}
Options=Init()#here we get the values from the Init function allowing us to create the pygame screen
ScreenOpt=Options[0]
ControlOpt=Options[1]
Language=Options[2]
if Options[3]==None:
    last_save="None"
else:
    last_save=Options[3]
print(ScreenOpt)
print(ControlOpt)
ratiox=screenx/1400#callculating the ratio of the screen from the base size, for the display of the health bar of the player
ratioy=screeny/700
SaveOption()#we save the Option, to prevent corruption from a crash
pygame.display.set_caption(Language["title"])#here we create the screen and load the background
frame=pygame.time.Clock()
bg=pygame.transform.scale(pygame.image.load('Graphism/bg (1).png').convert_alpha(),(screenx,screeny))
play=False#then we initialize all the variables used for the menu loops
start=True
end=False
settings=False
control_setting=False
language_setting=False
level_editor=False
choose_save=True
load_levels=False
boat_phase=False
nLevel=0
level_list=['NIVO1','NIVO2','NIVO3','BOAT']
g=9.81#defining the gravity constant
#loading textures
jumpright=[pygame.image.load('Graphism/Player/Boy/bjump_right.png').convert_alpha(),pygame.image.load('Graphism/Player/Girl/fjump_right.png').convert_alpha()]#loding the textures for the jump animation, from the two types of player
jumpleft=[pygame.image.load('Graphism/Player/Boy/bjump_left.png').convert_alpha(),pygame.image.load('Graphism/Player/Girl/fjump_left.png').convert_alpha()]
walkright=[]
walkleft=[]
#here we load all the images, for the animations of walk for all the ennmemies and players
temp=os.listdir('Graphism/Ennemies')#using the listdir method to get all the names of directories and images
for i in range(len(temp)):
    images=os.listdir('Graphism/Ennemies/'+temp[i])
    buffer=[]
    for j in range(4):
        print(images[j])
        buffer.append(pygame.image.load('Graphism/Ennemies/'+temp[i]+'/'+images[j]).convert_alpha())
    walkleft.append(buffer)
    print("buffer")
    buffer=[]
    for j in range(4,8):
        print(images[j])
        buffer.append(pygame.image.load('Graphism/Ennemies/'+temp[i]+'/'+images[j]).convert_alpha())
    walkright.append(buffer)

temp=os.listdir('Graphism/Player')
for i in range(len(temp)):
    images=os.listdir('Graphism/Player/'+temp[i])
    buffer=[]
    for j in range(2,6):
        buffer.append(pygame.image.load('Graphism/Player/'+temp[i]+'/'+images[j]).convert_alpha())
    walkleft.append(buffer)
    print("buffer")
    buffer=[]
    for j in range(6,10):
        buffer.append(pygame.image.load('Graphism/Player/'+temp[i]+'/'+images[j]).convert_alpha())
    walkright.append(buffer)
#then loading the unique textures
finish_line=pygame.transform.scale(pygame.image.load('Graphism/level_editor/ile_normal.png'),(128*4,128*4))
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
player=player(300,screeny//2,5,3,5) #initialysing the player
plank_texture=pygame.image.load('Graphism/plank1.png').convert_alpha()#loading the base texure for the platforms
#creating all the buttons
button_setting=image_button(256,128,screenx//2-128,screeny//2-64,pygame.image.load('Graphism/button0.png').convert_alpha())
button_control=text_button(256,128,screenx//2-128,screeny//2+128,Language['control_button'],20,128//3+20,(255,233,0))
button_control_left=control_button(128,64,128,20,Language['left_control_button'],0,0,(255,233,0))
button_control_jump=control_button(128,64,128,2*20+64,Language['jump_control_button'],0,0,(255,233,0))
button_control_right=control_button(128,64,128,3*20+2*64,Language['right_control_button'],0,0,(255,233,0))
button_control_down=control_button(128,64,128,4*20+3*64,Language['down_control_button'],0,0,(255,233,0))
button_control_shoot=control_button(128,64,128,5*20+4*64,Language['shoot_control_button'],0,0,(255,233,0))
button_controls=[button_control_left,button_control_right,button_control_down,button_control_jump,button_control_shoot]

#creating the button for the main menu
button_language=text_button(256,128,screenx//2-512,screeny//2+128,Language['language_button'],20,128//3+20,(255,233,0))
french_button=language_button(256,128,screenx//2-512,screeny//2-128,'French',pygame.image.load('Graphism/drapeaux_fr2.PNG').convert_alpha())
english_button=language_button(256,128,screenx-512,screeny//2-128,'English',pygame.image.load('Graphism/drapeaux_en2.PNG').convert_alpha())
button_languages=[french_button,english_button]
button_menu=[button_language,button_control]#putting them in a list to dispplay them easily by going through the list

#load saves
button_save_1=text_button(screenx/3-10, screeny-20, 10, 10, 'File1',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_2=text_button(screenx/3-10, screeny-20, 10+screenx/3, 10, 'File2',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save_3=text_button(screenx/3-10, screeny-20, 10+2*(screenx/3), 10, 'File3',posX=(screenx/3-3*10)/3,posY=(screeny-20)/2)
button_save=[button_save_1,button_save_2,button_save_3]

while not end:#Main loop of the program
    #main menu
    while not start:
        frame.tick(10)
        screen.fill([100,20, 20])#filling the screen to set the background
        screen.blit(pygame.image.load('Graphism/button0.png').convert_alpha(),(screenx//2-128,screeny//2-64))#displaying the PLAY button
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                end=True#if the player want to exit the program we set all the menu variable to their off state to quit the current loop and the main loop
                start=True
                play=False
        #button
        pygame.event.get()
        for button in button_menu:
            button.draw(screen)#here displaying all the button from the main menu by going through the list and using their draw function
            if button.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):#checking if the mouse collides with a button
                if pygame.mouse.get_pressed()[0]:#if the left click of the mouse is pressed
                    #we use the name of the button to know what to do, and what function to call
                    if button.name==Language['control_button']:
                        boat_phase=True
                        #control_setting=True#setting the on state of an other menu loop variable
                    elif button.name==Language['language_button']:
                        language_setting=True#setting the on state of an other menu loop variable
                    elif button.name==Language['level_editor_button']:
                        level_editor=True#setting the on state of an other menu loop variable
                    elif button.name==Language['button_load_levels']:
                        load_levels=True #here it's the menu that will display all the level that the user can load, after he unlocked the level editor
                        display_levels(plank_texture)#and this function will also call the load function ending up loading a level,
                        play=True#so we then activate the play loop
                    start=True#and we exit the main menu
        if screenx//2-128<=pygame.mouse.get_pos()[0]<=screenx//2+128 and screeny//2-64<pygame.mouse.get_pos()[1]<screeny//2+64:# if the mouse collide with the big PLAY button
            if pygame.mouse.get_pressed()[0]:#if the left click is pressed
                screen.blit(pygame.image.load('Graphism/button3.png').convert_alpha(),(screenx//2-128,screeny//2-64))
                if nLevel<3:
                    planks=[]#we re-initialize the lists, to ensure that they are empty, for example when the player has already played a level, and dedide to change to another save file
                    cps=[]
                    prjs=[]
                    enemies=[]
                    entities=[player]
                    reset_player()
                    load(next_level,plank_texture)#we then proceed to load the level
                    pygame.mixer.stop()
                    buttonsound.play()
                    soundtrack.play()
                    start=True#we will go to the play loop
                    play=True
                else:
                    boat_phase=True
                    start=True
            else:
                #if the user wasn't clicking, we show that the mouse is over this button by changing it's color
                screen.blit(pygame.image.load('Graphism/button2.png').convert_alpha(),(screenx//2-128,screeny//2-64))
        pygame.display.update()

    while choose_save:#the function that is called for the user to choose which save file he want to use
        screen.fill([100,20, 20])#we put the background of the menu
        for button in button_save:
            button.draw(screen,1)#we display the button for the files
            if button.collide(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]):
                if pygame.mouse.get_pressed()[0]:
                    print("choosed : "+button.info)
                    save_name=button.info
                    nLevel=load_save(save_name)
                    #here putting the continue button in grey if not activated or in yellow if activated
                    if level_editor_unlocked(save_name):#here putting a lock on the level editor button if not activated
                        button_level_editor=text_button(256,128,0,0,Language['level_editor_button'],20,128//3+20,(255,233,0))
                        button_load_levels=text_button(256,128,0,128,Language['button_load_levels'],20,128//3+20,(255,233,0))
                    else:
                        button_level_editor=image_button(256,128,0,0,pygame.transform.scale(pygame.image.load("Graphism/lock.png").convert_alpha(),(64,64)),96,32,1)
                        button_load_levels=text_button()#creating an empty button for the button menu to load it even if we don't wont to display it
                    button_menu.append(button_level_editor)
                    button_menu.append(button_load_levels)
                    next_level=level_list[nLevel]
                    start=False
                    choose_save=False
                    print(str(player.x)+'   '+str(player.y))
                    while pygame.mouse.get_pressed()[0]:
                        for event in pygame.event.get():#here the part that allow the player to quit the menu or the programm at any time
                            if event.type==pygame.QUIT:
                                choose_save=False
                                end=True
        for event in pygame.event.get():#here the part that allow the player to quit the menu or the programm at any time
            if event.type==pygame.QUIT:
                choose_save=False
                end=True
        pygame.display.update()

    #the game
    frame_per_frame=False#defining variables used to slow down or to pause the timen used to debug and test
    pause=False
    while play:#the most complex loop in this file that is used to play levels, in campaing mode, or by loading created levels with the level editor
        frame.tick(60)#setting the max framerate at 60 frames per seconde
        print(frame)#displaying it in the console to see how many frames are going
        if frame_per_frame:
            frame.tick(1)#if in frame per frame mode, setting the frames at 1/second
        if pause:#if in pause mode, we just wait until the user press RSHIFT + O to exit this mode
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
        screen.blit(bg,(0,0))#putting the background
        keys=pygame.key.get_pressed()#getting the key pressed
        player.spdx=0
        if keys[pygame.K_p] and not(keys[pygame.K_LSHIFT]) and not(frame_per_frame):#if the user press P and is not in frame per frame mode, putting the game in frame per frame mode
            frame_per_frame=True
        elif keys[pygame.K_LSHIFT] and keys[pygame.K_p] and frame_per_frame:#here exiting the frame per frame mode
            frame_per_frame=False
        elif keys[pygame.K_o] and not(keys[pygame.K_LSHIFT]) and not(pause):#pausing the game
            pause=True
        elif keys[pygame.K_d] or keys[ControlOpt['right']]:#if the right control is pressed
            player.stand=False#the player will not be standing anymore, and setting it to the right and giving him speed to the right in the x axis
            player.left=False
            player.right=True
            player.spdx=15
        elif keys[pygame.K_a] or keys[ControlOpt['left']]:
            player.stand=False#same thing as above but for the left side
            player.right=False
            player.left=True
            player.spdx=-15
        else:
            player.stand=True#if the player isn't going either left or right, putting it in stand mode

        for i in entities:#acting the weight force on all the entities (enemies and player)
            if not i.isground:#only if they are not on the ground
                i.spdy+=i.mass*g//7
            i.isground=False

        for i in planks:#for all the plancks, we chekc that they are in the view of the player, and we draw them only if they are
            i.check()
            i.draw()

        if (keys[pygame.K_w] or keys[ControlOpt['up']]) and player.isground and not player.spdy:#if control up and the player isn't already going upward
            jumpsound.play()
            player.spdy=player.jump#setting it's upward speed to the initial speed of the jump

        if player.y>screeny:#if the player has fallen outside of the camera
            if player.spawnpoint[0]!=300:#we will reset the position of all the enities / platform / checkpoints at the spawnpoint of the player
                for i in planks:
                    i.x+=300-player.spawnpoint[0]
                for i in cps:
                    i.x+=300-player.spawnpoint[0]
                for i in prjs:
                    i.x+=300-player.spawnpoint[0]
                for i in enemies:
                    i.x+=300-player.spawnpoint[0]
                player.finish[0]+=300-player.spawnpoint[0]
                player.spawnpoint[0]=300
            if player.spawnpoint[1]!=350:
                for i in planks:
                    i.y+=350-player.spawnpoint[1]
                for i in cps:
                    i.y+=350-player.spawnpoint[1]
                for i in prjs:
                    i.y+=350-player.spawnpoint[1]
                for i in enemies:
                    i.y+=350-player.spawnpoint[1]
                player.finish[1]+=350-player.spawnpoint[1]
                player.spawnpoint[1]=350
            player.spdy=0#we will reset the speed and position of the player
            player.x=player.spawnpoint[0]
            player.y=player.spawnpoint[1]-10
            player.life-=1#and make him lose a life
            player.isground=True
            deathsound.play()
        if keys[ControlOpt['shoot']]:
            player.attack()
        if player.hit==1:#here if the player has been hit, we set him in invulnerability mode
            player.hit=2
        for i in enemies:#if an ennemy is offscreen in the y axis, we kill it and remove it from the entities and enemies lists
            if i.y-player.spawnpoint[1]-1700-player.y_spawnpoint>screeny:
                i.life=0
                enemies.remove(i)
                entities.remove(i)
            if i.hit==1:#if an ennemy if hitted, we set him in invulnerability mode
                i.hit=2
            for k in prjs:#then we check for each projectile if they hit something
                if collide(i,k):
                    if i.hit==0:
                        i.hit=1
                        i.life-=1
                        if i.life==0:#and remove the enemies if they die
                            enemies.remove(i)
                            entities.remove(i)
                    elif i.hit==2:
                        i.hit=1
            if i.hit==2:
                i.hit=0
            for j in planks:#then doing the colision for the planks and the enemies
                if j.x+i.width-10<=i.x+i.width<=j.x+j.width+10:
                    if not i.turn and i.x+i.width>=j.x+j.width:
                        i.turn=True
                    if i.turn and j.x+i.width>=i.x+i.width:
                        i.turn=False
                    elif i.x-300<player.x<i.x and player.y-30<i.y<player.y+15:
                        i.turn=True
                    elif i.x+300>player.x>i.x and player.y-30<i.y<player.y+15:
                        i.turn=False
            if i.isground and not i.turn:#then applying the moving forces on the ennemyes
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
            if collide(i,player):
                if player.hit==0:
                    player.life-=1
                    player.hit=1
                    if i.direction=='left':
                        player.spdx-=10
                    elif i.direction=='right':
                        player.spdx+=10
                    player.spdy+=10
                elif player.hit==2:
                    player.hit=1
        if player.hit==2:
            player.hit=0'''
        for i in entities:#moving all the enities
            i.move()
        for i in prjs:
            i.move()
        #drawing all the things
        for i in planks:
            i.draw()
        for i in cps:
            i.draw()
        for i in entities:
            i.draw(hitbox=True)#here we can set hitbox to true to see the hitboxes of the entities
        for i in enemies:
            i.health_bar()#then drawing the health bar of the enemies
        screen.blit(player.finish[2],(player.finish[0],player.finish[1]))
        if player.x<=player.finish[0]+(128*4)<=player.x+player.width+(128*4) and player.y<=player.finish[1]+(128*4)<=player.y+player.height+(128*4):
            nLevel+=1
            next_level=level_list[nLevel]
            save_save(save_name)
            play=False
            start=False
            planks=[]
            cps=[]
            prjs=[]
            enemies=[]
            entities=[player]
        player.health_draw()#and the one for the player
        if player.life==0:#if the player died
            pygame.mixer.stop()#we reset all the lists and reset the player and quit this loop, to go to the main menu
            deathsound.play()
            game_over.play()
            reset_player()
            play=False
            start=False
            planks=[]
            cps=[]
            prjs=[]
            enemies=[]
            entities=[player]
        pygame.display.update()

    while control_setting:#the menu that allow the user to changes the controls of the game
        screen.fill([100,20, 20])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                settings=False
                end=True
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            control_setting=False
            start=False
        for Button in button_controls:#so we display all the buttons
            Button.draw(screen,1)
        if pygame.mouse.get_pressed()[0]:
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            for Button in button_controls:
                if Button.collide(posX,posY):#checking if there is a collision with the mouse
                    getting=True
                    print('getting')
                    while getting:#and then we wait to get the control from the keyboard
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                                getting=False
                            elif event.type == pygame.KEYDOWN:
                                print('get')
                                ControlOpt=Button.controls(event.key)
                                SaveOption()#and we save it directly to the file, to not lose it if there is a crash
        pygame.display.update()

    while language_setting:#here just getting the language by clicking on a language button
        screen.fill([100,20, 20])
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                language_setting=False
                end=True
                print("quit")
        keys=pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            print("exit")
            language_setting=False
            start=False
        for button in button_languages:
            button.draw(screen)
        mousepress=pygame.mouse.get_pressed()
        if mousepress[0]:
            while mousepress[0]:
                mousepress=pygame.mouse.get_pressed()
                for event in pygame.event.get():
                    if event.type==pygame.QUIT:
                        mousepress[0]==0
                        language_setting=False
                        end=True
            posX=pygame.mouse.get_pos()[0]
            posY=pygame.mouse.get_pos()[1]
            for Button in button_languages:
                if Button.collide(posX,posY):
                    print(Button.name)#we just get the name of the button, and we wrote it in the language section to save the change
                    Language["language"]=Button.name
                    with open("Language/"+Button.name+'.txt' ,'r') as text:
                        for line in text:
                            temp=line.split(' ')
                            Language[temp[0]]=temp[1].rstrip('\n')
                    SaveOption()
                    language_setting=False
                    start=False#and we exit the menu
        pygame.display.update()

    if level_editor:#here we call the main function of the level editor giving it the pygame screen
        while pygame.mouse.get_pressed()[0]:
            for event in pygame.event.get():#here the part that allow the player to quit the menu or the programm at any time
                if event.type==pygame.QUIT:
                    level_editor=False
                    end=True
        pygame.display.set_caption("Level Editor")
        print("level editor")
        screen=main(screen)
        level_editor=False
        start=False

    if boat_phase:
        main_boat()
        boat_phase=False
        start=False

pygame.quit()
