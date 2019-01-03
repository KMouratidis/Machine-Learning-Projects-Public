from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
import cv2
from PIL import Image
import numpy as np
import random
import warnings

# https://stackoverflow.com/a/45076236/6655150
from matplotlib.colors import ListedColormap 
cmap_light = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])

warnings.filterwarnings('ignore')

img = Image.open("tank_logo.png")
im = np.array(img)

im_blue = im.copy()
im_blue[:,:,2] += 140
im_red = im.copy()
im_red[:,:,0] += 140

distance = lambda p1, p2: np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2) 

class Game:
    """
        This class should handle the turns. If a move cannot happen in one turn, it should get queued or limited.
    """    
    
    pass


class Turn:
    
    def __init__(self, instructions):
        """
            orders: a dictionary of orders: {general:[[acquire_tank, {'T': T}], [order_tank, dict(**kwargs)], [order3...]]}
        """
        for general, orders in instructions.items():
            for order in orders:
                if order[0] == "acquire_tank":
                    general.acquire_tank(**order[1]) # T
                elif order[0] == "order_tank":
                    general.order_tank(**order[1]) # T, pos
                elif order[0] == "purchase_tanks":
                    general.purchase_tanks(**order[1]) # any of the valid kwargs


class General:
    
    def __init__(self, name, country, map_, pos=(0,0), tanks=None):
        self.name = name
        self.country = country
        if tanks is not None:
            self.tanks = tanks
        else:
            self.tanks = []
            
        self.map = map_
        self.x, self.y = pos
        
        
    ### Available commands (to be used by Turn) ###    
    
    def acquire_tank(self, T):
        self.tanks.append(T)
        
    def purchase_tanks(self, n=5, *, type_="StuG", types=None):
        if types is None:
            for _ in range(n):
                new_tank = Tank(type_, self.country)
                new_tank.general = self
                self.tanks.append(new_tank) # add tank to general's army
                self.map.add_tank(new_tank, x=self.x, y=self.y) # add tank to map
        else:
            if isinstance(types, (list, tuple)) and len(types)==n:
                for t in types:
                    new_tank = Tank(t, self.country)
                    new_tank.general = self
                    self.tanks.append(new_tank) # add tank to general's army
                    self.map.add_tank(new_tank, x=self.x, y=self.y) # add tank to map
            else:
                print("Error with purchasing tanks.")
                
    def order_tank(self, T, pos):
        assert(T in self.tanks)
        x,y = pos
        T.move(x, y)
            
            
class Country:
    
    def __init__(self, color="red"):
        self.color = color
        self.tanks = []
    
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
        self.general = None
        
        # finally, add tanky to Country's army
        country.add_tank(self)
        
    def __str__(self):
        return f"Tank {self.name}, ({self.x},{self.y})"
    
    def _move(self, x, y):
        self.x = x
        self.y = y
        
    def move(self, x, y):
        self._move(x,y)
        self.patch.remove(self) # remove self from old patch
        self.patch = self.map.map[y-1][x-1] # change reference patch
        self.patch.append(self) # add self to that patch
        
    
    
class Patch:
    
    def __init__(self, y, x, map_):
        self.x = x
        self.y = y
        self.residents = []
        self.map = map_
        
    def __str__(self):
        return f"Patch ({self.x}, {self.y}), [{len(self.residents)}]"
    
    def append(self, T):
        self.residents.append(T) # add tank to patch
        
        # see if enemy tanks are in the same patch
        # if so, kill new or old one with 50% probabilty
        for tank in self.residents:
            if tank.country != T.country:
                tank_to_kill = random.choice([tank, T])
                if tank_to_kill.general is not None:
                    tank_to_kill.general.tanks.remove(tank_to_kill)
                    tank_to_kill.general = None
                tank_to_kill.map.tanks.remove(tank_to_kill)
                tank_to_kill.map = None
                self.remove(tank_to_kill)
                tank_to_kill.patch = None
                tank_to_kill._move(None, None)
                
                
                    
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
        self.map = [[Patch(x, y, self) for y in range(1, size+1)] for x in range(1,size+1)]
        self.tanks = []
    
    def __str__(self):
        s = ""
        for row in self.map:
            for col in row:
                s += f"{col}\t"
            s += "\n"
        
        return s
    
    def add_tank(self, T, x=1, y=1):
        self.map[y-1][x-1].append(T) # this appends a tank to a patch of the map
        self.tanks.append(T)
            
    def to_array(self):
        return np.array([[len(patch.residents) for patch in row] for row in self.map])

    def plot(self, *, k=3):
        fig, ax = plt.subplots(figsize=(12,8)) 

        for tank in self.tanks:
            if tank.country.color == "blue":
                tank_im = im_blue
            else:
                tank_im = im_red
                
            ax.imshow(tank_im, aspect='auto',
                          extent=(tank.x+0.5, tank.x-0.5, tank.y-0.5, tank.y+0.5),
                          zorder=2)
            attack_range = plt.Circle((tank.x, tank.y), 2,
                                      color=tank.country.color, fill=False)
            ax.add_artist(attack_range)
            
            line_of_sight = plt.Circle((tank.x, tank.y), 4,
                                       color=tank.country.color, fill=False, alpha=0.5)
            ax.add_artist(line_of_sight)

        for row in self.map:
            for p in row:
                if len(p.residents)>=1:
                    ax.text(p.x+0.3, p.y+0.3, f'{len(p.residents)}',)

        ax.imshow(np.zeros((self.size, self.size)), cmap="gray_r")
        
        
        ## Plot area of influence
        if len(self.tanks)>=1:
            coords = np.array([(t.x, t.y) for t in self.tanks])
            countries = np.array([t.country.color for t in self.tanks])

            # K=3 nearest neighbor
            distances = np.array([distance((x,y), (coords[:,0], coords[:,1])).argsort()[:k]
                   for x,y in zip(xr, yr)])
            if len(self.tanks)>2:
                # https://stackoverflow.com/a/6252494/6655150
                col = np.array([mode(countries[d]).mode[0] for d in distances])
            else:
                col = np.array([countries[d][0] for d in distances])
            
            col = np.array([1 if v=="blue" else 0 for v in col])

            ax.pcolormesh(xx, yy, col.reshape((self.size+1, self.size+1)),
                          cmap=cmap_light, vmin=0, vmax=1.)
        
        
        ax.set_xlim(1, self.size)
        ax.set_xticks(np.arange(1, self.size+1))
        ax.set_ylim(1, self.size)
        ax.set_yticks(np.arange(1, self.size+1))


        plt.show()

if __name__ == '__main__':
    n = 25
    m = Map(n)

    xx, yy = np.meshgrid(list(range(0,n+1)), list(range(0,n+1)))
    xr, yr = xx.ravel(), yy.ravel()

    red = Country("red")
    blue = Country("blue")

    Rommel = General("Rommel", red, map_=m, pos=(2,2))
    Montgomery = General("Montgomery", blue, map_=m, pos=(12,12))

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

    if t2.patch is not None:
        t2.move(7,7)
    else:
        t.move(7,7)
    m.plot()

    Rommel.purchase_tanks(n=5)
    Montgomery.purchase_tanks(n=3)
    m.plot()

    Rommel.order_tank(Rommel.tanks[0], (3,3))
    m.plot()

    instructions = {
        Rommel : [["order_tank", {'T': Rommel.tanks[0], 'pos': (5,8)}],
                  ["order_tank", {'T': Rommel.tanks[1], 'pos': (6,9)}]
                 ],
        Montgomery: [["order_tank", {'T': Montgomery.tanks[0], 'pos': (18,19)}],
                     ["order_tank", {'T': Montgomery.tanks[1], 'pos': (15,17)}]
                    ],
    }
    Turn(instructions=instructions)
    m.plot()


    instructions = {
        Rommel : [["order_tank", {'T': Rommel.tanks[0], 'pos': (8,11)}],
                  ["order_tank", {'T': Rommel.tanks[1], 'pos': (9,10)}]
                 ],
        Montgomery: [["order_tank", {'T': Montgomery.tanks[0], 'pos': (14,12)}],
                     ["order_tank", {'T': Montgomery.tanks[1], 'pos': (10,11)}]
                    ],
    }
    Turn(instructions=instructions)
    m.plot()


    instructions = {
    Montgomery: [["order_tank", {'T': Montgomery.tanks[2], 'pos': (7,18)}],
                ],
    }
    Turn(instructions=instructions)
    m.plot()


    m.plot(k=1) # who can occupy first

