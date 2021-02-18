# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 18:03:04 2021

@author: Freddy
"""
import pandas as pd
import os


def change_ENTSOE_ProductionTypeName (ProductionTypeName):
    """
    Converts ENTSO-E ProductionTypeNames into INATECH technology type names.

    Parameters
    ----------
    ProductionTypeName : string
        DESCRIPTION.

    Returns
    -------
    string
        DESCRIPTION.

    """
    return ProductionTypeName.replace({
            'Fossil Hard coal': 'hard_coal', 
            'Fossil Brown coal/Lignite': 'lignite', 
            'Fossil Gas': 'gas',
            'Fossil Coal-derived gas': 'other_fossil',
            'Fossil Peat': 'other_fossil',
            'Nuclear': 'nuclear',
            'Biomass': 'biomass',
            'Waste': 'waste',
            'Geothermal': 'other_renewable',
            'Marine': 'other_renewable',
            'Other': 'other_fossil',
            'Hydro Pumped Storage': 'hydro',
            'Hydro Run-of-river and poundage': 'hydro',
            'Hydro Water Reservoir': 'hydro',
            'Fossil Oil': 'other_fossil',
            'Fossil Oil shale': 'other_fossil', 
            'Solar': 'solar',
            'Wind Onshore': 'wind_onshore',
            'Wind Offshore': 'wind_offshore',
            'Other renewable': 'other_renewable'}, inplace = False)



def load_timeseries_ENTSOE(path, fn):
    """
    Read generation data from time-series package own modification.


    Parameters
    ----------
    path : TYPE
        DESCRIPTION.
    fn : TYPE
        DESCRIPTION.

    Returns
    -------
    generation : TYPE
        DESCRIPTION.

    """
   
    generation = (pd.read_csv(os.path.join(path, fn), index_col=[0], header=[0, 1, 2, 3, 4, 5], parse_dates=True)
                    .dropna(how="all", axis=0))
        
  
    
    generation = generation.rename(columns={'GB_UKM' : 'GB'})
    generation = generation.drop(columns='cet_cest_timestamp', level='region')
    
    generation.columns = generation.columns.droplevel(level=[2,3,4,5])
       
    
    return generation

def get_country(string):
    # split string and takes the first part
    string = string.split(',')[-1]
    return string

def aligndata(data, CO2_cleaned):
    #consider only countries which appear in both datasets; to have all of them included specific effort is needed.
    data = data[pd.Series(CO2_cleaned.columns)[pd.Series(CO2_cleaned.columns).apply(lambda x: x in data.columns)]].sort_index()
    data = data.set_index(CO2_cleaned.index)
    return data
