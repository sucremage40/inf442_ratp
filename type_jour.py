import pandas as pd
import numpy as np
import datetime


def traitement_type_jours():
    ferie = pd.read_csv('type_jour/jours_feries.csv', sep=',')
    ferie['date'] = pd.to_datetime(ferie['date'])
    ferie['date'] = ferie['date'].dt.strftime('%d/%m/%Y')
    vacances = pd.read_csv('type_jour/calendrier_scolaire.csv', sep=';')

    vacances = vacances.loc[(vacances['zones'] == 'Zone C') & (vacances['location'] == 'Paris') & (vacances['population'] != 'Enseignants')]
    ferie = ferie.loc[(ferie['zone'] == 'Métropole')]



    vacances['start_date'] = vacances['start_date'].str.slice(0,10)
    vacances['end_date'] = vacances['end_date'].str.slice(0,10)
    vacances['start_date'] = pd.to_datetime(vacances['start_date'])
    vacances['start_date'] = vacances['start_date'].dt.strftime('%d/%m/%Y')
    vacances['end_date'] = pd.to_datetime(vacances['end_date'])
    vacances['end_date'] = vacances['end_date'].dt.strftime('%d/%m/%Y')


    vacances = vacances[['start_date', 'end_date']]
    ferie = ferie['date']

    print(ferie.head())
    print(vacances.head())

    ferie.to_csv(f'type_jour/jours_feries_reorg.csv', sep=';')
    vacances.to_csv(f'type_jour/vacances_scolaires_reorg.csv', sep=';')

def get_type(year, month, day):
    current_day = datetime.datetime(year, month, day)
    ferie = pd.read_csv(f'type_jour/jours_feries_reorg.csv', sep=';')
    vacances = pd.read_csv(f'type_jour/vacances_scolaires_reorg.csv', sep=';')
    vacances['start_date'] = pd.to_datetime(vacances['start_date'], format='%d/%m/%Y')
    vacances['end_date'] = pd.to_datetime(vacances['end_date'], format='%d/%m/%Y')
    ferie['date'] = pd.to_datetime(ferie['date'], format='%d/%m/%Y')

    current_ferie = ferie.loc[(ferie['date'] == current_day)]
    for index, rows in vacances.iterrows():
        if (rows['start_date']<= current_day and rows['end_date'] >= current_day):
            return 'VS'
        elif not current_ferie.empty:
            return 'FP'
    return 'HV'


if __name__ == '__main__':
    print(get_type(2018,1,1))