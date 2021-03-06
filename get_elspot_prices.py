# -*- coding: utf-8 -*-
"""
Created on Wed Jun 30 11:28:20 2021

@author: JPM
"""
import pickle
import requests
import json
import pandas as pd
import datetime as dt


def get_elspot_prices(start_date_str: str,
                      end_date_str: str,
                      save_to_pickle: bool = False) -> pd.DataFrame:
    '''
    Get elspot prices from EnergiDataService

    Parameters
    ----------
    start_date_str: str
        Start of period you want data from.
    end_date_str : str
        End of the period you want data from.
    save_to_file : bool, optional
        If you want the data saved this is set to True. The save name is
        elspot_prices_{start_date}_to_{end_date}.parquet. The default is False.

    Returns
    -------
    d_f : pandas.DataFrame
        Dataframe containing the elspot prices in hour resolution for the time
        period specified

    '''
    start_date = dt.datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end_date_str, "%Y-%m-%d")

    url_call = "https://api.energidataservice.dk/datastore_search_sql"
    sql_call = f"""SELECT * FROM "productionconsumptionsettlement"
    WHERE "HourUTC" >= '{start_date}' AND "HourUTC" < '{end_date}'
    AND "PriceArea" BETWEEN 'DK1' AND 'DK2'"""

    response = requests.get(url_call,
                            params={"sql": ' '.join(sql_call.split())})
    response = response.content.decode()
    response = json.loads(response)

    d_f = pd.DataFrame(response['result']['records'])

    if save_to_pickle:
        pkl_name = "data/consumption" + start_date_str
        pkl_name += "to" + end_date_str + ".pkl"

        with open(pkl_name, 'wb') as handle:
            pickle.dump(d_f, handle,
                        protocol=pickle.HIGHEST_PROTOCOL)

    return d_f



if __name__ == '__main__':
    for year in range(2015, 2021):
        start_date_str = f'{year}-01-01'
        end_date_str = f'{year+1}-01-01'
        get_elspot_prices(start_date_str, end_date_str, save_to_pickle=True)
