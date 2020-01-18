from cleaning_icd9_codes import convert_icd9
import pandas as pd

def add_los_columns(data):
    """Adds a new column to indicate length of stay in the hospital by
    subtracting the patient's admission time from their discharge time.
    """
    data['los'] = (pd.to_datetime(data.dischtime) - pd.to_datetime(data.admittime)).dt.total_seconds()/120
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
    data['age'] = data['age'].apply(lambda x: round(x.days / 365,2))
    data = data[data.age < 105]
    data = data.drop(columns='dob')
    print("Age column was added.")
    print("DOB column was dropped")
    return data

def selecting_firsts(data):
    """For each subject_id, selects only the first hospital visit and stores the values
    in a dictionary of subject_id and first admission admittime.
    """
    first_visit_dict = {}
    first_by_subj = data.groupby('subject_id')['admittime'].first().reset_index()
    for row in first_by_subj.index:
        first_visit_dict[first_by_subj.iloc[row, 0]] = first_by_subj.iloc[row, 1]
    return first_visit_dict

def isolating_firsts(data):
    """Creates a new dataframe with only the first visit for each unique patient.
    Leverages identifying_firsts to create a reference dictionary to identify all
    rows that are part of the patients first time visits. There should be an equal
    number of unique subject_ids in the origonal and new dataset."""

    unique_subjs_in_original_data = data.subject_id.nunique()
    first_visit_dict = selecting_firsts(data)
    first_visit_only = pd.DataFrame(columns=data.columns)

    for k, v in first_visit_dict.items():
        single_subj = data[(data.subject_id == k) & (data.admittime == v)]
        first_visit_only = first_visit_only.append(single_subj, ignore_index=True)

    new_data_unique_subjs = first_visit_only.subject_id.nunique()
    new_data_unique_hadm = first_visit_only.hadm_id.nunique()

    if unique_subjs_in_original_data == new_data_unique_subjs:
        print(f"There are {new_data_unique_subjs} unique subject_ids in the origonal and new dataset and {new_data_unique_hadm} unique hadm_ids.")
    else:
        print(f"Something went wrong. There are {new_data_unique_subjs} in the new dataset and {unique_subjs_in_original_data} in the origonal.")
    return first_visit_only

def removing_dead_subjects(data):
    """Removes all subjects that died while in the hospital as their length of stay is
    not indicative of a standard patient's LOS"""
    data = data[data.deathtime.isna()]
    data = data.drop(columns = ['deathtime'])
    print("Patients who died in the hospital were removed.")
    return data

def converting_langauge(data):
    """Consolidates languages to English, Unkown, and Other."""
    data.language = data.language.fillna('UNKNOWN')
    ind_language = list(data.columns).index('language')
    for i in range(data.shape[0]):
        if (data.iloc[i, ind_language] == 'ENGL'):
            data.iloc[i, ind_language] = 'ENGL'
        elif (data.iloc[i, ind_language] == 'UNKNOWN'):
            data.iloc[i, ind_language] = 'UNKNOWN'
        elif (data.iloc[i, ind_language] != 'ENG'):
            data.iloc[i, ind_language] = 'OTHER'
    print("Languages were cleaned.")
    return data

def converting_marital_status(data):
    """Consolidates marital status to currently married, single, was MARRIED
    and unkown
    """
    data.language = data.language.fillna('UNKNOWN')
    ind_ms = list(data.columns).index('marital_status')
    for i in range(data.shape[0]):
        if (data.iloc[i, ind_ms] == 'UNKNOWN (DEFAULT)'):
            data.iloc[i, ind_ms] = 'UNKOWN'
        elif (data.iloc[i, ind_ms] == 'MARRIED'):
            data.iloc[i, ind_ms] = 'CURRENTLY_MARRIED'
        elif (data.iloc[i, ind_ms] != 'SINGLE'):
            data.iloc[i, ind_ms] = 'SINGLE'
        else:
            data.iloc[i, ind_ms] = 'WAS_MARRIED'
    print("Marital status was cleaned.")
    return data

def converting_admission_location(data):
    """Consolidates admission location to unknown, referral, ER, or transfer"""
    data.admission_location = data.admission_location.fillna('UNKNOWN')
    ind_al = list(data.columns).index('admission_location')
    for i in range(data.shape[0]):
        if (data.iloc[i, ind_al] == 'CLINICAL REFERRAL/PREMATURE') | (data.iloc[i, ind_al] == 'PHYS REFERRAL/NORMAL DELI'):
            data.iloc[i, ind_al] = 'REFERRAL'
        else:
            continue
    print("Admissions locations were cleaned.")
    return data

def converting_religions(data):
    """Consolidates religions to unkown, other, catholic, protestant quaker, christian scientist,
    buddhist, jewish, and muslim
    """
    data.religion = data.religion.fillna('UNKNOWN')
    ind_religion = list(data.columns).index('religion')
    for i in range(data.shape[0]):
        if (data.iloc[i, ind_religion] == 'UNOBTAINABLE') | (data.iloc[i, ind_religion] == 'NOT SPECIFIED'):
            data.iloc[i, ind_religion] = 'UNKNOWN'
        else:
            continue
    print("Religions were cleaned.")
    return data

def converting_ethnicity(data):
    """Consolidates ethnicity to black/african american, white, unknown/not-specified, asian,
    hispanic/latino, american indian/alaska native federally recognized tribe, other
    """
    data.ethnicity = data.ethnicity.fillna('UNKNOWN')
    ind_ethnicity = list(data.columns).index('ethnicity')
    for i in range(data.shape[0]):
        if (data.iloc[i, ind_ethnicity] == 'HISPANIC/LATINO - PUERTO RICAN') | (data.iloc[i, ind_ethnicity] == 'HISPANIC OR LATINO'):
            data.iloc[i, ind_ethnicity] = 'HISPANIC/LATINO'
        else:
            continue
    print("Ethnicities were cleaned.")
    return data

def clean_data(data):
    """Takes in the dataframe and cleans data by performing the following actions: adding length
    of stay column, adding age column, selecting first time visits only, removing subjects who
    died in the hospital, and consolidating the responses for language, marital status, admit location,
    religion, and ethnicity.
    """
    with_los_col = add_los_columns(data)
    with_age_col = creating_age_column(with_los_col)
    first_visits_only = isolating_firsts(with_age_col)
    only_living_subj = removing_dead_subjects(first_visits_only)
    langauge_cleaned = converting_langauge(only_living_subj)
    marital_stat_cleaned = converting_marital_status(langauge_cleaned)
    admit_location_cleaned = converting_admission_location(marital_stat_cleaned)
    relig_cleaned = converting_religions(admit_location_cleaned)
    ethnicity_cleaned = converting_ethnicity(relig_cleaned)
    with_icd9_diagnosis = convert_icd9(ethnicity_cleaned)
    return(with_icd9_diagnosis)
