import pandas as pd
import numpy as np
from calendar import monthrange
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Button
import profil
import nombre_validation
import plots

years = [17, 18, 19, 20, 21]

def import_all():
    for y in years:
        for s in range(1, 3, 1):
            nombre_validation.Nombre_Validation(y, s)

if __name__ == '__main__':
    print("lez go")
    for y  in years:
        for s in range(2):
            nombre_validation.Nombre_Validation(y, s + 1)
    