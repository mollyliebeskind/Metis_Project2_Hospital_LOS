import pandas as pd
import numpy as np

def add_los_columns(data):
    """Adds a new column to indicate length of stay in the hospital by
    subtracting the patient's admission time from their discharge time.
    Removes outliers in the data above 2 standard deviations.
    """
    data['los'] = (pd.to_datetime(data.dischtime) - pd.to_datetime(data.admittime)).dt.total_seconds()/86400
    data = data.drop(columns=['dischtime'])
    print("Length of stay column was added.")
    return data

def creating_age_column(data):
    """Creates an age column by subtracting the patient's date of birth from their admittime.
    Then removes any ages greater than 105 which are caused by a date adjustment error (see note).
    Note: for each user, dates have been modified by a random number of years. The modification
    number of years is consistent within a patient's listings accross all columns.
    """
    data['age'] = (pd.to_datetime(data.admittime).dt.date - pd.to_datetime(data.dob).dt.date)
    data['age'] = data['age'].apply(lambda x: round(x.days / 365,0))
    data = data[data.age < 105]
    data = data.drop(columns='dob')
    print("Age column was added.")
    print("DOB column was dropped")
    return data

def removing_dead_subjects(data):
    """Removes all subjects that died while in the hospital as their length of stay is
    not indicative of a standard patient's LOS"""
    data = data[data.deathtime.isna()]
    data = data.drop(columns = ['deathtime'])
    print("Patients who died in the hospital were removed.")
    return data

def isolating_firsts(data):
    """isolates rows to only the first visit for each patient to remove
    any autocorrelatino impact."""
    grp_by_first_vis = data.groupby(['subject_id', 'hadm_id'])['admittime'].agg(['first']).reset_index()
    firsts_visits = grp_by_first_vis.merge(data, how='left', on=('subject_id', 'hadm_id'))
    print('Data isolated to first time visits only')
    firsts_visits = firsts_visits.drop(columns=['admittime', 'first'])
    return firsts_visits

def drop_nulls(data):
    """removes all rows with null values from the dataset"""
    data.first_careunit = data.first_careunit.fillna('not_admitted')
    null_dropped_data = data.dropna()
    print('Null values dropped.')
    return null_dropped_data

def add_cols_remove_rows(data):
    los_added = add_los_columns(data)
    add_age = creating_age_column(los_added)
    removed_daed = removing_dead_subjects(add_age)
    first_visits = isolating_firsts(removed_daed)
    null_dropped = drop_nulls(first_visits)
    return null_dropped
