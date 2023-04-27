import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset


dictionary = {}
trnc_horr_12 = {}

def create_dictionary():
    global dictionary
    global trnc_horr_12
    for h in range(24):
        dictionary[f'{h}H-{(h+1) % 24}H'] = round(np.sin(np.pi/6 * h - np.pi/2) + 1.2, 5)
        trnc_horr_12[f'{h}H-{(h+1) % 24}H'] = h



class Profil(dataset.Dataset):

    def __init__(self, _year, _semester):
        print(_year, _semester)
        global dictionary
        extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
        super().__init__(f'datasets/20{_year}S{_semester}_PROFIL_FER', extension.get(_year)) #'txt' for 16 and +, 'csv' for 15
        self.dataset = self.dataset[['TRNC_HORR_60', 'ID_REFA_LDA', 'CODE_STIF_ARRET', 'CAT_JOUR', 'pourc_validations']]
        self.dataset['TRNC_HORR_60'] = self.dataset['TRNC_HORR_60'].astype(str)
        self.dataset['heure_pointe'] = self.dataset.apply(lambda row: dictionary.get(row['TRNC_HORR_60'], 0.0), axis=1)
        self.dataset['TRNC_HORR_12'] = self.dataset.apply(lambda row: trnc_horr_12.get(row['TRNC_HORR_60'], 0.0), axis=1)
        self.dataset = self.dataset.loc[self.dataset['heure_pointe'] != 0]
        self.dataset = self.dataset.loc[self.dataset['TRNC_HORR_12'] != 0]
        
        self.dataset['pourc_validations'] = self.dataset['pourc_validations'].astype('str').str.replace(',', '.')
        self.dataset['pourc_validations'] = pd.to_numeric(self.dataset['pourc_validations'], errors='coerce')

        is_vac = []
        is_ouvrable = []
        is_dimanche = []
        for index, row in self.dataset.iterrows():
            if row['CAT_JOUR'] == 'JOHV':
                is_vac += [0]
                is_ouvrable += [1]
                is_dimanche += [0]
            elif row['CAT_JOUR'] == 'SAHV':
                is_vac += [0]
                is_ouvrable += [0]
                is_dimanche += [0]
            elif row['CAT_JOUR'] == 'JOVS':
                is_vac += [1]
                is_ouvrable += [1]
                is_dimanche += [0]
            elif row['CAT_JOUR'] == 'SAVS':
                is_vac += [1]
                is_ouvrable += [0]
                is_dimanche += [0]
            elif row['CAT_JOUR'] == 'DIJFP':
                is_vac += [0]
                is_ouvrable += [0]
                is_dimanche += [1]
            else:
                is_vac += [0]
                is_ouvrable += [0]
                is_dimanche += [0]
        self.dataset['is_vac'] = is_vac
        self.dataset['is_ouvrable'] = is_ouvrable
        self.dataset['is_dimanche'] = is_dimanche


    

    
if __name__ == '__main__':
    create_dictionary()
    S1_15 = Profil(15, 1)
    # print(S1_15.dataset)
    S1_15.dataset.to_csv('check_binary.csv', sep=';')

