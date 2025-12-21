import plotly.graph_objects as go  
import plotly.express as px
import pandas as pd


""" Plotly’s graph_objects module was used instead of Plotly Express because 
the analysis required dual-axis time-series plots and grouped bar charts with 
explicit control over axes and categorical variables, 
which are not fully supported by high-level plotting interfaces.
"""

def plot_bird_shift_climate_and_land_usage_data(climate_df: pd.DataFrame, country: str, bird_species: str):
    """
    Creates visualizations of climate-related bird movement data.

    This function filters climate summary data for a specific country and
    bird species, then generates:
    1. A dual-axis line chart showing population and maximum shift distance
       over time.
    2. A grouped bar chart comparing maximum shift distance and temperature
       for each year.

    :param climate_df: DataFrame containing summarized climate data.
                       Required columns: country, species, year,
                       population_at_max_shift, max_shift_km,
                       temperature_at_max_shift
    :type climate_df: pd.DataFrame
    :param country: Country name to filter the data
    :type country: str
    :param species: Bird species name to filter the data
    :type species: str
    :return: Tuple containing (line_chart_figure, bar_chart_figure).
             Returns (None, None) if no matching data is found.
    :rtype: tuple
    """

    # Filter the DataFrame by the selected country and species, then sort by year
    filtered = climate_df[
        (climate_df["country"] == country) &
        (climate_df["bird_species"] == bird_species)
    ].sort_values("year")

    # Return None if no data is available for the given filters
    if filtered.empty:
        return None, None

    # Convert year to string so Plotly treats it as a categorical axis
    filtered["year_str"] = filtered["year"].astype(str)

    # ---------- LINE GRAPH ----------
    # Create a figure for population and maximum shift over time
    line_fig = go.Figure()

    # Add max shift distance line (right y-axis)
    line_fig.add_trace(go.Scatter(
        x=filtered["year_str"],
        y=filtered["max_shift_km"],
        mode="lines+markers",
        name="Max Shift_km",
        yaxis="y1"
    ))
    # Add population line (left y-axis)
    line_fig.add_trace(go.Scatter(
        x=filtered["year_str"],
        y=filtered["population_at_max_shift"],
        mode="lines+markers",
        name="Population at max shift_km",
        yaxis="y2"
    ))

    

    # Configure layout with dual y-axes
    line_fig.update_layout(
        title=f"Population and Max Shift_km Over Time — {bird_species} in {country}",
        xaxis_title="Year",
        yaxis=dict(title=" Max Shift_km"),
        yaxis2=dict(
            title="Population at max shift_km",
            overlaying="y",
            side="right"
        )
    )

    # Reshape data for Plotly Express
    long_df = filtered.melt(
        id_vars="year_str",
        value_vars=["max_shift_km", "temperature_at_max_shift"],
        var_name="Variable",
        value_name="Value"
    )

    # Create grouped bar chart
    bar_fig = px.bar(
        long_df,
        x="year_str",
        y="Value",
        color="Variable",
        barmode="group",
        title=f"Max Shift_km and Temperature by Year — {bird_species} in {country}",
        labels={
            "year_str": "Year",
            "Value": "Value",
            "Variable": "Metric"
        }
    )
    
    return bar_fig, line_fig
