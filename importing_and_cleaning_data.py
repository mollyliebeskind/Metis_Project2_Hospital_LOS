"""
This script imports csv files downloaded from MIT's patient database. The files
are turned into Pandas dataframes and a series of joins and cleaning steps are
implemented. The final dataframe is then saved as a csv file.
"""

import pandas as pd

def importing(files_list):
    """Retruns a list of pandas dataframes generated from the files listed
    in the input argument.
    """

    dataframes = []

    for file in files_list:
        imported_df = pd.read_csv(f'full_data/{file}.csv')(file)
        imported_df.columns = imported_df.columns.str.strip().str.lower()
        dataframes.append(imported_df)

    return dataframes


def merging_data(dataframes_list):
    """Returns a single pandas dataframe that is a combination of the
    dataframes in the input list. All merges are outer joins on subject_id and
    hadm_id when available. Only features used for predicting length of stay
    are returned in the final dataframe.
    """

    adm, pat, diag, serv, icu = dataframes_list

    raw_data = adm.merge(pat, how='outer', on='subject_id')
    raw_data = raw_data.merge(diag, how='outer', on=('subject_id', 'hadm_id'))
    raw_data = raw_data.merge(serv, how='outer', on=('subject_id', 'hadm_id'))
    raw_data = raw_data.merge(icu, how='outer', on=('subject_id', 'hadm_id'))

    keeping_cols = ['subject_id', 'hadm_id', 'admittime', 'dischtime',
                    'admission_type', 'admission_location', 'insurance',
                    'religion', 'marital_status', 'ethnicity', 'gender', 'dob',
                    'deathtime', 'icd9_code', 'curr_service', "first_careunit"
                    ]

    raw_data = raw_data[keeping_cols]

    return raw_data

def data_cleaning(data):
    """Returns a dataframe with the following cleaning implementations.
       - Drop patients who died in the hospital as LOS is not accurate for
       them
       - Select only first time visits to reduce autocorrelation
       - Indicate if a patient was admitted to the ICU
       - Drop null values

    """
    # Dropping any patience who died while in the hospital
    data = data[data.deathtime.isna()]
    data = data.drop(columns=['deathtime'])

    # Isolate rows to only first time visits for each patients
    first_vis_grp = data.groupby(['subject_id', 'hadm_id'])['admittime'] \
                    .agg(['first']).reset_index()
    first_vis = first_vis_grp.merge(data, how='left',
                                    on=('subject_id', 'hadm_id'))
    first_vis = first_vis.drop(['first'], axis=1)

    # Indicate if patient was admitted to the ICU
    first_vis.first_careunit = first_vis.first_careunit.fillna('not_admitted')

    # Drop remaining null values
    first_vis = first_vis.dropna()

    return first_vis


def main():
    """Imports csv files from the MIT hospital database and saves a single
    merged and cleaned dataframe with selected columns as a csv file."""

    dataframes = importing(['admissions_data', 'patient_data',
                            'diagnoses_icd_data', 'services_data',
                            'icustays'])
    merged_data = merging_data(dataframes)
    cleaned = data_cleaning(merged_data)

    cleaned.to_csv('raw_hospital_data.csv')

main()
