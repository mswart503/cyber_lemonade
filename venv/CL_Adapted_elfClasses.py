import pygame, random, pygame.font, math, pickle, pygame.gfxdraw

# Global variables
red = (249, 65, 68)
orangered = (243, 114, 44)
orange = (248, 150, 30)
orangelite = (255, 176, 79)
yellow = (249, 199, 79)
green = (70, 175, 145)
purple = (128, 74, 103)
white = (235, 235, 235)
fieldcolor = (100, 100, 100)
grey = (214, 214, 214)
black = (32, 34, 28)
sidecolor = grey
gap = 10
cardwidth = 100
cardheight = 150
singleplayer = True
cardcolor = (20, 20, 20)

# stole from stack overflow to outline text
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points
def render(text, font, gfcolor=None, ocolor=None, opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

# stole from stack overflow to round corners
def draw_rounded_rect(surface, rect, color, corner_radius):
    ''' Draw a rectangle with rounded corners.
    Would prefer this:
        pygame.draw.rect(surface, color, rect, border_radius=corner_radius)
    but this option is not yet supported in my version of pygame so do it ourselves.

    We use anti-aliased circles to make the corners smoother
    '''
    if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
        raise ValueError(f"Both height (rect.height) and width (rect.width) must be > 2 * corner radius ({corner_radius})")

    # need to use anti aliasing circle drawing routines to smooth the corners
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.aacircle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.top+corner_radius, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.left+corner_radius, rect.bottom-corner_radius-1, corner_radius, color)
    pygame.gfxdraw.filled_circle(surface, rect.right-corner_radius-1, rect.bottom-corner_radius-1, corner_radius, color)

    rect_tmp = pygame.Rect(rect)

    rect_tmp.width -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)

    rect_tmp.width = rect.width
    rect_tmp.height -= 2 * corner_radius
    rect_tmp.center = rect.center
    pygame.draw.rect(surface, color, rect_tmp)


class Cardslot:
    def __init__(self, color, x, y, width, height, card, isEmpty, name='', strength='', priority='',
                 meleetext='', abilitytext='', tokentext='', background = '', image='', character='', side=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.card = card
        self.isEmpty = isEmpty
        self.name = str(name)
        self.strength = str(strength)
        self.priority = priority
        self.meleetext = meleetext
        self.abilitytext = abilitytext
        self.tokentext = tokentext
        self.detailwidth = self.width * 2
        self.detailheight = self.height * 2
        self.image = image
        self.character = character
        self.font = 'alagard.ttf'
        self.side = side


        # New Fav -> 'athelas'
        # Now doesn't work for some reason --> Strong font, probably my fav #'oriyamnttc'
        # looks more like fantasy text -> 'noteworthyttc'
        # Formal, but nice -> 'ptserifttc'
        # Looks like hyroglyphics a bit, could be good for story mode-> 'skia'

    def draw(self, window, outline=None, textdrop=None, selected=None, decision=None, token=None, detail=None, mycard=None, oppcard=None, facedown=None, char=None, title=None, imagetextsize=None):

        # call method to draw the card on screen
        if outline:
            if char:
                outlinerect = pygame.Rect(self.x+3, self.y +3, self.width-2, self.height-6)
                draw_rounded_rect(window,outlinerect,self.color,10)
            else:
                outlinerect = pygame.Rect(self.x, self.y, self.width+4, self.height+4)
                draw_rounded_rect(window, outlinerect, black, 10)

        therect = pygame.Rect(self.x+2, self.y+2, self.width-1, self.height-1)
        draw_rounded_rect(window, therect, self.color, 7)
        #pygame.draw.rect(window, self.color, (self.x+4, self.y+4, self.width-8, self.height-8))
        if char:
            try:
                if self.priority == "Day":
                    if selected:
                        background = pygame.image.load("Day_Night_Images/sunselected.jpg")

                    elif decision:
                        background = pygame.image.load("Day_Night_Images/sundecision.jpg")

                    else:
                        background = pygame.image.load("Day_Night_Images/sun.jpg")

                else:
                    if selected:
                        background = pygame.image.load("Day_Night_Images/moonselected.jpg")
                    elif decision:
                        background = pygame.image.load("Day_Night_Images/moondecision.jpg")
                    else:
                        background = pygame.image.load("Day_Night_Images/moon.jpg")
                character = pygame.image.load(self.character)
                window.blit(background, (self.x+6,self.y+6))
                window.blit(character, (self.x+self.width/2-(character.get_width()/2)-1, self.y+(self.height/2-character.get_height()/2)))
            except:
                pass
        if self.name != '':

            namecolor = (199, 15, 2)
            if title:
                fontsize = 50
            else:
                fontsize = 30
            nfont = pygame.font.Font(self.font, fontsize)
            nametext = nfont.render(str(self.name), 1, namecolor)
            while nametext.get_width() >= self.width - 10:
                fontsize -= 1
                nfont = pygame.font.Font(self.font, fontsize)
                nametext = nfont.render(str(self.name), 1, namecolor)
            while nametext.get_height() >= self.height - 6:
                fontsize -= 1
                nfont = pygame.font.Font(self.font, fontsize)
                nametext = nfont.render(str(self.name), 1, namecolor)
            if char:
                window.blit(render(str(self.name), nfont, gfcolor=white, ocolor=black),
                            (self.x + (self.width / 2 - nametext.get_width() / 2),
                             self.y + (self.height / 2 - nametext.get_height() / 2)+50))

            else:
                if textdrop != None:
                    window.blit(render(str(self.name), nfont, gfcolor=white, ocolor=black), (self.x + (self.width / 2 - nametext.get_width() / 2),
                                                                                         self.y + textdrop + (self.height / 2 - nametext.get_height() / 2)))
                else:
                    window.blit(render(str(self.name), nfont, gfcolor=white, ocolor=black), (self.x + (self.width / 2 - nametext.get_width() / 2),
                                                                                         self.y + (self.height / 2 - nametext.get_height() / 2)))


        if self.strength != '':
            sfontsize = 25
            sfont = pygame.font.Font(self.font, sfontsize)
            strengthdisp = sfont.render(str(self.strength), 1, white)
            while strengthdisp.get_width() >= self.width-8:
                sfontsize -= 1
                sfont = pygame.font.Font(self.font, sfontsize)
                strengthdisp = sfont.render(self.strength, 1, yellow)
            window.blit(render(str(self.strength), sfont, gfcolor=white, ocolor=black), (self.x + 4, self.y + 4))

        if self.tokentext != '':
            pfontsize = 15
            pfont = pygame.font.Font(self.font, pfontsize)
            tokentext = pfont.render(self.tokentext, 1, yellow)
            while tokentext.get_width() >= self.width:
                pfontsize -= 1
                pfont = pygame.font.Font(self.font, pfontsize)
                tokentext = pfont.render(self.tokentext, 1, yellow)
            window.blit(tokentext, (self.x + (self.width - gap * 4), self.y+4))

        if facedown:
            therect = pygame.Rect(self.x + 3, self.y + 3, self.width - 6, self.height - 6)
            draw_rounded_rect(window, therect, self.color, 10)
            titletext = "elf"
            fontsize = 30
            nfont = pygame.font.Font(self.font, fontsize)
            titletext = nfont.render(titletext, 1, (255,255,255))
            window.blit(titletext, (self.x + (self.width / 2 - titletext.get_width() / 2),
                                   self.y + (self.height / 2 - titletext.get_height() / 2)))

    def settokentext(self,newtext):
        if self.tokentext != "":
            self.tokentext = self.tokentext+newtext
        else:
            self.tokentext = newtext

    def blankOut(self):
        self.color = (255, 255, 255)
        self.card = None
        self.isEmpty = True
        self.name = ""
        self.strength = ""
        self.priority = ""
        self.meleetext = ""
        self.abilitytext = ""

    def isOver(self, pos):
        # pos is the mouse position, or a tuple of x,y coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


class PowerScoreboard:
    def __init__(self, x, y):
        self.daycoin = pygame.image.load("Day_Night_Images/SunCoinScoreboard.png")
        self.nightcoin = pygame.image.load("Day_Night_Images/MoonCoinScoreboard.png")
        self.x = x
        self.y = y
        self.width = 200
        self.height = 200
        self.backgroundcolor = black
        #self.borderRect = pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+3)
        #self.interiorRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.opdaypowerText = 0
        self.opnightpowerText = 0
        self.mydaypowerText = 0
        self.mynightpowerText = 0
        self.font = 'alagard.ttf'


    def draw(self, window, daypoweradvantage, nightpoweradvantage):
        opdaypowerloc = (self.x+40, self.y+40)
        opnightpowerloc = (self.x+140, self.y+40)
        mydaypowerloc = (self.x+40, self.y+130)
        mynightpowerloc = (self.x+140, self.y+130)
        #draw_rounded_rect(window, self.borderRect, self.backgroundcolor, 7)
        #draw_rounded_rect(window, self.interiorRect, sidecolor, 7)
        tfont = pygame.font.Font(self.font, 20)
        nfont = pygame.font.Font(self.font, 40)
        nfontoutline = nfont.render(str(self.opdaypowerText), 1, black)
        window.blit(render("Opponent's Power", tfont, gfcolor=white, ocolor=black), (self.x+20, self.y))
        window.blit(render("Your Power", tfont, gfcolor=white, ocolor=black), (self.x+50, self.y+95))

        #draw coins:

        if daypoweradvantage == "my":
            window.blit(self.daycoin, (mydaypowerloc[0] - self.daycoin.get_width()/2+nfontoutline.get_width()/2, mydaypowerloc[1]-self.daycoin.get_height()/2+nfontoutline.get_height()/2))
        elif daypoweradvantage == "op":
            window.blit(self.daycoin, (opdaypowerloc[0] - self.daycoin.get_width()/2+nfontoutline.get_width()/2, opdaypowerloc[1]-self.daycoin.get_height()/2+nfontoutline.get_height()/2))
        if nightpoweradvantage == "my":
            window.blit(self.nightcoin, (mynightpowerloc[0]- self.nightcoin.get_width()/2+nfontoutline.get_width()/2,mynightpowerloc[1]-self.nightcoin.get_height()/2+nfontoutline.get_height()/2))
        elif nightpoweradvantage == "op":
            window.blit(self.nightcoin, (opnightpowerloc[0]- self.nightcoin.get_width()/2+nfontoutline.get_width()/2,opnightpowerloc[1]-self.nightcoin.get_height()/2+nfontoutline.get_height()/2))

        nfont = pygame.font.Font(self.font, 40)
        # opdaypower
        window.blit(render(str(self.opdaypowerText), nfont, gfcolor=white, ocolor=black),
                    opdaypowerloc)

        # opnightpower
        window.blit(render(str(self.opnightpowerText), nfont, gfcolor=white, ocolor=black),
                    opnightpowerloc)

        # mydaypower
        window.blit(render(str(self.mydaypowerText), nfont, gfcolor=white, ocolor=black),
                    mydaypowerloc)

        #opdaypower
        window.blit(render(str(self.mynightpowerText), nfont, gfcolor=white, ocolor=black),
                    mynightpowerloc)


    def updatevalues(self, opdaypower, opnightpower, mydaypower, mynightpower):
        self.opdaypowerText = opdaypower
        self.opnightpowerText = opnightpower
        self.mydaypowerText = mydaypower
        self.mynightpowerText = mynightpower


class ImageBox:
    def __init__(self,image, x, y, text, fontsize, outlinethickness):
        self.image = image
        self.x = x
        self.y = y
        self.text = text
        self.fontsize = fontsize
        self.outlinethickness = outlinethickness

    def draw(self, window, textYshift=0, color=(199, 15, 2), textoutlinecolor=black, textinsidecolor=yellow):
        if self.image != '':
            img = pygame.image.load(self.image)
            window.blit(img, (self.x, self.y))
            opxchoice = self.fontsize/15
            font = "alagard.ttf"

            nfont = pygame.font.Font(font, self.fontsize)
            nametext = nfont.render(self.text, 1, color)
            while nametext.get_width() >= img.get_width() - 8:
                self.fontsize -= 1
                nfont = pygame.font.Font(font, self.fontsize)
                nametext = nfont.render(self.text, 1, color)
            while nametext.get_height() >= img.get_height() - 6:
                self.fontsize -= 1
                nfont = pygame.font.Font(font, self.fontsize)
                nametext = nfont.render(self.text, 1, color)
            window.blit(render(self.text, nfont, gfcolor=textinsidecolor, ocolor=textoutlinecolor, opx=self.outlinethickness),
                        (self.x + (img.get_width() / 2 - nametext.get_width() / 2),
                         self.y + (img.get_height() / 2 - nametext.get_height() / 2)+textYshift))


class PriorityCoin:
    def __init__(self, centerx, centery, radius, priority, image=None):
        self.centerx = int(centerx)
        self.centery = int(centery)
        self.radius = int(radius)
        self.priority = int(priority)
        try:
            self.image = image
        except:
            pass


    def draw(self, window, highlight=''):
        if self.image is not None:
            coinimg = pygame.image.load(self.image)
            window.blit(coinimg, (self.centerx - (coinimg.get_width() / 2) + 1, self.centery - (coinimg.get_height() / 2) + 1))

        else:
            if highlight != '':
                pygame.draw.circle(window, (163, 140, 194), (self.centerx, self.centery), self.radius + 3)
                pygame.draw.circle(window, (255, 255, 255), (self.centerx, self.centery), self.radius)
            else:
                pygame.draw.circle(window, (0, 0, 0), (self.centerx, self.centery), self.radius + 3)
                pygame.draw.circle(window, (255, 255, 255), (self.centerx, self.centery), self.radius)
            if self.priority:
                fontsize = 30
                nfont = pygame.font.Font('alagard.ttf', fontsize)
                nametext = nfont.render("P", 1, (0, 0, 0))
                window.blit(nametext,
                            (self.centerx - (nametext.get_width() / 2) + 1, self.centery - (nametext.get_height() / 2) + 1))

    def isOver(self, pos):
        # pos is the mouse position, or a tuple of x,y coordinates
        if pos[0] > (self.centerx-self.radius) and pos[0] < (self.centerx+self.radius):
            if pos[1] > self.centery-self.radius and pos[1] < self.centery + self.radius:
                return True
        return False


class Textbox:
    def __init__(self, color, x, y, width, height, text, fontsize):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = 'alagard.ttf'
        self.fontsize = fontsize

        self.renderedfont = pygame.font.Font(self.font, fontsize)

    def draw(self, window, outline=None, newline_each_time=None, selected=None, decision=None, blank=None, textonly=False):
        if not textonly:
            if outline:
                therect = pygame.Rect(self.x - 2, self.y - 2, self.width +4, self.height +4)
                draw_rounded_rect(window, therect, black, 7)

            if selected:
                pygame.draw.rect(window, (163, 140, 194), (self.x - 4, self.y - 4, self.width + 8, self.height + 8))
            if decision:
                pygame.draw.rect(window, (253, 109, 61), (self.x - 4, self.y - 4, self.width + 8, self.height + 8))

            if blank:
                pass
            else:
                therect = pygame.Rect(self.x, self.y, self.width, self.height)
                draw_rounded_rect(window, therect, self.color, 7)

        if self.text != '' or self.text != None:

            if newline_each_time:
                lines = self.text.split(";")
                linearray = []
                for line in lines:
                    linearray.append(line)


            else:
                lines = self.text.split(" ")
                linearray = []
                while len(lines) > 0:
                    line = ""
                    while len(line) < 60:
                        try:
                            if len(lines[0]) + len(line) > self.width:
                                break

                            else:
                                line = line + " " + lines.pop(0)
                        except:
                            break

                    linearray.append(line)

            originalfont = pygame.font.Font(self.font, self.fontsize)
            counter = 0
            for lineitem in linearray:
                oritext = originalfont.render(lineitem, 1, (0, 0, 0))
                # window.blit(render("Opponent's Power", tfont, gfcolor=white, ocolor=black), (self.x + 20, self.y))
                # window.blit(render("Your Power", tfont, gfcolor=white, ocolor=black), (self.x + 50, self.y + 95))
                text = originalfont.render(lineitem, 1, (0, 0, 0))
                window.blit(render(lineitem, self.renderedfont, gfcolor=white, ocolor=black), (self.x + (self.width / 2 - text.get_width() / 2),
                                   (self.y + gap / 2 + (oritext.get_height() * counter))))
                counter += 1


class Card:
    def __init__(self, name, strength, priority, abilityid, token, meleecheck, abilitytext, activeability, isEmpty, serial):
        self.name = name
        self.strength = strength
        self.priority = priority
        self.abilityid = abilityid
        self.token = token
        self.meleecheck = meleecheck
        self.abilitytext = abilitytext
        self.isEmpty = isEmpty
        self.serial = serial
        self.activeability = activeability

    def blank_out(self):
        self.name = ""
        self.strength = ""
        self.priority = ""
        self.abilityid = ""
        self.token = False
        self.abilitytext = ""
        self.isEmpty = True

    def get_name(self):
        return self.name

    def set_name(self, newname):
        self.name = newname

    def get_strength(self):
        return self.strength

    def set_strength(self, newstrength):
        self.strength = newstrength

    def get_priority(self):
        return self.priority

    def set_priority(self, newpriority):
        self.priority = newpriority

    def get_abilityid(self):
        return self.abilityid

    def set_abilityid(self, newabilityid):
        self.abilityid = newabilityid

    def get_token(self):
        return self.token

    def set_token(self, newtoken):
        self.token = newtoken

# League Classes below:
class Player:
    def __init__(self, playername):
        self.name = playername
        self.baseSynergyVision = 0
        self.baseThinkingAhead = 0
        self.baseMetaKnowledge = 0
        self.age = 0
        self.jobHours = (0, 0)
        self.gamesplayed = 0
        self.wins = 0
        self.score = 0
        self.rank = 0

    def applymatchtorank(self, win, changenumber):

        if win:
            self.wins += 1
            self.score = self.score + round(changenumber / 5)

        if not win:
            if self.score + round(changenumber / 2) <= 0:
                self.score = 0
            else:
                self.score = self.score + round(changenumber / 10)


        # To determine rank, I take the amount the person won by and divide it by 5 and round it. That number is their rank change.
        # Losses are reduced by half as much as winners are increased by. Hopefully this makes points more evenly spread.
        # In future I want to have the amount you rank fluctuates dependant on how high a rank the person you beat is.
        self.gamesplayed += 1


class League:
    def __init__(self):
        self.playerdict = {}
        self.rankingArray = []
        self.playerlist = []
        self.rankedDict = {}


    def createplayers(self, numberofplayers, gamestoprep):
        playernames = ["Amos", "Catalina", "Earl", "Clifford the Stump", "Lil Perry", "Ava", "Lucky Lucy",
                       "Buster", "Mabel", "Beatrix", "Liam", "Old Man Keith", "Fletcher", "Crabby Addy",
                       "Francis", "Reverend Gus", "Jasper", "Sweets", "Viviana", "Milton", "Norm",
                       "Big Otis", "Sly", "Roy", "Sterling", "Famous Otis", "Martha"]

        counter = 0
        # This section creates blank slate characters
        while counter < numberofplayers:
            random.shuffle(playernames)
            randomname = playernames.pop()
            curplayer = Player(randomname)
            self.playerdict[randomname] = curplayer
            self.playerlist.append(randomname)
            counter += 1
        self.playerdict["You"] = Player("You")
        self.playerlist.append("You")

        # This section makes them play against each other and change rankings
        # Matchups are completely random, want to make it so peoplw who show up at different times play each other.
        counter = 0
        while counter < gamestoprep:
            p1num = random.randint(0,numberofplayers-1)
            p2num = random.randint(0,numberofplayers-1)
            while p1num == p2num:
                p2num = random.randint(0, numberofplayers-1)
            winner, loser, winamount = self.aiMatch(self.playerdict[self.playerlist[p1num]],self.playerdict[self.playerlist[p2num]])
            winner.applymatchtorank(True, winamount)
            loser.applymatchtorank(False, -1*winamount)
            counter += 1
        self.rankleague()
        self.createsavefile()

    def rankleague(self):
        tempArray = []
        for player in self.playerlist:
            curplayer = self.playerdict[player]
            tempArray.append([curplayer.name, curplayer.score])

        rankedArray = []
        while tempArray != []:
            curplayer = tempArray.pop(0)
            if rankedArray == []:
                rankedArray.append(curplayer)
            else:
                counter = 0
                while True:
                    try:
                        checkplayer = rankedArray[counter]
                        if curplayer[1] >= checkplayer[1]:
                            rankedArray.insert(counter, curplayer)
                            break
                        else:
                            counter += 1
                    except:
                        rankedArray.append(curplayer)
                        break
        rank = 1
        for player in rankedArray:
            player.insert(0, rank)
            self.rankedDict[player[1]] = rank
            rank += 1

        return rankedArray

    def createsavefile(self):
        playerdict = self.playerdict.copy()
        playerlist = self.playerlist.copy()

        savefile = {"playerdict": playerdict,
                    "playerlist": playerlist,
                    }
        pickle.dump(savefile, open('savefiles/tavernleague.pkl', "wb"))

    def loadsavefile(self):
        savefile = pickle.load(open("savefiles/tavernleague.pkl", "rb"))
        self.playerdict = savefile["playerdict"]
        self.playerlist = savefile["playerlist"]

    def aiMatch(self, player1, player2):
        # Right now this is completely randomized, in future versions I want to have them play real games
        whowon = None
        wholost = None
        byhowmuch = 0
        winner = random.randint(0,100)
        if winner > 50:
            whowon = player2
            wholost = player1
            byhowmuch = winner-50
        else:
            whowon = player1
            wholost = player2
            byhowmuch = winner
        whowon.gamesplayed += 1
        whowon.wins += 1
        wholost.gamesplayed += 1

        return whowon, wholost, byhowmuch


class RankingBoard:
    def __init__(self, league, x, y, width, height, myplayername):
        self.league = league
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rankArray = []
        self.myplayername = myplayername
        self.rankDict = {}


    def topten(self):
        tempArray = []
        for player in self.league.playerlist:
            curplayer = self.league.playerdict[player]
            tempArray.append([curplayer.name, curplayer.score])

        rankedArray = []
        while tempArray != []:
            curplayer = tempArray.pop(0)
            if rankedArray == []:
                rankedArray.append(curplayer)
            else:
                counter = 0
                while True:
                    try:
                        checkplayer = rankedArray[counter]
                        if curplayer[1] >= checkplayer[1]:
                            rankedArray.insert(counter, curplayer)
                            break
                        else:
                            counter += 1
                    except:
                        rankedArray.append(curplayer)
                        break
        rank = 1
        for player in rankedArray:
            player.insert(0, rank)
            self.rankDict[player[1]] = rank
            rank += 1

        return rankedArray


    def draw(self, window):
        background = pygame.image.load("scroll.png")
        window.blit(background, (self.x, self.y))
        nfont = pygame.font.Font('alagard.ttf', 40)
        toptencolor = (140, 185, 209)
        nametext = nfont.render("Top Ten", 1, yellow)
        rank1 = Cardslot(toptencolor, self.x+45, self.y+90, self.width-100, 40, None, False, str(self.rankArray[0][0])+" - "+str(self.rankArray[0][1])+" - "+str(self.rankArray[0][2]))
        window.blit(render("Top Ten", nfont, gfcolor=yellow, ocolor=black), (self.x + self.width / 2 - nametext.get_width() / 2, self.y + 20))
        rank2 = Cardslot(toptencolor, rank1.x, rank1.y+rank1.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[1][0])+" - "+self.rankArray[1][1]+" - "+str(self.rankArray[1][2]))
        rank3 = Cardslot(toptencolor, rank1.x, rank2.y+rank2.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[2][0])+" - "+self.rankArray[2][1]+" - "+str(self.rankArray[2][2]))
        rank4 = Cardslot(toptencolor, rank1.x, rank3.y+rank3.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[3][0])+" - "+self.rankArray[3][1]+" - "+str(self.rankArray[3][2]))
        rank5 = Cardslot(toptencolor, rank1.x, rank4.y+rank4.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[4][0])+" - "+self.rankArray[4][1]+" - "+str(self.rankArray[4][2]))
        rank6 = Cardslot(toptencolor, rank1.x, rank5.y+rank5.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[5][0])+" - "+self.rankArray[5][1]+" - "+str(self.rankArray[5][2]))
        rank7 = Cardslot(toptencolor, rank1.x, rank6.y+rank6.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[6][0])+" - "+self.rankArray[6][1]+" - "+str(self.rankArray[6][2]))
        rank8 = Cardslot(toptencolor, rank1.x, rank7.y+rank7.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[7][0])+" - "+self.rankArray[7][1]+" - "+str(self.rankArray[7][2]))
        rank9 = Cardslot(toptencolor, rank1.x, rank8.y+rank8.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[8][0])+" - "+self.rankArray[8][1]+" - "+str(self.rankArray[8][2]))
        rank10 = Cardslot(toptencolor, rank1.x, rank9.y+rank9.height+10, rank1.width, rank1.height, None, False, str(self.rankArray[9][0])+" - "+self.rankArray[9][1]+" - "+str(self.rankArray[9][2]))
        rankings = [rank1,rank2,rank3,rank4,rank5,rank6,rank7,rank8,rank9,rank10]
        for player in rankings:
            if player.name == str(self.rankDict[self.myplayername])+ " - "+self.myplayername+ " - "+str(self.rankArray[int(self.rankDict[self.myplayername]) - 1][2]):
                player.color = (120, 36, 199)
                break
        for rank in rankings:
            rank.draw(window, outline=True)

        pygame.display.flip()


class Gametables:
    def __init__(self,x, y, width, height):
        self.seatcolor = (92, 224, 187)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sitDict = {"table1":["Open","Open"],
                        "table2": ["Open", "Open"],
                        "table3": ["Open", "Open"],
                        "table4": ["Open", "Open"]}
        self.seat1 = Cardslot(self.seatcolor, self.x + 224, self.y + 55, 150, 40, None, False, name=str(self.sitDict["table1"][0]))
        self.seat2 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 125, 150, 40, None, False, name=str(self.sitDict["table1"][1]))
        self.seat3 = Cardslot(self.seatcolor, self.seat1.x + 210, self.seat1.y, 150, 40, None, False, name=str(self.sitDict["table2"][0]))
        self.seat4 = Cardslot(self.seatcolor, self.seat3.x, self.seat3.y + 125, 150, 40, None, False, name=str(self.sitDict["table2"][1]))
        self.seat5 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 180, 150, 40, None, False, name=str(self.sitDict["table3"][0]))
        self.seat6 = Cardslot(self.seatcolor, self.seat1.x, self.seat5.y + 125, 150, 40, None, False, name=str(self.sitDict["table3"][1]))
        self.seat7 = Cardslot(self.seatcolor, self.seat5.x + 210, self.seat5.y, 150, 40, None, False, name=str(self.sitDict["table4"][0]))
        self.seat8 = Cardslot(self.seatcolor, self.seat7.x, self.seat7.y + 125, 150, 40, None, False, name=str(self.sitDict["table4"][1]))



    def draw(self, window):
        bg = pygame.image.load("map.png")
        table = pygame.image.load("taverntable.png")
        window.blit(bg,(self.x, self.y))
        window.blit(table, (self.x+250,self.y+100))
        window.blit(table, (self.x+460,self.y+100))
        window.blit(table, (self.x+250,self.y+280))
        window.blit(table, (self.x+460,self.y+280))
        self.seat1 = Cardslot(self.seatcolor, self.x + 224, self.y + 55, 150, 40, None, False, name=str(self.sitDict["table1"][0]))
        self.seat1.draw(window, outline=True)
        self.seat2 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 125, 150, 40, None, False, name=str(self.sitDict["table1"][1]))
        self.seat2.draw(window, outline=True)
        self.seat3 = Cardslot(self.seatcolor, self.seat1.x + 210, self.seat1.y, 150, 40, None, False, name=str(self.sitDict["table2"][0]))
        self.seat3.draw(window, outline=True)
        self.seat4 = Cardslot(self.seatcolor, self.seat3.x, self.seat3.y + 125, 150, 40, None, False, name=str(self.sitDict["table2"][1]))
        self.seat4.draw(window, outline=True)
        self.seat5 = Cardslot(self.seatcolor, self.seat1.x, self.seat1.y + 180, 150, 40, None, False, name=str(self.sitDict["table3"][0]))
        self.seat5.draw(window, outline=True)
        self.seat6 = Cardslot(self.seatcolor, self.seat1.x, self.seat5.y + 125, 150, 40, None, False, name=str(self.sitDict["table3"][1]))
        self.seat6.draw(window, outline=True)
        self.seat7 = Cardslot(self.seatcolor, self.seat5.x + 210, self.seat5.y, 150, 40, None, False, name=str(self.sitDict["table4"][0]))
        self.seat7.draw(window, outline=True)
        self.seat8 = Cardslot(self.seatcolor, self.seat7.x, self.seat7.y + 125, 150, 40, None, False, name=str(self.sitDict["table4"][1]))
        self.seat8.draw(window, outline=True)
        pygame.display.flip()

    def aitablepick(self):
        tablepick = random.randint(0,3)
        seatpick = random.randint(0,1)
        if tablepick == 0:
            table = "table1"
            if seatpick == 0:
                locnum = 0
            else:
                locnum = 1
        elif tablepick == 1:
            table = "table2"
            if seatpick == 0:
                locnum = 2
            else:
                locnum = 3
        elif tablepick == 2:
            table = "table3"
            if seatpick == 0:
                locnum = 4
            else:
                locnum = 5
        elif tablepick == 3:
            table = "table4"
            if seatpick == 0:
                locnum = 6
            else:
                locnum = 7


        return table, seatpick, locnum


    def playerupdate(self, window):
        pass


class PlayerStats:
    def __init__(self,x, y, width, height, name, wins, rank, score):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.wins = wins
        self.rank = rank
        self.score = score
        self.playercolor = (120, 36, 199)

    def draw(self, window):
        bg = pygame.image.load("myscroll.png")
        window.blit(bg,(self.x, self.y))

        nameslot = Cardslot(self.playercolor, self.x+100,self.y+self.height/2-40,150,50,None,False,self.name)
        nameslot.draw(window, outline=True)
        rankslot = Cardslot(self.playercolor, nameslot.x + nameslot.width + 40, self.y + self.height / 2 - 45, 75, 60, None, False, strength="Rank", priority=str(self.rank))
        rankslot.draw(window, outline=True)
        scoreslot = Cardslot(self.playercolor, rankslot.x + rankslot.width + 40, self.y + self.height / 2 - 45, 75, 60, None, False, strength="Score", priority=str(self.score))
        scoreslot.draw(window, outline=True)
        winslot = Cardslot(self.playercolor, scoreslot.x + scoreslot.width + 40, self.y + self.height / 2 - 45, 70, 60, None, False, strength="Wins", priority=str(self.wins))
        winslot.draw(window, outline=True)
        pygame.display.flip()

    def applyMatchToStats(self, win, byhowmuch):
        scorechange = round(byhowmuch/5)
        if win:
            self.wins += 1
            self.score += scorechange

        else:
            if self.score-scorechange<= 0:
                self.score = 0
            else:
                self.score = self.score-scorechange

