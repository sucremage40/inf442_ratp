import pandas as pd
import matplotlib.pyplot as plt

ds15 = ["datasets/2015S1_NB_FER.csv", "datasets/2015S1_PROFIL_FER.csv", "datasets/2015S2_NB_FER.csv", "datasets/2015S2_PROFIL_FER.csv"]

class Dataset:

    def __init__(self, _dataset):
        self.dataset = import_dataset(_dataset)
    
    def column_names(self):
        return self.dataset.columns

def import_dataset(data):
    current_dataset = pd.read_csv(data)
    print(current_dataset.head())
    return current_dataset

S1_15 = Dataset("datasets/2015S1_NB_FER.csv")
S1_15.column_names()