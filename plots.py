import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button # type: ignore
from calendar import monthrange
import datetime
import profil
import nombre_validation

extension = {15 : "csv", 16 : "txt", 17 : "txt", 18 : "txt", 19 : "txt", 20 : "txt", 21 : "txt"} #'txt' for 16 and +, 'csv' for 15
station = '1'
cat = 'DIJFP'
#dictionnaire_cat = {"Monday": "JOHV", "Tuesday": "JOHV","Wednesday": "JOHV", "Thursday": "JOHV" , "Friday": "JOHV", "Saturday": "SAHV", "Sunday": "DIJFP"}
dictionnaire_cat = ['JOHV', 'JOHV', 'JOHV', 'JOHV', 'JOHV', 'SAHV', 'DIJFP']

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
    cat = dictionnaire_cat[datetime.date(year,month,day).weekday()]
    print(jour)
    extract_row = val.loc[(val['JOUR'] == jour) & (val['CODE_STIF_ARRET'] == station)]
    affluence_journée = extract_row['NB_VALD'].item()
    profile_journée = prof.dataset.loc[(prof.dataset['CAT_JOUR'] == cat) &(prof.dataset['CODE_STIF_ARRET'] == station)]

    profile_to_plot = np.zeros((24))
    for k in range(24):
        temp_df = profile_journée[(profile_journée['TRNC_HORR_60'] == f'{k}H-{k+1}H')]
        if not temp_df.empty:
            temp_pourc = temp_df['pourc_validations'].item()
            if not isinstance(temp_pourc, float): # traiter les variables stockées "a la francaises"
                temp_pourc = temp_pourc.split(',')
                temp_pourc = float(f'{temp_pourc[0]}.{temp_pourc[1]}')
            profile_to_plot[k] = temp_pourc
            
    return profile_to_plot*affluence_journée/100 # Division pour normaliser les pourcentages

if __name__ == '__main__':
    years = np.arange(15,22,1)
    months = np.arange(1,13,1)

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.5)


    ax.bar(np.arange(1,25,1), values_to_plot(2015,1,1))


    years_ax = fig.add_axes([0.20, 0.1, 0.60, 0.03])
    slider_years = Slider(years_ax, "Année", 2015, 2021, valstep=1)

    months_ax = fig.add_axes([0.20, 0.2, 0.60, 0.03])
    slider_months = Slider(months_ax, "Mois", 1, 12, valstep=1)

    days_ax = fig.add_axes([0.20, 0.3, 0.60, 0.03])
    slider_days = Slider(days_ax, "jours", 1, 31, valstep=1)


    def update(val):
        end_day = monthrange(slider_years.val, slider_months.val)[1]
        slider_days.valmax = end_day
        fig.canvas.draw_idle()
        ax.clear()
        current_values = values_to_plot(slider_years.val, slider_months.val, slider_days.val)
        ax.bar(np.arange(1,25,1), current_values)



    slider_days.on_changed(update)
    slider_months.on_changed(update)
    slider_years.on_changed(update)


    plt.show()