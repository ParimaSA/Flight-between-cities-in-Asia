"""Module for Model Class"""
import pandas as pd


class Model:
    """Logic using for manage the data in App"""
    def __init__(self):
        """Initialize the data in App"""
        self.data = pd.read_csv('quality_of_life_data.csv')

    def get_data(self):
        """Return the data"""
        return self.data

    def columns(self):
        """Return the column list of the data"""
        return list(self.data.columns)

    def index_columns(self):
        """Return index column list of the data"""
        return ['Quality of Life Index', 'Purchasing Power Index', 'Safety Index', 'Health Care Index',
                'Cost of Living Index', 'Property Price to Income Ratio', 'Traffic Commute Time Ratio',
                'Pollution Index', 'Climate Index', 'Corruption Perception Index']

    def lower_value(self):
        """Return the index column, which lower value mean better quality of life"""
        return ['Cost of Living Index', 'Property Price to Income Ratio', 'Pollution Index',
                'Traffic Commute Time Ratio']

    def country_name(self):
        """Return list of all country name in the data"""
        return list(self.data.Country)

    def numerical_columns(self):
        """Return all columns list which has numerical data"""
        return ['Population', 'Area', 'Density'] + self.index_columns()

    def rows(self):
        """Return number of rows"""
        return len(self.data)

    def filter_data(self, filter_dict, df=None):
        """Return data which has filtered with filter dict
        :param filter_dict: dictionary with key is the name of the column and value is the value of that column
        :param df: the data using for filter, filter will use the original data if df is None
        :return f_data: df after filter with the filter dict
        """
        f_data = df
        if df is None:
            f_data = self.data.copy()
        filter_key = list(filter_dict.keys())
        filter_value = list(filter_dict.values())
        for n in range(len(filter_dict)):
            f_data = f_data[f_data[filter_key[n]] == filter_value[n]]
        return f_data

    def filter_range_data(self, min_range: float, max_range: float, df: pd.DataFrame):
        """Return the data which has filtered the minimum and maximum range
        :param min_range: minimum range of df
        :param max_range: maximum range of df
        :param df: data with only one column using for filtered
        :return f_data: df after filter min and max range
        """
        f_data = df.copy()
        if max_range:  # if range is None, do not filter the data
            f_data = f_data[f_data < max_range]
        if min_range:
            f_data = f_data[f_data > min_range]
        return f_data

    def group_data(self, by: str, attribute: str, df=None):
        """Return the data which has grouped with the attribute
        :param by: the column name used for group the df
        :param attribute: selected attribute choosing after group
        :param df: dataframe used for group, use the original data if df is None
        :return g_data: df after group with the attribute
        """
        g_data = df
        if df is None:
            g_data = self.data.copy()
        g_data = g_data.groupby(by=by)[attribute].mean().sort_values(ascending=False)
        return g_data

    def sort_data(self, by: str, df=None):
        """Return the data which has sorted by the attribute
        :param by: the column name to sort the df
        :param df: the data to sort, use the original data if df is None
        :return s_data: df that has sorted
        """
        s_data = df
        if df is None:
            s_data = self.data.copy()
        ascending = False
        if by in self.lower_value():
            ascending = True
        s_data.sort_values(by=by, ascending=ascending, inplace=True)
        s_data.reset_index(drop=True, inplace=True)
        return s_data
