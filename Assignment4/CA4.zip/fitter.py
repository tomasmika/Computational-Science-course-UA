# Name: Tomas Bosschieter en Sven de Ronde
# UvAnetID: 12195073 en 12409308
# Description: This program runs a number of models with different values of p0
# How to run:  python3 fitter.py <lower bound> <upper bound> <DATA_POINTS> <N>

from ca import *
import numpy as np
import sys

def get_burned_percentage(sim, p0):
    sim.wind_speed = 0
    sim.reset()
    sim.p_0 = p0

    while not sim.step():
        continue

    vegetation = 0
    burnt = 0

    for y in range(sim.height):
        for x in range(sim.width):
            if sim.config[y, x] != EMPTY_CELL:
                vegetation += 1
            if sim.config[y, x] == BURNT_VEGETATION:
                burnt += 1

    return burnt / vegetation * 100

def get_data(sim, points):
    return [get_data_at_dens(sim, point) for point in points]

def get_data_at_dens(sim, density):
    print(density, file=sys.stderr)
    return np.average([get_burned_percentage(sim, density) for _ in range(N)])

if __name__ == "__main__":
    try:
        lowest = float(sys.argv[1])
        largest = float(sys.argv[2])
        DATA_POINTS = int(sys.argv[3])
        N = int(sys.argv[4])
    except Exception:
        print("Give two floats: a lower and an upper bound for the test.\n" \
              "And two integers: the amount of datapoints, and the\n" \
              "amount of iterations per datapoint.")
        exit(1)

    sim = CASim()
    points = [lowest + (largest - lowest)*(i/(DATA_POINTS-1))
              for i in range(DATA_POINTS)]
    data = np.array(get_data(sim, points))
    for p, d in zip(points, data):
        print(p, d)
