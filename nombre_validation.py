import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset
import datetime


def periode_annee(year, semester):
    dataset = pd.read_csv(f'datasets_reorg/nombre_validation_20{year}S{semester}.csv', sep=';')

    dataset['saison_influence'] = dataset.apply(lambda row: coeff_periode(row, year), axis=1)
    dataset.to_csv(f'datasets_reorg/nombre_validation_20{year}S{semester}_periode.csv', sep=';')
    print(year, semester)

def coeff_periode(row, year):
    coeff = 0
    year_start = datetime.datetime(2000 + year, 1, 1)
    year_end = datetime.datetime(2001 + year, 1, 1)
    days_in_year = (year_end - year_start).days
    jour = is_date(str(row['JOUR']))
    if jour != None:
        coeff = (jour - year_start).days / days_in_year
        a = (datetime.datetime(2000+year, 4, 20) - year_start).days / days_in_year
        b = np.pi * 2
        coeff = np.sin((coeff - a)*b)
    return coeff

def is_date(string, format="%d/%m/%Y"):
    try:
        jour = datetime.datetime.strptime(string, format)
        return jour
    except ValueError:
        return None

class Nombre_Validation(dataset.Dataset):

    def __init__(self, _year, _semester):
        extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
        super().__init__(f'datasets/20{_year}S{_semester}_NB_FER', extension.get(_year)) #'txt' for 16 and +, 'csv' for 15
        self.dataset['NB_VALD'] = self.dataset['NB_VALD'].replace('Moins de 5', '0') #change to value to put in 'Moins de 5'
        self.dataset = self.dataset.fillna(0)

        if extension.get(_year) == "txt": #uniquement pour 2016 et après
            self.dataset['JOUR'] = self.dataset['JOUR'].str.replace('\n', '')
            print(self.dataset.head())

        self.dataset['NB_VALD'] = self.dataset['NB_VALD'].astype(int)
        self.dataset = self.dataset.groupby(['JOUR', 'ID_REFA_LDA', 'CODE_STIF_ARRET'])['NB_VALD'].agg(['sum','count'])
        self.dataset = self.dataset.rename(columns={'sum': 'NB_VALD'})
        self.dataset.to_csv(f'datasets_reorg/nombre_validation_20{_year}S{_semester}.csv', sep=';')

 
if __name__ == '__main__':
    print("Nombre validation")
    S1_15 = Nombre_Validation(15, 1)
    print(S1_15.dataset.head())
    # periode_annee(16, 1)
