from datetime import tzinfo
import pickle
import pandas as pd
import pytz
from dateutil.easter import easter
import holidays
from get_date_type import get_date_type


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

#Itereat through time in

print(d_f)