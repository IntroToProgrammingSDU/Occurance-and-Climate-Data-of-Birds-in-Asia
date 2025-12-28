import pandas as pd
import plotly.express as px


"""
Hafijur_rs.py

Research Analysis:
How environmental conditions (temperature, precipitation,
and human activity) shape habitat suitability patterns
for bird species across Asia (1980–2010).

This script produces two clear and simple visualizations:
1. Habitat Suitability vs Temperature (Scatter + Trendline)
2. Habitat Suitability vs Human Activity (Scatter + Trendline)

The visuals are intentionally minimal and easy to explain.
"""


def plot_habitat_suitability_analysis(df: pd.DataFrame, species: str):

    filtered = df[df["bird_species"] == species].copy()

    if filtered.empty:
        return None, None

    # Human activity index
    filtered["human_activity_index"] = (
        filtered["population"] + filtered["traffic"]
    ) / 2

    # ✅ CREATE habitat suitability index
    filtered["habitat_suitability"] = (
        (filtered["temperature"].rank(pct=True) * 0.4)
        + (filtered["precipitation"].rank(pct=True) * 0.4)
        - (filtered["human_activity_index"].rank(pct=True) * 0.2)
    )

    # ---------- Temperature vs Habitat Suitability ----------
    fig_temp = px.scatter(
        filtered,
        x="temperature",
        y="habitat_suitability",
        trendline="ols",
        title=f"Temperature vs Habitat Suitability<br><sup>{species} (Asia, 1980–2010)</sup>",
        labels={
            "temperature": "Average Temperature (°C)",
            "habitat_suitability": "Habitat Suitability Index"
        }
    )

    # ---------- Human Activity vs Habitat Suitability ----------
    fig_human = px.scatter(
        filtered,
        x="human_activity_index",
        y="habitat_suitability",
        trendline="ols",
        title=f"Human Activity vs Habitat Suitability<br><sup>{species} (Asia, 1980–2010)</sup>",
        labels={
            "human_activity_index": "Human Activity Index",
            "habitat_suitability": "Habitat Suitability Index"
        }
    )

    return fig_temp, fig_human



# -------------------- RUN TEST --------------------
if __name__ == "__main__":
    file_path = "../data/cleaned_bird_data.csv"
    df = pd.read_csv(file_path)

    # Example species (change if needed)
    fig1, fig2 = plot_habitat_suitability_analysis(
        df,
        species="Asian Koel"
    )

    if fig1 and fig2:
        fig1.show()
        fig2.show()
