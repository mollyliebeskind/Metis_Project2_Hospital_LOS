import pandas as pd

def renaming_icd9_cols(data):
    data = data.rename(columns = {'congenital_anomalie': 'd_anomalie',
                                  'diseases_of_the_blood_and_blood-forming_organ': 'd_blood',
                                  'diseases_of_the_circulatory_syste': 'd_circulatory',
                                  'diseases_of_the_digestive_syste': 'd_digestive',
                                  'diseases_of_the_genitourinary_syste': 'd_genitourinary',
                                  'diseases_of_the_musculoskeletal_system_and_connective_tissu': 'd_musculoskeletal',
                                  'diseases_of_the_nervous_system_and_sense_organ': 'd_nervous',
                                  'diseases_of_the_respiratory_syste': 'd_respiratory',
                                  'diseases_of_the_skin_and_subcutaneous_tissu': 'd_skin',
                                  'endocrine,_nutritional_and_metabolic_diseases,_and_immunity_disorder': 'd_endo_metabolic_immunity',
                                  'infectious_and_parasitic_disease': 'd_parasitic',
                                  'injury_and_poisonin': 'd_poison_injury',
                                  'mental_disorder': 'd_mental',
                                  'neoplasm': 'd_neoplasm',
                                  'supplementary_classification_of_external_causes_of_injury_and_poisonin': 'd_external_inj_poison',
                                  'supplementary_classification_of_factors_influencing_health_status_and_contact_with_health_service': 'd_suppl_health_service',
                                  'symptoms,_signs_and_ill-defined_condition':'d_ill_defined'}, errors="raise")
    return data

def dummifying_icd9(data):
    data = pd.concat((data, pd.get_dummies(data['icd_range'])), axis=1)
    data = data.drop(columns = 'icd_range')
    renamed_datadata = renaming_icd9_cols(data)

    #consolidates to a single line per subject_id with all diagnosis included
    grouped_dummy_data = renamed_datadata.groupby('subject_id').max().reset_index()
    grouped_dummy_data['number_of_diagnoses'] =  grouped_dummy_data['d_blood'] + grouped_dummy_data['d_anomalie'] + grouped_dummy_data['d_circulatory'] + grouped_dummy_data['d_digestive'] + grouped_dummy_data['d_digestive']

    print("ICD9 dummy variables created.")
    return grouped_dummy_data

def dummifying_cat_cols(data):
    icd9_dummed = dummifying_icd9(data)
    return icd9_dummed
