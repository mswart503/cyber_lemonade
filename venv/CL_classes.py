

class Instance:
    def __init__(self):
        self.day = 1
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        self.weekday = days_of_week[self.day % 7 - 1]
        self.hour = 6
        self.money = 100
        self.lemonade = 0
        self.lemon_ratio = 1
        self.water_ratio = 3
        self.sugar_ratio = 2

    def day_of_week_pick(self):
        days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return days_of_week[self.day % 7 - 1]