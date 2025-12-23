import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
from config import WHO_AREAS_COORDINATES

def plot_global_life_expectancy(global_data, colours, file_path):
    """
    Create a line plot for global average life expectancy (both sexes, male, and female).
    
    Args:
        global_data: dict with keys 'year', 'both', 'male', 'female' containing life expectancy values
        colours    : list of color hex codes for plotting each gender
        file_path  : directory path to save the figure
    """
    plt.figure(figsize=(10,6))

    for g, c in zip(['both','male','female'], colours):
        plt.plot(global_data['year'], global_data[g], marker='o', color=c, label=g.capitalize())

    plt.title('Global Average Life Expectancy (2019-2024)')
    plt.xlabel('Year')
    plt.ylabel('Life Expectancy (years)')
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{file_path}/global_average_life_expectancy.png')

def plot_area_life_expectancy(area_df, colours, areas, file_path):
    """
    Create bar plots of life expectancy by WHO area and gender for each year.

    Args:
        area_df  : DataFrame with columns ['area','year','gender','life_expectancy']
        colours  : list of color hex codes for plotting each gender
        areas    : list of WHO areas (used for consistent x-axis labels)
        file_path: directory path to save the figure
    """
    fig, axes = plt.subplots(2,3,figsize=(16,10),sharey=True)
    width = 0.25
    years = sorted(area_df['year'].unique())
    for i, year in enumerate(years):
        ax = axes[i//3,i%3]
        y_data = area_df[area_df['year']==year]
        for j, (g,c) in enumerate(zip(['both','male','female'], colours)):
            subset = y_data[y_data['gender']==g]
            x = np.arange(len(subset['area']))
            ax.bar(x+(j-1)*width, subset['life_expectancy'], width, label=g.capitalize(), color=c, alpha=0.7)
        ax.set_title(f'Life Expectancy by Area ({year})')
        ax.set_xticks(np.arange(len(areas)))
        ax.set_xticklabels(areas, rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.7)
    fig.tight_layout()
    plt.savefig(f'{file_path}/area_average_life_expectancy.png')

def plot_animated_map(area_df, file_path):
    """
    Create an animated bubble map of life expectancy for 'both' gender by WHO area.
    
    Args:
        area_df  : DataFrame with columns ['area','year','gender','life_expectancy']
        file_path: directory path to save the HTML animation
    """
    both_data = area_df[(area_df['gender']=='both') & (area_df['area']!='World')].copy() # Exclude 'World' for mapping
    both_data['lat'] = both_data['area'].map(lambda x: WHO_AREAS_COORDINATES[x]['lat']) # Get latitudes
    both_data['lon'] = both_data['area'].map(lambda x: WHO_AREAS_COORDINATES[x]['lon']) # Get longitudes

    both_data['scaled_size'] = (both_data['life_expectancy'] - both_data['life_expectancy'].min()) / \
                                (both_data['life_expectancy'].max() - both_data['life_expectancy'].min())*100
    fig = px.scatter_mapbox(both_data, lat='lat', lon='lon', color='life_expectancy',
                            size='scaled_size', hover_name='area', animation_frame='year',
                            size_max=40, zoom=1, color_continuous_scale='YlOrBr',
                            title='Life Expectancy by WHO Region (2019-2024)')
    fig.update_layout(mapbox_style='open-street-map') # Use open-street-map style
    fig.write_html(f'{file_path}/life_expectancy_animation.html')
