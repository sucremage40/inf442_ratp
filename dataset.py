import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ds15 = ["datasets/2015S1_NB_FER.csv", "datasets/2015S1_PROFIL_FER.csv", "datasets/2015S2_NB_FER.csv", "datasets/2015S2_PROFIL_FER.csv"]
ds16 = ["datasets/2016S1_NB_FER.csv", "datasets/2016S1_PROFIL_FER.csv", "datasets/2016S2_NB_FER.csv", "datasets/2016S2_PROFIL_FER.csv"]
ds17 = ["datasets/2017S1_NB_FER.csv", "datasets/2017S1_PROFIL_FER.csv", "datasets/2017S2_NB_FER.csv", "datasets/2017S2_PROFIL_FER.csv"]
ds18 = ["datasets/2018S1_NB_FER.csv", "datasets/2018S1_PROFIL_FER.csv", "datasets/2018S2_NB_FER.csv", "datasets/2018S2_PROFIL_FER.csv"]
ds19 = ["datasets/2019S1_NB_FER.csv", "datasets/2019S1_PROFIL_FER.csv", "datasets/2019S2_NB_FER.csv", "datasets/2019S2_PROFIL_FER.csv"]
ds20 = ["datasets/2020S1_NB_FER.csv", "datasets/2020S1_PROFIL_FER.csv", "datasets/2020S2_NB_FER.csv", "datasets/2020S2_PROFIL_FER.csv"]
ds21 = ["datasets/2021S1_NB_FER.csv", "datasets/2021S1_PROFIL_FER.csv", "datasets/2021S2_NB_FER.csv", "datasets/2021S2_PROFIL_FER.csv"]

class Dataset:

    def __init__(self, _dataset):
        self.dataset = import_dataset(_dataset)
        self.moins_de_5 = '0' #valeur à mettre à la place de "Moins de 5" validations


def import_dataset(data):
    current_dataset = pd.read_csv(data, sep="\t", lineterminator="\r") #sep = ';' for 15, " " for 16 and +
    return current_dataset