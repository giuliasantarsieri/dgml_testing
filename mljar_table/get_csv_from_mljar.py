import requests
import lxml.html as lh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


def get_csv_from_mljar_html(mljar_url):
    """Returns a csv table named *resource_id.csv* of the mljar profiling given its url
    --------------------------------------------------
    :param        :mljar_url: url of the mljar profiling of a given dataset
    :type         :mljar_url: string"""
    # store website content and parse data:
    page = requests.get(mljar_url)
    doc = lh.fromstring(page.content)
    tr_elements = doc.xpath('//tr')
    # Create empty list and for each row, store the header and an empty list
    col = []
    i = 0
    for t in tr_elements[0]:
        i += 1
        name = t.text_content()
        col.append((name, []))
    # fill col with the values of the dataframe to be
    for j in range(1, len(tr_elements)):
        T = tr_elements[j]
        # If row is not of size 6, the //tr data is not from our table
        if len(T) != 6:
            break
        i = 0
        for t in T.iterchildren():
            data = t.text_content()
            if i > 0:
                try:
                    data = int(data)
                except:
                    pass
            col[i][1].append(data)
            i += 1
    # get pandas dataframe
    Dict = {title: column for (title, column) in col}
    df = pd.DataFrame(Dict)
    # get csv
    df.to_csv('output_mljar_csv/' + mljar_url.split('/')[-2] + '.csv')
    return df


def plot_mljar_table(dataframe, mljar_url):
    """Returns a plot from the mljar dataframe with train_time of the x-axis and metric_value on the y axis
    -------------------------------------------------
    :param       :dataframe: dataframe mljar
    :type        :dataframe: pandas datafrme
    :param       :mljar_url: url of mljar report
    :type        :mljar_url: string"""
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    dataframe['train_time'] = dataframe['train_time'].astype(float)
    dataframe['metric_value'] = dataframe['metric_value'].astype(float)
    ax.plot(dataframe['train_time'], dataframe['metric_value'], 'o')
    dataframe['name'] = dataframe['name'].astype('category')
    groups = dataframe.groupby("name")
    for name, group in groups:
        plt.plot(group["train_time"], group["metric_value"], marker="o", linestyle="", label=name)
    for i, txt in enumerate(dataframe['name']):
        ax.annotate(txt, (dataframe['train_time'][i], dataframe['metric_value'][i]), va='bottom')
    if dataframe['metric_type'][1] == 'logloss':
        ax.set(xlabel='train_time (seconds)', ylabel='metric_value (logloss)')
    else:
        ax.set(xlabel='train_time(seconds)', ylabel='metric_value (rmse)')
    figure = plt.savefig('plots/' + mljar_url.split('/')[-2] + '.png')
    return figure


arbres = get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_arbres/README.html')
plot_mljar_table(arbres, 'https://etalab-ia.github.io/open_ML/automodels/AutoML_arbres/README.html')

airbnb=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_airbnb/README.html')
plot_mljar_table(airbnb,'https://etalab-ia.github.io/open_ML/automodels/AutoML_airbnb/README.html')

donn_carr=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_donn_carr/README.html')
plot_mljar_table(donn_carr,'https://etalab-ia.github.io/open_ML/automodels/AutoML_donn_carr/README.html')

emiss_veh=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_emiss_veh/README.html')
plot_mljar_table(emiss_veh,'https://etalab-ia.github.io/open_ML/automodels/AutoML_emiss_veh/README.html')

agrybalise=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_agribalyse/README.html')
plot_mljar_table(agrybalise,'https://etalab-ia.github.io/open_ML/automodels/AutoML_agribalyse/README.html')

conc_poll_reg=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_conc_poll_reg/README.html')
plot_mljar_table(conc_poll_reg,'https://etalab-ia.github.io/open_ML/automodels/AutoML_conc_poll_reg/README.html')

conc_poll_class=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_conc_poll_class/README.html')
plot_mljar_table(conc_poll_class,'https://etalab-ia.github.io/open_ML/automodels/AutoML_conc_poll_class/README.html')

alim_conf=get_csv_from_mljar_html('https://etalab-ia.github.io/open_ML/automodels/AutoML_alimconf/README.html')
plot_mljar_table(alim_conf,'https://etalab-ia.github.io/open_ML/automodels/AutoML_alimconf/README.html')
