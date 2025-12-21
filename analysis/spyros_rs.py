import pandas as pd
import plotly.graph_objects as go
import dash
import plotly.express as px





def plot_population_vs_env(df: pd.DataFrame, species: str):
    df_sorted = df.sort_values("year")
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted[species],
        mode='lines+markers',
        name=f"{species} Population",
        yaxis="y1",
    ))
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted["temperature"],
        mode='lines+markers',
        name=f"Temperature °C",
        yaxis="y2",
        visible="legendonly"
    ))
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted["precipitation"],
        mode='lines+markers',
        name=f"Precipitation mm",
        yaxis="y3",
        visible="legendonly"
    ))
    fig.add_trace(go.Scatter(
        x=df_sorted["year"],
        y=df_sorted["traffic"],
        mode='lines+markers',
        name=f"Traffic Index",
        yaxis="y4",
        visible="legendonly"
    ))
    fig.update_layout(
        title=f"Population and Environmental Trends for {species}",
        xaxis=dict(title="Year", domain=[0.1, 0.9]),
        yaxis=dict(
            title="Population", 
            side="left",
            position=0.0
        ),
        yaxis2=dict(
            title="Temperature (°C)", 
            overlaying="y", 
            side="right",
            position=1.0
        ),
        yaxis3=dict(
            title="Precipitation (mm)", 
            overlaying="y", 
            side="left", 
            position=0.1
        ),
        yaxis4=dict(
            title="Traffic Index", 
            overlaying="y", 
            side="right", 
            position=0.9
        ),
        legend=dict(x=1.15, y=1, xanchor='left'),
        margin=dict(t=80, r=100)
    )
    return fig

def get_population_change(df: pd.DataFrame, species: str):
    fig = px.scatter(
        df,
        x="year",
        y=species,
        labels={"year": "Year", species: "Population"},
        title=f"Population of {species} Over Time",
        trendline="ols"
    )
    fig.update_layout(
        margin=dict(l=60, r=40, t=100, b=60)
    )
    return fig

def compute_corr_with_env(df: pd.DataFrame, species: str) -> pd.DataFrame:
    """
    Compute correlation between a species population and environmental variables.
    Returns a dataframe with correlation values.
    """
    cols = [species, "temperature", "precipitation", "traffic"]
    corr_matrix = df[cols].corr()
    
    # Keep only correlations with the species
    corr_with_species = corr_matrix[[species]].drop(species)
    
    return corr_with_species

if __name__ == "__main__":
    file = "../data/cleaned_bird_data.csv"
    df = pd.read_csv(file)
    plot_population_vs_env(df, "Asian Koel")

