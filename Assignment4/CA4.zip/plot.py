# Name: Tomas Bosschieter en Sven de Ronde
# UvAnetID: 12195073 en 12409308
# Description: This program makes the plots from the data made by experiment.py
# How to run:  python3 plot.py <code>
#               - code : 0 plots the density experiment, 1 the p_den, 2
#                        the p_veg, both if omitted
#
# IMPORATANT: It might be the case that one plot is behind the other plot.
#             To fix: just remove the first one to see the second.

import numpy as np
import sys

COLOR = 'orange'        # The color of the line in the errorbar plot
ECOLOR = 'b'            # The color of the error bars
LINEWIDTH = 2

def make_density_plot(data, N):
    import matplotlib.pyplot as plt

    average = np.average(data, axis=1)
    error = np.std(data, axis=1)

    fig, ax = plt.subplots()
    fig.suptitle("Percentage burned")
    markers, caps, bars = ax.errorbar([i / N for i in range(N + 1)], average,
                                      error, color=COLOR, ecolor=ECOLOR)
    [bar.set_alpha(0.5) for bar in bars]
    markers.set_linewidth(LINEWIDTH)

    plt.xlabel("density")
    plt.ylabel("percentage burned")
    plt.show()

def make_pden_plot(data, N):
    import matplotlib.pyplot as plt

    average = np.average(data, axis=1)
    error = np.std(data, axis=1)

    fig, ax = plt.subplots()
    fig.suptitle("Percentage burned")
    markers, caps, bars = ax.errorbar([1.2 * i / N - .7 for i in range(N + 1)],
                                      average, error, color=COLOR,
                                      ecolor=ECOLOR)
    [bar.set_alpha(0.5) for bar in bars]
    markers.set_linewidth(LINEWIDTH)

    plt.xlabel("p_den")
    plt.ylabel("percentage burned")
    plt.show()

def make_pveg_plot(data, N):
    import matplotlib.pyplot as plt

    average = np.average(data, axis=1)
    error = np.std(data, axis=1)

    fig, ax = plt.subplots()
    fig.suptitle("Percentage burned")
    markers, caps, bars = ax.errorbar([1.2 * i / N - .6 for i in range(N + 1)],
                                      average, error, color=COLOR,
                                      ecolor=ECOLOR)
    [bar.set_alpha(0.5) for bar in bars]
    markers.set_linewidth(LINEWIDTH)

    plt.xlabel("p_veg")
    plt.ylabel("percentage burned")
    plt.show()

if __name__ == "__main__":
    code = -1
    try:
        if sys.argv[1]:
            code = int(sys.argv[1])
    except Exception:
        print("If you enter an argument, it has to be 0 or 1.")

    # code 0 means plot this oneone
    if code == 0 or code == -1:
        densitydata = np.loadtxt('densitydata')
        N = len(densitydata) - 1
        make_density_plot(densitydata, N)

    # code 1 means plot this oneone
    if code == 1 or code == -1:
        pdendata = np.loadtxt('pdendata')
        N = len(pdendata) - 1
        make_pden_plot(pdendata, N)

    # code 2 means plot this oneone
    if code == 2 or code == -1:
        pvegdata = np.loadtxt('pvegdata')
        N = len(pvegdata) - 1
        make_pveg_plot(pvegdata, N)
