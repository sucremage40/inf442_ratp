import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataset import Dataset

years = [15, 16, 17, 18, 19, 20, 21]
semesters = [1, 2]
extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"}

def nom_station():
    data = pd.DataFrame()
    for y in years:
        for s in semesters:
            temp_dataset = Dataset(f'datasets/20{y}S{s}_NB_FER', extension.get(y)).dataset
            data = pd.concat([data, temp_dataset])

    # code_unique = data['ID_REFA_LDA'].unique()

    data = data[['ID_REFA_LDA', 'CODE_STIF_ARRET', 'LIBELLE_ARRET']]
    data = data[pd.to_numeric(data['ID_REFA_LDA'], errors='coerce').notnull()]
    # data = data[data['ID_REFA_LDA'].apply(lambda x: isinstance(x, int))]
    data['ID_REFA_LDA'] = data['ID_REFA_LDA'].astype(int)
    data = data.drop_duplicates(subset='ID_REFA_LDA', keep='first')
    data = data.drop_duplicates(subset='CODE_STIF_ARRET', keep='first')

    data.to_csv('datasets_reorg/equivalence_code_station_drop.csv', sep=';')
    print(data.shape)
    

if __name__ == '__main__':
    print('Main')
    nom_station()