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
    start_summer = Cardslot(salmon, 840, 140, 300, 80, None, False, name="Start Summer")
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
                        "You get $20 to start, if you run out of money you have to close up shop. Can you make"
                        " it to the end of summer? Good luck!", 30)
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

    # Markers
    cur_instance.build_markers(win)

    make_lemonade_title = Cardslot(light_yellow, 760, 140, 400, 60, None, False, name="Make Lemonade Batch")
    make_lemonade_amount = Cardslot(salmon, 860, 205, 200, 40, None, False, name= str(cur_instance.lemonade_batch_size)+" cups for $"+str(int(cur_instance.lemonade_batch_size*cur_instance.lemonade_cogs)))
    raise_price = Cardslot(light_yellow, 765, 275, 175, 50, None, False, name="Raise Price $1")
    lower_price = Cardslot(light_yellow, 980, raise_price.y, raise_price.width, raise_price.height, None, False, name="Lower Price $1")
    upgrades = Cardslot(light_yellow, 760, 360, 400, 60, None, False, name="Upgrades")

    #day.draw(win, outline=True, textdrop = 13)
    #weekday.draw(win, outline=True, textdrop = 13)
    #hour.draw(win, outline=True, textdrop = 13)
    #money.draw(win, outline=True, textdrop = 13)
    #lemonade.draw(win, outline=True, textdrop = 13)
    #prep_title.draw(win, outline=True)
    make_lemonade_title.draw(win, outline=True)
    make_lemonade_amount.draw(win, outline=True)
    #cost_display.draw(win, outline=True, textdrop = 15)
    raise_price.draw(win, outline=True)
    lower_price.draw(win, outline=True)
    upgrades.draw(win, outline=True)

    pygame.display.flip()

    # Prep Phase
    prep = True
    while prep:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if make_lemonade_title.isOver(pos):
                    cur_instance.update_markers(new_lemonade = cur_instance.lemonade_batch_size, new_money = cur_instance.lemonade_cogs*cur_instance.lemonade_batch_size, new_hour = 1)
                    cur_instance.build_markers(win)
                    if int(cur_instance.open_time) == int(cur_instance.hour):

                        prep = False
                        break

    cur_instance.redraw_screen(win, title_text="You close in " + str(17 - cur_instance.hour) + " hours")
    cur_instance.build_selling_phase(win)
    # Selling phase
    selling = True
    while selling:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()


menu()