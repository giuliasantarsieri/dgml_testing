import pandas as pd
import requests

def latest_catalog():
    """This function returns the pandas dataframe of the latest version of dgf resource catalog
    (https://www.data.gouv.fr/en/datasets/catalogue-des-donnees-de-data-gouv-fr/#_)"""
    dgf_catalog = 'https://www.data.gouv.fr/fr/datasets/r/4babf5f2-6a9c-45b5-9144-ca5eae6a7a6d'  # latest url of the catalog
    dgf_catalog_df = pd.read_csv(dgf_catalog, delimiter=";", encoding='utf-8')
    pd.set_option('display.max_colwidth', None)  # to stop pandas from "cutting" long urls
    return dgf_catalog_df

catalog = latest_catalog()

def get_resource_url(id):
    """Given its id, this function returns the url of a given dgf resource.
    -----------------------------
    :param:     id: id of the dgf resource
    :type:      id: string"""
    resource = catalog
    url = resource[resource['id']==id]['url'].values.item()
    return url

def detect_csv(request):
    """Given the url request for a csv or txt file, this function returns a dictionary containing the csv encoding and separator.
    -------------------------------------------
    :param        url: url containing the csv
    :type         url: string"""
    text = request.text[0:100]
    encoding = request.encoding
    if ";" in text:
        sep = ";"
    elif "," in text:
        sep = ","
    elif "|" in text:
        sep = "|"
    else:
        raise TypeError('separator not detected')
    url_dict = {'encoding':encoding,'separator':sep}
    return url_dict

def load_csv(id):
    """This function loads a csv in the datasets folder given its id if the dataset is referenced by data.gouv.fr. Otherwise, you get
    an error and you should manually upload it. The function returns the pandas dataframe associated to the csv if the csv is referenced
    -------------------
    :param:     id: id of the dgf resource
    :type:      id: string"""
    url = get_resource_url(id)
    if 'data' in url.rsplit('://www.', 1)[-1]: # if the dataset is referenced
        request = requests.get(url)
        delimiter = detect_csv(request)['separator']
        encoding = detect_csv(request)['encoding']
        if encoding==None:
            encoding = 'latin-1'
        if url.rsplit('.', 1)[-1]=='zip': # handling zipped files
            compression = 'zip'
            error_bad_lines = False
        elif url.rsplit('.', 1)[-1]=='gzip':
            compression = 'gzip'
            error_bad_lines = False
        else:
            compression = 'infer'
            error_bad_lines = True
        dataframe = pd.read_csv(url,encoding=encoding,sep=delimiter,index_col=0,error_bad_lines=error_bad_lines)
        dataframe.to_csv('datasets/'+id+'.csv')
        return dataframe
    else:
        raise Exception('This dataset is associated with a dataset not referenced by datagouv.fr \n Please manually load it in the datasets folder and name it: id.csv')