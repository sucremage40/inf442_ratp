import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset


class Profil(dataset.Dataset):

    def __init__(self, _year, _semester):
        extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
        super().__init__(f'datasets/20{_year}S{_semester}_PROFIL_FER', extension.get(_year)) #'txt' for 16 and +, 'csv' for 15
        self.dataset = self.dataset[['TRNC_HORR_60', 'CODE_STIF_ARRET', 'CAT_JOUR', 'pourc_validations']]
    
if __name__ == '__main__':
    S1_15 = Profil(16, 1)
    print(S1_15.dataset.head())