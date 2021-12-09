# import plotly.express as px
from brain import data
import pandas as pd

Toyota = data[data['make'] == 'Toyota']
Land_Cruiser = Toyota[Toyota['model'] == 'Land cruiser']


info = {
    'year': [year for year in Land_Cruiser['year']],
    'odometer': [odometer for odometer in Land_Cruiser['odometer']],
    'price': [price for price in Land_Cruiser['price']],
}

