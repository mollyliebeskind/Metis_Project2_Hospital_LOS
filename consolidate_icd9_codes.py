import pandas as pd

def nummify_supplemental_icd9_codes(data):
    """converts all icd9 codes that start with a letter to a number in order
    to use number ranges to identify diagnoes."""
    data.icd9_code = data.icd9_code.apply(lambda x: '.1' if 'V' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: '.8' if 'M' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: '.5' if 'E' in x else x)
    data.icd9_code = data.icd9_code.apply(lambda x: x[:3] if ('E' not in x) & ('M' not in x) & ('V' not in x)else x)

    data.icd9_code = data.icd9_code.astype(float)
    print("Supplemental codes turned into floats")
    return data

def f(row):
    """assigned a diagnoses string to each icd9_code value. Returns a string
    value to replace the icd9_code with."""
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
    """replaces the 6000 unique ICD9_code column with 17 diagnoses,
    in a new column, 'diagnoses'."""
    all_numified = nummify_supplemental_icd9_codes(data)
    all_numified['diagnoses'] = all_numified.apply(f, axis=1)
    compressed_icd9 = all_numified.drop(columns=['icd9_code'])
    print("ICD9 codes truncated to 17 categories")
    return compressed_icd9
