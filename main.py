import pandas as pd
import numpy as np
from calendar import monthrange
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Button
import profil
import nombre_validation
import plots
from type_jour import traitement_type_jours
from sklearn.linear_model import LinearRegression

years = [15, 16, 17, 18, 19, 20, 21]

def import_all():
    for y in years:
        for s in range(1, 3, 1):
            nombre_validation.periode_annee(y, s)


if __name__ == '__main__':
    print("lez go")
    import_all()
    # print(profil.Profil(15,1).dataset.head())
    

# Run import_all(), then periode_annee(), then val_cat_jour(), then add_heure_val_pourc()