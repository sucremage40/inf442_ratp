import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset


class Profil(dataset.Dataset):

    def __init__(self, _year, _semester):
        super().__init__(f'datasets/20{_year}S{_semester}_PROFIL_FER.csv')
        self.dataset = self.dataset[['TRNC_HORR_60', 'CODE_STIF_ARRET', 'CAT_JOUR', 'pourc_validations']]
    
if __name__ == '__main__':
    S1_15 = Profil(15, 1)
    print(S1_15.dataset.head())