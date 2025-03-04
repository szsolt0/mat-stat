#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib.animation as animation
from matplotlib.lines import Line2D

ANIMATE = False  # Ha False, akkor nincs animáció, csak a végeredmény jelenik meg

def process_data():
    # Teljes adathalmaz feldolgozása (statikus mód).
    global n, cross_cnt, pi_estimates, sample_sizes, xdata_blue, ydata_blue, xdata_red, ydata_red

    for x0, y0, x1, y1, crosses_grid_line in matchsticks:
        n += 1
        if crosses_grid_line != 0:
            cross_cnt += 1
            xdata_red.extend([x0, x1, None])  # Piros: keresztezi a vonalat
            ydata_red.extend([y0, y1, None])
        else:
            xdata_blue.extend([x0, x1, None])
            ydata_blue.extend([y0, y1, None])

        # Pi becslés frissítése
        if cross_cnt > 0:
            pi_estimate = n / cross_cnt
            pi_estimates.append(pi_estimate)
            sample_sizes.append(n)

def animate(i):
    """Animált verzió - frissíti az ábrákat lépésenként."""
    global n, cross_cnt, pi_estimates, sample_sizes, text_info

    idx = frames[i]  # Az aktuális frame indexe
    x0, y0, x1, y1, crosses_grid_line = matchsticks[idx]

    n += 1
    if crosses_grid_line != 0:
        cross_cnt += 1
        xdata_red.extend([x0, x1, None])
        ydata_red.extend([y0, y1, None])
    else:
        xdata_blue.extend([x0, x1, None])
        ydata_blue.extend([y0, y1, None])

    # Frissítjük a vonalakat
    blue_lines.set_xdata(xdata_blue)
    blue_lines.set_ydata(ydata_blue)
    red_lines.set_xdata(xdata_red)
    red_lines.set_ydata(ydata_red)

    # Pi becslés frissítése
    pi_estimate = np.nan
    error = np.nan
    if cross_cnt > 0:
        pi_estimate = n / cross_cnt
        pi_estimates.append(pi_estimate)
        sample_sizes.append(n)
        error = abs(np.pi - pi_estimate)

    # Fejléc frissítése
    text_info.set_text(f"N = {n}, Becsült π = {pi_estimate:.6f}, Hiba = {error:.6f}")

    update_plots()

def update_plots():
    # Frissíti a középső és jobb oldali ábrákat.
    axs[1].clear()
    axs[1].plot(sample_sizes, pi_estimates, label="Becsült π", color="blue")
    axs[1].axhline(np.pi, color='red', linestyle='dashed', linewidth=2, label="Valódi π érték")
    axs[1].set_xlabel("Mintaszám (N)")
    axs[1].set_ylabel("Becsült π érték")
    axs[1].set_title("π becslésének konvergenciája")
    axs[1].legend()
    axs[1].grid(True)

    axs[2].clear()
    axs[2].hist(pi_estimates, bins=20, density=True, color='purple', alpha=0.6, label="Becsült π eloszlás")
    axs[2].axvline(np.pi, color='red', linestyle='dashed', linewidth=2, label="Valódi π érték")
    axs[2].set_xlabel("Becsült π értékek")
    axs[2].set_ylabel("Relatív gyakoriság")
    axs[2].set_title("Becsült π értékek eloszlása")
    axs[2].legend()
    axs[2].grid(True)

def read_lines_from_stdin():
    """Bemeneti adat beolvasása."""
    matchsticks = []
    try:
        for line in sys.stdin:
            x0, y0, x1, y1, is_good = map(float, line.split())
            matchsticks.append((x0, y0, x1, y1, is_good))
    except:
        pass
    return matchsticks

if __name__ == "__main__":
    matchsticks = read_lines_from_stdin()

    # Globális változók
    n = 0
    cross_cnt = 0
    pi_estimates = []
    sample_sizes = []
    xdata_blue, ydata_blue = [], []
    xdata_red, ydata_red = [], []

    # Három ábra létrehozása
    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].set_xlim(0, 8)
    axs[0].set_ylim(0, 8)
    axs[0].set_title("Gyufa szimuláció")
    axs[0].grid(True)

    # Előre definiált vonalak
    blue_lines, = axs[0].plot([], [], 'b-', label="Nem metsző gyufák")
    red_lines, = axs[0].plot([], [], 'r-', label="Metsző gyufák")
    axs[0].legend()

    # Fejléc inicializálása
    text_info = fig.suptitle("N = 0, Becsült π = N/A, Hiba = N/A", fontsize=14)

    if ANIMATE:
        # Animáció gyorsítása
        frames = np.linspace(0, len(matchsticks) - 1, len(matchsticks), dtype=int)
        ani = animation.FuncAnimation(fig, animate, frames=len(frames), interval=1, repeat=False, save_count=500)
    else:
        process_data()  # Ha nem animálunk, azonnal feldolgozzuk az adatokat
        blue_lines.set_xdata(xdata_blue)  # Statikus ábrán is legyenek tűk
        blue_lines.set_ydata(ydata_blue)
        red_lines.set_xdata(xdata_red)
        red_lines.set_ydata(ydata_red)
        update_plots()  # Egyből kirajzoljuk a végeredményt
        text_info.set_text(f"N = {n}, Becsült π = {pi_estimates[-1]:.6f}, Hiba = {abs(np.pi - pi_estimates[-1]):.6f}")

    plt.tight_layout()
    plt.show()
