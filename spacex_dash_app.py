# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Custom: get launch site names
launch_site_names = pd.unique(spacex_df['Launch Site'])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': launch_site_names[0], 'value': launch_site_names[0]},
                                        {'label': launch_site_names[1], 'value': launch_site_names[1]},
                                        {'label': launch_site_names[2], 'value': launch_site_names[2]},
                                        {'label': launch_site_names[3], 'value': launch_site_names[3]},
                                    ],
                                    value = 'ALL',
                                    placeholder = "Select a Launch Site Here",
                                    searchable = True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0, 
                                    max=10000, step=1000, 
                                    marks={0: '0', 100: '100'},
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-pie-chart', component_property='figure'),
               Input(component_id='site-dropdown', component_property='value'))

# Add computation to callback function and return graph
def get_pie_chart(selected_site):
    # Select 2019 data
    # df =  airline_data[airline_data['Year']==int(selected_site)]
    filtered_df = spacex_df
    if selected_site == 'ALL':
        print("TEST!")
        fig = px.pie(filtered_df, 
            values='class', 
            names='Launch Site', # fix
            title='Success by Launch Site')
        return fig
    else:
        filtered_df_b = spacex_df[spacex_df["Launch Site"] == selected_site]
        print(filtered_df_b['class'])
        fig = px.pie(filtered_df_b, 
            names='class', # fix
            title=selected_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# add callback decorator
@app.callback( Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])

# Add computation to callback function and return graph
def get_scatter(selected_site, selected_payload_range):
    # Select 2019 data
    # df =  airline_data[airline_data['Year']==int(selected_site)]
    filtered_df = spacex_df
    low_limit, high_limit = selected_payload_range
    if selected_site == 'ALL':
        print("TEST SCATTER!")
        print("Low: ", low_limit)
        print("High: ", high_limit)
        mask = (filtered_df['Payload Mass (kg)'] > low_limit) & (filtered_df['Payload Mass (kg)'] < high_limit)
        fig = px.scatter(filtered_df[mask], 
            x='Payload Mass (kg)', 
            y='class', # fix
            color="Booster Version Category")
        return fig
    else:
        filtered_df_b = spacex_df[spacex_df["Launch Site"] == selected_site]
        print(filtered_df_b['class'])
        mask = (filtered_df_b['Payload Mass (kg)'] > low_limit) & (filtered_df_b['Payload Mass (kg)'] < high_limit)
        fig = px.scatter(filtered_df_b[mask], 
            x='Payload Mass (kg)', 
            y='class', # fix
            color="Booster Version Category")
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
