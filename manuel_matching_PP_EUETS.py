# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 15:35:51 2021

@author: Freddy
"""

import os
import logging

import pandas as pd




input_directory_path = os.path.join('input')
Bootom_up_methode_input_directory_path = os.path.join('input', 'Bootom_up_methode')
processed_directory_path = 'processed'
output_directory_path = os.path.join('output')

os.makedirs(input_directory_path, exist_ok=True)
os.makedirs(Bootom_up_methode_input_directory_path, exist_ok=True)
os.makedirs(processed_directory_path, exist_ok=True)
os.makedirs(output_directory_path, exist_ok=True)


# Checks if the the input directories are empty or not
# Checks all filenames in the input directory

if not os.listdir(Bootom_up_methode_input_directory_path) :
    print("The directory for the bootom up method is empty. Please provide the data to the directory as described in the instructions above.")


filenames = [os.path.join(Bootom_up_methode_input_directory_path, fn) for fn in os.listdir(Bootom_up_methode_input_directory_path)]

print(filenames)

def change_ProductionTypeName(ProductionTypeName):
    return ProductionTypeName.replace(
                    {
            'Fossil Hard coal': 'hard_coal', 
            'Fossil Brown coal/Lignite': 'lignite', 
            'Fossil Gas': 'gas', 
            'Fossil Oil': 'other_fossil',
            'Fossil Coal-derived gas': 'other_fossil',
            'Fossil Peat': 'other_fossil',
            'Fossil Oil Shale': 'other_fossil',
            'Nuclear': 'nuclear',
            'Biomass': 'biomass',
            'Waste': 'waste',
            'Geothermal': 'geothermal',
            'Marine': 'marine',
            'Other': 'other_fossil',
            'Hydro Pumped Storage': 'hydro',
            'Hydro Run-of-river and poundage': 'hydro',
            'Hydro Water Reservoir': 'hydro',
            'Fossil Oil': 'oil',
            'Fossil Oil shale': 'oil', 
            'Solar': 'solar',
            'Wind Onshore': 'wind_onshore',
            'Wind Offshore': 'wind_offshore',
            'Other renewable': 'other_renewable',
                                 }, regex = True, inplace = False)

def load_matching_data_EU(path, fn):
    """
    Matching List for EU power plants with Entso e identifier and the EUTL identifier.
        
    Parameters
    ----------
    path: str
        path to data
    fn : str
        filename
        
    """
    
    logging.info(f'Loading data from {fn}')
    
    df = pd.read_csv(os.path.join(path, fn), sep = ',', header = 0, index_col=0)

    return df

def load_EUTL_data(path, fn):
    """
    EU Emissions Data (EUTL)
        
    Parameters
    ----------
    path: str
        path to data
    fn : str
        filename
        
    """
    
    logging.info(f'Loading data from {fn}')
    
    df = pd.read_csv(os.path.join(path, fn),sep = ';', header = 13, encoding='ISO-8859-1')

    return df

def load_generation_data(path, fn):
    """
    Entso e gernation data per unit
        
    Parameters
    ----------
    path: str
        path to data
    fn : str
        filename
        
    """
    
    logging.info(f'Loading data from {fn}')
    
    df = pd.read_csv(os.path.join(path, fn),sep = ',',index_col=0,parse_dates=True)
    

    return df

def load_unit_data(path, fn):
    """
    Entso e generation unit information
        
    Parameters
    ----------
    path: str
        path to data
    fn : str
        filename
        
    """
    
    logging.info(f'Loading data from {fn}')
    
    df = pd.read_csv(os.path.join(path, fn),sep = ',',index_col=0)
    
    # Rename production type name according to own convention
    df.ProductionTypeName = change_ProductionTypeName(df.ProductionTypeName)
    
    # set name for the index
    df.index.set_names('GenerationUnitEIC', inplace=True)

    return df

def load_timeseries_opsd(path, fn):
    """
    Read data from OPSD time-series package own modification.

    
    """
    generation = (pd.read_csv(os.path.join(path, fn), index_col=[0], header=[0, 1, 2, 3, 4, 5], parse_dates=True)
                    .dropna(how="all", axis=0))
        
  
    
    generation = generation.rename(columns={'GB_UKM' : 'GB'})
    generation = generation.drop(columns='cet_cest_timestamp', level='region')
       
    
    return generation



generation_unit_info = load_unit_data(input_directory_path, 'unit_data_2018.csv')
generation_per_unit = load_generation_data(input_directory_path, 'gen_data_2018.csv')
EUTL_emissions = load_EUTL_data(Bootom_up_methode_input_directory_path, 'verified_emissions_2018_en.csv')
unit_matching_EU = load_matching_data_EU(Bootom_up_methode_input_directory_path, 'matching_ENTSOE_EU_ETS.csv')


unit_matching_EU['ID'] = unit_matching_EU.EUTL_countrycode + unit_matching_EU.EUTL_ID.astype(str)


EUTL_emissions['ID'] = EUTL_emissions.REGISTRY_CODE + EUTL_emissions.INSTALLATION_IDENTIFIER.astype(str)


EUTL_emissions_needed = EUTL_emissions[~EUTL_emissions.ID.isin(unit_matching_EU.ID)]
EUTL_emissions_needed = EUTL_emissions_needed[EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 != 'Excluded']

EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 = EUTL_emissions_needed.VERIFIED_EMISSIONS_2018.astype(int)

EUTL_emissions_we_have = EUTL_emissions[EUTL_emissions.ID.isin(unit_matching_EU.ID)]

#filzer
# REGISTRY_CODE = country
# MAIN_ACTIVITY_TYPE_CODE = 20 (buring fuel)

EUTL_emissions_check = EUTL_emissions_needed[(EUTL_emissions_needed.REGISTRY_CODE == 'FR') & (EUTL_emissions_needed.MAIN_ACTIVITY_TYPE_CODE == 20)]



# test = EUTL_emissions[EUTL_emissions.ID.isin(unit_matching_EU.ID)]
# EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 == 'Excluded'
# EUTL_emissions_needed[~EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 == 'Excluded']
# EUTL_emissions_needed[~(EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 == 'Excluded')]

# EUTL_emissions_needed = EUTL_emissions_needed[~(EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 == 'Excluded')]
# EUTL_emissions_needed.VERIFIED_EMISSIONS_2018.astype(int)
# EUTL_emissions_needed.VERIFIED_EMISSIONS_2018 = EUTL_emissions_needed.VERIFIED_EMISSIONS_2018.astype(int)
# EUTL_emissions_needed[~(EUTL_emissions_needed.MAIN_ACTIVITY_TYPE_CODE == '20')]
# EUTL_emissions_needed = EUTL_emissions_needed[~(EUTL_emissions_needed.MAIN_ACTIVITY_TYPE_CODE == '20')]
# EUTL_emissions = load_EUTL_data(Bootom_up_methode_input_directory_path, 'verified_emissions_2018_en.csv')


# EUTL_emissions = load_EUTL_data(Bootom_up_methode_input_directory_path, 'verified_emissions_2018_en.csv')