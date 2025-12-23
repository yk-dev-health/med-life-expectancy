import pandas as pd
import numpy as np
from config import WHO_AREAS_COORDINATES

def read_life_expectancy_data():
    """Load life expectancy and population CSVs."""
    life_expectancy = {
        'both': pd.read_csv('data/raw/UNdata_Export_20250106_135531463.csv'),
        'male': pd.read_csv('data/raw/UNdata_Export_20250106_135951253.csv'),
        'female': pd.read_csv('data/raw/UNdata_Export_20250106_140234264.csv'),
    }
    population = {
        'both': pd.read_csv('data/raw/UNdata_Export_20250217_214426488.csv'),
        'male': pd.read_csv('data/raw/UNdata_Export_20250217_214612681.csv'),
        'female': pd.read_csv('data/raw/UNdata_Export_20250217_214748417.csv'),
    }
    return life_expectancy, population

def extract_values(df, area):
    """""
    Extract life expectancy or population values for a specific area from 2019 to 2024.
    Args:
        df: DataFrame containing the raw data
        area: str, area name (e.g., WHO region)
    Returns:
        dict: year -> value
    """
    return {year: df[(df['Country or Area']==area) & (df['Year(s)']==year)]['Value'].values[0]
            for year in range(2019, 2025) if not df[(df['Country or Area']==area) & (df['Year(s)']==year)].empty}

def calculate_mean_life_expectancy(life_dfs):
    """
    Extract life expectancy or population values for a specific area from 2019 to 2024.
    Args:
        df: DataFrame containing the raw data
        area: str, area name (e.g., WHO region)
    Returns:
        dict: year -> value
    """
    return {area: {g: extract_values(df, area) for g, df in life_dfs.items()} for area in WHO_AREAS_COORDINATES.keys()}

def calculate_population(pop_dfs):
    """
    Calculate population by area and gender.
    Args:
        pop_dfs: dict of DataFrames for each gender
    Returns:
        dict: area -> gender -> year -> population
    """
    return {area: {g: extract_values(df, area) for g, df in pop_dfs.items()} for area in WHO_AREAS_COORDINATES.keys()}

def calculate_weighted_life_expectancy(mean_area, pop_area):
    """
    Compute global weighted life expectancy by weighting each area's life expectancy
    by its population.
    Args:
        mean_area: dict of area -> gender -> year -> life expectancy
        pop_area: dict of area -> gender -> year -> population
    Returns:
        dict: year -> gender -> weighted global life expectancy
    """
    global_data = {'year': list(range(2019,2025)), 'both':[], 'male':[], 'female':[]}
    for year in range(2019,2025):
        for g in ['both','male','female']:
            life_values, pop_values = [], []
            for area in mean_area.keys():
                if year in mean_area[area][g]:
                    life_values.append(mean_area[area][g][year])
                    pop_values.append(pop_area[area][g][year])
            if pop_values:
                weighted = np.nansum(np.array(life_values)*np.array(pop_values))/np.nansum(pop_values)
            else:
                weighted = np.nan
            global_data[g].append(weighted)
    return global_data

def prepare_area_life_expectancy_df(mean_area):
    """
    Flatten nested mean_area dict to a DataFrame suitable for plotting.
    Args:
        mean_area: dict of area -> gender -> year -> life expectancy
    Returns:
        pd.DataFrame with columns ['area', 'year', 'gender', 'life_expectancy']
    """
    records = []
    for area, gender_dict in mean_area.items():
        for gender, year_dict in gender_dict.items():
            for year, val in year_dict.items():
                records.append({'area': area, 'year': year, 'gender': gender, 'life_expectancy': val})
    return pd.DataFrame(records)