from dash import Dash, html, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import analysis.rs1 as rs1
import analysis.research_question_2 as research_question_2
import dash_bootstrap_components as dbc

df = pd.read_csv("./data/cleaned_bird_data.csv")
title_rq1 = "How have bird populations of climate-sensitive species changed across Asia, and how are these changes associated with regional trends in temperature, precipitation, and urbanization?"
fixed_df = rs1.prepare_data(df)

#research question 2
# modeled dataset
modeled_df_rq2 = research_question_2.get_bird_shift_climate_and_land_usage_data(df)
# Get unique countries and species
countries=set(modeled_df_rq2["country"])
bird_species=set(modeled_df_rq2["bird_species"])

# Get a sorted list of  countries  and species for dropdown items
country_list = sorted(list(countries))
bird_species_list = sorted(list(bird_species))
title_rq2 = "Research Question: Can bird movement patterns (Shift_km) be used as early-warning indicators of climate (Temperature) and land-use (Population) change across Asian ecosystems from 1980–2010? "
description_rq2 = "This analysis explores how the maximum annual movement distance (Shift_km) of bird species changes over time within each country, and how these temporal shifts occur in relation to climatic conditions and population levels, supporting the idea that changes in movement patterns can act as early indicators of environmental change."

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    html.Div([
        html.H1("Bird Population & Environmental Trends", 
                className="mb-2",
                style={'color': '#1a365d', 'fontWeight': '600'}),
        html.P("Analyzing climate-sensitive species across Asia",
               style={'color': '#64748b', 'fontSize': '1.1rem'})
    ], className="my-4 pb-3", style={'borderBottom': '3px solid #3b82f6'}),
    
    dbc.Card([
        dbc.CardBody([
            html.H5("Research Question", className="mb-2", style={'color': '#1e40af'}),
            html.P("Spyridon Mitsis", className="text-muted small mb-2"),
            html.P(title_rq1, style={'lineHeight': '1.6'})
        ])
    ], className="mb-4", style={'border': 'none', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'}),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Species", className="fw-semibold mb-2", 
                      style={'color': '#334155'}),
            dcc.Dropdown(
                id='species-dropdown',
                options=[{'label': s, 'value': s} for s in sorted(df["Bird_Species"].unique())],
                value='Siberian Crane',
                clearable=False
            )
        ], width=12, md=6)
    ], className="mb-4"),
    
    dbc.Card([
        dbc.CardBody([
            html.H5("Correlation with Environmental Variables", 
                   className="mb-3",
                   style={'color': '#1e40af'}),
            html.Div(id='correlation-table')
        ])
    ], className="mb-4", style={'border': 'none', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'}),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Population vs Environmental Factors", 
                              style={'backgroundColor': '#f8fafc', 'fontWeight': '600'}),
                dbc.CardBody([
                    dcc.Graph(id='graph-1', config={'displayModeBar': False})
                ])
            ], style={'border': 'none', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'})
        ], width=12, lg=7, className="mb-4 mb-lg-0"),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Population Change Over Time",
                              style={'backgroundColor': '#f8fafc', 'fontWeight': '600'}),
                dbc.CardBody([
                    dcc.Graph(id='graph-2', config={'displayModeBar': False})
                ])
            ], style={'border': 'none', 'boxShadow': '0 2px 8px rgba(0,0,0,0.08)'})
        ], width=12, lg=5)
    ], className="mb-4"),


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

    ], className="mb-4")
    
], fluid=True, style={'backgroundColor': '#f9fafb', 'minHeight': '100vh', 'padding': '2rem 1rem'})




@callback(
    Output('graph-1', 'figure'),
    Output('graph-2', 'figure'),
    Output('correlation-table', 'children'),
    Input('species-dropdown', 'value')
)
def update_graph(species):
    # Figures
    fig1 = rs1.plot_population_vs_env(fixed_df, species)
    fig2 = rs1.get_population_change(fixed_df, species)
    
    # Clean figure styling
    for fig in [fig1, fig2]:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'family': 'system-ui, -apple-system, sans-serif', 'size': 12},
            margin=dict(t=10, b=10, l=10, r=10)
        )
    
    corr_df = rs1.compute_corr_with_env(fixed_df, species)
    
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
    bar_fig,line_fig = research_question_2.plot_bird_shift_climate_and_land_usage_data(
        modeled_df_rq2,
        selected_country,
        selected_bird_species
    )
    return  bar_fig,line_fig

if __name__ == "__main__":
    app.run(debug=True)
