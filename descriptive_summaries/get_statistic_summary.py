import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport

def get_statistic_summary(dgf_resource_url):
    """Returns a csv file containing all the dataset  from pandas profiling"""
    data = pd.read_csv(dgf_resource_url)
    profiler_report = ProfileReport(data, minimal=True).get_description()
    # nb of rows
    table = profiler_report['table']
    rows_nb = table['n']
    # nb of columns
    cols_nb = table['n_var']
    # numerical/categorical variables
    table['types'] = {str(k): int(v) for k, v in table['types'].items()}
    cat = table['types']['Categorical']
    num = table['types']['Numeric']
    #high cardinality and high correlation
    messages = profiler_report["messages"]
    warnings = ["HIGH_CARDINALITY", "HIGH_CORRELATION"]
    nb_high_card = 0
    nb_high_corr = 0
    for message in messages:
        message_type = message.message_type.name
        if message_type in warnings[0]:
            nb_high_card += 1
        elif message_type in warnings[1]:
            nb_high_corr += 1
    # missing values percentage
    mis = round(table['p_cells_missing'], 2) * 100
    #retrieve id
    id = dgf_resource_url.split('/')[-1]
    column_names = ["Number of rows", "Number of columns", "Numerical variables", "Categorical variables","Percentage of missing values","High cardinality variables"
                    ,"High correlation variables"]
    df = pd.DataFrame(columns=column_names)
    df.loc[1] = [rows_nb,cols_nb,num,cat,mis,nb_high_card,nb_high_corr]
    df.to_csv(id+'.csv')

get_statistic_summary('https://www.data.gouv.fr/fr/datasets/r/123e1c18-37e0-4147-ad65-768320387800')