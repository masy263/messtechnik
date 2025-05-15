# Python SetUp

import numpy as np
import matplotlib.pyplot as plt
import sympy as sym

from sympy import *
from IPython.display import display, Math, Latex
from sympy.interactive import printing

printing.init_printing(use_latex='mathjax')
# plt.style.use('dark_background')
plt.rcParams['figure.figsize'] = [10, 10]

def fct_gain2(x1, y1, x2, y2, x3, y3):
  return (y3 - (y2 - y1) / (x2 - x1) * (x3 - x1) - y1) / (x3**2 - x1**2 + (x1**2 - x2**2) / (x2 - x1) * (x3 - x1))

def fct_gain1(x1, y1, x2, y2, x3, y3):
   return (y2 - y1) / (x2 - x1) + fct_gain2(x1, y1, x2, y2, x3, y3) * (x1**2 - x2**2) / (x2 - x1)

def fct_offset(x1, y1, x2, y2, x3, y3):
   return y1 - fct_gain2(x1, y1, x2, y2, x3, y3) * x1**2 - fct_gain1(x1, y1, x2, y2, x3, y3) * x1

def fct_k(K, y0, x):
  return K * x + y0

# Kennlinien

x  = np.array([-3,3])

fig, ax = plt.subplots(2,2)
ax[0][0].plot(x, fct_k(1, 0, x),   color="blue",   label="$K = 1, y_0 = 0$")
ax[0][0].plot(x, fct_k(2, 0, x),   color="red",    label="$K = 2, y_0 = 0,5$")
ax[0][0].plot(x, fct_k(1, 0.5, x), color="green",  label="$K = 1, y_0 = 0$")
ax[0][0].plot(x, fct_k(2, 0.5, x), color="orange", label="$K = 2, y_0 = 0,5$")
ax[0][0].set_title("Kennlinien im Vergleich")
ax[0][0].set_xlabel("$x$")
ax[0][0].set_ylabel("$y$")
ax[0][0].set_ylim(bottom=-3, top=3)
ax[0][0].set_xlim(left=-3, right=3)
ax[0][0].legend(loc='lower right', shadow=True)
ax[0][0].grid()

# Eingangssignal

t = np.arange(0, 1.01, 0.01)
x = np.sin(2 * np.pi * t)

ax[1][0].plot(x, t, color="black", label="Eingangssignal $x$")
ax[1][0].set_xlabel("$x$")
ax[1][0].set_ylabel("$t$")
ax[1][0].set_title("Eingangssignal")
ax[1][0].set_xlim(left=-3, right=3)
ax[1][0].grid()

# Ausgangssignale

ax[0][1].plot(t, fct_k(1, 0,   x), color="blue",   label="$K = 1, y_0 = 0$")
ax[0][1].plot(t, fct_k(2, 0,   x), color="red",    label="$K = 2, y_0 = 0,5$")
ax[0][1].plot(t, fct_k(1, 0.5, x), color="green",  label="$K = 1, y_0 = 0$")
ax[0][1].plot(t, fct_k(2, 0.5, x), color="orange", label="$K = 2, y_0 = 0,5$")
ax[0][1].set_title("Ausgangssignale im Vergleich")
ax[0][1].grid()
ax[0][1].set_ylim(bottom=-3, top=3)
ax[0][1].set_xlabel("$t$")
ax[0][1].set_ylabel("$y$")

ax[1][1].axis('off')

x1 = -1; x2 = 0;    x3 = 1
y1 = -1; y2 = 0.45; y3 = 1
a = fct_gain2(x1, y1, x2, y2, x3, y3)
b = fct_gain1(x1, y1, x2, y2, x3, y3)
c = fct_offset(x1, y1, x2, y2, x3, y3)

def fct_K1(x): # quadratisch interpolierter NTC10K im Bereich 15...25 Grad Celsius
  return a * x**2 + b * x + c

def fct_K2(x): # linearisierte Kennlinie im Arbeitspunkt 20 Grad Celsius
  x0 = 0.5
  return (2 * a * x0 + b) * (x - x0) + fct_K1(x0)

## Kennlinie

x_min = 0
x_max = 1
dx    = 1E-2
x = np.arange(x_min, x_max + dx, dx)

fig, ax = plt.subplots(2,2)
ax[0][0].plot(x, fct_K1(x), color="blue", label="quadratische Kennlinie")
ax[0][0].plot(x, fct_K2(x), color="red", label="lineare Kennlinie")
ax[0][0].set_title("Kennlinien im Vergleich")
ax[0][0].set_xlabel("Messgroesse x")
ax[0][0].set_ylabel("Messwert y")
ax[0][0].set_xlim(left=x_min, right=x_max)
ax[0][0].set_ylim(bottom=fct_K1(x_min), top=fct_K2(x_max))
ax[0][0].legend(loc='upper left', shadow=True)
ax[0][0].grid()

# Eingangssignal

t = np.arange(0, 1.01, 0.01)
x1 = np.sin(7 * np.pi * t) * 0.25 + 0.5
x2 = np.sin(2 * np.pi * t) * 0.5  + 0.5

ax[1][0].plot(x1, t, color="black")
ax[1][0].plot(x2, t, '--', color="black")
ax[1][0].set_xlabel("$x$")
ax[1][0].set_ylabel("$t$")
ax[1][0].set_title("Eingangssignal")
ax[1][0].set_xlim(left=x_min, right=x_max)
ax[1][0].grid()

# Ausgangssignal

ax[0][1].plot(t, fct_K1(x1), color="blue")
ax[0][1].plot(t, fct_K1(x2), '--', color="blue")
ax[0][1].plot(t, fct_K2(x1), color="red")
ax[0][1].plot(t, fct_K2(x2), '--', color="red")
ax[0][1].set_xlabel("$x$")
ax[0][1].set_ylabel("$t$")
ax[0][1].set_title("Ausgangssignal")
ax[0][1].set_xlim(left=0, right=1)
ax[0][1].set_ylim(bottom=fct_K1(x_min), top=fct_K2(x_max))
ax[0][1].grid()

# Fehler

ax[1][1].plot(t, (fct_K2(x1) / fct_K1(x1) - 1) * 100, color="blue")
ax[1][1].plot(t, (fct_K2(x2) / fct_K1(x2) - 1) * 100, color="red")
ax[1][1].set_ylabel("$\Delta y_{Rel} [\%]$")
ax[1][1].set_xlabel("$t$")
ax[1][1].set_title("Relative Abweichung")
ax[1][1].set_xlim(left=0, right=1)
ax[1][1].grid()

plt.show()
