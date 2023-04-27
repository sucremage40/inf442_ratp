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

    def __init__(self, _dataset_path, _extension):
        self.dataset_path = _dataset_path + "." + _extension
        self.extension = _extension
        self.dataset = self.import_dataset()


    def import_dataset(self):
        if self.extension == 'csv':
            current_dataset = pd.read_csv(self.dataset_path, sep=";", low_memory=False) #for 2015
        elif self.extension == 'txt':
            current_dataset = pd.read_csv(self.dataset_path, sep="\t", lineterminator="\r", low_memory=False) #for 2016 and later
        else: #consider csv as the norm, open to json in future if needed
            current_dataset = pd.read_csv(self.dataset_path, sep=";", low_memory=False)
        return current_dataset