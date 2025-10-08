#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal.windows
from scipy.fft import rfft, rfftfreq
from scipy.signal import welch#, hanning

# Path to *.hist files
file1 = r"/home/thk/openfoam_opencfs_coupling/openCFS/history/propagation-acouIntensity-element-25-mic2e.hist"
file2 = r"/home/thk/openfoam_opencfs_coupling/openCFS/history/propagation-acouIntensity-element-7125-mic1e.hist"

rho = 1.204
# c = 343.5

p0 = 20e-6  # reference pressure in Pa

flag_savePlots = False

# - Read File 1 ----------------------------------------------------------------------------------

fobj = open(file1, "r")
cont = fobj.read()
fobj.close()
txt = cont.split("\n")
t1 = []
y1 = []

for i in range(len(txt) - 4):
    line = txt[i + 3].split("  ")
    t1.append(float(line[0]))
    yvalue = float(line[1])
    yvalue = yvalue * rho
    y1.append(yvalue)

# - Read File 2 -----------------------------------------------------------------------------------

fobj = open(file2, "r")
cont = fobj.read()
fobj.close()
txt = cont.split("\n")
t2 = []
y2 = []

for i in range(len(txt) - 4):
    line = txt[i + 3].split("  ")
    t2.append(float(line[0]))
    yvalue = float(line[1])
    yvalue = yvalue * rho
    y2.append(yvalue)

# - Plot time series ----------------------------------------------------------------------------------

plt.plot(t1, y1)
plt.plot(t2, y2)
plt.grid()
# plt.title("mic1")
plt.ylabel("$p^\mathrm{a}$ in Pa")
plt.xlabel("time in s")
plt.legend(('Mic 1', 'Mic 2'))
plt.tight_layout()
if flag_savePlots:
    picname = "mic_data.png"
    plt.savefig(picname, dpi=100)

plt.show()

# - Cut data ----------------------------------------------------------------------------------
startStep = 0

y1 = np.array(y1)
y2 = np.array(y2)

y1 = y1[startStep:]
y2 = y2[startStep:]

# - Calculate power spectral density ----------------------------------------------------------------------------------

fs1 = 1.0 / (t1[1] - t1[0])
fs2 = 1.0 / (t2[1] - t2[0])

nblock = 128
overlap = 32
win = scipy.signal.windows.hann(nblock, True)

f1, Pxxf1 = welch(y1, fs1, window=win, noverlap=overlap, nfft=nblock, return_onesided=True, detrend=False)
f2, Pxxf2 = welch(y2, fs2, window=win, noverlap=overlap, nfft=nblock, return_onesided=True, detrend=False)

# - Plot SPL ----------------------------------------------------------------------------------

ASD1 = np.sqrt(Pxxf1)
ASD2 = np.sqrt(Pxxf2)

# Define the reference pressure in Pascals
pref = 20e-6

# Calculate the frequency resolution
delta_f1 = f1[1] - f1[0]  # or fs1 / nblock
delta_f2 = f2[1] - f2[0]  # or fs2 / nblock

# Calculate SPL

SPL1 = 10 * np.log10(Pxxf1 / (pref**2)) + 10 * np.log10(delta_f1)
SPL2 = 10 * np.log10(Pxxf2 / (pref**2)) + 10 * np.log10(delta_f2)

plt.plot(f1, SPL1, '-')
plt.plot(f2, SPL2, '-')

plt.grid()

plt.ylabel("Sound pressure level in dB")
plt.xlabel("frequency in Hz")
plt.legend(('Mic 1', 'Mic 2'))
plt.tight_layout()

if flag_savePlots:
    picname = "mic_SPL.png"
    plt.savefig(picname, dpi=100)

plt.show()
