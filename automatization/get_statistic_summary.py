import pandas_profiling
from pandas_profiling import ProfileReport
from get_dataset import *


def get_statistic_summary(id):
    """Returns a csv file containing all the relevant dataset statistics from pandas profiling.
    -----------------------------------------------
    :param:       id: id of the dataset
    :type:        id: string
    """
    data = load_dataset(id)
    profiler_report = ProfileReport(data, minimal=True).get_description()
    table = profiler_report['table']
    rows_nb = table['n']  # nb of rows
    cols_nb = table['n_var']  # nb of columns
    table['types'] = {str(k): int(v) for k, v in table['types'].items()}
    cat = table['types']['Categorical']  # numerical/categorical variables
    num = table['types']['Numeric']
    messages = profiler_report["messages"]
    warnings = ["HIGH_CARDINALITY", "HIGH_CORRELATION"]  # high cardinality and high correlation
    nb_high_card = 0
    nb_high_corr = 0
    for message in messages:
        message_type = message.message_type.name
        if message_type in warnings[0]:
            nb_high_card += 1
        elif message_type in warnings[1]:
            nb_high_corr += 1
    mis = round(table['p_cells_missing'], 2) * 100  # missing values percentage
    column_names = ["Number of rows", "Number of columns", "Numerical variables", "Categorical variables",
                    "Percentage of missing values", "High cardinality variables"
        , "High correlation variables"]
    df = pd.DataFrame(columns=column_names,index_col=0)
    df.loc[1] = [rows_nb, cols_nb, num, cat, mis, nb_high_card, nb_high_corr]
    df.to_csv('statistics_csv/'+id + '.csv')

