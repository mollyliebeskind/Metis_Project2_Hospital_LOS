def compressing_admission_type(data): 
    eng_data = data
    eng_data.admission_type = eng_data.admission_type.apply(lambda x: 'EMERGENCY' if x == 'URGENT' else x)
    print("Admission type compressed.")
    return eng_data

def r(row):
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
    eng_data = data
    eng_data['age'] = eng_data.apply(r, axis=1)
    print("Age column compressed.")
    return eng_data

def compressing_careunit(data):
    eng_data = data
    eng_data.first_careunit = eng_data.first_careunit.apply(lambda x: 'ICU' if (x == 'MICU') | (x == 'SICU') | (x == 'CCU') | (x == 'CSRU') | (x == 'TSICU') else x)
    print("Careunit compressed.")
    return eng_data

def compressing_curr_serv(data):
    eng_data = data
    eng_data.curr_service = eng_data.curr_service.apply(lambda x: 'SURGERGY' if (x == 'CSURG') | (x == 'NSURG') | (x == 'ORTHO') | (x == 'PSURG') | (x == 'SURG') | (x == 'TSURG') | (x == 'VSURG') else x)
    eng_data.curr_service = eng_data.curr_service.apply(lambda x: "MED" if (x == 'CMED') | (x == 'OMED') | (x == 'NMED') | (x == 'TRAUM') else x)
    eng_data.curr_service = eng_data.curr_service.apply(lambda x: "GYNOCOLOGY/NEWBORN" if (x == 'NB') | (x == 'NBB') | (x == 'OBS') | (x == 'GYN') else x)
    eng_data.curr_service = eng_data.curr_service.apply(lambda x: "OTHER" if (x == "GU") | (x == "ENT") | (x == "DENT") | (x == "PSYCH") else x)
    print("Services compressed.")
    return eng_data

def compressing_ethnicity(data):
    eng_data = data
    eng_data.ethnicity = eng_data.ethnicity.apply(lambda x: 'WHITE' if ("WHITE" in x) else x)
    eng_data.ethnicity = eng_data.ethnicity.apply(lambda x: "ASIAN" if ("ASIAN" in x) else x)
    eng_data.ethnicity = eng_data.ethnicity.apply(lambda x: "HISPANIC/LATINO" if ("LATINA" in x) | ("HISPANIC" in x) else x)
    eng_data.ethnicity = eng_data.ethnicity.apply(lambda x: "OTHER/UNKNOWN" if (x=="AMERICAN INDIAN/ALASKA NATIVE FEDERALLY RECOGNIZED TRIBE") | (x=="SOUTH AMERICAN") | (x=="CARIBBEAN ISLAND") | (x=="NATIVE HAWAIIAN OR OTHER PACIFIC ISLANDER") |(x=="AMERICAN INDIAN/ALASKA NATIVE") | (x=="MIDDLE EASTERN") | (x=="PORTUGUESE") | (x=="MULTI RACE ETHNICITY") | (x=="PATIENT DECLINED TO ANSWER") | (x=="OTHER") | ("UNKNOWN" in x) | ("OBTAIN" in x) else x)
    eng_data.ethnicity = eng_data.ethnicity.apply(lambda x: "BLACK_AFRICAN/OTHER" if ("BLACK" in x) else x)
    print("Ethnicities compressed.")
    return data

def compressing_marital_status(data):
    eng_data = data
    eng_data.marital_status = eng_data.marital_status.apply(lambda x: 'LIFE_PARTNER' if (x == 'MARRIED') | (x == 'LIFE PARTNER') else x)
    eng_data.marital_status = eng_data.marital_status.apply(lambda x: 'SINGLE' if (x == 'WIDOWED') | (x == 'DIVORCED') | (x == 'SEPARATED') else x)
    eng_data.marital_status = eng_data.marital_status.apply(lambda x: 'OTHER/UNKNOWN' if (x == 'UNKNOWN (DEFAULT)') else x)
    print("Marital status compressed.")
    return data

def compressing_religion(data):
    eng_data = data
    eng_data.religion = eng_data.religion.apply(lambda x: 'RELIGIOUS' if (x == "LUTHERAN") | (x == "METHODIST") | (x == "HEBREW") | (x == "BAPTIST") | (x == "HINDU") | (x == "UNITARIAN-UNIVERSALIST") | (x == "ROMANIAN EAST. ORTH") | (x == "7TH DAY ADVENTIST") | (x == "JEHOVAH'S WITNESS") | (x == 'MUSLIM') | (x == 'BUDDHIST') | (x == 'CHRISTIAN SCIENTIST') | (x == 'GREEK ORTHODOX') | (x == 'EPISCOPALIAN') | (x == 'OTHER') | (x == 'JEWISH') | (x == 'CATHOLIC') | (x == 'PROTESTANT QUAKER') else x)
    print("Religion compressed.")
    return data

def compressing_admit_location(data):
    eng_data = data
    eng_data.admission_location = eng_data.admission_location.apply(lambda x: 'ER_ADMIT' if (x == 'EMERGENCY ROOM ADMIT ') else x)
    eng_data.admission_location = eng_data.admission_location.apply(lambda x: 'REFERRAL' if (x == 'HMO REFERRAL/SICK') | (x == 'PHYS REFERRAL/NORMAL DELI') | (x == 'CLINIC REFERRAL/PREMATURE') else x)
    eng_data.admission_location = eng_data.admission_location.apply(lambda x: 'TRANSFER' if (x == 'TRANSFER FROM HOSP/EXTRAM') | (x == 'TRANSFER FROM SKILLED NUR') | (x == 'TRANSFER FROM OTHER HEALT') | (x == 'TRSF WITHIN THIS FACILITY')else x)
    eng_data.admission_location = eng_data.admission_location.apply(lambda x: 'OTHER/UNKNOWN' if (x == '** INFO NOT AVAILABLE **')  else x)
    print("Admissiong location compressed.")
    print("Done compressing.")
    return eng_data

def all_feature_engineering(data):
    fe_data = compressing_admission_type(data)
    fe_data = age_to_cat(fe_data)
    fe_data = compressing_careunit(fe_data)
    fe_data = compressing_curr_serv(fe_data)
    fe_data = compressing_ethnicity(fe_data)
    fe_data = compressing_marital_status(fe_data)
    fe_data = compressing_religion(fe_data)
    fe_data = compressing_admit_location(fe_data)

    return fe_data
