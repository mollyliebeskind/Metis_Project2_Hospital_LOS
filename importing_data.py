import pandas as pd

def import_files(file_name):
    """Reads in all CSV files and converts them to dataframes"""
    print(f"{file_name} imported")
    return pd.read_csv(f'data/{file_name}.csv')

def creating_dataframe(admission, patients, diagnosis, services):
    """Takes in individual dataframes and combines them on common columns"""
    adm = import_files(admission)
    pat = import_files(patients)
    diag = import_files(diagnosis)
    serv = import_files(services)
    raw_data = adm.merge(pat, how='outer', on='subject_id')
    raw_data = raw_data.merge(diag, how='outer', on=('subject_id', 'hadm_id'))
    raw_data = raw_data.merge(serv, how='outer', on=('subject_id', 'hadm_id'))
    print("Sucess, all files were merged.")
    return raw_data

def selecting_columns(data):
    """Selects only relevant columns from the dataframe"""
    keeping_cols = ['subject_id',
                'hadm_id',
                'admittime',
                'dischtime',
                'admission_type',
                'admission_location',
                'insurance',
                'language',
                'religion',
                'marital_status',
                'ethnicity',
                'gender',
                'dob',
                'deathtime',
                'icd9_code',
                'curr_service'
               ]
    raw_data = data[keeping_cols]
    print("Success, appropriate columns were selected.")
    return raw_data

def import_data():
    raw_data = creating_dataframe('admissions', 'patients', 'diagnoses_icd', 'services')
    raw_data_selected_cols = selecting_columns(raw_data)
    print("Success, files imported and columns selected.")
    return raw_data_selected_cols
