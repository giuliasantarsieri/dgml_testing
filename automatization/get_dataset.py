import pandas as pd
import requests
import math


def latest_catalog():
    """This function returns the pandas dataframe of the latest version of dgf resource catalog
    (https://www.data.gouv.fr/en/datasets/catalogue-des-donnees-de-data-gouv-fr/#_)"""
    dgf_catalog = 'https://www.data.gouv.fr/fr/datasets/r/4babf5f2-6a9c-45b5-9144-ca5eae6a7a6d'  # latest url of the catalog
    dgf_catalog_df = pd.read_csv(dgf_catalog, delimiter=";", encoding='utf-8')
    pd.set_option('display.max_colwidth', None)  # to stop pandas from "cutting" long urls
    return dgf_catalog_df

def info_from_catalog(id):
    """This function returns a dictionary containing : the resource url, the resource format and the url of its data.gouv.fr page
    --------------------------------------------
    :param:     id: id of the dgf resource
    :type:      id: string"""
    catalog = latest_catalog()
    url = catalog[catalog['id'] == id]['url'].values.item()
    file_format = catalog[catalog['id'] == id]['format'].values.item()
    dgf_page = catalog[catalog['id'] == id]['dataset.url'].values.item()
    catalog_dict = {'url_resource': url, 'format': file_format,'url_dgf':dgf_page}
    return catalog_dict



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
    elif "\t" in text:
        sep = "\t"
    else:
        raise TypeError('separator not detected')
    url_dict = {'encoding': encoding, 'separator': sep}
    return url_dict


def load_dataset(id):
    """This function loads a csv in the datasets folder/creates a pandas datafram given its id if the dataset is referenced by data.gouv.fr.
    Otherwise, you get an error and you should manually upload it.
    Remark: on data.gouv.fr, datasets are available in various "formats": json, shp, csv, zip, document, xls, pdf, html, xlsx,geojson etc.
    to this day, our repository only contains files with .csv,.txt, .xls extensions, therefore we only treat these extensions.
    -------------------
    :param:     id: id of the dgf resource (must be a txt, csv or xls file)
    :type:      id: string"""
    url = info_from_catalog(id)['url_resource']
    headers = requests.head(url).headers
    downloadable = 'attachment' in headers.get('Content-Disposition', '')
    if downloadable is True:  # if the dataset is referenced
        file_format = info_from_catalog(id)['format']
        request = requests.get(url)
        delimiter = detect_csv(request)['separator']
        encoding = detect_csv(request)['encoding']
        if (file_format == 'csv') or (math.isnan(
                file_format) is True):  # if the format is not available on dgf, we assume it is a csv by default
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, index_col=0)
        elif file_format == 'txt':
            dataframe = pd.read_table(url, sep=delimiter, encoding=encoding, index_col=0)
        elif (file_format == 'xls') or (file_format == 'xlsx'):
            dataframe = pd.read_excel(url, sheet_name=None, index_col=0)
        elif (file_format == 'zip') or (url.rsplit('.', 1)[-1] == 'zip'):
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='zip',
                                    error_bad_lines=False, index_col=0)
        elif (file_format == 'gz') or (url.rsplit('.', 1)[-1] == 'gz'):
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='gzip',
                                    error_bad_lines=False, index_col=0)
        elif (file_format == 'bz2') or (url.rsplit('.', 1)[-1] == 'bz2'):
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='bz2',
                                    error_bad_lines=False, index_col=0)
        elif (file_format == 'xz') or (url.rsplit('.', 1)[-1] == 'xz'):
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='xz',
                                    error_bad_lines=False, index_col=0)
        else:
            raise TypeError(
                'Please choose a dataset that has one of the following extensions: .csv, .txt, .xls or choose a zipped file')
        #dataframe.to_csv('datasets/' + id + '.csv')
        return dataframe
    else:
        dgf_page = info_from_catalog(id)['url_dgf']
        raise Exception(
            'This id is associated to a dataset not referenced by data.gouv.fr. \n Please check the dataset here:' + dgf_page + '\n Please manually load it in the datasets folder and name it: id.csv')

# Remark on separators detection : the 'python engine' in pd.read_csv/read_table  works pretty well most of the time. However, it does not handle well some
# exceptions (see for instance the dataset: 90a98de0-f562-4328-aa16-fe0dd1dca60f).
# Improvements/to do: detect_csv:  separators detection should be handled better (not very robust, possibly does not cover all the exceptions)
