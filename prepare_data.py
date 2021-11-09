from datetime import tzinfo
import pickle
import pandas as pd
import pytz
from dateutil.easter import easter
from workalendar.europe import Denmark
from get_date_type import get_date_type
import matplotlib.pyplot as plt


#loading data from consumption files and makes it into one large DataFrame
#DONE: needs to make file name automaticly
d_f_consumption = pd.DataFrame()
for year in range(2015, 2021):
    pkl_name = "data/consumption" + str(year) + '-01-01'
    pkl_name += "to" + str(year) + '-12-31' + '.pkl'
    d_f_consumption = pd.concat([d_f_consumption, pd.read_pickle(pkl_name)])
# print(d_f_consumption)

# print(d_f_consumption.keys())
#removing every other row than Gross Consumption from d_f_consumption
d_f_consumption = d_f_consumption[['GrossConsumptionMWh', 'HourUTC']]

d_f_consumption_sum = d_f_consumption.groupby('HourUTC').sum().reset_index()
d_f_consumption_sum.rename(columns = {'HourUTC' : 'time'}, inplace=True)
d_f_consumption_sum
# print(d_f_consumption_sum)

#loading data from weather
pkl_name = "data/temp_stations_dict" + '2015-01-01'
pkl_name += "to" + '2021-06-01' + ".pkl"

with open(pkl_name, 'rb') as handle:
    dict_file = pickle.load(handle)

#Turning dict_file into a dataframe: d_f_weather
d_f_weather = pd.DataFrame.from_dict(dict_file["06031"])
d_f_weather = d_f_weather.append(pd.DataFrame.from_dict(dict_file["06032"]))
d_f_weather = d_f_weather.append(pd.DataFrame.from_dict(dict_file["06065"]))

# print(d_f_weather)

#getting the average temperature by time and storing in dataframe avg_temp
avg_temp = d_f_weather.groupby("time").mean().reset_index()

# print(avg_temp)

#Converting to datetime on both avg_temp and d_f_consumption_sum
avg_temp['time'] = pd.to_datetime(avg_temp['time'])
d_f_consumption_sum['time'] = pd.to_datetime(d_f_consumption_sum['time']).dt.tz_localize(pytz.UTC)

# print(d_f_consumption_sum)
# print(avg_temp)

#Make a data set that includes all relevant data for training
d_f = pd.merge(avg_temp, d_f_consumption_sum, how='inner', on="time")

# #Plot data
# d_f.plot(x='time', y='GrossConsumptionMWh')
# # plt.figure(1)
# # plt.plot(d_f)
# # plt.legend()
# plt.show(block=True)

# d_f.plot(x='time', y='temperature')
# plt.show(block=True)

#one hot encoding time of day
d_f_hour_one_hot = pd.get_dummies(d_f.time.dt.hour, drop_first = True, prefix='hour')
d_f = pd.concat([d_f, d_f_hour_one_hot], axis = 1)

#including column on if it is a working day
#This is done by iterating through all the hours and seeing if the day is a work day or not
cal = Denmark()
workday = []
for hour in d_f['time']:
    if cal.is_working_day(hour):
        workday.append(1)
    else:
        workday.append(0)

#Adds the column
d_f = pd.concat([pd.DataFrame({'workday': workday}), d_f], axis = 1)
#save to parquet file
d_f.to_parquet('data/dataframe_consumption_temp.parquet', compression='gzip')

# print(d_f)