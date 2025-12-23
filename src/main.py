import argparse
from data_processing import read_life_expectancy_data, calculate_mean_life_expectancy, calculate_population, calculate_weighted_life_expectancy, prepare_area_life_expectancy_df
from visualisation import plot_global_life_expectancy, plot_area_life_expectancy, plot_animated_map
from stats_utils import perform_ttest, perform_anova

file_path = 'data/output'                           # Output directory for generated plots
colours = ['#F4D0A2', '#A6C9F2', '#D3AED6']   # Color palette for plotting

import pandas as pd

def print_stats_summary(t_results, f_stat, p_val, alpha=0.05):
    """
    Print ANOVA and post-hoc t-test results in a readable table.
    - t_results: dict of post-hoc t-test p-values by area
    - f_stat   : ANOVA F statistic
    - p_val    : ANOVA p-value
    - alpha    : significance threshold
    """
    print("\n=== Statistical Summary ===")
    print(f"ANOVA: F = {f_stat:.2f}, p = {p_val:.2e}")

    if p_val < alpha:
        print("→ Significant differences detected among areas.\n")
    else:
        print("→ No significant differences detected among areas.\n")

    rows = []
    for area, p in t_results.items():
        rows.append({
            "Area": area,
            "p-value": p,
            "Significant": "Yes" if p < alpha else "No"
        })

    # Sort areas by p-value and display as a table
    df = pd.DataFrame(rows).sort_values("p-value")

    print("Post-hoc t-tests (vs rest of world):")
    print(df.to_string(index=False, formatters={"p-value": lambda x: f"{x:.2e}"}))

def main(plot_type="global", gender="both", no_stats=False):
    """
    Main workflow for life expectancy analysis.
    - plot_type: type of plot to generate ('global', 'area', 'animated')
    - gender   : filter by 'male', 'female', or 'both'
    - no_stats : if True, skip statistical analysis
    """
    life_dfs, pop_dfs = read_life_expectancy_data()                       # Load raw life expectancy and population data

    mean_area = calculate_mean_life_expectancy(life_dfs)                  # Calculate mean life expectancy by
    pop_area = calculate_population(pop_dfs)                              # Calculate population
    global_life = calculate_weighted_life_expectancy(mean_area, pop_area) # Global weighted life expectancy
    area_df = prepare_area_life_expectancy_df(mean_area)                  # Flattened DataFrame for area life expectancy

    areas = area_df['area'].unique().tolist()

    # Filter by gender only (no year filtering)
    if gender != "both":
        area_df = area_df[area_df['gender'] == gender]

    # Generate plots based on selected type
    if plot_type == "global":
        plot_global_life_expectancy(global_life, colours, file_path)
    elif plot_type == "area":
        plot_area_life_expectancy(area_df, colours, areas, file_path)
    elif plot_type == "animated":
        plot_animated_map(area_df, file_path)

    # Stats (across all years) if not skipped
    if not no_stats:
        t_results = perform_ttest(area_df)
        f_stat, p_val = perform_anova(area_df)
        print_stats_summary(t_results, f_stat, p_val)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Life Expectancy Analysis CLI")
    parser.add_argument("--no-stats", action="store_true", help="Skip statistical analysis and only generate visual outputs")
    parser.add_argument("--plot", choices=["global", "area", "animated"], default="global")
    parser.add_argument("--gender", choices=["both", "male", "female"], default="both")
    args = parser.parse_args()

    main(plot_type=args.plot, gender=args.gender, no_stats=args.no_stats)