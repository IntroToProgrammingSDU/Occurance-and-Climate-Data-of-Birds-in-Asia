import pandas as pd
import plotly.express as px

from data.cleaner import clean_bird_data, model_data_mahfuz
# cleaner.py lives in data/, and now contains model_data_mahfuz(df)


def build_species_per_country_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Use the shared modelling function to build a small summary table.

    The result will have one row per country and show
    how many different bird species appear in that country.
    """
    # Call the helper in cleaner.py so the logic lives in one place
    species_per_country = model_data_mahfuz(df)
    return species_per_country


def plot_species_diversity_by_country(species_per_country: pd.DataFrame):
    """
    Draw a bar chart that shows, for each country,
    how many different bird species it has.
    """
    # Sort so the countries with the highest number of species appear first
    data_sorted = species_per_country.sort_values(
        "species_count", ascending=False
    )

    # Build a bar chart: x = country, y = number of unique bird species
    fig = px.bar(
        data_sorted,
        x="country",
        y="species_count",
        labels={
            "country": "Country",
            "species_count": "Number of unique bird species",
        },
        title="Bird species diversity by country",
    )

    # Give the finished plot back to the caller (main.py or a test file)
    return fig


if __name__ == "__main__":
    # Small standalone test so the teacher can run only this file if needed

    # 1. Clean the raw data once using cleaner.py
    df_clean = clean_bird_data("./Occurance_and_climatedata_of_birds.csv")

    # 2. Build the species-per-country table for Mahfuz's question
    species_per_country = build_species_per_country_table(df_clean)

    # 3. Make the bar chart and show it
    fig = plot_species_diversity_by_country(species_per_country)
    fig.show()
