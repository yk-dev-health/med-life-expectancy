import numpy as np
from scipy.stats import ttest_ind, f_oneway

def perform_ttest(df):
    """"
    Perform t-tests between male and female life expectancy for each area.
    """
    results = {}
    for area in df['area'].unique():
        subset = df[df['area']==area]
        male_vals = subset[subset['gender']=='male']['life_expectancy']
        female_vals = subset[subset['gender']=='female']['life_expectancy']
        if len(male_vals)>0 and len(female_vals)>0:
            t, p = ttest_ind(male_vals,female_vals,equal_var=False)
        else:
            t, p = np.nan, np.nan
        results[area] = p
    return results

def perform_anova(df):
    """
    Perform one-way ANOVA across all areas.
    """
    groups = [df[df['area']==area]['life_expectancy'].dropna() for area in df['area'].unique()]
    f_stat, p_val = f_oneway(*groups) # Unpack groups for f_oneway
    return f_stat, p_val