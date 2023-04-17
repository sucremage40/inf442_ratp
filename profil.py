import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset


class Profil(dataset.Dataset):

    def __init__(self, _year, _semester):
        super().__init__(f'datasets/20{_year}S{_semester}_PROFIL_FER.csv')

    def reorg_data(self):
        pourc_val = self.dataset['pourc_validations']
        station = self.dataset['LIBELLE_ARRET']
        reorg = { self.dataset.columns[6]: [k%24 for k in range(len(pourc_val))], self.dataset.columns[4]: [station[k] for k in range(len(pourc_val))], self.dataset.columns[7]: pourc_val}
        return pd.DataFrame(data=reorg)
    
if __name__ == '__main__':
    S1_15 = Profil(15, 1)
    print(S1_15.reorg_data().head())