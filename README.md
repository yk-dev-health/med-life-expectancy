# Life Expectancy Analysis (Healthcare Data)

This project provides a reproducible CLI-based analysis pipeline for exploring
regional and gender-based differences in global life expectancy
using UN Data (2019–2024).

The workflow is designed as a lightweight analytics tool,
covering data aggregation, statistical comparison, and visualisation,
with outputs suitable for reporting and exploratory analysis
in a healthcare or population data context.

## Key Features
- Aggregation of life expectancy data across WHO regions
- Gender-based and region-based statistical comparison
- ANOVA with post-hoc t-tests for regional differences
- Static plots and interactive animated visualisations
- CLI-driven workflow for reproducibility
- Optional flag to skip statistical analysis (`--no-stats`)

**Future enhancements (planned):**
- Export statistical results to CSV (`--export results.csv`) for downstream analysis  
- Dedicated sample output documentation (`docs/sample_output.md`) for detailed examples


## Directory Structure
<pre>
med-life-expectancy/
├── data/
│   ├── raw/                # Original CSV datasets
│   └── output/             # Graphs and outputs
│     ├── area_average_life_expectancy.png
│     ├── global_average_life_expectancy.png
│     └── life_expectancy_animation.html
│
├── src/
│   ├── __init__.py
│   ├── data_processing.py  # Data loading, aggregation, and weighted average calculations
│   ├── statistics.py       # T-test and ANOVA functions
│   ├── visualization.py    # Plotting and visualization functions
│   └── main.py             # Main workflow of the project
├── README.md
└── requirements.txt
</pre>


## Data Source

- **UN Data:** [Life expectancy datasets](https://data.un.org/)  
  - Both sexes combined  
  - Male  
  - Female  

The dataset covers the period **2019–2024**, enabling comparison
before, during, and after the COVID-19 pandemic.

# Usage

Install dependencies:

```bash
git clone <repo-url>
pip install -r requirements.txt
python src/main.py
```

## Available Options

- `--plot {global,area,animated}`  
  Select the type of visual output.

- `--gender {both,male,female}`  
  Filter analysis by gender.

- `--no-stats`  
  Skip statistical analysis and generate visual outputs only.  
  Useful for exploratory analysis or animation generation.

## Example Output

Below is an example of the statistical summary produced by the CLI (when stats are enabled):

```text
=== Statistical Summary ===
ANOVA: F = 100.64, p = 3.15e-44
→ Significant differences detected among WHO regions.

Post-hoc t-tests (vs global average):
Area                                         p-value   Significant
WHO: Western Pacific region (WPRO)           6.68e-12  Yes
WHO: European Region (EURO)                  9.87e-08  Yes
WHO: African region (AFRO)                   1.93e-05  Yes
WHO: Americas (AMRO)                         3.56e-05  Yes
WHO: Eastern Mediterranean Region (EMRO)     4.16e-05  Yes
WHO: South-East Asia region (SEARO)           2.76e-03  Yes

## Regional Breakdown (WHO)
- **AFRO (African Region):** Countries in Africa.
- **AMRO (Americas Region):** North, Central, and South America.
- **EMRO (Eastern Mediterranean Region):** Middle East and North Africa.
- **EURO (European Region):** European countries.
- **SEARO (South-East Asia Region):** South Asian countries.
- **WPRO (Western Pacific Region):** East Asia and Pacific Islands.
- **World:** Global data combining all regions.
```

This summary enables quick identification of regions
with statistically significant deviations in life expectancy.


## Generated Outputs

The analysis produces the following artefacts:

- `area_average_life_expectancy.png`
- `global_average_life_expectancy.png`
- `life_expectancy_animation.html`

These outputs can be used for reporting, presentations, or exploratory data analysis.


## Notes

- Statistical analysis is intended for exploratory and comparative purposes.  
- `--no-stats` allows skipping statistics for faster visualisation-only runs.  

**Planned future enhancements:**

- Export CSV output for downstream analysis (`--export results.csv`)  
- Detailed output examples in `docs/sample_output.md`


## License

This project is intended for portfolio and demonstration purposes.  
No formal license is currently applied.