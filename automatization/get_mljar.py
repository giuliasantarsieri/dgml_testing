from get_dataset import *
from get_statistic_summary import *
import numpy as np
from sklearn.model_selection import train_test_split
from supervised.automl import AutoML
import IPython
import markdown


# Minimal rules to be followed to get mljar working
# (0. What if a dataset is really not adequate for Machine Learning?)
# 1. No nan in the target variable
# 2. Drop columns with > 70%?? of  missing values because useless?
# 3. Drop columns labeled as unsupported by Pandas Profiling and redundant columns
# 4. Check for the proper data types:
# a. Target variable type must be: integer or float if regression,categorical if classification
# b. Check if a variable has been badly labelised (ex. a numeric value that is in a string format and is therefore classified as categorical
# -> this is hard to fix because fixing it can cause different problems (ex. see geo_2d in ce203343-6ed9-4fd3-b310-e553ae437f6d dataset)
# c. url and long texts are unsupported
# d. what about High Cardinality?
# e. Dates?


def prepare_to_mljar(data, target_variable, task, profiling):
    """This function returns a dataset properly prepared to be used by mljar
    :param:     id: id of the dgf resource (must be a txt, csv or xls file)
    :type:      id: string
    :param:     target_variable: name of the target variable of the chosen ML task
    :type:      target_variable: string
    :param:     task: chosen ML task (regression, binary_classification, multi_classification
    :type:      task: string
    """
    data = data[data[target_variable].isna() == False]  # handle NaN in target variable
    list_rej = rejected_var(profiling)
    if len(list_rej)!=0:
        data = data.drop(columns=list_rej)  # drop unsupported variables
    data = data.drop(columns=[col for col in data.columns if
                              data[col].isna().sum() / len(data) > 0.7])  # drop columns with more than 70% of NaN
    data = data.T.drop_duplicates().T   #drop redundant columns if there are any
    # check if the type of the target variable is right
    description = profiling.get_description()
    type_target = str(description['variables'][target_variable]['type'])
    if task == 'regression':
        if type_target == 'Categorical':
            data[target_variable] = data[target_variable].str.replace(',', '.', regex=True)
            try:
                data[target_variable] = data[target_variable].astype(float)
            except ValueError:
                raise TypeError('Please modify the target variable: values must be numeric.')
        elif type_target == 'Unsupported':
            raise TypeError('Please choose another target variable. This target variable is unsupported.')
        else:
            print('The type of your target variable is ok.')
    elif (task == 'binary_classification') or (task == 'multi_classification'):
        if type_target == 'Unsupported':
            raise TypeError('Please choose another target variable. This target variable is unsupported.')
        else:
            print(
                'The type of your target variable is ok. AutoML will tranform it into a categorical variable if needed.')
    else:
        raise ValueError(
            'Please enter one of the following words as task: regression, binary_classification, multi_classification')
    #pandas_cat_col = [key for key, value in description['variables'].items() if
                      #str(value['type']) == 'Categorical']  # get rid of variables containing long text
    #long_text_cols = [(data[col].str.split().str.len().mean(), col) for col in pandas_cat_col if
                      #np.any([isinstance(val, str) for val in data[col]])]
    #columns_to_drop = [long_text_cols[i][1] for i in range(len(long_text_cols)) if long_text_cols[i][0] > 15]
    #data = data.drop(columns=columns_to_drop)
    return data


def generate_mljar(data, target_variable):
    """This function takes a properly prepared dataframe and performs AutoML on it. The generated output is the html report.
    ------------------------------------------------
    :param:     :data: dataframe on which we want to perform a given ML task
    :type:      :data: pandas dataframe
    :param:     :target_variable: chosen target_variable for the ML task
    :type:      :target_variable: string"""
    y = data[target_variable].values
    X = data.drop(columns=[target_variable])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
    automl = AutoML(total_time_limit=5 * 60, mode='Explain')
    automl.fit(X_train, y_train)
    predictions = automl.predict(X_test)
    automl.report()
