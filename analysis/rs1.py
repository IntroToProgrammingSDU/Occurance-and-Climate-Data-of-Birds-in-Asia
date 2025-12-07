import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    # Aggregate population per species per year
    df_yearly = df.groupby(["Bird_Species", "Year"])["Population"].sum().reset_index()

    # Pivot population table
    df_pivot = (
        df_yearly.pivot(
            index="Year",
            columns="Bird_Species",
            values="Population"
        ).reset_index()
    )

    # Compute average temperature, precipitation, traffic per year
    df_avg = (
        df.groupby("Year")[["Temperature", "Precipitation", "Traffic"]]
        .mean()
        .reset_index()
    )

    # Merge population pivot with environmental variables
    df_merged = (
        pd.merge(
            df_pivot,
            df_avg,
            on="Year",
            how="inner"
        )
    )


    return df_merged



def plot_population_vs_env(df: pd.DataFrame, species: str):
    df_sorted = df.sort_values("Year")
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df[species],
        mode='lines+markers',
        name=f"{species} Population",
        yaxis="y1",
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Temperature"],
        mode='lines+markers',
        name=f"Temperature °C",
        yaxis="y2",
        visible="legendonly"
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Precipitation"],
        mode='lines+markers',
        name=f"Precipitation mm",
        yaxis="y3",
        visible="legendonly"
    ))

    fig.add_trace(go.Scatter(
        x=df["Year"],
        y=df["Traffic"],
        mode='lines+markers',
        name=f"Traffic Index",
        yaxis="y4",
        visible="legendonly"
    ))

    fig.update_layout(
        title=f"Population and Environmental Trends for {species}",
        xaxis=dict(title="Year"),
        yaxis=dict(title="Population", side="left"),
        yaxis2=dict(title="Temperature (°C)", overlaying="y", side="right"),
        yaxis3=dict(title="Precipitation (mm)", overlaying="y", side="left", position=0.05),
        yaxis4=dict(title="Traffic Index", overlaying="y", side="right", position=0.95),
        legend=dict(x=1.05, y=1),
    )

    return fig


def get_population_change(df: pd.DataFrame, species: str):
    fig = px.scatter(
        df,
        x=df["Year"],
        y=df[species],
        labels={"x": "Year", "y": "Population"},
        title=f"Population of {species} Over Time",
        trendline="ols"
    )
    return fig


def compute_corr_with_env(df: pd.DataFrame, species: str) -> pd.DataFrame:
    """
    Compute correlation between a species population and environmental variables.
    Returns a dataframe with correlation values.
    """
    cols = [species, "Temperature", "Precipitation", "Traffic"]
    corr_matrix = df[cols].corr()
    
    # Keep only correlations with the species
    corr_with_species = corr_matrix[[species]].drop(species)
    
    return corr_with_species

if __name__ == "__main__":
    file = "../Occurance_and_climatedata_of_birds.csv"
    df = pd.read_csv(file)
    df_fixed = prepare_data(df)
    plot_population_vs_env(df_fixed, "Asian Koel")

