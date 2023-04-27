import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def load_final():
    data = pd.read_csv(f'datasets_final/final_2018S1_int.csv', sep=';')
    data = data[['day_of_year', 'CAT_JOUR_INT', 'distance', 'TRNC_HORR_12', 'is_vac_y', 'is_dimanche_y', 'is_ouvrable_y', 'NB_VALD_HORR_60']]
    print('Parsing...')
    keep_indices = np.sort(np.random.choice(data.index, size=(len(data)//(100*14)), replace=False))
    data = data.loc[keep_indices]
    return data

def normalize(do_normalize, data):
    scaler = StandardScaler()
    if not do_normalize :
        return data
    data =(data-data.mean())/data.std()
    return data
    

def regression(do_normalize, type):
    print('Import data...')
    train_dataset = load_final()
    test_dataset = pd.read_csv('datasets_final/final_2017S2_int.csv', sep=';')
    test_dataset = test_dataset[['day_of_year', 'CAT_JOUR_INT', 'distance', 'TRNC_HORR_12', 'is_vac_y', 'is_dimanche_y', 'is_ouvrable_y', 'NB_VALD_HORR_60']]

    train_dataset = train_dataset.groupby(['day_of_year','distance', 'CAT_JOUR_INT'])['NB_VALD_HORR_60'].sum().reset_index()
    test_dataset= test_dataset.groupby(['day_of_year','distance', 'CAT_JOUR_INT'])['NB_VALD_HORR_60'].sum().reset_index()
    print('Done.')


    model = LinearRegression()

    print('Filter data')
    # print(train_dataset.head(), test_dataset.head())

    train_dataset = normalize(do_normalize, train_dataset)
    test_dataset = normalize(do_normalize, test_dataset)
    print(train_dataset.head(), test_dataset.head())

    print(f'Columns names : {train_dataset.columns}')

    print('Create X and y')
    y_train = train_dataset['NB_VALD_HORR_60']
    X_train = train_dataset.drop('NB_VALD_HORR_60', axis=1)
    y_test = test_dataset['NB_VALD_HORR_60']
    X_test = test_dataset.drop('NB_VALD_HORR_60', axis=1)

    if type == 'linear':
        print('Fit coefficients')
        model.fit(X_train, y_train)
        print(f'Coefficients : {model.coef_}, Intercept : {model.intercept_}')
        print('Corrélations : ', train_dataset.corr())
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)   
        print("Mean squared error: ", mse)
        print("R-squared score: ", r2)
        print("Mean absolute error: ", mae)
        pd.DataFrame({'reg' : y_pred, 'reel' : y_test}).to_csv('test_reg.csv', sep=';')
    if type == 'cluster':
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(X_train)
        labels_test = kmeans.predict(X_test)
        print(labels_test)




if __name__ == '__main__':
    print("Regression")
    regression(True, 'linear')