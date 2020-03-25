import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tools.tools import add_constant
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.linear_model import LinearRegression, Lasso, Ridge, ElasticNet
from sklearn.model_selection import train_test_split, KFold

def dummy_cat_cols(data):
    """Creates dummy variables for each categorical column.
    Groups the rows by admission event (hadm_id) so that each admission event is a single row
    with a recording for each diagnoses recieved during that admission event. Each admission
    event can have multiple diagnoses. Drops subject_id and hadm_id which are no longer needed."""
    #cat_cols = ['admission_type', 'admission_location', 'insurance', 'religion', 'marital_status', 'ethnicity', 'gender', 'curr_service', 'diagnoses']
    cat_cols = [col for col in data.columns if (data[col].dtype == 'O')]

    dummied_data = pd.get_dummies(data, drop_first=True, columns=cat_cols)

    #groups the rows so that each admission is a single row and the diagnoses are summed for that admission
    grouped_dummy_data = dummied_data.groupby('hadm_id').max().reset_index()
    select_cols = grouped_dummy_data.drop(columns = ['subject_id', 'hadm_id'])

    print("Dummy variables created.")

    return select_cols


def splitting_test_and_train(data, t_size=.2):
    """Separates data into X and y. Splits the data into test and train data for holdout testing."""
    X, y = data.drop('los', axis=1), data['los']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=t_size, random_state=10) #hold out 20% of the data for final testing

    #this helps with the way kf will generate indices below
    print("Train and test data are separated")

    return X_train, X_test, y_train, y_test


def cross_val_testing_lr(X_train, X_test, y_train, y_test):
    """Within the 80% train data, splits the model into 10 folds for cross-validation testing.
    Runs a linear regression on the train and validation data without standard scaling as all
    factors are categorical other than age. Prints R^2, RMSE, and MAE for in and out of sample
    predictions."""

    kf = KFold(n_splits=10, shuffle=True, random_state = 71)

    cv_lm_r2s, in_sample_r2s = [], [] #collect the validation results for both models
    cv_lm_rmse, in_sample_rmses = [], []
    cv_lm_mae, in_sample_mae = [], []

    print("Kfolds created. Running linear regression.")

    for train_ind, val_ind in kf.split(X_train,y_train):

        X_tr, y_tr = X_train.iloc[train_ind], y_train.iloc[train_ind]
        X_val, y_val = X_train.iloc[val_ind], y_train.iloc[val_ind]

        #defining simple linear regression
        lm = LinearRegression()
        lm.fit(X_tr, y_tr)
        in_sample_predict = lm.predict(X_tr)
        out_of_sample_predict = lm.predict(X_val)

        cv_lm_r2s.append(lm.score(X_val, y_val))
        in_sample_r2s.append(lm.score(X_tr, y_tr))

        cv_lm_rmse.append(np.sqrt(mean_squared_error(y_val, out_of_sample_predict)))
        in_sample_rmses.append(np.sqrt(mean_squared_error(y_tr, in_sample_predict)))

        cv_lm_mae.append(mean_absolute_error(y_val, out_of_sample_predict))
        in_sample_mae.append(mean_absolute_error(y_tr, in_sample_predict))

        mean_r2 = float(np.mean(cv_lm_r2s))
        mean_rmse = float(np.mean(cv_lm_rmse))
        mean_mae = float(np.mean(in_sample_mae))

    print('\nLinear regression scores r^2: ', cv_lm_r2s, '\n')
    print(f'Linear regression mean cv r^2: {np.mean(cv_lm_r2s):.3f} +- {np.std(cv_lm_r2s):.3f}\n')
    print(f"Mean r^2 for in sample data: {np.mean(in_sample_r2s):.3f} +- {np.std(in_sample_r2s):.3f} \n\n")

    print('Linear regression scores rmse: ', cv_lm_rmse, '\n')
    print(f'Linear regression mean cv rmse: {np.mean(cv_lm_rmse):.3f} +- {np.std(cv_lm_rmse):.3f}\n')
    print(f"Mean rmse for in sample data: {np.mean(in_sample_rmses):.3f} +- {np.std(in_sample_rmses):.3f}")

    print('Linear regression scores mae: ', cv_lm_mae, '\n')
    print(f'Linear regression mean cv mae: {np.mean(cv_lm_mae):.3f} +- {np.std(cv_lm_mae):.3f}\n')
    print(f"Mean mae for in sample data: {np.mean(in_sample_mae):.3f} +- {np.std(in_sample_mae):.3f}")

    return mean_r2, mean_rmse, mean_mae

def linear_regression_no_cv(X_train, X_test, y_train, y_test):
    """Runs linear regression without cross-validation for final model implementation on
    holdout dataset. Returns in-sample and out of sampel R^2, RMSE, and MAE. """
    cv_lm_r2s, in_sample_r2s = [], [] #collect the validation results for both models
    cv_lm_rmse, in_sample_rmses = [], []
    cv_lm_mae, in_sample_mae = [], []

    #defining simple linear regression
    lm = LinearRegression()
    lm.fit(X_train, y_train)
    in_sample_predict = lm.predict(X_train)
    out_of_sample_predict = lm.predict(X_test)

    cv_lm_r2s.append(lm.score(X_test, y_test))
    in_sample_r2s.append(lm.score(X_train, y_train))

    cv_lm_rmse.append(np.sqrt(mean_squared_error(y_test, out_of_sample_predict)))
    in_sample_rmses.append(np.sqrt(mean_squared_error(y_train, in_sample_predict)))

    cv_lm_mae.append(mean_absolute_error(y_test, out_of_sample_predict))
    in_sample_mae.append(mean_absolute_error(y_train, in_sample_predict))


    print('\nLinear regression score r^2: ', cv_lm_r2s, '\n')
    print('\nIn sample linear regression score r^2: ', in_sample_r2s, '\n')


    print('Linear regression scores rmse: ', cv_lm_rmse, '\n')
    print('In sample linear regression scores rmse: ', in_sample_rmses, '\n')

    print('Linear regression scores mae: ', cv_lm_mae, '\n')
    print('In sample linear regression scores mae: ', in_sample_mae, '\n')

    return out_of_sample_predict


def SM_OLS_cv(X_train, X_test, y_train, y_test):
    """Splits data into 10 folds for cross-validation OLS. Performs OLS
    and returns the result summary."""

    #adds column of ones for B_0 constant coefficient
    X_train = add_constant(X_train)
    kf = KFold(n_splits=10, shuffle=True, random_state = 71) 
    print("Kfolds created. Running OLS.")

    for train_ind, val_ind in kf.split(X_train,y_train):

        X_tr, y_tr = X_train.iloc[train_ind], y_train.iloc[train_ind]
        X_val, y_val = X_train.iloc[val_ind], y_train.iloc[val_ind]

        #Running OLS
        los_model = sm.OLS(y_tr, X_tr)
        results = los_model.fit()
    print("OLS run. Result summary returned.")

    return results.summary()

def SM_OLS_no_cv(X_train, X_test, y_train, y_test):
    """Runs OLS without cross-validation for final, hold out dataset OLS
    model implementation. Returns results summary."""

    #adds column of ones for B_0 constant coefficient
    X_train = add_constant(X_train)

    #Running OLS
    los_model = sm.OLS(y_train, X_train)
    results = los_model.fit()

    return results.summary()
