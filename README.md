# Metis_Project2_Hospital_LOS
Regression analysis to predict hospital length of stays

## Objective: Optimize BIDMC’s resourcing strategy by understand how intake factors can predict hospital Length of Stay (LOS)

## Data Sources:
* Database: https://physionet.org/content/mimiciii/1.4/
* Data Info: https://mimic.physionet.org/mimictables/callout/
* Wiki for ICD9 Codes: https://en.wikipedia.org/wiki/List_of_ICD-9_codes_001%E2%80%93139:_infectious_and_parasitic_diseases

**Featured Techniques**
* EDA
* Feature Engineering
* Linear Regression

## Definitions:

Length of Stay (LOS): Amount of time spent in the hospital from admission time to discharge time  
ICD9_codes: 5 digit code that identifies each diagnoses  

Time Shifting as Defined by MIMIC-III:  
"All dates in the database have been shifted to protect patient confidentiality. Dates will be internally consistent for the same patient, but randomly distributed in the future. This means that if measurement A is made at 2150-01-01 14:00:00, and measurement B is made at 2150-01-01 15:00:00, then measurement B was made 1 hour after measurement A.

The date shifting preserved the following:

* Time of day - a measurement made at 15:00:00 was actually made at 15:00:00 local standard time. Day of the week - a measurement made on a Sunday will appear on a Sunday in the future. Seasonality - a measurement made during the winter months will appear during a winter month. The date shifting removed the following:

* Year - The year is randomly distributed between 2100 - 2200. Day of the month - The absolute day of the month is not preserved. Inter-patient information - Two patients in the ICU on 2150-01-01 were not in the ICU at the same time. Dates of birth"
