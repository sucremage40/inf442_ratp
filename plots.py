import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
from calendar import monthrange
import datetime
import profil
import nombre_validation


station = '10'
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
    print(cut_year, month // 7 + 1, day // 10, jour)
    affluence_journée = val.loc[(val['JOUR'] == jour) & (val['CODE_STIF_ARRET'] == station)].iloc[0,-1]
    profile_journée = prof.dataset.loc[(prof.dataset['CAT_JOUR'] == cat) &(prof.dataset['CODE_STIF_ARRET'] == station)]

    profile_to_plot = np.zeros((24))
    for k in range(24):
        temp_df = profile_journée[(profile_journée['TRNC_HORR_60'] == f'{k}H-{k+1}H')]
        if not temp_df.empty:
            profile_to_plot[k] = temp_df.iloc[0, -1]
            
    return profile_to_plot*affluence_journée

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
        ax.bar(np.arange(1,25,1), values_to_plot(slider_years.val, slider_months.val, slider_days.val))



    slider_days.on_changed(update)
    slider_months.on_changed(update)
    slider_years.on_changed(update)


    plt.show()