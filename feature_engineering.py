"""
This script loads in the raw MIT data and returns a new dataframe with
feature engineering applied. Engineered features include the following.

Newly generated features:
  -- Hostpial length of stay (dependent variable)
  -- Patient age

Compressed features:
  -- Admission type
  -- Age
  -- Care unit
  -- Current service
  -- Ethnicity
  -- Marital Status
  -- Religion
  -- Admission Location
  -- ICD9 Codes
"""

import pandas as pd

def new_features(data):
    """Returns the dataframe with two additional features: length of stay in
    the hospital and patient age.
    """

    # Add length of stay column as the dependent variable, 'y'
    start = pd.to_datetime(data.admittime)
    end = pd.to_datetime(data.dischtime)
    data['los'] = (start - end).dt.total_seconds()/86400

    # Add age feature and remove outliers
    admit = pd.to_datetime(data.admittime).dt.date
    dob = pd.to_datetime(data.dob).dt.date
    data['age'] = (admit - dob).apply(lambda x: round(x.days / 365, 0))
    data = data[data.age < 105].drop(columns='dob')
    return data


def compressing_admission_type(data):
    """Returns the dataframe with addmission type compressed so that emergency
    and urgent are both marked as urgent.
    """

    data.admission_type = data.admission_type.apply(lambda x: 'EMERGENCY' if x
                                                    == 'URGENT' else x)
    return data

def assign_cats(row):
    """Helper function for age_to_cat that assigns categories based on patient
    age.
    """

    if 0 <= row['age'] <= 3:
        val = 'Baby'
    elif 3 <= row['age'] <= 18:
        val = 'Child/Teen'
    elif 19 <= row['age'] <= 40:
        val = 'Young_Aduld'
    elif 41 <= row['age'] <= 60:
        val = "Adult"
    elif 61 <= row['age'] <= 100:
        val = "Senior"

    return val

def age_to_cat(data):
    """Returns a dataframe with ages compressed into categorical groups."""

    data['age'] = data.apply(assign_cats, axis=1)
    return data

def compressing_careunit(data):
    """Returns the dataframe with all ICU subcategories combined into a single
    'ICU' category.
    """

    data.first_careunit = data.first_careunit.apply(lambda x: 'ICU' if
                                                    (x == 'MICU') |
                                                    (x == 'SICU') |
                                                    (x == 'CCU') |
                                                    (x == 'CSRU') |
                                                    (x == 'TSICU')
                                                    else x)
    return data

def compressing_curr_serv(data):
    """Returns the dataframe with the survice area compressed to only
    SURGERY, MED, GYNOCOLOGY/NEWBORN, and OTHER.
    """
    data.curr_service = data.curr_service.apply(lambda x: 'SURGERGY' if
                                                (x == 'CSURG') |
                                                (x == 'NSURG') |
                                                (x == 'ORTHO') |
                                                (x == 'PSURG') |
                                                (x == 'SURG') |
                                                (x == 'TSURG') |
                                                (x == 'VSURG')
                                                else x)

    data.curr_service = data.curr_service.apply(lambda x: "MED"
                                                if (x == 'CMED') |
                                                (x == 'OMED') |
                                                (x == 'NMED') |
                                                (x == 'TRAUM')
                                                else x)

    data.curr_service = data.curr_service.apply(lambda x: "GYNOCOLOGY/NEWBORN"
                                                if (x == 'NB') |
                                                (x == 'NBB') |
                                                (x == 'OBS') |
                                                (x == 'GYN')
                                                else x)

    data.curr_service = data.curr_service.apply(lambda x: "OTHER"
                                                if (x == "GU") |
                                                (x == "ENT") |
                                                (x == "DENT") |
                                                (x == "PSYCH")
                                                else x)

    return data

def compressing_ethnicity(data):
    """Returns the dataframe with ethnicity compressed into only the majority
    groups, WHITE, ASIAN, HISPANIC/LATINO, BLACK_AFRICAN/OTHER and
    OTHER/UNKOWN.
    """

    data.ethnicity = data.ethnicity.apply(lambda x: 'WHITE'
                                          if ("WHITE" in x) else x)

    data.ethnicity = data.ethnicity.apply(lambda x: "ASIAN"
                                          if ("ASIAN" in x)  else x)

    data.ethnicity = data.ethnicity.apply(lambda x: "HISPANIC/LATINO"
                                          if ("LATINA" in x) |
                                          ("HISPANIC" in x)
                                          else x)

    data.ethnicity = data.ethnicity.apply(lambda x: "OTHER/UNKNOWN"
                                          if (x == "AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE") |
                                          (x == "SOUTH AMERICAN") |
                                          (x == "CARIBBEAN ISLAND") |
                                          (x == "NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER") |
                                          (x == "AMERICAN INDIAN/ALASKA NATIVE") |
                                          (x == "MIDDLE EASTERN") |
                                          (x == "PORTUGUESE") |
                                          (x == "MULTI RACE ETHNICITY") |
                                          (x == "PATIENT DECLINED TO ANSWER") |
                                          (x == "OTHER") |
                                          ("UNKNOWN" in x) |
                                          ("OBTAIN" in x)
                                          else x)

    data.ethnicity = data.ethnicity.apply(lambda x: "BLACK_AFRICAN/OTHER"
                                          if ("BLACK" in x) else x)

    return data

def compressing_marital_status(data):
    """Returns the dataframe with marital status compressed to only
    LIFE_PARTNER, SINGLE, OTHER/UNKOWN.
    """

    data.marital_status = data.marital_status.apply(lambda x: 'LIFE_PARTNER'
                                                    if (x == 'MARRIED') |
                                                    (x == 'LIFE PARTNER')
                                                    else x)

    data.marital_status = data.marital_status.apply(lambda x: 'SINGLE'
                                                    if (x == 'WIDOWED') |
                                                    (x == 'DIVORCED') |
                                                    (x == 'SEPARATED')
                                                    else x)

    data.marital_status = data.marital_status.apply(lambda x: 'OTHER/UNKNOWN'
                                                    if (x == 'UNKNOWN (DEFAULT)')
                                                    else x)

    return data

def compressing_religion(data):
    """Returns the dataframe with relgion compressed to either RELIGIOUS or
    NOT RELIGOUS.
    """

    data.religion = data.religion.apply(lambda x: 'RELIGIOUS'
                                        if (x == "LUTHERAN") |
                                        (x == "METHODIST") |
                                        (x == "HEBREW") |
                                        (x == "BAPTIST") |
                                        (x == "HINDU") |
                                        (x == "UNITARIAN-UNIVERSALIST") |
                                        (x == "ROMANIAN EAST. ORTH") |
                                        (x == "7TH DAY ADVENTIST") |
                                        (x == "JEHOVAH'S WITNESS") |
                                        (x == 'MUSLIM') |
                                        (x == 'BUDDHIST') |
                                        (x == 'CHRISTIAN SCIENTIST') |
                                        (x == 'GREEK ORTHODOX') |
                                        (x == 'EPISCOPALIAN') |
                                        (x == 'OTHER') |
                                        (x == 'JEWISH') |
                                        (x == 'CATHOLIC') |
                                        (x == 'PROTESTANT QUAKER')
                                        else x)

    return data

def compressing_admit_location(data):
    """Returns the dataframe with admit location compressed to only ER_ADMIT,
    REFERRAL, TRANSFER, and OTHER/UNKNOWN.
    """

    data.admission_location = data.admission_location.apply(lambda x: 'ER_ADMIT'
                                                            if (x == 'EMERGENCY ROOM ADMIT ')
                                                            else x)

    data.admission_location = data.admission_location.apply(lambda x: 'REFERRAL'
                                                            if (x == 'HMO REFERRAL/SICK') |
                                                            (x == 'PHYS REFERRAL/NORMAL DELI') |
                                                            (x == 'CLINIC REFERRAL/PREMATURE')
                                                            else x)

    data.admission_location = data.admission_location.apply(lambda x: 'TRANSFER'
                                                            if (x == 'TRANSFER FROM HOSP/EXTRAM') |
                                                            (x == 'TRANSFER FROM SKILLED NUR') |
                                                            (x == 'TRANSFER FROM OTHER HEALT') |
                                                            (x == 'TRSF WITHIN THIS FACILITY')
                                                            else x)

    data.admission_location = data.admission_location.apply(lambda x: 'OTHER/UNKNOWN'
                                                            if (x == '** INFO NOT AVAILABLE **')
                                                            else x)

    return data

def icd9_descriptions(row):
    """Assigned a diagnoses string to each icd9_code value. Returns a string
    value to replace the icd9_code.
    """

    if 1 <= row['icd9_code'] <= 139:
        val = 'Parasitic_Disease'
    elif 140 <= row['icd9_code'] <= 239:
        val = 'Neoplasm'
    elif 240 <= row['icd9_code'] <= 279:
        val = 'Endocrine'
    elif 280 <= row['icd9_code'] <= 289:
        val = "Blood"
    elif 290 <= row['icd9_code'] <= 319:
        val = "Mental_Disorder"
    elif 320 <= row['icd9_code'] <= 389:
        val = "Nervous_System"
    elif 390 <= row['icd9_code'] <= 459:
        val = "Circulatory_System"
    elif 460 <= row['icd9_code'] <= 519:
        val = "Respiratory_System"
    elif 520 <= row['icd9_code'] <= 579:
        val = "Digestive_System"
    elif 580 <= row['icd9_code'] <= 629:
        val = "Genitourinary_System"
    elif 630 <= row['icd9_code'] <= 679:
        val = "Pregnancy"
    elif 680 <= row['icd9_code'] <= 709:
        val = "Skin"
    elif 710 <= row['icd9_code'] <= 739:
        val = "Musculoskeletal"
    elif 740 <= row['icd9_code'] <= 759:
        val = "Congenital_Anomalies"
    elif 760 <= row['icd9_code'] <= 779:
        val = "Perinatal"
    elif 780 <= row['icd9_code'] <= 799:
        val = "Ill-Defined"
    elif 800 <= row['icd9_code'] <= 999:
        val = "Injury/Poison"
    elif row['icd9_code'] < .4:
        val = "Supplemental_factors"
    elif .4 <= row['icd9_code'] < .7:
        val = "External_Cause_Inj_Poison"
    elif .7 <= row['icd9_code'] < .9:
        val = "Morphology_of_Neoplasms"
    else:
        val = row['icd9_code']

    return val

def compress_icd9_codes(data):
    """Returns the dataframe with the 6000 unique ICD9 codes reduced into 17
    diagnoses categories based on standard definitions. A new column is
    created to contain diagnoses.
    """

    data.icd9_code = data.icd9_code.apply(lambda x: '.1' if 'V' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: '.8' if 'M' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: '.5' if 'E' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: x[:3] if ('E' not in x) &
                                          ('M' not in x) &
                                          ('V' not in x)
                                          else x)

    data.icd9_code = data.icd9_code.astype(float)


    data['diagnoses'] = data.apply(icd9_descriptions, axis=1)
    data = data.drop(columns=['icd9_code'])

    return data

def main():
    """Loads the raw hospital data and returns a dataframe with feautre
    engineering applied.
    """
    raw_data = pd.read_csv('data/raw_hospital_data.csv')

    fe_data = new_features(raw_data)
    fe_data = compressing_admission_type(data)
    fe_data = age_to_cat(fe_data)
    fe_data = compressing_careunit(fe_data)
    fe_data = compressing_curr_serv(fe_data)
    fe_data = compressing_ethnicity(fe_data)
    fe_data = compressing_marital_status(fe_data)
    fe_data = compressing_religion(fe_data)
    fe_data = compressing_admit_location(fe_data)
    fe_data = compress_icd9_codes(fe_data)

    fe_data.to_csv('data/feature_engineering_data.csv')

main()
