import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport

def read_data(path):
    """Returns a pandas dataframe given the path or the url of a csv file"""
    dataframe = pd.read_csv(path)
    return dataframe

def get_info_from_profiler(data):
    """Returns a list of list of the information extracted from the Pandas Profiling of the dataframe data
    :param      data:  Dataframe
    :type       dim:  Pandas DataFrame"""
    profiler_report = ProfileReport(data, minimal=True).get_description()
    #nb of rows
    table = profiler_report['table']
    rows_nb = table['n']
    #nb of columns
    cols_nb = table['n_var']
    #numerical/categorical variables
    table['types']= {str(k):int(v) for k,v in table['types'].items()}
    cat = table['types']['Categorical']
    num = table['types']['Numeric']
    #info about high cardinality
    messages = [profiler_report['messages'][i] for i in range(0,len(profiler_report['messages']))]
    if 'HIGH_CARDINALITY'in str(messages):
        str_card = 'Yes'
    else:
        str_card = 'No'
    #missing values
    mis = round(table['p_cells_missing'],2)*100
    L = [['nb_rows',rows_nb],['nb_cols',cols_nb],['nb_categorical_var',cat],['nb_numerical_var',num],['high_cardinality',str_card],['missing_cells_pct',mis]]
    return L

def add_to_dict(dictionary,L,J):
    """Updates previous dictionary with elements taken from a list L of new keys and items
    :param      dictionary: original dictionary
    :type       dictionary: dictionary
    :param      L: list of new extracted values
    :type       L: list of list
    :param      J: list of manually entered values
    :type       J: list of list"""
    for i in range(0,len(L)):
        for k,v in dictionary.items():
            if k == L[i][0]:
                dictionary[k].append(L[i][1])
    for j in range(0,len(J)):
        for k,v in dictionary.items():
            if k == J[j][0]:
                dictionary[k].append(J[j][1])
    return dictionary

def update_csv(dictionary):
    """Returns a csv containing the data from the dictionary"""
    df = pd.DataFrame.from_dict(dictionary)
    csv = df.to_csv('output_csv/openml_table.csv')