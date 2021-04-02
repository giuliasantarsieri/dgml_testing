import pandas as pd
import pandas_profiling
from generate_csv import *
#get last version of csv as a dictionary
file = pd.read_csv('output_csv/openml_table.csv',index_col=0)
csv_dictionary = file.to_dict(orient='list')
#read a given csv file
url = input('Please enter url of new dataset:')
data = read_data(url)
#generate a list of informations extracted from its pandas profiling
L = get_info_from_profiler(data)
#ask the user to manually enter some information
resource_id = input('Please enter resource_id of the new dataset:')
has_label = input('Please enter VRAI if your dataset is certified, otherwise enter FAUX:')
title = input('Please enter the title of your dataset:')
description = input('Please enter a short description of the dataset:')
topic = input('Please enter the topic of your dataset:')
task = input('Please enter the ML task for this dataset:')
target_variable = input('Please enter the target variable of the ML task:')
model_metric = input('Please enter the chosen model metric:')
best_value = input('Please enter the best value of the metric:')
best_model = input('Please enter the name of the best model:')
dgf_dataset_url = input('Please enter the url of the dgf page containing the dataset:')
dgf_resource_url = input('Please enter the url of the resource (csv) from dgf:')
automl_url = input('Please enter the url of the automl report:')
profile_url = input('Please enter the url of the Pandas Profiling report:')
dict_url = input('Please enter the url of the dictionary of variables. If not available press Enter:')
etalab_xp_url = input('Please enter the url of the Etalab notebook:')
external_xp_url = input('Please enter the url of the external example.  If not available press Enter:')
#enter these info in the csv
J = [['resource_id',resource_id],['has_label',has_label],['title',title],['description',description],['topic',topic],['task',task],['target_variable',target_variable],['model_metric',model_metric],['best_value',best_value],['best_model',best_model],['dgf_dataset_url', dgf_dataset_url],['dgf_resource_url',dgf_resource_url],['automl_url',automl_url],['profile_url',profile_url],['dict_url',dict_url],['etalab_xp_url',etalab_xp_url],['external_xp_url',external_xp_url]]
new_dictionary = add_to_dict(csv_dictionary,L,J)
update_csv(new_dictionary)
print("Successfully updated openml_table.csv")