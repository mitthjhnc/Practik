import pandas as pd
import sklearn.linear_model
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
import train_model_lm


#Uses pandas .read_parquet to read dataframe from file, file made in prepare_data.py
d_f = pd.read_parquet('data/dataframe_consumption_temp.parquet')


#Creating training data and test data using pandas .query method
d_f_train = d_f.query("time < '2015-06-07 00:00:00+00:00' & time > '2015-06-01 00:00:00+00:00'")
d_f_test = d_f.query("time > '2020-01-01 00:00:00+00:00'")

#########################################################################
#with data on workdays and year

#Trains model
model_workdays_year, X_test_workdays_year, y_test_workdays_year = train_model_lm.train_model_with_workdays_year(d_f_train, d_f_test)

#prints co-efficiant and intercept
print(model_workdays_year.coef_, model_workdays_year.intercept_)

#saves predictions of model in y_pred_workdays_year
y_pred_workdays_year = model_workdays_year.predict(X_test_workdays_year)

d_f_compare = pd.DataFrame({'y_pred' : y_pred_workdays_year, 'y_test' : y_test_workdays_year})
d_f_compare.plot()
plt.show(block = True)

#########################################################################

#Trains on data including info on work days
model_workdays, X_test_workdays, y_test_workdays = train_model_lm.train_model_with_workdays(d_f_train, d_f_test)

#prints co-efficiant and intercept
# print(model_workdays.coef_, model_workdays.intercept_)

#saves predictions of model in y_pred_workdays
y_pred_workdays = model_workdays.predict(X_test_workdays)

##########################################################################

#Trains model with out using workdays data
model_no_workdays, X_test_no_workdays, y_test_no_workdays = train_model_lm.train_model_no_workdays(d_f_train, d_f_test)

#prints co-efficiant and intercept
# print(model_no_workdays.coef_, model_no_workdays.intercept_)

#saves predictions of model in y_pred_no_workdays
y_pred_no_workdays = model_no_workdays.predict(X_test_no_workdays)

###########################################################################

#Gets accuracy_score for both models
workdays_year = mean_absolute_error(y_test_workdays_year, y_pred_workdays_year)

workdays = mean_absolute_error(y_test_workdays, y_pred_workdays)

no_workdays = mean_absolute_error(y_test_no_workdays, y_pred_no_workdays)

#compares how well the two models did
print(f' workdays_year: {workdays_year}\n', f'workdays: {workdays}\n', f'no_workdays: {no_workdays}')

# (y_pred_workdays - y_test_workdays).plot()
# plt.show(block = True)