from CL_Adapted_elfClasses import Cardslot
from CL_Adapted_elfClasses import Textbox
import pygame
from pygame import *
import os
import random, pickle
pygame.init()

background = "Backgrounds/the_stand_smaller.jpg"
bg = pygame.image.load(background)
clock = pygame.time.Clock()
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
        self.customer_interaction = Textbox(red_grey, 797, 230, 340, 120, "Saying Things!", 20)
        self.customer_text = Textbox(red_grey, 100, 350, 200, 100,"Basic Text", 20)


    def day_of_week_pick(self):
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return days_of_week[self.day % 7 - 1]

    def build_markers(self, win, noflip=""):
        for marker in self.marker_list:
            drop = 0
            if marker.strength != '':
                drop = 13

            marker.draw(win, outline=True, textdrop=drop)
        if noflip == "":
            pygame.display.flip()
        else:
            pass

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

    def redraw_screen(self, win, title_text = "", noflip = ""):
        win.fill(orange)
        win.blit(bg, (0, 0))
        self.prep_title.name = title_text
        if noflip == "":
            self.build_markers(win)
        else:
            self.build_markers(win, noflip = noflip)

    def build_selling_phase(self, win, noflip = ""):
        self.lemonade_sold_today.draw(win, outline=True, textdrop = 13)
        self.money_made_today.draw(win, outline=True, textdrop = 13)
        self.customer_interaction.draw(win, outline=True)
        if noflip != "":
            pass
        else:
            pygame.display.flip()

    def setup_selling_hour(self):
        cust_number = self.number_of_customer_this_hour()
        counter = 0
        times_to_show = []
        while counter < cust_number:
            show_up_time = random.randint(0, 60)
            if show_up_time not in times_to_show:
                times_to_show.append(show_up_time)
                counter += 1
        customers_to_show = random.sample(self.society.people_list, cust_number)
        customer_list_with_time = []

        # empty lists are false so the following runs until the list is empty
        while customers_to_show:
            cust_to_add = customers_to_show.pop()
            cust_to_add.arrival_time = times_to_show.pop()
            customer_list_with_time.append(cust_to_add)
        return customer_list_with_time


    def selling_hour_tick(self, win):
        timer = 0


        self.customer_inter("darwin", win)

    def customer_inter(self, customer, win):
        self.move_up_to_counter(customer, win)

    # This moves the customer to the counter while allowing events to continue
    def move_in_time(self, customer_list, win, actual_time, noflip=""):

        for customer in customer_list:
            if customer.arrival_time <= actual_time:
                customer.arrived = True
            if customer.arrived:
                cur_customer = pygame.image.load(customer.image)
                current_location = customer.location
                if customer.hover_location == customer.hover_loop[1]:
                    customer.hover_increase = False
                elif customer.hover_location == customer.hover_loop[0]:
                    customer.hover_increase = True

                new_location = (current_location[0]+3, current_location[1] + customer.hover_location)
                customer.location = new_location
                if customer.hover_increase ==True:
                    customer.hover_location += .5
                elif customer.hover_increase ==False:
                    customer.hover_location -= .5
                self.redraw_screen(win, noflip = "no", title_text="You close in " + str(17 - self.hour) + " hours")
                win.blit(cur_customer, new_location)
            pygame.display.flip()


    # This moves the customer up to the counter all at once pausing all events
    def move_up_to_counter(self, customer, win, time):
        start_location = (0, 480)
        end_location = (230, start_location[1])
        cur_customer = pygame.image.load("/Users/Elizabeth/PycharmProjects/CyberLemonade/venv/characters/Random.png")
        cur_location = start_location
        win.blit(cur_customer, cur_location)
        pygame.display.flip()
        hover_loop = [-5, 5]
        hover_loc = hover_loop[0]
        hover_increase = True
        while cur_location[0]<end_location[0]:
            if hover_loc == hover_loop[1]:
                hover_increase = False
            elif hover_loc == hover_loop[0]:
                hover_increase = True
            first_loc_x = cur_location[0]
            second_loc_x = int(first_loc_x)+3
            first_loc_y = cur_location[1]
            second_loc_y = int(first_loc_y) + hover_loc
            if hover_increase == True:
                hover_loc += .5
            elif hover_increase == False:
                hover_loc -= .5

            cur_location = (second_loc_x, second_loc_y)
            self.redraw_screen(win, noflip = "no", title_text="You close in " + str(17 - cur_instance.hour) + " hours")
            win.blit(cur_customer, cur_location)
            pygame.display.flip()
            clock.tick(60)

        input("hold it")
        pass

    def number_of_customer_this_hour(self):
        new_customers = random.randint(0, 3)
        hour_modifier = round(self.new_customer_ratio*(self.hour-9))
        new_customers = new_customers+hour_modifier
        return new_customers

class Society:
    def __init__(self):
        self.people = {}
        self.groups = {}
        self.storage = []
        self.people_list = []

        if os.stat("saved_game/society.pickle").st_size == 0:
            self.create_new_society()
            with open("saved_game/society.pickle", "wb") as file:
                self.storage = file

        else:
            self.people, self.groups, *_ = pickle.load(open("saved_game/society.pickle", "rb"))

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
            self.people_list.append(new_person)

            count += 1
        save_stuff = [self.people, self.groups]
        pickle.dump(save_stuff, open("saved_game/society.pickle", 'wb'))

class Customer:
    def __init__(self, first_name, last_name, group):
        self.visits = 0
        self.name = first_name+" "+last_name
        self.group = group
        self.location = (0, 400)
        self.image = "/Users/Elizabeth/PycharmProjects/CyberLemonade/venv/characters/Random.png"
        self.hover_loop = [-5, 5]
        self.hover_location = self.hover_loop[0]
        self.hover_increase = True
        self.arrival_time = 0
        self.arrived = False
