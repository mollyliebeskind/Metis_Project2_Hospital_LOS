"""This script implements the final linear regression model for predicting a
patients length of stay in the hospital. Additional testing and cross
validation was performed separately and can be accessed in the notebook file.
"""

import pickle

import pandas as pd
import numpy as np

from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def dummy_cat_cols(data):
    """Returns a dataframe with one hot encoded categorical columns and rows
    grouped by by admission event (hadm_id). Each admission event is therefore
    a single row with a recording for each diagnoses recieved during that
    admission event. Each admission event can have multiple diagnoses.
    Following grouping, subject_id and hadm_id which are no longer needed."""

    # One hot encoding
    cat_cols = [col for col in data.columns if data[col].dtype == 'O']
    dummied_data = pd.get_dummies(data, drop_first=True, columns=cat_cols)

    # Group by admission event
    grouped_dummy_data = dummied_data.groupby('hadm_id').max().reset_index()
    select_data = grouped_dummy_data.drop(columns=['subject_id', 'hadm_id'])

    return select_data

def splitting_test_and_train(data):
    """Returns 80/20 train and test sets for model implementation."""

    X, y = data.drop('los', axis=1), data['los']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2,
                                                        random_state=10)

    return X_train, X_test, y_train, y_test



def final_model_linreg(data):
    """Runs linear regression for final model implementation on holdout
    dataset. Prints in-sample and out of sampel R^2, RMSE, and MAE. Pickles
    the model."""

    dummied_data = dummy_cat_cols(data)
    X_train, X_test, y_train, y_test = splitting_test_and_train(dummied_data)

    #defining simple linear regression
    lm = LinearRegression()
    lm.fit(X_train, y_train)
    in_sample_predict = lm.predict(X_train)
    out_of_sample_predict = lm.predict(X_test)

    oos_r2 = lm.score(X_test, y_test)
    in_r2 = lm.score(X_train, y_train)
    print('\nLinear regression r^2: ', oos_r2, '\n')
    print('\nIn sample linear regression r^2: ', in_r2, '\n')

    oos_rmse = np.sqrt(mean_squared_error(y_test, out_of_sample_predict))
    in_rmse = np.sqrt(mean_squared_error(y_train, in_sample_predict))
    print('\nLinear regression rmse: ', oos_rmse, '\n')
    print('\nIn sample linear regression rmse: ', in_rmse, '\n')

    oos_mae = mean_absolute_error(y_test, out_of_sample_predict)
    in_mae = mean_absolute_error(y_train, in_sample_predict)
    print('\nLinear regression mae: ', oos_mae, '\n')
    print('\nIn sample linear regression mae: ', in_mae, '\n')

    pickle.dump(lm, open('los_model.pkl', 'wb'))

def main():
    """Loads cleaned and feature engineered hospital dataframe and predicts
    a patient's lengh of stay in the hospital.
    """

    hospital_data = pd.read_csv('data/feature_engineering_data.csv')
    final_model_linreg(hospital_data)

main()
