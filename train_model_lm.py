import pandas as pd
import sklearn.linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score


def train_model_with_workdays_year(d_f_train : pd.DataFrame, d_f_test : pd.DataFrame):
    """This function trains a linear regression model using the data inputed

    The function expects a training spesific data set and will only work with that data frame.
    It will train using the workdays data and including a linear increasing trend.
    
    The function will return the model, first, then the X_test and lastly the y_test
    """
    #creates a X_train and y_train to be inputted in the sklearn .fit method
    X_train = d_f_train.drop(columns=['time', 'GrossConsumptionMWh'])
    y_train = d_f_train['GrossConsumptionMWh']

    #creates a X_test to input into sklearn .predict method and y_test to be used to test answers.
    X_test = d_f_test.drop(columns=['time', 'GrossConsumptionMWh'])
    y_test = d_f_test['GrossConsumptionMWh']

    #creates the model and trains it
    model = sklearn.linear_model.LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test


def train_model_with_workdays(d_f_train : pd.DataFrame, d_f_test : pd.DataFrame):
    """This function trains a linear regression model using the data inputed

    The function expects a training spesific data set and will only work with that data frame.
    It will train using the workdays data.
    
    The function will return the model, first, then the X_test and lastly the y_test
    """
    #creates a X_train and y_train to be inputted in the sklearn .fit method
    X_train = d_f_train.drop(columns=['time', 'GrossConsumptionMWh', 'year'])
    y_train = d_f_train['GrossConsumptionMWh']

    #creates a X_test to input into sklearn .predict method and y_test to be used to test answers.
    X_test = d_f_test.drop(columns=['time', 'GrossConsumptionMWh', 'year'])
    y_test = d_f_test['GrossConsumptionMWh']

    #creates the model and trains it
    model = sklearn.linear_model.LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

def train_model_no_workdays(d_f_train, d_f_test):
    """This function trains a linear regression model using the data inputed

    The function expects a training spesific data set and will only work with that data frame.
    It will train and not use the workdays data.
    
    The function will return the model, first, then the X_test and lastly the y_test
    """
    #creates a X_train and y_train to be inputted in the sklearn .fit method
    X_train = d_f_train.drop(columns=['time', 'GrossConsumptionMWh', 'workday', 'year'])
    y_train = d_f_train['GrossConsumptionMWh']

    #creates a X_test to input into sklearn .predict method and y_test to be used to test answers.
    X_test = d_f_test.drop(columns=['time', 'GrossConsumptionMWh', 'workday', 'year'])
    y_test = d_f_test['GrossConsumptionMWh']

    #creates the model and trains it
    model = sklearn.linear_model.LinearRegression()
    model.fit(X_train, y_train)

    return model, X_test, y_test

