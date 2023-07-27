#rgSnake
#Autorstwa Mateusza Kuliga
#Reaktywacja popularnej niegdyś gry "Wąż"
#Copyright RedGhost 2017r
#version beta 0.2_o


import time
from tkinter import *
import random
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


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
        PowerUp.img = imagine.create_rectangle(PowerUp.location[0] * 8 - 1, PowerUp.location[1] * 8 - 1,
                                               PowerUp.location[0] * 8 + 1, PowerUp.location[1] * 8 + 1,
                                               fill='red')

    def new_place(self):
        x = None
        y = None
        if PowerUp.location == None:
            while self.check_parts(x, y) or x == None:
                x = random.randint(1, 15)
                y = random.randint(1, 7)
            PowerUp.location = [x, y]
            coords = [PowerUp.location[0] * 8 - 1,
                      PowerUp.location[1] * 8 - 1,
                      PowerUp.location[0] * 8 + 1,
                      PowerUp.location[1] * 8 + 1]
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
                imagine.move(BodyParts.rects[part], 0, -8)

            if BodyParts.parts[part][2] == 'E':
                BodyParts.parts[part][0] += 1
                imagine.move(BodyParts.rects[part], 8, 0)

            if BodyParts.parts[part][2] == 'S':
                BodyParts.parts[part][1] += 1
                imagine.move(BodyParts.rects[part], 0, 8)

            if BodyParts.parts[part][2] == 'W':
                BodyParts.parts[part][0] -= 1
                imagine.move(BodyParts.rects[part], -8, 0)

        for i in range(1, len(BodyParts.parts)):
            BodyParts.parts[i][2] = BodyParts.parts[i][3]
        self.taken = False  #zresetuj klawisz

    def change_facing(self, nesw):
        series = 0
        #print(str(nesw))
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
        if BodyParts.parts[0][0] >= 16 or BodyParts.parts[0][0] <= 0:
            return True
        elif BodyParts.parts[0][1] >= 8 or BodyParts.parts[0][1] <= 0:
            return True
        for i in range(1, len(BodyParts.parts)):
            if BodyParts.parts[0][0] == BodyParts.parts[i][0] and BodyParts.parts[0][1] == BodyParts.parts[i][1]:
                return True
        else:
            return False
    def gameloop(self):
        RST = 24
        DC = 23
        SPI_PORT = 0
        SPI_DEVICE = 0
        disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC,
                                               spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))
        disp.begin()

        disp.clear()
        disp.display()
        width = disp.width
        height = disp.height
        image = Image.new('1', (width, height))
        draw = ImageDraw.Draw(image)

        crt_time = time.time()
        last_time = crt_time
        start = ['3', '2', '1']
        for i in start:
            print(i)
            time.sleep(1)
        while self.end != True:
            crt_time = time.time()
            self.change_facing('take')
            if crt_time - last_time > 0.5:
                #print(BodyParts.parts)
                #print(str(PowerUp.location) + '\n')
                #print(BodyParts.parts[0])
                self.rect_move()    #ruch
                last_x = BodyParts.parts[len(BodyParts.parts) - 1][0]
                last_y = BodyParts.parts[len(BodyParts.parts) - 1][1]
                if PowerUp.addone == True:
                    BodyParts(last_x, last_y)
                    BodyParts.rects.append(imagine.create_rectangle(last_x * 8 - 4, last_y * 8 - 4,
                                                                    last_x * 8 + 4, last_y * 8 + 4,fill='white'))
                    PowerUp.addone = False


                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                for coord in range(0, len(BodyParts.parts)):
                    draw.rectangle((BodyParts.parts[coord][0] * 8 + 4, BodyParts.parts[coord][1] * 8 + 4,
                                    BodyParts.parts[coord][0] * 8 - 4,
                                    BodyParts.parts[coord][1] * 8 - 4), outline=255)
                draw.rectangle((PowerUp.location[0]*8+1, PowerUp.location[1]*8+1, PowerUp.location[0]*8-1,
                                PowerUp.location[1]*8-1), outline=255)
                draw.rectangle((1, 1, width - 1, height - 1), outline=255)
                disp.image(image)
                disp.display()


                last_time = crt_time
            meat.check_collect()
            meat.new_place()
            imagine.update()
            imagine.update_idletasks()
            self.end = self.collison()
            if self.end == True:
                font = ImageFont.load_default()
                draw.rectangle((0, 0, width, height), outline=0, fill=0)
                draw.text((10, 10), "Koniec gry!", font=font, fill=255)
                disp.image(image)
                disp.display()
            time.sleep(0.01)


BodyParts(11, 4)
BodyParts(10, 4)
BodyParts(9, 4)
BodyParts(8, 4)


root = Tk()
root.geometry(str(16*8) + 'x' + str(8*8))
imagine = Canvas(root, width=16*10, height=8*10, bd=0)
imagine.grid()


for i in BodyParts.parts:
    BodyParts.rects.append(imagine.create_rectangle(i[0]*8-4, i[1]*8-4, i[0]*8+4, i[1]*8+4, fill='white'))
meat = PowerUp(5, 5)
play = Game()

imagine.bind_all('<KeyPress-Up>', play.change_facing)
imagine.bind_all('<KeyPress-Right>', play.change_facing)
imagine.bind_all('<KeyPress-Down>', play.change_facing)
imagine.bind_all('<KeyPress-Left>', play.change_facing)

play.gameloop()

end_text  = imagine.create_text(80, 40, text='Koniec gry!')
mainloop()


