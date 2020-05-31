import pygame
import os

ScreenOpt={}
if os.path.exists("Config"):#same thing for the Config directory
    with open("Config/Game_Option.txt", "r") as optionFile:#if it exist, we will fo through the Game_Option and Controls file to get the screen size, last save used, and last language used
        for line in optionFile:#so here we read each line, and split it from the space characters
            temp=line.split(' ')
            if "screen" in temp[0]:
                ScreenOpt[temp[0]]=int(temp[1])

screenx=ScreenOpt['screenX']#getting the size of the screen
screeny=ScreenOpt['screenY']

screen=pygame.display.set_mode((screenx,screeny))
