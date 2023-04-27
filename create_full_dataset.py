import pandas as pd
import numpy as np
import profil
import datetime as dt
import nombre_validation
from plots import get_type
import type_jour

# Going to need to transform the data to perform regression on it, as dates, code_stif, heure and type jour don't get represented by their value at the moment
dictionnaire_cat = ['JOHV', 'JOHV', 'JOHV', 'JOHV', 'JOHV', 'SAHV', 'DIJFP']
dictionnaire_cat_holiday = ['JOVS', 'JOVS', 'JOVS', 'JOVS', 'JOVS', 'SAVS', 'DIJFP']
types_jours = ['JOVS', 'JOHV', 'SAHV', 'SAVS', 'DIJFP']
years = [15, 16, 17, 18, 19, 20, 21]
semester = [1, 2]
dictionary = {}
profil.create_dictionary()

def day_to_int():
    # years = [15]
    # semester = [1, 2]
    for y in years:
        for s in semester:
            print(y,s)
            val = pd.read_csv(f'datasets_reorg/nombre_validation_20{y}S{s}.csv', sep=';')
            val['CODE_STIF_ARRET'] = val['CODE_STIF_ARRET'][pd.to_numeric(val['CODE_STIF_ARRET'], errors='coerce').notnull()]
            val['ID_REFA_LDA'] = val['ID_REFA_LDA'][pd.to_numeric(val['ID_REFA_LDA'], errors='coerce').notnull()]
            val = val.dropna(subset=['JOUR', 'CODE_STIF_ARRET', 'ID_REFA_LDA'], how='any')
            val['day_of_year'] = val.apply(lambda row: dt.datetime.strptime(row['JOUR'], '%d/%m/%Y').strftime('%j'), axis=1)
            val['year'] = val.apply(lambda row: dt.datetime.strptime(row['JOUR'], '%d/%m/%Y').strftime('%y'), axis=1)
            val.to_csv(f'datasets_reorg/nombre_validation_20{y}S{s}.csv', sep=';')

def val_cat_jour(): 
    # years = [15, 16]
    # semester = [1]


    equivalence = pd.read_csv('datasets_reorg/equivalence_finale_avec_distance.csv', sep=';')
    full_table = pd.DataFrame()
    for y in years:
        for s in semester:
            print(y,s)
            val = pd.read_csv(f'datasets_reorg/nombre_validation_20{y}S{s}_periode.csv', sep=';')
            
            # val['type_jour'] = val.apply(lambda row : find_type_jour(row['JOUR']), axis=1)

            is_vac = []
            is_ouvrable = []
            is_dimanche = []
            cat_jour = []
            previous_day = 0
            type_jour = 0
            for index, row in val.iterrows():
                current_day = row['JOUR']
                if previous_day != current_day:
                    previous_day = current_day
                    type_jour = find_type_jour(current_day)
                cat_jour += [type_jour]
                if type_jour == 'JOHV':
                    is_vac += [0]
                    is_ouvrable += [1]
                    is_dimanche += [0]
                elif type_jour == 'SAHV':
                    is_vac += [0]
                    is_ouvrable += [0]
                    is_dimanche += [0]
                elif type_jour == 'JOVS':
                    is_vac += [1]
                    is_ouvrable += [1]
                    is_dimanche += [0]
                elif type_jour == 'SAVS':
                    is_vac += [1]
                    is_ouvrable += [0]
                    is_dimanche += [0]
                elif type_jour == 'DIJFP':
                    is_vac += [0]
                    is_ouvrable += [0]
                    is_dimanche += [1]
                else:
                    is_vac += [0]
                    is_ouvrable += [0]
                    is_dimanche += [0]
                # if len(is_vac) % 100 == 0: print(len(is_vac))
            val['is_vac'] = is_vac
            val['is_ouvrable'] = is_ouvrable
            val['is_dimanche'] = is_dimanche
            val['cat_jour'] = cat_jour
            val = val[val['cat_jour'].isin(types_jours)]

            # val_profil = pd.merge(val['ID_REFA_LDA', 'NB'])
            # arret_profil = pd.concat(prof.dataset[['']])
            # full_table = pd.concat(full_table, pd.concat(val[['']]))
            # # print(len(jours), len(stations))
            val[['JOUR', 'day_of_year', 'year', 'ID_REFA_LDA', 'CODE_STIF_ARRET', 'NB_VALD', 'saison_influence', 'is_vac', 'is_ouvrable', 'is_dimanche', 'cat_jour']].to_csv(f'datasets_reorg/nombre_validation_20{y}S{s}_periode_cat_jour.csv', sep=';')

def prod(row):
    return row['pourc_validations']*row['NB_VALD']


def add_heure_val_pourc():
    years = [15, 16, 17, 18, 19, 20, 21]
    semester = [1, 2]

    for y in years:
        for s in semester:
            print(f'Performing calculations on semester {s} of 20{y}')
            temp_dataset = pd.DataFrame
            equiv = pd.read_csv('datasets_reorg/equivalence_finale_avec_distance.csv', sep=';')
            val = pd.read_csv(f'datasets_reorg/nombre_validation_20{y}S{s}_periode_cat_jour.csv', sep=';')
            prof = profil.Profil(y, s)
            print(prof.dataset.head())
            prof.dataset['heure_pointe'] = pd.to_numeric(prof.dataset['heure_pointe'], errors='coerce')
            prof.dataset['TRNC_HORR_12'] = pd.to_numeric(prof.dataset['TRNC_HORR_12'], errors='coerce')

            val['ID_REFA_LDA'] = val['ID_REFA_LDA'][pd.to_numeric(val['ID_REFA_LDA'], errors='coerce').notnull()]
            val['CODE_STIF_ARRET'] = val['CODE_STIF_ARRET'][pd.to_numeric(val['CODE_STIF_ARRET'], errors='coerce').notnull()]
            val = val.dropna(subset=['JOUR', 'CODE_STIF_ARRET', 'ID_REFA_LDA'], how='any')

            prof.dataset['ID_REFA_LDA'] = prof.dataset['ID_REFA_LDA'][pd.to_numeric(prof.dataset['ID_REFA_LDA'], errors='coerce').notnull()]
            prof.dataset['CODE_STIF_ARRET'] = prof.dataset['CODE_STIF_ARRET'][pd.to_numeric(prof.dataset['CODE_STIF_ARRET'], errors='coerce').notnull()]
            prof.dataset = prof.dataset.dropna(subset=['CODE_STIF_ARRET', 'ID_REFA_LDA'], how='any')

            val[['ID_REFA_LDA', 'CODE_STIF_ARRET']] = val[['ID_REFA_LDA', 'CODE_STIF_ARRET']].astype('int64')
            prof.dataset[['ID_REFA_LDA', 'CODE_STIF_ARRET']] = prof.dataset[['ID_REFA_LDA', 'CODE_STIF_ARRET']].astype('int64')

            temp_dataset = pd.merge(val, prof.dataset, left_on=['ID_REFA_LDA', 'CODE_STIF_ARRET', 'cat_jour'], right_on=['ID_REFA_LDA', 'CODE_STIF_ARRET', 'CAT_JOUR'])

            temp_dataset['NB_VALD_HORR_60'] = temp_dataset.apply(lambda row: prod(row), axis=1)
            temp_dataset['day_of_year'] = temp_dataset.apply(lambda row: dt.datetime.strptime(row['JOUR'], '%d/%m/%Y').strftime('%j'), axis=1)

            temp_dataset['ID_REFA_LDA'] = pd.to_numeric(temp_dataset['ID_REFA_LDA'], errors='coerce')
            temp_dataset['CODE_STIF_ARRET'] = pd.to_numeric(temp_dataset['CODE_STIF_ARRET'], errors='coerce')
            temp_dataset = temp_dataset.dropna(subset=['ID_REFA_LDA', 'CODE_STIF_ARRET'], how='any')
            temp_dataset[['ID_REFA_LDA', 'CODE_STIF_ARRET']] = temp_dataset[['ID_REFA_LDA', 'CODE_STIF_ARRET']].astype(int)


            temp_dataset = pd.merge(temp_dataset, equiv, on=['ID_REFA_LDA','CODE_STIF_ARRET'])
            # print(temp_dataset[['ID_REFA_LDA', 'CODE_STIF_ARRET', 'JOUR', 'NB_VALD_HORR_60', 'distance', 'route_long_name', 'stop_name', 'heure_pointe']])
            temp_dataset[['day_of_year', 'CAT_JOUR', 'heure_pointe', 'distance', 'TRNC_HORR_12', 'ID_REFA_LDA' , 'is_vac_y', 'is_dimanche_y', 'is_ouvrable_y', 'saison_influence', 'NB_VALD_HORR_60']].to_csv(f'datasets_final/final_20{y}S{s}.csv', sep=';')
            # temp_dataset[['day_of_year', 'CAT_JOUR', 'heure_pointe', 'distance', 'TRNC_HORR_12', 'ID_REFA_LDA' , 'is_vac_y', 'is_dimanche_y', 'is_ouvrable_y', 'NB_VALD_HORR_60']].to_csv(f'datasets_final/final_20{y}S{s}.csv', sep=';')

def add_jour_int():
    for y in years:
        for s in semester:
            print(y,s)
            types_jours = {'JOVS' : 0, 'JOHV' : 1, 'SAHV' : 2, 'SAVS' : 3, 'DIJFP' : 4}
            data = pd.read_csv(f'datasets_final/final_20{y}S{s}.csv', sep=';')
            # keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(50*14)), replace=False))
            # data = data.loc[keep_indices]
            # data = data.reset_index(drop=True)
            data['CAT_JOUR_INT'] = data.apply(lambda row: types_jours.get(row['CAT_JOUR'], 0.0), axis=1)
            data.to_csv(f'datasets_final/final_20{y}S{s}_int.csv', sep=';') #uncomment to update test file

def add_line():
    for y in years:
        for s in semester:
            print(y,s)
            equiv = pd.read_csv('datasets_reorg/equivalence_finale.csv', sep=';')
            data = pd.read_csv(f'datasets_final/final_20{y}S{s}_int.csv', sep=';')
            data = pd.merge(data, equiv[['route_id', 'ID_REFA_LDA']], on='ID_REFA_LDA')
            data.to_csv(f'datasets_final/final_20{y}S{s}_int_line.csv', sep=';') #uncomment to update test file

def concat_all(appendice):
    final_dataframe = pd.DataFrame()
    for y in years:
        for s in semester:
            final_dataframe = pd.concat([final_dataframe, pd.read_csv(f'datasets_final/final_20{y}S{s}_{appendice}.csv', sep=';')]) #j'ai oublié de mettre sep=';' en crééant argh
            print(y, s)
    final_dataframe.to_csv(f'datasets_final/final_{appendice}.csv', sep=';')


def find_type_jour(jour):
    try:
        jour = dt.datetime.strptime(jour, '%d/%m/%Y')
    except:
        return None
    year = jour.year
    month = jour.month
    day = jour.day
    is_holiday = get_type(year, month, day)
    if is_holiday == 'HV':
        cat = dictionnaire_cat[dt.date(year,month,day).weekday()]
    elif is_holiday == 'VS':
        cat = dictionnaire_cat_holiday[dt.date(year,month,day).weekday()]
    else:
        cat = 'DIJFP'
    return cat

if __name__ == '__main__':
    print("hihe")
    # day_to_int()
    # val_cat_jour()
    # add_heure_val_pourc()
    # add_jour_int()
    # add_line()
    concat_all('int_line')
    