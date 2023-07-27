#rgSnake
#Autorstwa Mateusza Kuliga
#Reaktywacja popularnej niegdyś gry "Wąż"
#Copyright RedGhost 2017r
#version beta 0.2


import time
from tkinter import *
import random

class BodyParts(object):
    parts = []
    rects = []
    def __init__(self, x, y):
        self.parts.append([x, y, None, None])

class PowerUp(object):
    location = None
    img = None
    addone = False
    def __init__(self, x, y):
        PowerUp.location = [x, y]
        PowerUp.img = imagine.create_rectangle(PowerUp.location[0] * 10 - 2, PowerUp.location[1] * 10 - 2,
                                               PowerUp.location[0] * 10 + 2, PowerUp.location[1] * 10 + 2,
                                               fill='red')

    def new_place(self):
        x = None
        y = None
        if PowerUp.location == None:
            while self.check_parts(x, y) or x == None:
                x = random.randint(1, 19)
                y = random.randint(1, 19)
            PowerUp.location = [x, y]
            coords = [PowerUp.location[0] * 10 - 2,
                      PowerUp.location[1] * 10 - 2,
                      PowerUp.location[0] * 10 + 2,
                      PowerUp.location[1] * 10 + 2]
            imagine.coords(PowerUp.img, coords)

    def check_parts(self, x, y):
        for i in BodyParts.parts:
            if i[0] == x and i[1] == y:
                return True
        return False

    def check_collect(self):
        if BodyParts.parts[0][0] == PowerUp.location[0] and BodyParts.parts[0][1] == PowerUp.location[1]:
            PowerUp.location = None
            PowerUp.addone = True


class Game(object):
    def __init__(self):
        self.toward = None
        self.end = False
        self.taken = False
        for i in range(0, len(BodyParts.parts)):
            BodyParts.parts[i][2] = 'E'


    def rect_move(self):
        for part in range(0, len(BodyParts.parts)):
            if BodyParts.parts[part][2] == 'N':
                BodyParts.parts[part][1] -= 1
                imagine.move(BodyParts.rects[part], 0, -10)

            if BodyParts.parts[part][2] == 'E':
                BodyParts.parts[part][0] += 1
                imagine.move(BodyParts.rects[part], 10, 0)

            if BodyParts.parts[part][2] == 'S':
                BodyParts.parts[part][1] += 1
                imagine.move(BodyParts.rects[part], 0, 10)

            if BodyParts.parts[part][2] == 'W':
                BodyParts.parts[part][0] -= 1
                imagine.move(BodyParts.rects[part], -10, 0)

        for i in range(1, len(BodyParts.parts)):
            BodyParts.parts[i][2] = BodyParts.parts[i][3]
        self.taken = False

    def change_facing(self, nesw):
        #print(str(nesw))
        series = 0
        for i in str(nesw):
            if i == 'k':
                series += 1
                continue
            elif i == 'e' and series == 1:
                series += 1
                continue
            elif i == 'y' and series == 2:
                series += 1
                continue
            elif i == 's' and series == 3:
                series += 1
                continue
            elif i == 'y' and series == 4:
                series += 1
                continue
            elif i == 'm' and series == 5:
                series += 1
                continue
            elif series == 6:
                series += 1
                continue
            elif series == 7:
                self.toward = i
                break
            else:
                series = 0

        if self.toward == 'U' and BodyParts.parts[1][2] != 'S' and self.taken == False:
            BodyParts.parts[0][2] = 'N'
            self.toward = None
            self.taken = True
        elif self.toward == 'R' and BodyParts.parts[1][2] != 'W' and self.taken == False:
            BodyParts.parts[0][2] = 'E'
            self.toward = None
            self.taken = True
        elif self.toward == 'D' and BodyParts.parts[1][2] != 'N' and self.taken == False:
            BodyParts.parts[0][2] = 'S'
            self.toward = None
            self.taken = True
        elif self.toward == 'L' and BodyParts.parts[1][2] != 'E' and self.taken == False:
            BodyParts.parts[0][2] = 'W'
            self.toward = None
            self.taken = True

        if nesw == 'take':
            for i in range(1, len(BodyParts.parts)):
                BodyParts.parts[i][3] = BodyParts.parts[i-1][2]

    def collison(self):
        if BodyParts.parts[0][0] >= 20 or BodyParts.parts[0][0] <= 0:
            return True
        elif BodyParts.parts[0][1] >= 20 or BodyParts.parts[0][1] <= 0:
            return True
        for i in range(1, len(BodyParts.parts)):
            if BodyParts.parts[0][0] == BodyParts.parts[i][0] and BodyParts.parts[0][1] == BodyParts.parts[i][1]:
                return True
        else:
            return False
    def gameloop(self):
        crt_time = time.time()
        last_time = crt_time
        start = ['3', '2', '1']
        for i in start:
            print(i)
            time.sleep(1)
        while self.end != True:
            crt_time = time.time()
            self.change_facing('take')
            if crt_time - last_time > 0.2:
                #print(BodyParts.parts)
                #print(str(PowerUp.location) + '\n')
                #print(BodyParts.parts[0])
                self.rect_move()
                last_x = BodyParts.parts[len(BodyParts.parts) - 1][0]
                last_y = BodyParts.parts[len(BodyParts.parts) - 1][1]
                if PowerUp.addone == True:
                    BodyParts(last_x, last_y)
                    BodyParts.rects.append(imagine.create_rectangle(last_x * 10 - 5, last_y * 10 - 5,
                                                                    last_x * 10 + 5, last_y * 10 + 5,fill='white'))
                    PowerUp.addone = False
                last_time = crt_time
            meat.check_collect()
            meat.new_place()
            imagine.update()
            imagine.update_idletasks()
            self.end = self.collison()
            if self.end == True:
                rect_to_text = imagine.create_rectangle(60, 90, 140, 110, fill='white')
                end_text = imagine.create_text(100, 100, text='Koniec gry!')
            time.sleep(0.01)


BodyParts(11, 10)
BodyParts(10, 10)
BodyParts(9, 10)
BodyParts(8, 10)
BodyParts(7, 10)
BodyParts(6, 10)
BodyParts(5, 10)


root = Tk()
root.geometry(str(20*10) + 'x' + str(20*10))
imagine = Canvas(root, width=20*10, height=20*10, bd=0)
imagine.grid()


for i in BodyParts.parts:
    BodyParts.rects.append(imagine.create_rectangle(i[0]*10-5, i[1]*10-5, i[0]*10+5, i[1]*10+5, fill='white'))

meat = PowerUp(5, 5)
play = Game()

imagine.bind_all('<KeyPress-Up>', play.change_facing)
imagine.bind_all('<KeyPress-Right>', play.change_facing)
imagine.bind_all('<KeyPress-Down>', play.change_facing)
imagine.bind_all('<KeyPress-Left>', play.change_facing)

play.gameloop()


mainloop()


