from get_dataset import *
from get_statistic_summary import *
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from supervised.automl import AutoML
import IPython
import markdown


# Minimal rules to be followed to get mljar working
# (0. What if a dataset is really not adequate for Machine Learning?)
# 1. No nan in the target variable
# 2. Drop columns with > 70%?? of  missing values because useless?
# 3. Drop columns labeled as unsupported by Pandas Profiling
# 4. Check for the proper data types:
# a. Target variable type must be: integer or float if regression,categorical if classification
# b. Check if a variable has been badly labelised (ex. a numeric value that is in a string format and is therefore classified as categorical
# c. Dates format?
# d. url and long texts (ex. more then 10 words??) are unsupported
# e. what about High Cardinality?


def prepare_to_mljar(id, target_variable,task):
    """This function returns a dataset properly prepared to be used by mljar
    :param:     id: id of the dgf resource (must be a txt, csv or xls file)
    :type:      id: string
    :param:     target_variable: name of the target variable of the chosen ML task
    :type:      target_variable: string
    :param:     task: chosen ML task (regression, binary_classification, multi_classification
    :type:      task: string
    """
    data = load_dataset(id)
    data = data[data[target_variable].isna() == False]  # handle NaN in target variable
    list_rej = rejected_var(id)
    data = data.drop(columns=list_rej)  # drop unsupported variables
    data = data.drop(columns=[col for col in data.columns if
                              data[col].isna().sum() / len(data) > 0.7])  # drop columns with more than 70% of NaN
    pandas_prof = generate_pandas_profiling(id)
    description = pandas_prof.get_description()
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
    elif (task == 'binary_classification') or (task == 'multi_classification'):
        if type_target == 'Unsupported':
            raise TypeError('Please choose another target variable. This target variable is unsupported.')
    else:
        raise ValueError('Please enter one of the following words as task: regression, binary_classification, multi_classification')
