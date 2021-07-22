# Name: Tomas Bosschieter en Sven de Ronde
# UvAnetID: 12195073 en 12409308
# Description: This file contains the CA model, and if executed
#              it will start a GUI with which you can use the model
# How to run:  python3 ca.py

import math
import numpy as np
import random
from random import sample

from pyics import Model

STATE_COUNT = 5
EMPTY_CELL = 0
VEGETATION = 1
DRY_VEGETATION = 2
BURNING_VEGETATION = 3
BURNT_VEGETATION = 4

C1 = 0.045
C2 = 0.131

COLORLIST = np.array([
    'lightgray',
    'green',
    'yellow',
    'red',
    'black'
])

RANGE = 1

# Returns True with chance p.
def decision(p):
    return random.random() < p

def density_setter(val):
    return max(0, min(1, val))

def p_0_setter(val):
    return max(0, val)

def p_veg_setter(val):
    return max(-1, val)

def p_den_setter(val):
    return max(-1, val)

def p_fire_done_setter(val):
    return max(0, min(1, val))

def initial_wind_dir_setter(val):
    return val % 360

def wind_dir_change_setter(val):
    return max(0, min(360, val))

def initial_wind_speed_setter(val):
    return max(0, val)

def wind_speed_change_setter(val):
    return max(0, val)

def dim_setter(val):
    return max(1, val)

class CASim(Model):
    def __init__(self):
        Model.__init__(self)

        self.t = 0
        self.k = STATE_COUNT
        self.r = RANGE
        self.p_burn = 0.0
        self.wind_dir = 0.0
        self.wind_speed = 1.0
        self.fire_going_on = False
        self.config = None
        self.make_param('density', 1.0, setter=density_setter)
        self.make_param('p_0', 0.225, setter=p_0_setter)
        self.make_param('p_veg', 0.4, setter=p_veg_setter)
        self.make_param('p_den', 0.0, setter=p_den_setter)
        self.make_param('initial_wind_dir', 0.0, setter=initial_wind_dir_setter)
        self.make_param('wind_dir_change', 0.0, setter=wind_dir_change_setter)
        self.make_param('initial_wind_speed', 0.0, setter=initial_wind_speed_setter)
        self.make_param('wind_speed_change', 0.0, setter=wind_speed_change_setter)
        self.make_param('random_fire', False)
        self.make_param('fire_density', 0.0, setter=density_setter)
        self.make_param('width', 50, setter=dim_setter)
        self.make_param('height', 50, setter=dim_setter)

    def p_wind(self, dx, dy):
        """
        This method calculates p_w, which is the effect of the wind.
        """
        theta = math.atan2(dx, dy) + math.radians(self.wind_dir)
        cos = (math.cos(theta) - 1)
        return math.exp(self.wind_speed * (C1 + C2 * cos))

    def sim_fire(self, x, y, new_config):
        """
        This method takes a look around all the cells of a fire,
        and decides which become fires or dry.
        """
        xrange = range(max(x - self.r, 0), min(x + self.r + 1, self.width))
        yrange = range(max(y - self.r, 0), min(y + self.r + 1, self.height))

        for i in yrange:
            for j in xrange:
                p = self.p_burn * self.p_wind(x - i, y - j)

                if (i,j) != (y, x) and self.config[i, j] == VEGETATION:
                    if decision(p):
                        new_config[i,j] = BURNING_VEGETATION
                    elif decision(p):
                        new_config[i,j] = DRY_VEGETATION
                elif (i,j) != (y, x) and self.config[i, j] == DRY_VEGETATION:
                    if decision((1 + p) / 2):
                        new_config[i,j] = BURNING_VEGETATION

        # It was a fire, so now it is burnt.
        new_config[y, x] = BURNT_VEGETATION

    def setup_initial_grid(self):
        # If you want to randomly set a forest on fire, you can do that too!
        if self.random_fire:
            fdd = (1 - self.fire_density) * self.density
            l = np.random.choice([EMPTY_CELL, VEGETATION, BURNING_VEGETATION],
                                size=(self.height, self.width),
                                p=[1 - self.fire_density - fdd,
                                   fdd, self.fire_density])
        # This creates a random forest, where a single cell is on fire.
        else:
            l = np.random.choice([EMPTY_CELL, VEGETATION],
                                size=(self.height, self.width),
                                p=[(1 - self.density), self.density])
            l[self.height // 2, self.width // 2] = BURNING_VEGETATION

        self.fire_going_on = True
        return l

    def reset(self):
        self.t = 0

        # Reset the grid
        self.config = self.setup_initial_grid()

        # Reset the p_burn value.
        self.p_burn = self.p_0 * (1 + self.p_den) * (1 + self.p_veg)

        # Reset the wind direction and speed
        self.wind_dir = self.initial_wind_dir
        self.wind_speed = self.initial_wind_speed

    def draw(self):
        """Draws the current state of the grid."""

        import matplotlib
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib.colors import ListedColormap, LinearSegmentedColormap

        plt.cla()
        if not plt.gca().yaxis_inverted():
            plt.gca().invert_yaxis()

        newcolormap = ListedColormap(COLORLIST)

        plt.imshow(self.config, interpolation='none', vmin=0, vmax=self.k - 1,
                cmap=newcolormap)
        plt.axis('image')
        plt.title('t = %d' % self.t)

    def step(self):
        """
        This function calculates the next iteration of the CA and
        the new values of the wind direction and speed.
        As long as there is a cell with the state BURNING_VEGETATION,
        the simulation will continue, so when there are no more cells like
        that, the step function will return True, and the sim will be ended.
        """
        if not self.fire_going_on:
            return True
        self.t += 1

        new_config = np.copy(self.config)
        on_fire = False


        # Iterate over all fire cells in the new grid,
        # and calculate their, and their neighbours' state.
        firelist = np.argwhere(new_config == BURNING_VEGETATION)
        if len(firelist):
            on_fire = True

        for y, x in firelist:
            self.sim_fire(x, y, new_config)

        self.fire_going_on = on_fire
        self.config = new_config

        # Calculate new wind speed, by adding a random value between
        # + and -self.wind_dir_change
        dir_diff = random.choice([-1,1]) * random.uniform(0, self.wind_dir_change)
        self.wind_dir = (self.wind_dir + dir_diff) % 360

        # Calculate new wind speed, by adding a random value between
        # + and -self.wind_speed_change
        speed_diff = random.uniform(-self.wind_speed_change, self.wind_speed_change)
        self.wind_speed = max(self.wind_speed + speed_diff, 0)

if __name__ == '__main__':
    sim = CASim()
    from pyics import GUI
    cx = GUI(sim)
    cx.start()
