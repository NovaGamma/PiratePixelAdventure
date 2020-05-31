import pygame

class button:#defining the basic clas that will be used for the different types of button
    def __init__(self,height,width,x,y,type=None):
        self.height=height
        self.width=width
        self.x=x
        self.y=y
        self.type=type

    def collide(self,posX,posY):#using a collide function to check if a given point is in the hitbox of the button
        if (posX>=self.x and posX<=self.x+self.width) and (posY>=self.y and posY<=self.y+self.height):
            return 1
        return 0

    def type(self):#return the type of the button, either text, image or other, can return None if the button class has been directly called
        return type


class text_button(button):#defining the text button class, a button that will use text
    def __init__(self,width=0,height=0,x=0,y=0,text='',posX=0,posY=0,color=None,font=None):#posX and posY the position of the text in the button
        self.info=text#self.info is the raw str type text while self.text is the rendered text using pygame font render
        self.textX=posX
        self.textY=posY
        if font==None:
            pygame.init()
            pygame.font.init()
            self.font=pygame.font.Font(None,50)
        else:
            self.font=font
        if color==None:
            self.text=self.font.render(text,0,(255,255,255))
        else:
            self.text=self.font.render(text,0,color)
        self.name=text
        self.rect=pygame.Surface((width,height))#here self.rect is the border of the button (the rectangle showing the limits of the button)
        self.rect.fill((115, 54, 0))
        self.rect.set_alpha(180)
        if width==0 and height==0:
            temp=self.font.size(text)
            self.width=temp[0]
            self.height=temp[1]
        else:
            self.width=width
            self.height=height
        button.__init__(self,self.height,self.width,x,y)

    def draw(self,screen,r=1):
        if r:#when calling the draw function, we specified if we want to draw the self.rect
            screen.blit(self.rect,(self.x,self.y))
        screen.blit(self.text,(self.x+self.textX,self.y+self.textY))#otherwise putting the text at the intended position

class image_button(button):
    def __init__(self,width=0,height=0,x=0,y=0,image=None,posX=0,posY=0,r=0):
        if image==None:
            raise Exception("No image given for the button")
        self.image=image
        if width==height==0:
            width=image.get_width()+20
            height=image.get_height()+20
        self.posX=posX
        self.posY=posY
        self.r=r
        button.__init__(self,height,width,x,y)
        self.rect=pygame.Surface((width,height))
        self.rect.fill((115,54,0))
        self.rect.set_alpha(180)
    def draw(self,screen):
        if self.r:
            screen.blit(self.rect,(self.x,self.y))
        screen.blit(self.image,(self.x+self.posX,self.y+self.posY))


class control_button(text_button):#here control button is a text button but with other functionnalities
    def __init__(self,width,height,x,y,text,posX=0,posY=0,color=None):
        text_button.__init__(self,width,height,x,y,text,posX,posY,color)
        self.control=text

    def controls(self,Id):#control is the control that we are going to change, Id is the id of the key that will be used for that control
        ControlOpt[self.control]=Id#we change the key id in the control option list wich will then be saved in the option file
        return ControlOpt

class language_button(button):#language button is a button that uses both image and text button to display the name of the language and the flag
#but it is otherwise the same as a classic button
    def __init__(self,width,height,x,y,text,image,color_text=None):
        self.rect=pygame.Surface((width,height))
        self.rect.fill((179, 179, 179))
        self.rect.set_alpha(180)
        self.name=text
        self.image=image_button(width,height,x+10,y+(height//3)-10,image)
        button.__init__(self,height,width,x,y)
        self.text=text_button(width,height,x+70,y+(height//3),text,color=color_text)

    def draw(self,screen):
        screen.blit(self.rect,(self.x,self.y))
        self.image.draw(screen)
        self.text.draw(screen,0)

class level_button(button):
    def __init__(self,width,height,x,y,text,image,color_text=None):
        self.rect=pygame.Surface((width,height))
        self.rect.fill((179, 179, 179))
        self.rect.set_alpha(180)
        self.name=text
        self.image=image_button(width,height,x+10,y+(height//3)-10,image)
        button.__init__(self,height,width,x,y)
        self.text=text_button(width,height,x+70,y+(height//3),text,color=color_text)

    def draw(self,screen):
        screen.blit(self.rect,(self.x,self.y))
        self.image.draw(screen)
        self.text.draw(screen,0)
