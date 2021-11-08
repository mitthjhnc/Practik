# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 13:37:20 2021

@author: JPM
"""

import pandas as pd
import requests
import json
import pickle
from typing import Dict


def get_dmi_data(
        api_key: str,
        json_filename: str = 'inputs/weather_stations.json',
        start_date: str = '2015-01-01',
        end_date: str = '2021-06-01',
        save_to_pickle: bool = False) -> Dict:
    '''
    Get temperature data from DMI for a list of stations in for every hour
    between midnight at a specified start and end date.

    Parameters
    ----------
    api_key : str
        API-key acquired from DMI.
    stations : str
        Name of json file with the weather stations to load data from.
        The default is 'inputs/weather_stations.json'
    start_date : str, optional
        Start date from which to gather the data. Day is included in the data.
        The default is '2015-01-01'.
    end_date : str, optional
        Date to collect data to. Date is not included in the output data.
        The default is '2021-06-01'.
    save_to_pickle : bool, optional
        If true, saves the output to a .pkl file with the filename
        "data/Weather/temp_stations_dict<start_date>to<end_date>.pkl"
        The default is False.

    Returns
    -------
    stations_data: Dict
        Dictionary with the station ID as key and a pandas dataframe with
        time, temperature data and station id as value.

    '''
    json_file = open(json_filename, encoding='utf-8')
    station_ids = json.load(json_file)
    json_file.close()

    station_ids = list(station_ids.keys())

    url = "https://dmigw.govcloud.dk/v2/climateData/collections/stationValue/"
    items = "items?"
    station = "stationId="
    resolution = "timeResolution=hour"
    datetime = "datetime="
    limit = "limit=60000"
    start_date_time = start_date + "T00:00:00Z/"
    end_date_time = end_date + "T00:00:00Z"
    parameters = "parameterId="
    parameter_id = "mean_temp"

    stations_data = {}
    for station_id in station_ids:
        url_call = url + items + station + station_id + '&' + datetime
        url_call += start_date_time + end_date_time + '&' + resolution + '&'
        url_call += limit + '&' + parameters + parameter_id + '&' + 'api-key='
        url_call += api_key

        print(url_call)
        response = requests.get(url_call)

        dates = []
        values = []
        data_list = response.json()['features']
        for data in data_list:
            date_to = pd.to_datetime(
                data['properties']['to']).astimezone('UTC')
            dates.append(date_to)
            values.append(data['properties']['value'])

        d_f = pd.DataFrame({
            "time": dates,
            "temperature": values,
            "station_id": station_id
            })

        stations_data[station_id] = d_f

    if save_to_pickle:
        pkl_name = "data/Weather/temp_stations_dict" + start_date
        pkl_name += "to" + end_date + ".pkl"

        with open(pkl_name, 'wb') as handle:
            pickle.dump(stations_data, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    return stations_data


if __name__ == '__main__':
    credentials = 'inputs/dmi_credentials.json'
    f = open(credentials)
    api_key = json.load(f)
    f.close()

    api_key = api_key['api-key']
    start_date = '2015-01-01'
    end_date = '2021-06-01'
    json_filename = 'inputs/weather_stations.json'

    stations_data = get_dmi_data(api_key,
                                 json_filename,
                                 start_date=start_date,
                                 end_date=end_date,
                                 save_to_pickle=True)

    print(stations_data)

    pkl_name = "data/Weather/temp_stations_dict" + '2015-01-01'
    pkl_name += "to" + '2021-06-01' + ".pkl"

    with open(pkl_name, 'rb') as handle:
        dict_file = pickle.load(handle)

    print(dict_file)
