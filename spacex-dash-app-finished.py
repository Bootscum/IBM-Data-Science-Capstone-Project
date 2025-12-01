# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),

    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        searchable=True
    ),

    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    dcc.RangeSlider(
        id='payload-slider',
        min=0, max=10000, step=1000,
        marks={0: '0',
                10000: '10000'},
        value=[min_payload, max_payload]),

    html.Br(),
    
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))




])




##### ADD Callbacks && Functions
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)


###Make Charts
    ####Pie
def update_pie(site):
    df = spacex_df

    if site == 'ALL':
        fig = px.pie(
            df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches for All Sites'
        )
    else:
        filtered_df = df[df['Launch Site'] == site]
        fig = px.pie(
            filtered_df,
            names='class',
            title=f'Success vs Failure for {site}'
        )

    return fig
###Slider

@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
    )

def update_scatter(selected_site, payload_range):
    
    low, high = payload_range

    # Filter by payload
    df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    ]

    # Filter by site if not ALL
    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version',
        title='Payload vs Launch Outcome'
    )

    return fig


# Run the app
if __name__ == '__main__':
    app.run()
