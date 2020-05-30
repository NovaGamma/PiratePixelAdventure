import pygame
import os
from Classes.button import*
from data_level_editor import*

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
        self.height=h#getting the height
        self.width=w#getting the width
        if self.width==0 or self.height==0:
            self.img=pygame.transform.scale(img,(self.width+1,self.height+1))
        else:
            self.img=pygame.transform.scale(img,(self.width,self.height))#rescaling the texture according to the size of the platform
        self.touched=False
        self.right=False
        self.left=False
        self.up=False
        self.right=False
        planks.append(self)#adding the platform to the list of all platforms
        entities.insert(0,self)#adding the platform to the list of all entities at the first pos to know that this is the last one that we added
    def draw(self):#defining the draw method of the class
        screen.blit(self.img,(self.x+screendelta_x,self.y+screendelta_y))
        if not tools['cp'] and not tools['spawn'] and not tools['ennemie'] and (self==entities[0] or not mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].width or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].height)):
            screen.blit(pygame.transform.scale(black,(self.width,4)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(self.width,4)),(self.x+screendelta_x,self.y+screendelta_y+self.height-4))
            screen.blit(pygame.transform.scale(black,(4,self.height)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(4,self.height)),(self.x+screendelta_x+self.width-4,self.y+screendelta_y))
            if tools['size'] and (self.touched or self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height and (entities[0]==self or entities[0].touched==False and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].width or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].height))):
                if self.up and self.right:
                    screen.blit(arrow_leftup,(self.x+screendelta_x,self.y+screendelta_y))
                elif self.up and not self.right:
                    screen.blit(arrow_rightup,(self.x+screendelta_x+self.width-64,self.y+screendelta_y))
                elif not self.up and not self.right:
                    screen.blit(arrow_rightdown,(self.x+screendelta_x+self.width-64,self.y+screendelta_y+self.height-64))
                elif not self.up and self.right:
                    screen.blit(arrow_leftdown,(self.x+screendelta_x,self.y+screendelta_y+self.height-64))
            if tools['move'] and self==entities[0]:
                screen.blit(pointed,(self.x+screendelta_x+self.width//2-8,self.y+screendelta_y+self.height//2-8))
    def check(self):
        if (self.height<=1 or self.width<=1) and not mousepress[0]:
            planks.remove(self)
            entities.remove(self)
        if tools['size']:
            if self.touched or self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height:
                if not self.touched:
                    if self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width/2:
                        self.right=False
                    else:
                        self.right=True
                    if self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height/2:
                        self.up=False
                    else:
                        self.up=True
                if not self.touched and mousepress[0]:
                    self.touched=True
                elif not mousepress[0]:
                    self.touched=False
            if self.touched:
                if self.height+mousedelta[1]>0 and self.up:
                    self.height+=mousedelta[1]
                elif mousedelta[1]<0 or self.height-mousedelta[1]>0:
                    self.up=False
                    self.height-=mousedelta[1]
                    self.y+=mousedelta[1]
                else:
                    self.up=True
                if self.width+mousedelta[0]>0 and self.right:
                    self.width+=mousedelta[0]
                elif mousedelta[0]<0 or self.width-mousedelta[0]>0:
                    self.right=False
                    self.width-=mousedelta[0]
                    self.x+=mousedelta[0]
                else:
                    self.right=True
                if self.width==0 or self.height==0:
                    self.img=pygame.transform.scale(self.img,(self.width+1,self.height+1))
                else:
                    self.img=pygame.transform.scale(self.img,(self.width,self.height))

        if not self.touched and mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height:
            self.touched=True
        if self.touched and tools['move']:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

class chestpoint(object):
    def __init__(self,x,y):
        self.x=x-screendelta_x
        self.y=y-screendelta_y
        self.width=128
        self.height=128
        self.touched=False
        self.img=chest_texture
        entities.insert(0,self)
        cps.append(self)

    def draw(self):
        screen.blit(self.img,(self.x+screendelta_x,self.y+screendelta_y))
        if not tools['cp'] and not tools['spawn'] and not tools['ennemie'] and (self==entities[0] or not mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].width or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].height)):
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y+128-4))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x+128-4,self.y+screendelta_y))
        if tools['move'] and self==entities[0]:
            screen.blit(pointed,(self.x+screendelta_x+self.width//2-8,self.y+screendelta_y+self.height//2-8))

    def check(self):
        if not self.touched and mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height:
            self.touched=True
        if self.touched and tools['move']:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

class ennemy(object):
    def __init__(self,x,y,type='Captain'):
        self.x=x-screendelta_x
        self.y=y-screendelta_y
        self.width=64
        self.height=64
        self.touched=False
        self.img=ennemy_texture[type]
        self.type=type
        entities.insert(0,self)
        ennemies.append(self)

    def draw(self):
        screen.blit(self.img,(self.x+screendelta_x,self.y+screendelta_y))
        if not tools['cp'] and not tools['spawn'] and not tools['ennemie'] and (self==entities[0] or not mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height and (entities[0].x>mousepos[0] or mousepos[0]>entities[0].x+entities[0].width or entities[0].y>mousepos[1] or mousepos[1]>entities[0].y+entities[0].height)):
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(128,4)),(self.x+screendelta_x,self.y+screendelta_y+128-4))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x,self.y+screendelta_y))
            screen.blit(pygame.transform.scale(black,(4,128)),(self.x+screendelta_x+128-4,self.y+screendelta_y))
        if tools['move'] and self==entities[0]:
            screen.blit(pointed,(self.x+screendelta_x+self.width//2-8,self.y+screendelta_y+self.height//2-8))

    def check(self):
        if not self.touched and mousepress[0] and self.x+screendelta_x<=mousepos[0]<=self.x+screendelta_x+self.width and self.y+screendelta_y<=mousepos[1]<=self.y+screendelta_y+self.height:
            self.touched=True
        if self.touched and tools['move']:
            self.x+=mousedelta[0]
            self.y+=mousedelta[1]
        if self.touched and not mousepress[0]:
            self.touched=False

def get_name():
    question=text_button(900,100,10,10,"Please give the name of the level that you created",10,25)
    answer=text_button(200,60,600,280,"CONFIRM",10,10)
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
    answer.draw(screen)
    question.draw(screen)
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
                    while mousepress[0]:
                        mousepress=pygame.mouse.get_pressed()
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                return True
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
            level.write('plank '+str(plank.x/screenx)+' '+str(plank.y/screeny)+' '+str(plank.height/screeny)+' '+str(plank.width/screenx)+'\n')
        for cp in cps:
            level.write('cp '+str(cp.x/screenx)+' '+str(cp.y/screeny)+'\n')
        for ennemy in ennemies:
            level.write('ennemy '+str(ennemy.x/screenx)+' '+str(ennemy.y/screeny)+' '+str(ennemy.type)+'\n')
        level.write('spawn '+str(spawn_x/screenx)+' '+str(spawn_y/screeny)+'\n')
        level.write('finish '+str(finish_x/screenx)+' '+str(finish_y/screeny))
    #re-blitting the entities and the bg but without the tools to have a clean preview
    screen.blit(bg,(0,0))
    for i in range(len(entities)):
        entities[-i-1].draw()
    screen.blit(spawn,(spawn_x+screendelta_x,spawn_y+screendelta_y))
    screen.blit(finish,(finish_x+screendelta_x,finish_y+screendelta_y))
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
            button.draw(screen)
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
            for line in level:
                parameters=line.split(' ')
                if parameters[0]=='cp':
                    chestpoint(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny))
                elif parameters[0]=='plank':
                    platform(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),int(float(parameters[3])*screeny),int(float(parameters[4])*screenx),plank1)
                elif parameters[0]=='spawn':
                    spawn_x=int(float(parameters[1])*screenx)
                    spawn_y=int(float(parameters[2])*screeny)
                elif parameters[0]=='ennemy':
                    ennemy(int(float(parameters[1])*screenx),int(float(parameters[2])*screeny),int(parameters[3]))
                elif parameters[0]=='finish':
                    finish_x=int(float(parameters[1])*screenx)
                    finish_y=int(float(parameters[2])*screeny)

def blit_tools():
    for i in range(len(tools)):
        if not tools[toolList[i]]:
            screen.blit(tool[i*2],(4+i*(64+4),screeny-64-4))
        else:
            screen.blit(tool[i*2+1],(4+i*(64+4),screeny-64-4))

def ask():
    rect=pygame.Surface((325,105))#surface for the buttons
    rect2=pygame.Surface((675,105))#surface for the question
    rect.fill((179, 179, 179))#filling the surface with grey
    rect.set_alpha(180)#setting the "transparency" of the surface
    rect2.fill((179, 179, 179))#filling the surface with grey
    rect2.set_alpha(180)#setting the "transparency" of the surface
    yes=text_button(325,105,350,320,"YES",10,30)#creating the button for the Yes answer
    no=text_button(325,105,700,320,"NO",10,30)#creating the button for the No answer
    choosed=False
    fond=pygame.Surface((screenx,screeny))
    fond.fill((102,0,0))
    fond.set_alpha(150)
    screen.blit(fond,(0,0))
    question=font.render("DO YOU WANT TO SAVE ?",0,(255,255,255))
    screen.blit(rect2,(350,150))
    screen.blit(question,(360,150+35))
    yes.draw(screen)
    no.draw(screen)
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

def main(scren):
    global screen
    screen=scren
    global end,tools,ennemy_type,toolEnemies,tool,toolList,creating,spawning,finishing,spawn_x,spawn_y,finish_x,finish_y,screendelta_x,screendelta_y,mousepress,mousedelta,mousepos,entities,ennemies,planks,cps,undo,redo,clipboard
    undo_cooldown=True
    redo_cooldown=True
    copy_cooldown=True
    paste_cooldown=True
    save_cooldown=True
    load_cooldown=True
    finish_cooldown=True
    print("\n\n\n\n\n\n\n\n\n\n\n\nControls :\n\nzqsd or arrows to move the camera\n1, 2, 3 or 4 to select a tool\ntab to select another platform\nsuppr to delete the selected platform\nctr+z to respawn a deleted platform\nctrl+y to delete a respawned platform\nctrl+c to copy a platform, its size and position\nctrl+v to paste the copied platform\nctrl+o to open an existing level\nctrl+s to save your level\nctrl+r to reset the screen position\nshift to lock the camera")
    while not end:
        keys=pygame.key.get_pressed()
        mousepress=pygame.mouse.get_pressed()
        mousedelta=pygame.mouse.get_rel()
        mousepos=pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return None
        if keys[pygame.K_ESCAPE]:
            return screen
        if keys[pygame.K_1]:
            for key in tools.keys():
                tools[key]=False
            tools['move']=True
        elif keys[pygame.K_2]:
            for key in tools.keys():
                tools[key]=False
            tools['size']=True
        elif keys[pygame.K_3]:
            for key in tools.keys():
                tools[key]=False
            tools['place']=True
        elif keys[pygame.K_4]:
            for key in tools.keys():
                tools[key]=False
            tools['cp']=True
        elif keys[pygame.K_5]:
            for key in tools.keys():
                tools[key]=False
            tools['spawn']=True
        elif keys[pygame.K_6] and not ennemy_type[2]:
            ennemy_type[2]=True
            if tools['ennemie']:
                if ennemy_type[0]<4:
                    ennemy_type[0]+=1
                else:
                    ennemy_type[0]=0
                tool[10]=toolEnemies[2*ennemy_type[0]]
                tool[11]=toolEnemies[2*ennemy_type[0]+1]
            for key in tools.keys():
                tools[key]=False
            tools['ennemie']=True
        elif not keys[pygame.K_6]:
            ennemy_type[2]=False
        elif keys[pygame.K_7]:
            for key in tools.keys():
                tools[key]=False
            tools['finish']=True
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
            if (tools['move'] or tools['size']) and len(entities)>0 and entities[0].touched:
                entities[0].x+=screendelta_x
                entities[0].y+=screendelta_y
            screendelta_x=screendelta_y=0
        if keys[pygame.K_c] and (keys[pygame.K_RCTRL] or keys[pygame.K_LCTRL]) and copy_cooldown:
            if len(entities)>0:
                if entities[0] in planks:
                    clipboard=[entities[0].x,entities[0].y,entities[0].height,entities[0].width,entities[0].img,'p']
                elif entities[0] in cps:
                    clipboard=[entities[0].x,entities[0].y,entities[0].height,entities[0].width,entities[0].img,'c']
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
            for key in tools.keys():
                tools[key]=False
            tools['move']=True
            if entities!=[]:
                answer=ask()
                if answer==0:
                    save()
            #clearing the space
            cps=[]
            planks=[]
            entities=[]
            ennemies=[]
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
        if tools['place'] and mousepress[0]:
            platform(mousepos[0],mousepos[1],0,0,plank1)
            tools['place']=False
            tools['size']=True
            creating=True
        elif tools['size'] and creating and not mousepress[0]:
            tools['place']=True
            tools['size']=False
            creating=False
        if tools['cp'] and mousepress[0] and not creating:
            chestpoint(mousepos[0]-64,mousepos[1]-64)
            creating=True
        elif creating and not mousepress[0]:
            creating=False
        if tools['spawn'] and mousepress[0]:
            spawn_x=mousepos[0]-48-screendelta_x
            spawn_y=mousepos[1]-64-screendelta_y
        if tools['ennemie'] and mousepress[0] and not spawning:
            ennemy(mousepos[0]-64,mousepos[1]-64,ennemy_type[0])
            spawning=True
        elif spawning and not mousepress[0]:
            spawning=False
        if tools['finish'] and mousepress[0] and not finishing:
            finish_x=mousepos[0]-64-screendelta_x
            finish_y=mousepos[1]-64-screendelta_x
        elif finishing and not mousepress[0]:
            finishing=False
        only=False
        for i in entities:
            if not only:
                i.check()
            if i.touched==True and (tools['move'] or tools['size']) and i in entities:
                entities.remove(i)
                only=True
                entities.insert(0,i)
        #blitting the entities
        for i in range(len(entities)):
            entities[-i-1].draw()
        screen.blit(spawn,(spawn_x+screendelta_x,spawn_y+screendelta_y))
        screen.blit(finish,(finish_x+screendelta_x,finish_y+screendelta_y))
        if tools['cp']:
            screen.blit(chest_texture2,(mousepos[0]-64,mousepos[1]-64))
        if tools['spawn']:
            screen.blit(spawn2,(mousepos[0]-48,mousepos[1]-64))
        if tools['ennemie']:
            screen.blit(ennemy_texture2,(mousepos[0]-64,mousepos[1]-64))
        if tools['finish']:
            screen.blit(finish2,(mousepos[0]-64,mousepos[1]-64))
        if not (keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]):
            screen_moving=False
            if ((len(entities)>0 and entities[0].touched==True) and (tools['move'] or tools['size']) or tools['spawn']) or tools['cp']:
                if mousepos[0]<50 or keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    if tools['move']:
                        entities[0].x-=20
                    if tools['size']:
                        entities[0].x-=20
                        entities[0].width+=20
                    screendelta_x+=20
                    screen_moving=True
                if mousepos[0]>1350 or keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    screendelta_x-=20
                    screen_moving=True
                    if tools['move']:
                        entities[0].x+=20
                    if tools['size']:
                        entities[0].width+=20
                if mousepos[1]<50 or (keys[pygame.K_w] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_UP]:
                    screendelta_y+=20
                    screen_moving=True
                    if tools['move']:
                        entities[0].y-=20
                    if tools['size']:
                        entities[0].y-=20
                        entities[0].height+=20
                if mousepos[1]>650 or (keys[pygame.K_s] and not keys[pygame.K_RCTRL] and not keys[pygame.K_LCTRL]) or keys[pygame.K_DOWN]:
                    screendelta_y-=20
                    screen_moving=True
                    if tools['move']:
                        entities[0].y+=20
                    if tools['size']:
                        entities[0].height+=20
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
