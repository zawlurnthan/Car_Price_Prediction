from joblib import load
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler, \
    MaxAbsScaler, RobustScaler, QuantileTransformer, Normalizer
import warnings


warnings.filterwarnings('ignore')
LinearRegressor = load('model.joblib')
col_names = load('col_names.joblib')


data = pd.read_csv('static/car.csv', low_memory=False)


def get_makes(df):
    makes = df['make'].unique().tolist()
    makes.sort()
    return makes


def get_cars(df):
    makes = df['make'].unique().tolist()
    makes.sort()
    cars = {}
    for make in makes:
        models = df.loc[df.make == make, 'model'].unique().tolist()
        models.sort()
        cars[make] = models
    return cars


# Function that convert inputs into a dataframe with required columns
def input_process(year, odometer, make, model, transmission):
    cols = col_names
    dic = {}

    for col in cols:
        if col == 'make_' + make:
            dic[col] = [1]

        elif col == 'model_' + model:
            dic[col] = [1]

        elif col == 'transmission_' + transmission:
            dic[col] = [1]

        else:
            dic[col] = [0]

    df = pd.DataFrame(dic)
    df['year'] = year
    df['odometer'] = odometer
    return df


# Make prediction here by using different Scaler which vary output
def make_predict(check):
    df = check.copy()
    columns_names = ['year', 'odometer']
    features = df[columns_names]
    predictions = {}

    min_max = MinMaxScaler()
    df[columns_names] = min_max.fit_transform(features.values)
    mms = LinearRegressor.predict(df)
    predictions['Min Max Scaler'] = mms[0]

    min_max_val = MinMaxScaler(feature_range=(5, 10))
    df[columns_names] = min_max_val.fit_transform(features.values)
    mms_range = LinearRegressor.predict(df)
    predictions['Min Max Scaler (range)'] = mms_range[0]

    std = StandardScaler()
    df[columns_names] = std.fit_transform(features.values)
    sts = LinearRegressor.predict(df)
    predictions['Standard Scaler'] = sts[0]

    max_abs = MaxAbsScaler()
    df[columns_names] = max_abs.fit_transform(features.values)
    mas = LinearRegressor.predict(df)
    predictions['Max Abs Scaler'] = mas[0]

    robust = RobustScaler()
    df[columns_names] = robust.fit_transform(features.values)
    rob = LinearRegressor.predict(df)
    predictions['Robust Scaler'] = rob[0]

    quantile = QuantileTransformer()
    df[columns_names] = quantile.fit_transform(features.values)
    qua_tran = LinearRegressor.predict(df)
    predictions['Quantile Transformer'] = qua_tran[0]

    normal = Normalizer(norm='l2')
    df[columns_names] = normal.fit_transform(features.values)
    nor = LinearRegressor.predict(df)
    predictions['Normalizer'] = nor[0]

    return predictions
