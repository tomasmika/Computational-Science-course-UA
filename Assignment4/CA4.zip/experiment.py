# Name: Tomas Bosschieter en Sven de Ronde
# UvAnetID: 12195073 en 12409308
# Description: This program runs the experiment and outputs it into data
#              files.
# How to run:  python3 experiment.py <code>
#               - code : 0 runs the density experiment, 1 the p_den, 2 the p_veg
#                        both if ommitted

from ca import *
import numpy as np
import sys

DATA_POINTS = 40
DATA_POINTS_pden = 48
N = 25

def get_burned_percentage(sim, grow_density=-1, p_den=-1, p_veg=-1, size=None):
    if size:
        sim.height, sim.width = size

    if grow_density != -1:
        sim.density = grow_density
    elif p_veg != -1:
        sim.p_veg = p_veg
    else:
        sim.p_den = p_den

    sim.wind_speed = 0
    sim.reset()

    while not sim.step():
        continue

    # We start at -1, since we don't count the cell where the fire starts,
    # because that one cell might already be over 10% of all the vegetation.
    # And it won't have a significant impact on the higher densities, since
    # 1 cell compared to thousands is nothing.
    vegetation = -1
    burnt = -1

    for y in range(sim.height):
        for x in range(sim.width):
            if sim.config[y, x] != EMPTY_CELL:
                vegetation += 1
            if sim.config[y, x] == BURNT_VEGETATION:
                burnt += 1

    if vegetation == 0:
        return 0

    return burnt / vegetation * 100

def get_density_data(sim):
    return [get_data_at_dens(sim, k/DATA_POINTS) for k in range(DATA_POINTS + 1)]

def get_data_at_dens(sim, density):
    print(density)
    return [get_burned_percentage(sim, grow_density=density) for _ in range(N)]

def get_p_den_data(sim):
    return [get_data_at_pden(sim, -.7 + 1.2*k/DATA_POINTS_pden)
            for k in range(DATA_POINTS_pden + 1)]

def get_data_at_pden(sim, pden):
    print(pden)
    return [get_burned_percentage(sim, p_den=pden) for _ in range(N)]

def get_p_veg_data(sim):
    return [get_data_at_pveg(sim, -.6 + 1.2*k/DATA_POINTS_pden)
            for k in range(DATA_POINTS_pden + 1)]

def get_data_at_pveg(sim, pveg):
    print(pveg)
    return [get_burned_percentage(sim, p_veg=pveg) for _ in range(N)]

if __name__ == "__main__":
    code = -1
    try:
        if sys.argv[1]:
            code = int(sys.argv[1])
    except Exception:
        print("If you enter an argument, it has to be 0 or 1.")

    # code 0 means test this one
    if code == 0 or code == -1:
        sim = CASim()
        data = np.array(get_density_data(sim))
        np.savetxt('densitydata', data)

    # code 1 means test this one
    if code == 1 or code == -1:
        sim2 = CASim()
        data = np.array(get_p_den_data(sim2))
        np.savetxt('pdendata', data)

    # code 2 means test this one
    if code == 2 or code == -1:
        sim3 = CASim()
        data = np.array(get_p_veg_data(sim3))
        np.savetxt('pvegdata', data)

