#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import rc

# rc('text', usetex=True)
from scipy.fft import rfft, rfftfreq
import scipy

plt.rc('font', family='serif')
rc('font', size=16.0)
rc('lines', linewidth=1.5)
rc('legend', fontsize='medium', numpoints=1)  # framealpha=1.0,
rc('svg', fonttype='none')

# - User Input ----------------------------------------------------------------------------------


data_path = "mics"  # Path to mics folder

ts = 1e-3  # Sample time in s
plt_freq = 77  # Frequency to plot in Hz

flag_savePlots = False

# - Read Mic data ----------------------------------------------------------------------------------

p = []
for i in range(1, 201):
    p.append(np.loadtxt(f'{data_path}/micArrayResults_2m_acouPotentialD1_CellCentroid-{i}', usecols=[3], delimiter=',', dtype=float, skiprows=1))

p = np.array(p)

# - Calculate FFT ----------------------------------------------------------------------------------

startStep = 0

yf = []

win = scipy.signal.windows.hann(p.shape[0] - startStep, True)

for i in range(p.shape[1]):
    y = p[startStep:, i] * win
    yf.append(abs(rfft(y)))

yf = np.array(yf)
xf = rfftfreq(p.shape[0] - startStep, ts)

# - Directivity plot ----------------------------------------------------------------------------------

index_plt = np.argmin(abs(xf - plt_freq))
yf_plt = yf[:, index_plt] / max(yf[:, index_plt])

theta = np.arange(0, 2 * np.pi, 2 * np.pi / p.shape[1])
ax = plt.subplot(111, projection='polar')
ax.plot(theta, yf_plt, label="Size 2m")

plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=10.0)

if flag_savePlots:
    plt.savefig("mic.pdf", bbox_inches='tight', transparent=True)

plt.show()
