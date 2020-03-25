import pandas as pd

def import_files(file_name):
    """Reads in all CSV files and converts them to dataframes"""
    imported_file = pd.read_csv(f'full_data/{file_name}.csv')
    print(f"{file_name}.csv was imported")
    return imported_file

def creating_dataframe(admission, patients, diagnosis, services, icu):
    """Takes in individual dataframes and combines them on common columns"""
    adm = import_files(admission)
    pat = import_files(patients)
    diag = import_files(diagnosis)
    serv = import_files(services)
    icu = import_files(icu)
    print("All files loaded")
    return adm, pat, diag, serv, icu

def cleaning_column_names(data):
    data.columns = data.columns.str.strip().str.lower()
    return data

def merging_data(adm, pat, diag, serv, icu):
    """Merges all data frames on pre-identified columns: 'subject_id' and
    'hadm_id'."""
    raw_data = adm.merge(pat, how='outer', on='subject_id')
    raw_data = raw_data.merge(diag, how='outer', on=('subject_id', 'hadm_id'))
    raw_data = raw_data.merge(serv, how='outer', on=('subject_id', 'hadm_id'))
    raw_data = raw_data.merge(icu, how='outer', on=('subject_id', 'hadm_id'))
    print("All files were merged.")
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
                'religion',
                'marital_status',
                'ethnicity',
                'gender',
                'dob',
                'deathtime',
                'icd9_code',
                'curr_service',
                "first_careunit"
               ]
    raw_data = data[keeping_cols]
    print("Appropriate columns were selected.")
    return raw_data

def import_data():
    """imports and merges 5 datasets: admissions, patients, diagnoses,
    services, and icustays."""
    adm, pat, diag, serv, icu = creating_dataframe('admissions_data', 'patient_data', 'diagnoses_icd_data', 'services_data', 'icustays')
    adm_c = cleaning_column_names(adm)
    pat_c = cleaning_column_names(pat)
    diag_c = cleaning_column_names(diag)
    serv_c = cleaning_column_names(serv)
    icu_c = cleaning_column_names(icu)
    merged_data = merging_data(adm_c, pat_c, diag_c, serv_c, icu_c)
    raw_data_selected_cols = selecting_columns(merged_data)
    print("Files imported.")
    print("Columns selected.")
    return raw_data_selected_cols 
