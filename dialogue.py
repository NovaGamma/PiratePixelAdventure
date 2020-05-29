import pygame
from math import*

def dialogue(text,x=0,y=0,x_max=None,y_max=None,color=(255,255,255),speed=10,given_Font=None,size=50):
    if speed==None:
        speed=10
    if x_max==None:
        x_max=screenx
    if y_max==None:
        y_max=screeny
    base_y=y
    font=pygame.font.Font(given_Font,size)
    linezise=font.get_linesize()
    temp=''
    word=text.split(' ')
    real_size=(1/3)*size
    i=0
    nchar=0
    nchar_line=0
    nword=0
    char_words=0
    while i<len(text):
        pygame.event.get()
        for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    return -1#mean that the dialogue was stopep because the user wanted to exit the program
        char_words=0
        if nchar==len(word[nword]):
            nword+=1
            nchar=-1
            print(nword)
            print((len(word[nword])+nchar_line)*real_size)
            if (font.size(word[nword])[0])+(nchar_line)*real_size>x_max-x:
                y+=linezise
                if y>y_max-base_y:
                    y=base_y
                    screen.fill([100,20,20])
                nchar_line=0
                temp=''
        pygame.time.delay(speed)
        temp=temp+text[i]
        a=font.render(temp,0,color)
        screen.blit(a,(x,y))
        pygame.display.flip()
        i+=1
        nchar_line+=1
        nchar+=1
    return 0 #mean that the dialogue ended well

pygame.init()
pygame.font.init()
screenx=1400
screeny=700
screen=pygame.display.set_mode((screenx,screeny))
frame=pygame.time.Clock()
screen.fill([100,20, 20])
text="Pygame est une bibliothèque Python (écrite principalement en C) qui permet de créer des jeux simples. Elle permet de faire facilement des animations (déplacements d’images à l’écran , ...), de gérer du son ou de la vidéo.Pygame n’est pas fourni par défaut lorsqu’on installe Python. Pour l’installer, on peut choisir une distributioncomme Edupython qui installe, en même temps que Python, un certain nombre de modules.On peut également l’installer après avoir installé Python à condition de bien choisir le fichier correspondant ausystème d’exploitation et à la version de Python déjà installée (Téléchargement de pygame). Attention, pygamene fonctionne qu’avec une version 32 bits de Python (si on a une version 64 bits de Python, il faut la désinstalleret installer une version 32 bits).Le principe consiste à créer une boucle while principale : à chaque passage, une nouvelle image, où chaque objetest légèrement déplacé, est générée dans un buffer (mémoire tampon qui évite de dessiner directement à l’écranpour éviter de voir les éléments se dessiner au fur et à mesure). L’écran est ensuite effacé, puis la nouvelle image(une fois entièrement mise à jour dans le buffer) est affichée à l’écran.La succession rapide de toutes ces images donne l’impression de mouvement dans la"
dialogue(text,100,100,1200,700,(255,255,255),10,None,100)
a=True
while a:
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type==pygame.QUIT:
                a=False
pygame.quit()
