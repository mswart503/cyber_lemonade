from CL_Adapted_elfClasses import Cardslot
from CL_Adapted_elfClasses import Textbox
from CL_classes import Instance
import pygame
from pygame import *
import os
import random
pygame.init()
red = (253, 1, 35)

yellow = (73, 69, 100)
lite_green = (0, 206, 67)
green = (0, 150, 107)
lite_blue = (143, 242, 239)
tan = (252, 247, 146)

grey = (34,53,76)
orange = (255,170,95)
red_grey = (141,108,122)
salmon = (208,123,90)
light_yellow = (251,220,163)
brown = (124,74,52)

screenwidth = 1200
screenheight = 750


def menu():
    pygame.display.set_caption('Cyber Lemonade')
    background = "Backgrounds/the_stand_smaller.jpg"
    bg = pygame.image.load(background)
    win = pygame.display.set_mode((screenwidth, screenheight))
    win.fill(orange)
    win.blit(bg, (0, 0))
    welcome = Textbox(salmon, screenwidth/2-300, 30, 600, 50, "Welcome To Cyber Lemonade",40)
    start_summer = Cardslot(salmon, 940, 140, 200, 80, None, False, name="Start Summer")
    options = Cardslot(salmon, start_summer.x, start_summer.y+start_summer.height+40, start_summer.width, start_summer.height, None, False, name="Options")
    awards = Cardslot(salmon, start_summer.x, options.y+options.height+40, options.width, options.height, None, False, name="Awards")
    welcome.draw(win, outline=True)
    start_summer.draw(win, outline=True)
    options.draw(win, outline=True)
    awards.draw(win, outline=True)
    pygame.display.flip()
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if start_summer.isOver(pos):
                    begin_instance(win, bg)


def begin_instance(win, bg):
    win.fill(orange)
    win.blit(bg, (0, 0))
    explainer = Textbox(salmon, screenwidth / 2 - 455, 200, 910, 200,
                        "Summer is here! Your father has given you ownership of one of his lemonade stands. "
                        "You get $100 to start, if you run out of money you have to close up shop. Can you make"
                        "it to the end of summer? Good luck!", 30)
    close_explainer = Cardslot(red_grey, explainer.x+375, 335, 150, 50, None, False, name="Let's Go")
    explainer.draw(win, outline=True)
    close_explainer.draw(win, outline=True)

    pygame.display.flip()
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if close_explainer.isOver(pos):
                    game_loop(win, bg)

        # input("Here's the loop")
def game_loop(win, bg):
    win.fill(orange)
    win.blit(bg, (0, 0))
    cur_instance = Instance()
    day = Cardslot(salmon, 40, 40, 60, 80, None, False, name=str(cur_instance.day), strength="Day")
    weekday = Cardslot(salmon, day.x + day.width + 30, 40, 90, 80, None, False, name=cur_instance.weekday,
                       strength="Weekday")
    hour = Cardslot(salmon, weekday.x + weekday.width + 30, 40, 60, 80, None, False, name=str(cur_instance.hour),
                    strength="Hour")
    money = Cardslot(salmon, hour.x + hour.width + 200, 40, 90, 80, None, False, name="$ "+str(cur_instance.money),
                    strength="Money")
    cost_display = Cardslot(salmon, 235, 670, 150, 60, None, False, name="$ "+str(cur_instance.lemonade_price),
                    strength="Current Price:")
    lemonade = Cardslot(salmon, money.x + money.width + 30, 40, 90, 80, None, False, name=str(cur_instance.lemonade),
                    strength="Lemonade")
    prep_title = Cardslot(light_yellow, 750, 40, 420, 60, None, False, name="You open in "+str(9-cur_instance.hour)+" hours")
    make_lemonade = Cardslot(light_yellow, 760, 140, 400, 60, None, False, name="Make Lemonade Batch - $ "+str(int(cur_instance.lemonade_cogs*cur_instance.lemonade_batch_size))+
                                                                                " for "+str(cur_instance.lemonade_batch_size)+" cups")
    raise_price = Cardslot(light_yellow, 760, make_lemonade.y+100, 400, 60, None, False, name="Raise Lemonade Price by $ 1")

    day.draw(win, outline=True, textdrop = 13)
    weekday.draw(win, outline=True, textdrop = 13)
    hour.draw(win, outline=True, textdrop = 13)
    money.draw(win, outline=True, textdrop = 13)
    lemonade.draw(win, outline=True, textdrop = 13)
    prep_title.draw(win, outline=True)
    make_lemonade.draw(win, outline=True)
    cost_display.draw(win, outline=True, textdrop = 15)
    raise_price.draw(win, outline=True)
    pygame.display.flip()
    start = False
    while start == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if day.isOver(pos):
                    pass
menu()