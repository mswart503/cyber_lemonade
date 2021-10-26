from CL_Adapted_elfClasses import Cardslot
from CL_Adapted_elfClasses import Textbox
import pygame
from pygame import *
import os
import random
pygame.init()

background = "Backgrounds/the_stand_smaller.jpg"
bg = pygame.image.load(background)
grey = (34,53,76)
orange = (255,170,95)
red_grey = (141,108,122)
salmon = (208,123,90)
light_yellow = (251,220,163)
brown = (124,74,52)

class Instance:
    def __init__(self):
        self.day = 1
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.weekday = days_of_week[self.day % 7 - 1]
        self.hour = 6
        self.money = 20
        self.lemonade = 0
        self.lemon_ratio = 1
        self.water_ratio = 3
        self.sugar_ratio = 2
        self.lemonade_price = 1
        self.lemonade_cogs = .5
        self.lemonade_batch_size = 4
        self.open_time = 9
        self.day_marker = Cardslot(salmon, 40, 40, 60, 80, None, False, name=str(self.day), strength="Day")
        self.weekday_marker = Cardslot(salmon, self.day_marker.x + self.day_marker.width + 30, 40, 90, 80, None, False, name=self.weekday,
                           strength="Weekday")
        self.hour_marker = Cardslot(salmon, self.weekday_marker.x + self.weekday_marker.width + 30, 40, 60, 80, None, False, name=str(self.hour),
                        strength="Hour")
        self.money_marker = Cardslot(salmon, self.hour_marker.x + self.hour_marker.width + 150, 40, 90, 80, None, False, name="$ "+str(self.money),
                        strength="Money")
        self.cost_marker = Cardslot(salmon, 235, 670, 150, 60, None, False, name="$ "+str(self.lemonade_price),
                        strength="Current Price:")
        self.lemonade_marker = Cardslot(salmon, self.money_marker.x + self.money_marker.width + 30, 40, 140, 80, None, False, name=str(self.lemonade),
                        strength="Lemonade Cups")
        self.prep_title = Cardslot(salmon, 750, 20, 420, 100, None, False,
                              name="You open in " + str(9 - self.hour) + " hours")

        self.marker_list = [self.day_marker, self.weekday_marker, self.hour_marker, self.money_marker, self.cost_marker, self.lemonade_marker, self.prep_title]

        self.lemonade_sold_today = Cardslot(salmon, 800, 140, 150, 70, None, False, name=0, strength="Cups Sold Today")
        self.money_made_today = Cardslot(salmon, 980, 140, 150, 70, None, False, name="$0", strength="Money Made Today")
    def day_of_week_pick(self):
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return days_of_week[self.day % 7 - 1]

    def build_markers(self, win):
        for marker in self.marker_list:
            drop = 0
            if marker.strength != '':
                drop = 13

            marker.draw(win, outline=True, textdrop=drop)
        pygame.display.flip()

    def update_markers(self, new_lemonade=0, new_money = 0, new_hour = 0):
        if new_lemonade != 0:
            self.lemonade = self.lemonade + new_lemonade
            self.lemonade_marker.name = str(self.lemonade)
        if new_money != 0:
            self.money = self.money - new_money
            self.money_marker.name = "$"+str(int(self.money))
        if new_hour != 0:
            self.hour = self.hour + new_hour
            self.hour_marker.name = str(self.hour)
            self.prep_title.name = "You open in " + str(9 - self.hour) + " hours"

    def redraw_screen(self, win, title_text = ""):
        win.fill(orange)
        win.blit(bg, (0, 0))
        self.prep_title.name = title_text
        self.build_markers(win)

    def build_selling_phase(self, win):
        self.lemonade_sold_today.draw(win, outline=True, textdrop = 13)
        self.money_made_today.draw(win, outline=True, textdrop = 13)
        pygame.display.flip()