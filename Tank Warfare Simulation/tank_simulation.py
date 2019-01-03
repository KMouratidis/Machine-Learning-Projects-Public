import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from PIL import Image
import numpy as np
import random


img = Image.open("tank_logo.png")
im = np.array(img)

im_blue = im.copy()
im_blue[:,:,2] += 140
im_red = im.copy()
im_red[:,:,0] += 140


class Country:

    def __init__(self, color="red"):
        self.color = color
        self.tanks = []
        pass

    def add_tank(self, T):
        self.tanks.append(T)

    def __str__(self):
        return self.color.upper()


class Tank:

    def __init__(self, name, country):
        """
            name: name of the tank (doesn't really matter)
            country: pick a color for plotting options
        """

        # initialize tank
        self.name = name
        self.country = country
        self.x = None
        self.y = None
        self.patch = None
        self.map = None

        # finally, add tanky to Country's army
        country.add_tank(self)

    def __str__(self):
        return f"Tank {self.name}"

    def _move(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        self._move(x,y)
        self.patch.remove(self)
        self.map.map[y-1][x-1].append(self)



class Patch:

    def __init__(self, y, x, map_):
        self.x = x
        self.y = y
        self.residents = []
        self.map = map_

    def __str__(self):
        return f"[{len(self.residents)}]"

    def append(self, T):
        self.residents.append(T) # add tank to patch

        # see if enemy tanks are in the same patch
        # if so, kill new or old one with 50% probabilty
        for tank in self.residents:
            if tank.country != T.country:
                tank_to_kill = random.choice([tank, T])
                tank_to_kill.patch = None
                tank_to_kill.map.tanks.remove(tank_to_kill)
                tank_to_kill.map = None
                self.remove(tank_to_kill)
                print(f"Tank '{tank_to_kill.name}' from Country: '{tank_to_kill.country}' got destroyed!")
                return


        T._move(self.x, self.y)
        T.patch = self
        T.map = self.map

    def remove(self, T):
        self.residents.remove(T)


class Map:

    def __init__(self, size=9):
        self.size = size
        self.map = [[Patch(y, x, self) for y in range(1, size+1)] for x in range(1,size+1)]
        self.tanks = []

    def __str__(self):
        s = ""
        for row in self.map:
            for col in row:
                s += f"{col}\t"
            s += "\n"

        return s

    def add_tank(self, T, x=1, y=1):
        self.map[y-1][x-1].append(T)
        self.tanks.append(T)

    def to_array(self):
        return np.array([[len(patch.residents) for patch in row] for row in self.map])

    def plot(self):
        fig, ax = plt.subplots()

        for tank in self.tanks:
            if tank.country.color == "blue":
                tank_im = im_blue
            else:
                tank_im = im_red

            ax.imshow(tank_im, aspect='auto',
                          extent=(tank.x+0.5, tank.x-0.5, tank.y-0.5, tank.y+0.5),
                          zorder=2)
            circle = plt.Circle((tank.x, tank.y), 2, color=tank.country.color, fill=False)
            ax.add_artist(circle)


        ax.imshow(np.zeros((self.size, self.size)), cmap="gray_r")

        ax.set_xlim(1, self.size)
        ax.set_xticks(np.arange(1, self.size+1))
        ax.set_ylim(1, self.size)
        ax.set_yticks(np.arange(1, self.size+1))

        plt.show()


if __name__ == '__main__':
    m = Map(10)

    red = Country("red")
    blue = Country("blue")

    t = Tank("StuG", country=red)
    m.add_tank(t, 3,3)

    t.move(2,2)
    m.plot()

    t2 = Tank("Panzer", country=blue)
    m.add_tank(t2, 6,6)
    m.plot()

    t2.move(4,4)
    m.plot()

    t2.move(2,2)
    m.plot()
