import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import RangeSlider, Button
import profil
import nombre_validation
import plots


if __name__ == '__main__':
    print("Affluence en fonction de l'horaire")
    plots.affluence_horaire()