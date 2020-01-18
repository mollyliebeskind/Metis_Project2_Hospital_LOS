import numpy as np
from bs4 import BeautifulSoup
from IPython.core.display import display, HTML
import requests

def load_for_scraping():
    print("Scraping beginning.")
    url = "https://en.wikipedia.org/wiki/List_of_ICD-9_codes_E_and_V_codes:_external_causes_of_injury_and_supplemental_classification"
    response = requests.get(url)
    status = response.status_code
    if status == 200:
        page = response.text
        soup = BeautifulSoup(page, "lxml")
        return soup
    else:
        print(f"Unable to scrape Wikipedia - status code: {status}")
    return

def scraping_icd9():
    """Scrapes the ICD-9 wikipedia page for ICD-9 codes and diagnoses"""
    soup = load_for_scraping()
    tables = soup.find(class_ = 'wikitable')
    diagnosis_dict = {}
    rows = [row for row in tables.find_all('tr')]
    for row in rows[1:]:
        items = row.find_all('td')
        link = items[1].find('a')
        num_range = link.text
        name_column= items[2]
        name = name_column.text[:-2]
        diagnosis_dict[num_range] = name
    print("ICD9 codes scraped from Wikipedia.")
    return diagnosis_dict

def create_icd_indicator_col(data):
    """Creates a support column with only numerical values to indicate ICD9 diagnosis.
    """
    indicator = []
    data['icd_indicator'] = np.nan
    data.icd9_code = data.icd9_code.astype(str)

    for val in data.icd9_code:
        if val[0] == 'V':
            indicator.append(.1)
        if val[0] == 'E':
            indicator.append(.7)
        if (val[0] != 'E') & (val[0] != 'V'):
            indicator.append(float(val[:3]))
    data.icd_indicator = indicator
    print("Temp indicator column created.")
    return data

def converting_icd9_range(data):
    """Assigns a diagnosis to each ICD9 code"""

    indicator = []
    diagnosis_dict = scraping_icd9()
    keys = list(diagnosis_dict.keys())
    indicating_data = create_icd_indicator_col(data)

    #indicating_data['icd_diagnosis'] = diagnosis_dict[indicating_data.icd_range]
    for val in indicating_data.icd_indicator:
        if 1 <= val < 139:
            indicator.append(diagnosis_dict[keys[0]])
        elif 140 <= val <= 239:
            indicator.append(diagnosis_dict[keys[1]])
        elif 240 <= val <= 279:
            indicator.append(diagnosis_dict[keys[2]])
        elif 280 <= val <= 289:
            indicator.append(diagnosis_dict[keys[3]])
        elif 290 <= val <= 319:
            indicator.append(diagnosis_dict[keys[4]])
        elif 320 <= val <= 389:
            indicator.append(diagnosis_dict[keys[5]])
        elif 390 <= val <= 459:
            indicator.append(diagnosis_dict[keys[6]])
        elif 460 <= val <= 519:
            indicator.append(diagnosis_dict[keys[7]])
        elif 520 <= val <= 579:
            indicator.append(diagnosis_dict[keys[8]])
        elif 580 <= val <= 629:
            indicator.append(diagnosis_dict[keys[9]])
        elif 630 <= val <= 679:
            indicator.append(diagnosis_dict[keys[10]])
        elif 680 <= val <= 709:
            indicator.append(diagnosis_dict[keys[11]])
        elif 710 <= val <= 739:
            indicator.append(diagnosis_dict[keys[12]])
        elif 740 <= val <= 759:
            indicator.append(diagnosis_dict[keys[13]])
        elif 760 <= val <= 779:
            indicator.append(diagnosis_dict[keys[14]])
        elif 780 <= val <= 799:
            indicator.append(diagnosis_dict[keys[15]])
        elif 800 <= val <= 999:
            indicator.append(diagnosis_dict[keys[16]])
        elif val < .5:
            indicator.append(diagnosis_dict[keys[17]])
        elif .5 <= val < 1:
            indicator.append(diagnosis_dict[keys[18]])
        else:
            print(val)

    data['icd_range'] = indicator

    return data

def convert_icd9(data):
    """Calls support functions to create the ICD9 diagnosis column and then normalizes
    the columns inputs"""
    converted_data = converting_icd9_range(data)

    #converted_data['icd_range'] = converted_data['icd_range'].astype(str)
    converted_data['icd_range'] = converted_data['icd_range'].str.lower()
    converted_data['icd_range'] = converted_data['icd_range'].str.replace(' ', '_')

    converted_data = converted_data.drop(columns=['icd9_code', 'icd_indicator'])
    print("ICD9 codes converted.")

    return converted_data
