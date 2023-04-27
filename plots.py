import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button # type: ignore
from calendar import monthrange
import datetime
import profil
from type_jour import get_type
import nombre_validation

extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
station = '71030'
cat = 'DIJFP'
equivalence = pd.read_csv('datasets_reorg/equivalence_code_station.csv', sep=';')
#dictionnaire_cat = {"Monday": "JOHV", "Tuesday": "JOHV","Wednesday": "JOHV", "Thursday": "JOHV" , "Friday": "JOHV", "Saturday": "SAHV", "Sunday": "DIJFP"}
dictionnaire_cat = ['JOHV', 'JOHV', 'JOHV', 'JOHV', 'JOHV', 'SAHV', 'DIJFP']
dictionnaire_cat_holiday = ['JOVS', 'JOVS', 'JOVS', 'JOVS', 'JOVS', 'SAVS', 'DIJFP']

def type_of_day(year, month, day):
    ferie = pd.read_csv('type_jour/jours_feries.csv', sep=',')
    vacances = pd.read_csv('type_jour/calendrier_scolaire.csv', sep=';')
    


def write_day(year, month, day):
    if (month // 10 > 0):
        if (day // 10 > 0):
            jour = f'{day}/{month}/{year}'
        else:
            jour = f'0{day}/{month}/{year}'
    else:
        if (day // 10 > 0):
            jour = f'{day}/0{month}/{year}'
        else:
            jour = f'0{day}/0{month}/{year}'

    return jour

def values_to_plot(year, month, day):
    cut_year = year%100
    val = pd.read_csv(f'datasets_reorg/nombre_validation_20{cut_year}S{month // 7 + 1}.csv', sep=';')
    prof = profil.Profil(cut_year, month // 7 + 1)
    jour = write_day(year,month,day)
    is_holiday = get_type(year, month, day)
    print(jour, is_holiday, station)
    if is_holiday == 'HV':
        cat = dictionnaire_cat[datetime.date(year,month,day).weekday()]
    elif is_holiday == 'VS':
        cat = dictionnaire_cat_holiday[datetime.date(year,month,day).weekday()]
    else:
        cat = 'DIJFP'

    extract_row = val.loc[(val['JOUR'] == jour) & (val['ID_REFA_LDA'] == station)]
    affluence_journée = extract_row['NB_VALD'].item()
    profile_journée = prof.dataset.loc[(prof.dataset['CAT_JOUR'] == cat) &(prof.dataset['ID_REFA_LDA'] == station)]

    profile_to_plot = np.zeros((24))
    for k in range(24):
        temp_df = profile_journée[(profile_journée['TRNC_HORR_60'] == f'{k}H-{k+1}H')]
        if not temp_df.empty:
            temp_pourc = temp_df['pourc_validations'].item()
            if not isinstance(temp_pourc, float): # traiter les variables stockées "a la francaises"
                temp_pourc = temp_pourc.split(',')
                temp_pourc = float(f'{temp_pourc[0]}.{temp_pourc[1]}')
            profile_to_plot[k] = temp_pourc
            
    return np.array(profile_to_plot*affluence_journée/100) # Division pour normaliser les pourcentages

if __name__ == '__main__':
    years = np.arange(15,22,1)
    months = np.arange(1,13,1)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.5)
    fig.suptitle(f'Affluence horaire dans la station {equivalence["LIBELLE_ARRET"].iloc[0]}')
    plt.xlabel('Heure')
    plt.ylabel('Nombre de voyageurs')

    ax.bar(np.arange(1,25,1), values_to_plot(2015,1,1))


    years_ax = fig.add_axes([0.20, 0.21, 0.60, 0.03])
    slider_years = Slider(years_ax, "Année  ", 2015, 2021, valstep=1)

    months_ax = fig.add_axes([0.20, 0.14, 0.60, 0.03])
    slider_months = Slider(months_ax, "Mois  ", 1, 12, valstep=1)

    days_ax = fig.add_axes([0.20, 0.07, 0.60, 0.03])
    slider_days = Slider(days_ax, "Jour  ", 1, 31, valstep=1)

    station_ax = fig.add_axes([0.20, 0.28, 0.60, 0.03])
    slider_station = Slider(station_ax, "Station  ", 1, equivalence.shape[0], valstep=1)


    def update(val):
        #Change for station counter
        global station
        fig.suptitle(f'Affluence horaire dans la station {equivalence["LIBELLE_ARRET"].iloc[slider_station.val-1]}')
        station = equivalence['ID_REFA_LDA'].iloc[slider_station.val-1]
        #Change for date
        end_day = monthrange(slider_years.val, slider_months.val)[1]
        slider_days.valmax = end_day
        fig.canvas.draw_idle()
        ax.clear()
        current_values = values_to_plot(slider_years.val, slider_months.val, slider_days.val)
        if np.linalg.norm(current_values) == 0:
            ax.text(0.5, 0.5, 'No data', transform=ax.transAxes, fontsize=40, color='gray', alpha=0.5, ha='center', va='center', rotation=0)
        ax.bar(np.arange(1,25,1), current_values) 
        ax.set_xlabel('Heure')
        ax.set_ylabel('Nombre de voyageurs')
        



    slider_days.on_changed(update)
    slider_months.on_changed(update)
    slider_years.on_changed(update)
    slider_station.on_changed(update)


    plt.show()