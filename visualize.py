import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import figure
from scipy.stats import gaussian_kde
from matplotlib import colors

def plot_var(case):
    coord_to_value = {0 : 'distance', 1 : 'NB_VALD_HORR_60', 2 : 'day_of_year', 3 : 'TRNC_HORR_12'}
    colors = {0 : 'b', 1 : 'g', 2 : 'r', 3 : 'c', 4 : 'm'}
    types_jours = {'JOVS' : 0, 'JOHV' : 1, 'SAHV' : 2, 'SAVS' : 3, 'DIJFP' : 4}
    inv_types_jours = {v: k for k, v in types_jours.items()}
    n = len(coord_to_value)


    row = 1
    fig, axs = plt.subplots() #default for pylance

    if case == 0:
        data = pd.read_csv('datasets_final/final.csv', sep=';')
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(100*14)), replace=False))
        data = data.loc[keep_indices]
        data = data.reset_index(drop=True)
        data['CAT_JOUR_INT'] = data.apply(lambda row: types_jours.get(row['CAT_JOUR'], 0.0), axis=1)

        fig, axs = plt.subplots(1, 2)
        axs[0].set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(2)}, {row}, {2}')
        plt.colorbar(axs[0].scatter(data[coord_to_value.get(2)], data[coord_to_value.get(row)], marker='o', s=1, c=data['distance']))

        axs[1].set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(3)}, {row}, {3}')
        plt.colorbar(axs[1].scatter(data[coord_to_value.get(3)], data[coord_to_value.get(row)], marker='o', s=1, c=data['distance']))

    elif case == 1:  #Tracer NB_VALD_HORR_60 fonction de distance
        print('Loading...')
        data = pd.read_csv('datasets_final/final_int.csv', sep=';')
        print('Loaded')
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(10*14)), replace=False))
        data = data.loc[keep_indices]
        # data = data.reset_index(drop=True)
        # print(f'Loaded {data.shape[0]} elemnts')
        # data['CAT_JOUR_INT'] = data.apply(lambda row: types_jours.get(row['CAT_JOUR'], 0.0), axis=1)
        print('Data processed')
        

        fig, axs = plt.subplots(1, 5)
        for col in range(5):
            data_temp = data.loc[(data['CAT_JOUR_INT']) == col]
            axs[col].set(xlim=(-2000, 50000), ylim=(-0.025e6, 0.5e6))

            x = data_temp['distance']
            y = data_temp['NB_VALD_HORR_60']

            density = gaussian_kde(np.vstack([x, y]))
            densities = density(np.vstack([x, y]))*1e9
            threshold = 0.01

            color_heure = data_temp['TRNC_HORR_12'] # une couleur par heure
            color_unique = [colors.get(col) for k in range(len(y[densities >= threshold]))] # une couleur par graph

            axs[col].set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(0)}, {row}, {0}')
            plt.colorbar(axs[col].scatter(x[densities > threshold], y[densities > threshold], marker='o', s=1, c=color_heure[densities > threshold]))

    elif case == 2:
        print('Loading...')
        data = pd.read_csv(f'datasets_final/final_2015S1.csv', sep=';')
        print('Loaded')
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(1000)), replace=False))
        data = data.loc[keep_indices]
        data = data.reset_index(drop=True)
        data['CAT_JOUR_INT'] = data.apply(lambda row: types_jours.get(row['CAT_JOUR'], 0.0), axis=1)
        print(f'Data selected {data.shape[0]} elements')

        fig, axs = plt.subplots(1, 2)
        axs[0].set_title(f'NB_VALD fonction de day_of_year, {row}, {2}')

        data_vald = data.groupby(['day_of_year'])['NB_VALD_HORR_60'].sum()
        data_vald_dist = data.groupby(['day_of_year', 'distance'])['NB_VALD_HORR_60'].sum()
        data_daytype = data.drop_duplicates('day_of_year')['CAT_JOUR_INT']
        data_distance = data.drop_duplicates(['day_of_year', 'distance'])['distance']
        print(data)
        axs[0].scatter(data['day_of_year'].unique(), data_vald, marker='o', s=1, c=data_daytype)
        uniques_day = data['day_of_year'].unique()
        axs[1].scatter([uniques_day[k]*data[[data['day_of_year'] == uniques_day[k]]].shape[0] for k in range(len(uniques_day))], data_vald_dist, marker='o', s=1, c=data_distance)

    elif case == 3:  #Tracer NB_VALD_HORR_60 fonction de distance
        route_line = {}
        print('Loading...')
        data = pd.read_csv('datasets_final/final_2018S2_int_line.csv', sep=';')
        print('Loaded')
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(10*14)), replace=False))
        data = data.loc[keep_indices]
        print(len(data))
        data = data.groupby(['distance', 'CAT_JOUR_INT', 'route_id'])['NB_VALD_HORR_60'].sum().reset_index()
        for l in data['route_id'].unique():
            route_line[l] = len(route_line)
        data['route_id'] = data.apply(lambda row: route_line.get(row['route_id'], 0.0), axis=1)
        print('Data processed')
        

        fig = plt.figure(figsize=figure.figaspect(0.5))
        ax = fig.add_subplot(projection='3d')
        col = 3
        data_temp = data.loc[(data['CAT_JOUR_INT']) == col]
        # axs[col].set(xlim=(-2000, 50000), ylim=(-0.025e6, 1.6e6))

        x = data_temp['distance']
        y = data_temp['NB_VALD_HORR_60']

        density = gaussian_kde(np.vstack([x, y]))
        densities = density(np.vstack([x, y]))*1e9
        threshold = 0.01

        ax.set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(0)}, {row}, {inv_types_jours.get(col)}')
        ax.scatter(x[densities > threshold], y[densities > threshold], data_temp['route_id'][densities > threshold], marker='o', s=1)
        fig.set_size_inches(10, 10)
        plt.show()
    
    elif case == 4:
        route_line = {}
        print('Loading...')
        data = pd.read_csv('datasets_final/final_int_line.csv', sep=';')
        print('Processing...')
        data = data[['day_of_year','distance','TRNC_HORR_12','NB_VALD_HORR_60','route_id', 'CAT_JOUR_INT']]
        coord_to_value = {0 : 'day_of_year', 1 : 'distance', 2 : 'TRNC_HORR_12', 3 : 'NB_VALD_HORR_60', 4 : 'CAT_JOUR_INT', 5 : 'route_id'}
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(10*14)), replace=False))
        data = data.loc[keep_indices]
        data = data.reset_index(drop=True)
        for l in data['route_id'].unique():
            route_line[l] = len(route_line)
        data['route_id'] = data.apply(lambda row: route_line.get(row['route_id'], 0.0), axis=1)

        print('Displaying...')
        fig, axs = plt.subplots(5, 5)
        to_range = 5
        for row in range(to_range):
            for col in range(to_range):
                axs[row, col].set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(col)}, {row}, {col}')
                axs[row, col].scatter(data[coord_to_value.get(col)], data[coord_to_value.get(row)], marker='o', s=1, c=data['CAT_JOUR_INT'])

    elif case == 5:
        route_line = {}
        print('Loading...')
        data = pd.read_csv('datasets_final/final_int_line.csv', sep=';')
        print('Processing...')
        data = data[['day_of_year','distance','NB_VALD_HORR_60','route_id', 'CAT_JOUR_INT']]
        coord_to_value = {0 : 'day_of_year', 1 : 'distance', 2 : 'NB_VALD_HORR_60', 3 : 'CAT_JOUR_INT', 4 : 'route_id'}
        keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(10*14)), replace=False))
        data = data.loc[keep_indices]
        data = data.reset_index(drop=True)
        data = data.groupby(['day_of_year','distance','route_id', 'CAT_JOUR_INT'])['NB_VALD_HORR_60'].sum().reset_index()
        for l in data['route_id'].unique():
            route_line[l] = len(route_line)
        data['route_id'] = data.apply(lambda row: route_line.get(row['route_id'], 0.0), axis=1)

        print('Displaying...')
        to_range = 5
        fig, axs = plt.subplots(to_range, to_range)
        for row in range(to_range):
            for col in range(to_range):
                axs[row, col].set_title(f'{coord_to_value.get(row)} fonction de {coord_to_value.get(col)}, {row}, {col}')
                axs[row, col].scatter(data[coord_to_value.get(col)], data[coord_to_value.get(row)], marker='o', s=1, c=data['distance'])


    print('Fin calcul')
    

    # fig, ax = plt.subplots()
    # ax.set_title(f'{coord_to_value.get(1)} fonction de {coord_to_value.get(3)}')
    # fig_1 = ax.scatter(data[coord_to_value.get(1)], data[coord_to_value.get(3)], marker='o', s=0.2, c=data[coord_to_value.get(0)])
    # plt.colorbar(ax.scatter(data[coord_to_value.get(1)], data[coord_to_value.get(3)], marker='o', s=0.2, c=data[coord_to_value.get(0)]))


    fig.set_dpi(300)
    if case == 0:
        fig.set_size_inches(20, 10)
    elif case == 1:
        fig.set_size_inches(50, 10)
    elif case == 3:
        fig.set_size_inches(10, 10)
    elif case == 2:
        fig.set_size_inches(10, 5)
    elif case == 4:
        fig.set_size_inches(50, 50)
    elif case == 5:
        fig.set_size_inches(50, 50)
    plt.savefig(f'figs/plot_var_{case}.png', )
    print(f'Saved to plot_var_{case}')
    # plt.show()



if __name__ == '__main__':
    print('Visualize')
    plot_var(4)