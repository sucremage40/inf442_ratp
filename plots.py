import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from calendar import monthrange
import profil
import nombre_validation

def affluence_horaire(): #remember problem for nbr days in specific month
    years = np.arange(15,22,1)
    months = np.arange(1,13,1)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.25)


    return