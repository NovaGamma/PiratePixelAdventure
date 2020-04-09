import pygame
import os

class TextInput:
    """
    Copyright 2017, Silas Gyger, silasgyger@gmail.com, All rights reserved.

    Borrowed from https://github.com/Nearoo/pygame-text-input under the MIT license.

    This class lets the user input a piece of text, e.g. a name or a message.
    This class let's the user input a short, one-lines piece of text at a blinking cursor
    that can be moved using the arrow-keys. Delete, home and end work as well.
    """
    def __init__(
            self,
            initial_string="",
            font_family="",
            font_size=35,
            antialias=True,
            text_color=(0, 0, 0),
            cursor_color=(0, 0, 1),
            repeat_keys_initial_ms=400,
            repeat_keys_interval_ms=35,
            max_string_length=20):
        """
        :param initial_string: Initial text to be displayed
        :param font_family: name or list of names for font (see pygame.font.match_font for precise format)
        :param font_size:  Size of font in pixels
        :param antialias: Determines if antialias is applied to font (uses more processing power)
        :param text_color: Color of text (duh)
        :param cursor_color: Color of cursor
        :param repeat_keys_initial_ms: Time in ms before keys are repeated when held
        :param repeat_keys_interval_ms: Interval between key press repetition when held
        :param max_string_length: Allowed length of text
        """

        # Text related vars:
        self.antialias = antialias
        self.text_color = text_color
        self.font_size = font_size
        self.max_string_length = max_string_length
        self.input_string = initial_string  # Inputted text

        if not os.path.isfile(font_family):
            font_family = pygame.font.match_font(font_family)

        self.font_object = pygame.font.Font(font_family, font_size)

        # Text-surface will be created during the first update call:
        self.surface = pygame.Surface((1, 1))
        self.surface.set_alpha(0)

        # Vars to make keydowns repeat after user pressed a key for some time:
        self.keyrepeat_counters = {}  # {event.key: (counter_int, event.unicode)} (look for "***")
        self.keyrepeat_intial_interval_ms = repeat_keys_initial_ms
        self.keyrepeat_interval_ms = repeat_keys_interval_ms

        # Things cursor:
        self.cursor_surface = pygame.Surface((int(self.font_size / 20 + 1), self.font_size))
        self.cursor_surface.fill(cursor_color)
        self.cursor_position = len(initial_string)  # Inside text
        self.cursor_visible = False  # Switches every self.cursor_switch_ms ms
        self.cursor_switch_ms = 500  # /|\
        self.cursor_ms_counter = 0

        self.clock = pygame.time.Clock()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.cursor_visible = True  # So the user sees where he writes

                # If none exist, create counter for that key:
                if event.key not in self.keyrepeat_counters:
                    self.keyrepeat_counters[event.key] = [0, event.unicode]

                if event.key == pygame.K_BACKSPACE:
                    self.input_string = (
                        self.input_string[:max(self.cursor_position - 1, 0)]
                        + self.input_string[self.cursor_position:]
                    )

                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)
                elif event.key == pygame.K_DELETE:
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + self.input_string[self.cursor_position + 1:]
                    )

                elif event.key == pygame.K_RETURN:
                    return True

                elif event.key == pygame.K_RIGHT:
                    # Add one to cursor_pos, but do not exceed len(input_string)
                    self.cursor_position = min(self.cursor_position + 1, len(self.input_string))

                elif event.key == pygame.K_LEFT:
                    # Subtract one from cursor_pos, but do not go below zero:
                    self.cursor_position = max(self.cursor_position - 1, 0)

                elif event.key == pygame.K_END:
                    self.cursor_position = len(self.input_string)

                elif event.key == pygame.K_HOME:
                    self.cursor_position = 0

                elif len(self.input_string) < self.max_string_length or self.max_string_length == -1:
                    # If no special key is pressed, add unicode of key to input_string
                    self.input_string = (
                        self.input_string[:self.cursor_position]
                        + event.unicode
                        + self.input_string[self.cursor_position:]
                    )
                    self.cursor_position += len(event.unicode)  # Some are empty, e.g. K_UP

            elif event.type == pygame.KEYUP:
                # *** Because KEYUP doesn't include event.unicode, this dict is stored in such a weird way
                if event.key in self.keyrepeat_counters:
                    del self.keyrepeat_counters[event.key]

        # Update key counters:
        for key in self.keyrepeat_counters:
            self.keyrepeat_counters[key][0] += self.clock.get_time()  # Update clock

            # Generate new key events if enough time has passed:
            if self.keyrepeat_counters[key][0] >= self.keyrepeat_intial_interval_ms:
                self.keyrepeat_counters[key][0] = (
                    self.keyrepeat_intial_interval_ms
                    - self.keyrepeat_interval_ms
                )

                event_key, event_unicode = key, self.keyrepeat_counters[key][1]
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=event_key, unicode=event_unicode))

        # Re-render text surface:
        self.surface = self.font_object.render(self.input_string, self.antialias, self.text_color)


        self.clock.tick()
        return False

    def get_surface(self):
        return self.surface

    def get_text(self):
        return self.input_string

    def get_cursor_position(self):
        return self.cursor_position

    def set_text_color(self, color):
        self.text_color = color

    def set_cursor_color(self, color):
        self.cursor_surface.fill(color)

    def clear_text(self):
        self.input_string = ""
        self.cursor_position = 0


class platform(object):#defining the class to create platforms
    def __init__(self,x,y,h,w,img):#init method to get all the requirement such as the position x and y the size (height and width) and the texture of the platforms
        self.x=x-screendelta_x#getting x
        self.y=y-screendelta_y#getting y
        self.h=h#getting the height
        self.w=w#getting the width
        if self.w==0 or self.h==0:
            self.img=pygame.transform.scale(img,(self.w+1,self.h+1))
        else:
            self.img=pygame.transform.scale(img,(self.w,self.h))#rescaling the texture according to the size of the platform
        self.touched=False
        self.right=False
        self.left=False
        self.up=False
        self.right=False
        planks.append(self)#adding the platform to the list of all platforms
        entities.insert(0,self)#adding the platform to the list of all entities at the first pos to know that this is the last one that we added
    def draw(self):#defining the draw method of the class
        screen.blit(self.img,(self.x+screendelta_x,self.y+screendelta_y))
        if not cp_tool and not spawn_tool and (self==entities[0] or not mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h)):
            screen.blit(pygame.transform.scale(black,(self.w,4)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(self.w,4)),(self.x+screendelta_x,self.y+screendelta_y+self.h-4))
            screen.blit(pygame.transform.scale(black,(4,self.h)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(4,self.h)),(self.x+screendelta_x+self.w-4,self.y+screendelta_y))
            if size_tool and (self.touched or self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h and (entities[0]==self or entities[0].touched==False and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h))):
                if self.up and self.right:
                    screen.blit(arrow_leftup,(self.x+screendelta_x,self.y+screendelta_y))
                elif self.up and not self.right:
                    screen.blit(arrow_rightup,(self.x+screendelta_x+self.w-64,self.y+screendelta_y))
                elif not self.up and not self.right:
                    screen.blit(arrow_rightdown,(self.x+screendelta_x+self.w-64,self.y+screendelta_y+self.h-64))
                elif not self.up and self.right:
                    screen.blit(arrow_leftdown,(self.x+screendelta_x,self.y+screendelta_y+self.h-64))
            if move_tool and self==entities[0]:
                screen.blit(pointed,(self.x+screendelta_x+self.w//2-8,self.y+screendelta_y+self.h//2-8))
    def check(self):
        if (self.h<=1 or self.w<=1) and not mousepress[0]:
            planks.remove(self)
            entities.remove(self)
        if size_tool:
            if self.touched or self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h:
                if not self.touched:
                    if self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w/2:
                        self.right=False
                    else:
                        self.right=True
                    if self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h/2:
                        self.up=False
                    else:
                        self.up=True
                if not self.touched and mousepress[0]:
                    self.touched=True
                elif not mousepress[0]:
                    self.touched=False
            if self.touched:
                if self.h+mousedelta[1]>0 and self.up:
                    self.h+=mousedelta[1]
                elif mousedelta[1]<0 or self.h-mousedelta[1]>0:
                    self.up=False
                    self.h-=mousedelta[1]
                    self.y+=mousedelta[1]
                else:
                    self.up=True
                if self.w+mousedelta[0]>0 and self.right:
                    self.w+=mousedelta[0]
                elif mousedelta[0]<0 or self.w-mousedelta[0]>0:
                    self.right=False
                    self.w-=mousedelta[0]
                    self.x+=mousedelta[0]
                else:
                    self.right=True
                if self.w==0 or self.h==0:
                    self.img=pygame.transform.scale(self.img,(self.w+1,self.h+1))
                else:
                    self.img=pygame.transform.scale(self.img,(self.w,self.h))

        if not self.touched and mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h:
            self.touched=True
        if self.touched and move_tool:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

class chestpoint(object):
    def __init__(self,x,y):
        self.x=x-screendelta_x
        self.y=y-screendelta_y
        self.w=128
        self.h=128
        self.touched=False
        self.img=chest_texture
        entities.insert(0,self)
        cps.append(self)
    def draw(self):
        screen.blit(self.img,(self.x+screendelta_x,self.y+screendelta_y))
        if not cp_tool and not spawn_tool and (self==entities[0] or not mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].w or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].h)):
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y+128-4))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x+128-4,self.y+screendelta_y))
        if move_tool and self==entities[0]:
            screen.blit(pointed,(self.x+screendelta_x+self.w//2-8,self.y+screendelta_y+self.h//2-8))
    def check(self):
        if not self.touched and mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.w and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.h:
            self.touched=True
        if self.touched and move_tool:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

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
    def __init__(self,width=0,height=0,x=0,y=0,text='',color=None,posX=None,posY=None):#posX and posY are in function of the pos of the button
        if posX!=None and posY!=None:
            self.textX=posX
            self.textY=posY
        else:
            self.textX='0'
        if color==None:
            self.text=font.render(text,0,(255,255,255))
        else:
            self.text=font.render(text,0,(color))
        self.rect=pygame.Surface((width,height))
        self.rect.fill((179, 179, 179))
        self.rect.set_alpha(180)
        temp=font.size(text)
        self.width=temp[0]
        self.height=temp[1]
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


class level_button(button):
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

def get_name():
    question=text_button(900,100,10,10,"Please give the name of the level that you created",None,10,25)
    answer=text_button(200,60,600,280,"CONFIRM",None,10,10)
    textinput = TextInput()
    textinput.cursor_visible = False
    getting=True
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    screen.blit(fond, (0,0))
    rect=pygame.Surface((400,60))
    rect.fill((179, 179, 179))
    rect.set_alpha(180)
    screen.blit(rect,(190,280))
    answer.draw(1)
    question.draw(1)
    while getting:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        mousepress=pygame.mouse.get_pressed()
        mousepos=pygame.mouse.get_pos()
        if mousepress[0]:
            if answer.collide(mousepos[0],mousepos[1]):
                if textinput.get_text()!='':
                    return textinput.get_text()
                    getting=False
        textinput.update(events)
        screen.blit(rect,(190,280))
        screen.blit(textinput.get_surface(), (200, 300))
        pygame.display.update()

def save():
    name=get_name()
    if not(os.path.exists("Levels")):
        os.mkdir("Levels")
    print("Saving level...")
    working=False
    while not(working):
        if not(os.path.exists('Levels/'+name)):
            try:
                os.mkdir('Levels/'+name)
                working=True
            except:
                print("Wrong name, please ensure that the given name doesn't contain special characters that could cause problems")
                textinput.clear_text()
                name=get_name()
        else:
            working=True
    with open("Levels/"+name+'/'+'entities.txt','w+') as level:
        for plank in planks:
            level.write('plank '+str(plank.x/screenx)+' '+str(plank.y/screeny)+' '+str(plank.h/screeny)+' '+str(plank.w/screenx)+'\n')
        for cp in cps:
            level.write('cp '+str(cp.x/screenx)+' '+str(cp.y/screeny)+'\n')
        level.write('spawn '+str(spawn_x/screenx)+' '+str(spawn_y/screeny))
    #re-blitting the entities and the bg but without the tools to have a clean preview
    screen.blit(bg,(0,0))
    for i in range(len(entities)):
        entities[-i-1].draw()
    pygame.display.flip()#updating the screen
    pygame.image.save(screen,'Levels/'+name+'/level_preview.PNG')#saving the preview
    print("Level saved !")

def load(plank1):
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
            button.draw()
        pygame.display.update()
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
        with open("Levels/"+levels_name[pos]+'/'+'entities.txt','r') as level:
            for line in  level:
                parameters=line.split(' ')
                if parameters[0]=='cp':
                    chestpoint(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny))
                elif parameters[0]=='plank':
                    platform(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),int(float(parameters[3])*screeny),int(float(parameters[4])*screenx),plank1)
                elif parameters[0]=='spawn':
                    spawn_x=int(float(parameters[1])*screenx)
                    spawn_y=int(float(parameters[2])*screeny)

def blit_tools():
    for i in range(5):
        if i==1 and not size_tool or i==0 and not move_tool or i==2 and not place_tool or i==3 and not cp_tool or i==4 and not spawn_tool:
            screen.blit(tool[i*2],(4+i*(64+4),screeny-64-4))
        elif i==1 and size_tool or i==0 and move_tool or i==2 and place_tool or i==3 and cp_tool or i==4 and spawn_tool:
            screen.blit(tool[i*2+1],(4+i*(64+4),screeny-64-4))

def ask():
    rect=pygame.Surface((325,105))#surface for the buttons
    rect2=pygame.Surface((675,105))#surface for the question
    rect.fill((179, 179, 179))#filling the surface with grey
    rect.set_alpha(180)#setting the "transparency" of the surface
    rect2.fill((179, 179, 179))#filling the surface with grey
    rect2.set_alpha(180)#setting the "transparency" of the surface
    yes=text_button(325,105,350,320,"YES",None,10,30)#creating the button for the Yes answer
    no=text_button(325,105,700,320,"NO",None,10,30)#creating the button for the No answer
    choosed=False
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    screen.blit(fond,(0,0))
    question=font.render("DO YOU WANT TO SAVE ?",0,(255,255,255))
    screen.blit(rect2,(350,150))
    screen.blit(question,(360,150+35))
    yes.draw(1)
    no.draw(1)
    pygame.display.update()
    mousepos=pygame.mouse.get_pos()
    while not(choosed):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEMOTION:
                mousepos=pygame.mouse.get_pos()
        mousepress=pygame.mouse.get_pressed()
        if mousepress[0]:
            if yes.collide(mousepos[0],mousepos[1]):
                return 0
            elif no.collide(mousepos[0],mousepos[1]):
                return 1
        pygame.display.update()

pygame.init()
pygame.font.init()
textinput = TextInput()
font=pygame.font.Font(None,50)
pygame.display.set_caption("Level Editor")
screenx,screeny=1920,1080
screendelta_x=screendelta_y=0
screen=pygame.display.set_mode((screenx,screeny))
size_tool=False
move_tool=True
place_tool=False
cp_tool=False
spawn_tool=False
bg=pygame.transform.scale(pygame.image.load('bg (1).png'),(screenx,screeny))
plank1=pygame.image.load('plank1.png')
chest_texture=pygame.image.load('chestpoint (1).png')
chest_texture2=pygame.image.load('chestpoint (1)_invi.png')
spawn=pygame.transform.scale(pygame.image.load('rright0.png'),(2*48,2*64))
spawn2=pygame.transform.scale(pygame.image.load('rright0_invi.png'),(2*48,2*64))
black=pygame.image.load('black.png')
pointed=pygame.image.load('pointed.png')
arrow_leftup=pygame.transform.scale(pygame.image.load('arrow_leftup.png'),(64,64))
arrow_leftdown=pygame.transform.scale(pygame.image.load('arrow_leftdown.png'),(64,64))
arrow_rightup=pygame.transform.scale(pygame.image.load('arrow_rightup.png'),(64,64))
arrow_rightdown=pygame.transform.scale(pygame.image.load('arrow_rightdown.png'),(64,64))
tool=[pygame.image.load('edit_tool0.png'),pygame.image.load('edit_tool1.png'),pygame.image.load('edit_tool2.png'),pygame.image.load('edit_tool3.png'),pygame.image.load('edit_tool4.png'),pygame.image.load('edit_tool5.png'),pygame.image.load('edit_tool6.png'),pygame.image.load('edit_tool7.png'),pygame.image.load('edit_tool8.png'),pygame.image.load('edit_tool9.png')]
spawn_x,spawn_y=300,350
end=False
creating=False
screen_moving=False
entities=[]
planks=[]
cps=[]
undo=[]
redo=[]
clipboard=[]
del_cooldown=True
undo_cooldown=True
redo_cooldown=True
copy_cooldown=True
paste_cooldown=True
save_cooldown=True
load_cooldown=True
print("\n\n\n\n\n\n\n\n\n\n\n\nControls :\n\nzqsd or arrows to move the camera\n1, 2, 3 or 4 to select a tool\ntab to select another platform\nsuppr to delete the selected platform\nctr+z to respawn a deleted platform\nctrl+y to delete a respawned platform\nctrl+c to copy a platform, its size and position\nctrl+v to paste the copied platform\nctrl+o to open an existing level\nctrl+s to save your level\nctrl+r to reset the screen position\nshift to lock the camera")

while not end:
    keys=pygame.key.get_pressed()
    mousepress=pygame.mouse.get_pressed()
    mousedelta=pygame.mouse.get_rel()
    mousepos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            end=True
    if keys[pygame.K_2]:
        size_tool=True
        move_tool=False
        place_tool=False
        cp_tool=False
        spawn_tool=False
    elif keys[pygame.K_1]:
        size_tool=False
        move_tool=True
        place_tool=False
        cp_tool=False
        spawn_tool=False
    elif keys[pygame.K_3]:
        size_tool=False
        move_tool=False
        place_tool=True
        cp_tool=False
        spawn_tool=False
    elif keys[pygame.K_4]:
        size_tool=False
        move_tool=False
        place_tool=False
        cp_tool=True
        spawn_tool=False
    elif keys[pygame.K_5]:
        size_tool=False
        move_tool=False
        place_tool=False
        cp_tool=False
        spawn_tool=True
    if keys[pygame.K_TAB] and tab_cooldown:
        for i in range(len(entities)-1):
            entities[i],entities[i+1]=entities[i+1],entities[i]
        tab_cooldown=False
    elif not keys[pygame.K_TAB]:
        tab_cooldown=True
    if keys[pygame.K_DELETE] and len(entities)>0 and del_cooldown:
        undo.append(entities[0])
        if entities[0] in planks:
            planks.remove(entities[0])
        elif entities[0] in cps:
            cps.remove(entities[0])
        entities.remove(entities[0])
        redo=[]
        del_cooldown=False
    elif not keys[pygame.K_DELETE]:
        del_cooldown=True
    if keys[pygame.K_w] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and undo_cooldown:
        if len(undo)>0:
            entities.insert(0,undo[len(undo)-1])
            redo.append(undo[len(undo)-1])
            undo.remove(undo[len(undo)-1])
        undo_cooldown=False
    elif not keys[pygame.K_w]:
        undo_cooldown=True
    if keys[pygame.K_y] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and redo_cooldown:
        if len(redo)>0:
            if redo[len(redo)-1] in planks:
                planks.remove(redo[len(redo)-1])
            elif redo[len(redo)-1] in cps:
                cps.remove(redo[len(redo)-1])
            entities.remove(redo[len(redo)-1])
            undo.append(redo[len(redo)-1])
            redo.remove(redo[len(redo)-1])
        redo_cooldown=False
    elif not keys[pygame.K_y]:
        redo_cooldown=True
    if keys[pygame.K_r] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and (screendelta_x!=0 or screendelta_y!=0):
        if (move_tool or size_tool) and len(entities)>0 and entities[0].touched:
            entities[0].x+=screendelta_x
            entities[0].y+=screendelta_y
        screendelta_x=screendelta_y=0
    if keys[pygame.K_c] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and copy_cooldown:
        if len(entities)>0:
            if entities[0] in planks:
                clipboard=[entities[0].x,entities[0].y,entities[0].h,entities[0].w,entities[0].img,'p']
            elif entities[0] in cps:
                clipboard=[entities[0].x,entities[0].y,entities[0].h,entities[0].w,entities[0].img,'c']
            copy_cooldown=False
    elif not keys[pygame.K_c]:
        copy_cooldown=True
    if keys[pygame.K_v] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and paste_cooldown:
        if len(clipboard)>0:
            if clipboard[5]=='p':
                platform(clipboard[0]+screendelta_x,clipboard[1]+screendelta_y,clipboard[2],clipboard[3],clipboard[4])
            elif clipboard[5]=='c':
                chestpoint(clipboard[0]+screendelta_x,clipboard[1]+screendelta_y)
            paste_cooldown=False
    elif not keys[pygame.K_v]:
        paste_cooldown=True
    if keys[pygame.K_o] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and load_cooldown:
        size_tool=False
        move_tool=True
        place_tool=False
        cp_tool=False
        spawn_tool=False
        if entities!=[]:
            answer=ask()
            if answer==0:
                save()
        #clearing the space
        cps=[]
        planks=[]
        entities=[]
        screendelta_x=screendelta_y=0
        end=load(plank1)
        load_cooldown=False
    elif not keys[pygame.K_o] and not(load_cooldown):
        load_cooldown=True
    if keys[pygame.K_s] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and save_cooldown:
        save()
        save_cooldown=False
    elif not keys[pygame.K_s] and not(save_cooldown):
        save_cooldown=True


    #not getting the keys anymore
    screen.blit(bg,(0,0))
    if place_tool and mousepress[0]:
        platform(mousepos[0],mousepos[1],0,0,plank1)
        place_tool=False
        size_tool=True
        creating=True
    elif size_tool and creating and not mousepress[0]:
        place_tool=True
        size_tool=False
        creating=False
    if cp_tool and mousepress[0] and not creating:
        chestpoint(mousepos[0]-64,mousepos[1]-64)
        creating=True
    elif creating and not mousepress[0]:
        creating=False
    if spawn_tool and mousepress[0]:
        spawn_x=mousepos[0]-48-screendelta_x
        spawn_y=mousepos[1]-64-screendelta_y
    only=False
    for i in entities:
        if not only:
            i.check()
        if i.touched==True and (move_tool or size_tool) and i in entities:
            entities.remove(i)
            only=True
            entities.insert(0,i)
    #blitting the entities
    for i in range(len(entities)):
        entities[-i-1].draw()
    screen.blit(spawn,(spawn_x+screendelta_x,spawn_y+screendelta_y))
    if cp_tool:
        screen.blit(chest_texture2,(mousepos[0]-64,mousepos[1]-64))
    if spawn_tool:
        screen.blit(spawn2,(mousepos[0]-48,mousepos[1]-64))
    if not (keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]):
        screen_moving=False
        if ((len(entities)>0 and entities[0].touched==True) and (move_tool or size_tool) or spawn_tool) or cp_tool:
            if mousepos[0]<50 or keys[pygame.K_a] or keys[pygame.K_LEFT]:
                if move_tool:
                    entities[0].x-=20
                if size_tool:
                    entities[0].x-=20
                    entities[0].w+=20
                screendelta_x+=20
                screen_moving=True
            if mousepos[0]>1350 or keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                screendelta_x-=20
                screen_moving=True
                if move_tool:
                    entities[0].x+=20
                if size_tool:
                    entities[0].w+=20
            if mousepos[1]<50 or (keys[pygame.K_w] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_UP]:
                screendelta_y+=20
                screen_moving=True
                if move_tool:
                    entities[0].y-=20
                if size_tool:
                    entities[0].y-=20
                    entities[0].h+=20
            if mousepos[1]>650 or (keys[pygame.K_s] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_DOWN]:
                screendelta_y-=20
                screen_moving=True
                if move_tool:
                    entities[0].y+=20
                if size_tool:
                    entities[0].h+=20
        if not screen_moving:
            if (keys[pygame.K_w] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_UP]:
                screendelta_y+=20
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                screendelta_x+=20
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                screendelta_x-=20
            if (keys[pygame.K_s] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_DOWN]:
                screendelta_y-=20
    blit_tools()#blitting the tools (optionnal and unwanted for the preview of levels)
    pygame.display.update()#updating the display to show the new elements
if entities!=[]:#asking to save only if the level isn't empty
    answer=ask()
    if answer==0:
        save()#saving
pygame.quit()#closing pygame and ending the process
