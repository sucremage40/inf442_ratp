import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dataset



class Nombre_Validation(dataset.Dataset):

    def __init__(self, _year, _semester):
        extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
        super().__init__(f'datasets/20{_year}S{_semester}_NB_FER', extension.get(_year)) #'txt' for 16 and +, 'csv' for 15
        self.dataset['NB_VALD'] = self.dataset['NB_VALD'].replace('Moins de 5', '0') #change to value to put in 'Moins de 5'
        self.dataset = self.dataset.fillna(0)

        if extension.get(_year) == "txt": #uniquement pour 2016 et après
            self.dataset['JOUR'] = self.dataset['JOUR'].str.replace('\n', '')
            print(self.dataset.head())

        
        jour = self.dataset['JOUR'].unique()
        station = self.dataset['CODE_STIF_ARRET'].unique()
        station_final_array = np.array([[s for s in station] for j in jour]).ravel()
        jour_final_array = np.array([[j for s in station] for j in jour]).ravel()
        sum_day = np.zeros((len(jour), len(station)))
        #Solution fonctionnelle mais très lente
        # nb_val = self.dataset['NB_VALD']
        # list_index_jour = []       
        # for j in jour:
        #     temp_jour = self.dataset.loc[(self.dataset['JOUR'] == j)]
        #     for s in station:
        #         temp_jour_station = temp_jour.loc[(self.dataset['CODE_STIF_ARRET'] == s)].index.values.tolist()
        #         sum_day += [np.sum([int(nb_val[int(id)]) for id in temp_jour_station])]
        #     print(j)
        # print(np.array(list_index_jour).shape)
        # print(list_index_jour[130])
        # sum_day = [np.sum([nb_val[int(id)] for id in list_ids]) for list_ids in list_index_jour]

        previous_day = 0
        previous_station = 0
        j, s = -1, -1
        for index, row in self.dataset.iterrows():
            current_day = row['JOUR']
            current_station = row['CODE_STIF_ARRET']
            if previous_station != current_station:
                for k in range(len(station)):
                    if station[k] == current_station: s = k
            if previous_day != current_day:
                for k in range(len(jour)):
                    if jour[k] == current_day: j = k
            
            sum_day[j][s] += int(row['NB_VALD'])
            previous_day = current_day
            previous_station = current_station
        sum_day = np.array(sum_day).ravel()

        self.dataset = pd.DataFrame({self.dataset.columns[0]: jour_final_array, self.dataset.columns[3]: station_final_array, self.dataset.columns[7]: sum_day})
        self.dataset.to_csv(f'datasets_reorg/nombre_validation_20{_year}S{_semester}.csv', sep=';')

 
if __name__ == '__main__':
    S1_15 = Nombre_Validation(16, 2)
    print(S1_15.dataset.head())
