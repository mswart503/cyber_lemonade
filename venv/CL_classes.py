from CL_Adapted_elfClasses import Cardslot
from CL_Adapted_elfClasses import Textbox
import pygame
from pygame import *
import os
import random, json
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
        self.society = Society()
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
        self.new_customer_ratio = .2

        # permanent markers around store
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

        # selling phase markers
        self.lemonade_sold_today = Cardslot(salmon, 800, 140, 150, 70, None, False, name=0, strength="Cups Sold Today")
        self.money_made_today = Cardslot(salmon, 980, 140, 150, 70, None, False, name="$0", strength="Money Made Today")
        self.customer_interaction = Textbox(red_grey, 800, 230, 340, 120, 20)


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
        self.customer_interaction.draw(win, outline=True)
        pygame.display.flip()

    def selling_hour(self, win):
        new_customers = random.randint(0, 3)
        hour_modifier = round(self.new_customer_ratio*(self.hour-9))
        new_customers = new_customers+hour_modifier


    def customer_interaction(self, customer):
        pass


class Society:
    def __init__(self):
        self.people = {}
        self.groups = {}

        if os.stat("saved_game/society.txt").st_size == 0:
            self.create_new_society()
        else:
            with open("saved_game/society.txt") as json_file:
                data = json.load(json_file)
        print(self.people)
        print(self.groups)
        input("check")
    def create_new_society(self):
        self.first_names = ["Baron", "Bianca", "Marty", "Shannon", "Filbert", "Draco", "Grace", "Constantine",
                            "Catalina", "Lenny"]
        self.last_names = ["Viel", "Combat", "Wellwish", "Smith", "Serenity", "Rivers", "Xylo", "Yillman"]
        self.group_names = ["Wishers","Dreamers","Battlers","Conspirators","Lookers","Beauties","Mondays","Utilities",
                            "Reavers","Toppers","Accelerants"]
        for g_names in self.group_names:
            self.groups[g_names] = []
        self.used_names = []
        customer_count = 10
        count = 0
        while count < customer_count:
            not_new = True
            while not_new:
                first = self.first_names[random.randint(0, len(self.first_names)-1)]
                last = self.last_names[random.randint(0, len(self.last_names)-1)]
                name = first+" "+last
                if name not in self.used_names:
                    not_new = False
                    self.used_names.append(name)
            group = self.group_names[random.randint(0, len(self.group_names)-1)]
            new_person = Customer(first, last, group)
            self.people[name] = new_person
            self.groups[group].append(new_person)
            count += 1
        with open("saved_game/society.txt", "w") as json_file:
            save_stuff = [self.people, self.groups]
            json.dump(save_stuff, json_file)

class Customer:
    def __init__(self, first_name, last_name, group):
        self.visits = 0
        self.name = first_name+" "+last_name
        self.group = group

