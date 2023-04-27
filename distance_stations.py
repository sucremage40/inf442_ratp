import pandas as pd
import numpy as np

lines_ids = ['IDFM:C01378', 'IDFM:C01381', 'IDFM:C01383', 'IDFM:C01727', 'IDFM:C01373', 'IDFM:C01379', 'IDFM:C01743', 'IDFM:C01729', 'IDFM:C01371', 'IDFM:C01372', 'IDFM:C01728', 'IDFM:C01375', 'IDFM:C01742', 'IDFM:C01377', 'IDFM:C01386', 'IDFM:C01374', 'IDFM:C01376', 'IDFM:C01380', 'IDFM:C01382', 'IDFM:C01384', 'IDFM:C01387']

def reorg_data():
    final_dataset = pd.DataFrame
    arrets_lignes = pd.read_csv('extraction_stations/arrets_lignes.csv', sep=';')
    relations = pd.read_csv('extraction_stations/relations.csv', sep=';')
    correspondance = pd.read_csv('extraction_stations/zones_de_correspondance.csv', sep=';')

    final_dataset = arrets_lignes[(arrets_lignes['route_id'].isin(lines_ids))][['route_id', 'route_long_name', 'stop_id', 'stop_name']]
    final_dataset['stop_id'] = final_dataset['stop_id'].str.replace(r'\D+', '').astype('int64')

    # print(final_dataset)
    
    relations_metro = relations.rename(columns={'ArRId' : 'stop_id', 'ZdCId' : 'correspondance_id'})
    relations_metro = relations_metro.drop_duplicates(subset='stop_id', keep='first')
    relations_metro = relations_metro[['stop_id', 'correspondance_id']]

    relations_rer = relations.rename(columns={'ZdAId' : 'stop_id', 'ZdCId' : 'correspondance_id'})
    relations_rer = relations_rer.drop_duplicates(subset='stop_id', keep='first')
    relations_rer = relations_rer[['stop_id', 'correspondance_id']]

    final_dataset_metro = pd.merge(final_dataset, relations_metro, on='stop_id')
    final_dataset_rer = pd.merge(final_dataset, relations_rer, on='stop_id')

    correspondance = correspondance[['ZdCId', 'ZdCXEpsg2154', 'ZdCYEpsg2154']]
    correspondance = correspondance.rename(columns={'ZdCId' : 'correspondance_id', 'ZdCXEpsg2154' : 'coord_X', 'ZdCYEpsg2154' : 'coord_Y'})
    correspondance = correspondance.drop_duplicates(subset='correspondance_id', keep='first')

    final_dataset_metro = pd.merge(final_dataset_metro, correspondance, on='correspondance_id')
    final_dataset_rer = pd.merge(final_dataset_rer, correspondance, on='correspondance_id')
    final_dataset_metro = final_dataset_metro.drop_duplicates(subset=['correspondance_id', 'route_id'], keep='first')

    final_dataset = pd.concat([final_dataset_metro, final_dataset_rer])
    final_dataset.to_csv('datasets_reorg/equivalence_total.csv', sep=';')

    print(final_dataset.head())

    return 'Done'

def join_equi():
    equi_reel = pd.read_csv('datasets_reorg/equivalence_code_station_drop.csv', sep=';')
    equi_theo = pd.read_csv('datasets_reorg/equivalence_total.csv', sep=';')
    equi = pd.merge(equi_reel, equi_theo, left_on='ID_REFA_LDA', right_on='correspondance_id')
    equi = equi[['ID_REFA_LDA', 'CODE_STIF_ARRET', 'LIBELLE_ARRET', 'route_id', 'route_long_name', 'stop_name', 'coord_X', 'coord_Y']]
    equi.to_csv('datasets_reorg/equivalence_finale.csv', sep=';')

def calculate_center_of_mass():
    stations_equiv = pd.read_csv('datasets_reorg/equivalence_finale.csv', sep=';')
    stations_equiv = stations_equiv.sort_values('route_long_name', ascending=True)

    lines = stations_equiv['route_long_name'].unique()
    centers = np.zeros((len(lines), 2))

    for l in range(len(lines)):
        temp_dataset = stations_equiv[(stations_equiv['route_long_name'] == lines[l])]
        for e in range(len(temp_dataset)):
            centers[l, 0] += int(temp_dataset.iloc[e, -2])
            centers[l, 1] += int(temp_dataset.iloc[e, -1])
        centers[l] /= len(temp_dataset)

    return centers

def calculate_distances():
    stations_equiv = pd.read_csv('datasets_reorg/equivalence_finale.csv', sep=';')
    stations_equiv = stations_equiv.sort_values('route_long_name', ascending=True)
    lines = stations_equiv['route_long_name'].unique()
    dictionary = {}

    centers = calculate_center_of_mass()
    distances = np.zeros(stations_equiv.shape[0])

    for c in range(len(centers)):
        dictionary[lines[c]] = centers[c]

    row_counter = 0
    for index, row in stations_equiv.iterrows():
        distances[row_counter] = distance(dictionary.get(row['route_long_name']), row[['coord_X', 'coord_Y']])
        row_counter += 1

    stations_equiv['distance'] = distances
    stations_equiv.to_csv('datasets_reorg/equivalence_finale_avec_distance.csv', sep=';')


def distance(center, coords):
    return np.sqrt(pow(center[0]-coords[0], 2) + pow(center[1]-coords[1], 2))

if __name__ == '__main__':
    print("Geo")
    # reorg_data()
    # join_equi()
    # calculate_center_of_mass()
    # calculate_distances()