from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import analysis.spyros_rs as spyros_rs
import analysis.hafsa_rs as hafsa_rs
import analysis.mahfuz_rs as mahfuz_rs
import dash_bootstrap_components as dbc
import data.cleaner as cleaner



df = pd.read_csv("./data/cleaned_bird_data.csv")

title_spyros = "Reseach Question: How have bird populations of climate-sensitive species changed across Asia, and how are these changes associated with regional trends in temperature, precipitation, and urbanization?"

description_spyros = (
    "This analysis examines how populations of climate-sensitive bird species have changed "
    "across Asian regions over time, and investigates how these population trends are related "
    "to variations in temperature, precipitation, and levels of urbanization. By linking "
    "population dynamics with environmental factors, the analysis aims to highlight patterns "
    "that may indicate ecological responses to climate and land-use change."
)

modeled_df_spyros = cleaner.model_data_spyros(df)

#research question 2
# modeled dataset
modeled_df_hafsa = cleaner.get_bird_shift_climate_and_land_usage_data(df)
# Get unique countries and species
countries=set(modeled_df_hafsa["country"])
bird_species=set(modeled_df_hafsa["bird_species"])

# Get a sorted list of  countries  and species for dropdown items
country_list = sorted(list(countries))
bird_species_list = sorted(list(bird_species))
title_rq2 = "Research Question: Can bird movement patterns (Shift_km) be used as early-warning indicators of climate (Temperature) and land-use (Population) change across Asian ecosystems from 1980–2010? "
description_rq2 = "This analysis explores how the maximum annual movement distance (Shift_km) of bird species changes over time within each country, and how these temporal shifts occur in relation to climatic conditions and population levels, supporting the idea that changes in movement patterns can act as early indicators of environmental change."


# ========= Research Question 3 (Mahfuz) =========
species_per_country = mahfuz_rs.build_species_per_country_table(df)
species_diversity_fig = mahfuz_rs.plot_species_diversity_by_country(species_per_country)

title_rq3 = (
    "Research Question: How does bird species diversity vary across countries, "
    "and which country stands out as the richest habitat?"
)

description_rq3 = (
    "This analysis compares bird species diversity across Asian countries in our "
    "dataset. All countries have the same number of recorded bird species, so no "
    "single country clearly stands out as the richest habitat here, which suggests "
    "that the dataset is too limited to capture true differences in diversity."
)


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
# Research Question 1 (Spyros)
    html.H1(
        "Bird Population & Environmental Trends",
        className="text-center my-4"
    ),
    dbc.Row(
        dbc.Col(
            html.H3(
                title_spyros,
                className="text-primary"
            ),
            width=12
        ),
        className="mb-3 mx-3"
    ),
    
    dbc.Row(
        dbc.Col(
            html.H4(
                "By Spyridon Mitsis",
                className="lead"
            ),
            width=12
        ),
        className="mb-3 mx-3"
    ),
    
    dbc.Row(
        dbc.Col(
            html.P(
                description_spyros,
                className="lead"
            ),
            width=12
        ),
        className="mb-4 mx-3"
    ),
    
    # Dropdown
    dbc.Row(
        dbc.Col([
            html.Label("Select Species:"),
            dcc.Dropdown(
                id='species-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(df["bird_species"].unique())],
                value='Siberian Crane',
                clearable=False
            )
        ], width=6),
        justify="center",
        className="mb-4"
    ),
    
    # Correlation Table
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5(
                        "Correlation with Environmental Variables",
                        className="text-primary mb-3"
                    ),
                    html.Div(id='correlation-table')
                ])
            ),
            width=10
        ),
        justify="center",
        className="mb-4"
    ),
    
    # Plots
    dbc.Row([
        dbc.Col(
            dcc.Graph(id='graph-1', config={'displayModeBar': False}),
            width=7
        ),
        dbc.Col(
            dcc.Graph(id='graph-2', config={'displayModeBar': False}),
            width=5
        )
    ], className="mb-5"),


 #research question 2

# Title
    html.H1(
        "Bird Climate Early-Warning Dashboard",
        className="text-center my-4"
    ),
    dbc.Row(
            dbc.Col(html.H3(
                            title_rq2,
                            className="text-primary"), width=12),
                             className="mb-4 mx-3"
                         ),
    dbc.Row(
            dbc.Col(html.H4(
                            " By Hafsa Akter",
                            className="lead"), width=12),
                             className="mb-4 mx-3"
                         ),                     
    dbc.Row(
            dbc.Col(html.P(
                description_rq2,
                className="lead"), width=12),
                 className="mb-4 mx-3"
        ),

    # Dropdowns for country and bird species selection
    dbc.Row([

        dbc.Col([
            html.Label("Select Country:"),
            dcc.Dropdown(
                id="country-dropdown",
                options=[{"label": c, "value": c} for c in country_list],
                value=country_list[0],
                clearable=False
            )
        ], width=5),

        dbc.Col([
            html.Label("Select Bird Species:"),
            dcc.Dropdown(
                id="bird-species-dropdown",
                options=[{"label": s, "value": s} for s in bird_species_list],
                value=bird_species_list[0],
                clearable=False
            )
        ], width=5)

    ], justify="center", className="mb-4"),

    
# Plots Section (Side-by-Side)
   dbc.Row([
        dbc.Col([
           dcc.Graph(
            id="bar-plot",
            style={"height": "70vh"}
            )
        ], width=6),

        dbc.Col([
          dcc.Graph(
            id="line-plot",
            style={"height": "70vh"}
            )
        ], width=6)

    ], className="mb-4"),
        html.H1(
            "Bird Species Diversity Dashboard",
            className="text-center my-4",
        ),
        dbc.Row(
            dbc.Col(
                html.H3(
                    title_rq3,
                    className="text-primary",
                ),
                width=12,
            ),
            className="mb-3 mx-3",
        ),
        dbc.Row(
            dbc.Col(
                html.H4(
                    "By Mahfuz",
                    className="lead",
                ),
                width=12,
            ),
            className="mb-3 mx-3",
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    description_rq3,
                    className="lead",
                ),
                width=12,
            ),
            className="mb-4 mx-3",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(
                    id="species-diversity-graph",
                    figure=species_diversity_fig,
                    style={"height": "70vh"},
                ),
                width=10,
            ),
            justify="center",
            className="mb-4",
        ),
    ],
    fluid=True,
    style={
        "backgroundColor": "#f9fafb",
        "minHeight": "100vh",
        "padding": "2rem 1rem",
    },
)




@callback(
    Output('graph-1', 'figure'),
    Output('graph-2', 'figure'),
    Output('correlation-table', 'children'),
    Input('species-dropdown', 'value')
)
def update_graph(species):
    # Figures
    fig1 = spyros_rs.plot_population_vs_env(modeled_df_spyros, species)
    fig2 = spyros_rs.get_population_change(modeled_df_spyros, species)
    
    # Clean figure styling
    for fig in [fig1, fig2]:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'family': 'system-ui, -apple-system, sans-serif', 'size': 12},
            margin=dict(t=80, b=10, l=10, r=10)
        )
    
    corr_df = spyros_rs.compute_corr_with_env(modeled_df_spyros, species)
    
    table_rows = []
    for var, val in zip(corr_df.index, corr_df[species]):
        table_rows.append(
            html.Tr([
                html.Td(var, style={'padding': '0.75rem', 'fontWeight': '500'}),
                html.Td(
                    f"{val:.3f}",
                    style={
                        'padding': '0.75rem',
                        'textAlign': 'right',
                        'fontWeight': '600'
                    }
                )
            ])
        )
    
    table = dbc.Table(
        [
            html.Thead(
                html.Tr([
                    html.Th("Variable", style={'padding': '0.75rem'}),
                    html.Th("Correlation", style={'padding': '0.75rem', 'textAlign': 'right'})
                ]), style={'backgroundColor': '#f1f5f9'}
            ),
            html.Tbody(table_rows)
        ],
        bordered=True,
        hover=True,
        style={'marginBottom': '0'}
    )
    
    return fig1, fig2, table
#research question 2 callbacks
@app.callback(
    [Output("bar-plot", "figure"), Output("line-plot", "figure")],
    [Input("country-dropdown", "value"),Input("bird-species-dropdown", "value")]
)
def update_plots(selected_country, selected_bird_species):
    """
    Updates dashboard plots based on selected country and bird species.
    """
    bar_fig,line_fig = hafsa_rs.plot_bird_shift_climate_and_land_usage_data(
        modeled_df_hafsa,
        selected_country,
        selected_bird_species
    )
    return  bar_fig,line_fig

if __name__ == "__main__":
    app.run(debug=True)
