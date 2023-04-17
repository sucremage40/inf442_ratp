import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset



class Nombre_Validation(dataset.Dataset):

    def __init__(self, _year, _semester):
        super().__init__(f'datasets/20{_year}S{_semester}_NB_FER.csv')

    def sum_by_day(self):
        nb_val = self.dataset['NB_VALD']
        nb_val = nb_val.replace(['Moins de 5'], self.moins_de_5)
        jour = self.dataset['JOUR']
        station = self.dataset['LIBELLE_ARRET']
        sum_day = [np.sum([int(nb_val[6*k + l]) for l in range(6)]) for k in range(len(nb_val) // 6)]
        return pd.DataFrame({self.dataset.columns[0]: [jour[6*k] for k in range(len(nb_val) // 6)], self.dataset.columns[4]: [station[6*k] for k in range(len(nb_val) // 6)], self.dataset.columns[7]: sum_day})

if __name__ == '__main__':
    S1_15 = Nombre_Validation(15, 1)
    print(S1_15.sum_by_day().head())
