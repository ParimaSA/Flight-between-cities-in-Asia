import pandas as pd


class Model:
    def __init__(self):
        self.data = pd.read_csv('quality_of_life_data.csv')

    def columns(self):
        return list(self.data.columns)

    def index_columns(self):
        return ['Quality of Life Index', 'Purchasing Power Index', 'Safety Index', 'Health Care Index',
                'Cost of Living Index', 'Property Price to Income Ratio', 'Traffic Commute Time Ratio',
                'Pollution Index', 'Climate Index', 'Corruption Perception Index']

    def lower_value(self):
        return ['Cost of Living Index', 'Property Price to Income Ratio', 'Pollution Index',
                'Traffic Commute Time Ratio']

    def country_name(self):
        return list(self.data.Country)

    def numerical_columns(self):
        return ['Population', 'Area', 'Density'] + self.index_columns()

    def rows(self):
        return len(self.data)

    def filter_data(self, filter_dict, df=None):
        f_data = df
        if df is None:
            f_data = self.data.copy()
        filter_key = list(filter_dict.keys())
        filter_value = list(filter_dict.values())
        for n in range(len(filter_dict)):
            f_data = f_data[f_data[filter_key[n]] == filter_value[n]]
        return f_data

    def filter_range_data(self, min_range, max_range, df):
        f_data = df.copy()
        if max_range:
            f_data = f_data[f_data < max_range]
        if min_range:
            f_data = f_data[f_data > min_range]
        return f_data

    def group_data(self, by, attribute, df=None):
        g_data = df
        if df is None:
            g_data = self.data.copy()
        g_data = g_data.groupby(by=by)[attribute].mean().sort_values(ascending=False)
        return g_data

    def sort_data(self, by: str, df=None):
        s_data = df
        if df is None:
            s_data = self.data.copy()
        ascending = False
        if by in self.lower_value():
            ascending = True
        s_data.sort_values(by=by, ascending=ascending, inplace=True)
        s_data.reset_index(drop=True, inplace=True)
        return s_data


if __name__ == '__main__':
    data = Model()
    print(data.rows())
