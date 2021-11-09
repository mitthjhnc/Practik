import pandas as pd
import sklearn.linear_model
import matplotlib.pyplot as plt

#Uses pandas .read_parquet to read dataframe from file, file made in prepare_data.py
d_f = pd.read_parquet('data/dataframe_consumption_temp.parquet')

#Creating training data and test data using pandas .query method
d_f_train = d_f.query("time < '2015-06-07 00:00:00+00:00' & time > '2015-06-01 00:00:00+00:00'")
d_f_test = d_f.query("time > '2020-01-01 00:00:00+00:00'")

# print(d_f_train)

#creates a X_train and y_train to be inputted in the sklearn .fit method
X_train = d_f_train[['temperature']]
y_train = d_f_train['GrossConsumptionMWh']

d_f_train.iloc[:].plot(x='time', y='temperature')
plt.show(block=True)

#creates a X_test to input into sklearn .predict method and y_test to be used to test answers.
X_test = d_f_test[['temperature']]
y_test = d_f_test['GrossConsumptionMWh']

model = sklearn.linear_model.LinearRegression()
model.fit(X_train, y_train)

print(model.coef_, model.intercept_)

y_pred = model.predict(X_test)

d_f_compare = pd.DataFrame({'y_pred': y_pred, 'y_test': y_test})
d_f_compare.iloc[:100].plot()
plt.show(block=True)