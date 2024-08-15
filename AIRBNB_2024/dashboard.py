#Terminal commands

#pip3.11 install setuptools
#python3.11 -m pip install packaging
#python3.11 -m pip install pandas dash
#pip3 install httpx==0.20 dash plotly

#python3.11 dashboard.py



import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import datetime as dt

#Create app
app = dash.Dash(__name__)

#Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

# Read airbnb cleaned data
df =  pd.read_csv('dashboard_file.csv')


#Layout Section of Dash
#Task 1 Add the Title to the Dashboard
app.layout = html.Div(children=[html.H1('New York Airbnb Accommodations by Neighbourhood Group', 
                                style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 26}),
# TASK 2: Add the radio items and a dropdown right below the first inner division
     #outer division starts
     html.Div([

                    #Dropdown to select neighbourhood
                    html.Div([
                            html.H2('Select Neighbourhood Group:', style={'margin-right': '2em'}),
                        dcc.Dropdown(df['neighbourhood group'].unique(), value = 'Brooklyn',id='place')
                    ]),
#TASK 3: Add two empty divisions for output inside the next inner division. 
         #Second Inner division for adding 2 inner divisions for 2 output graphs
                    html.Div([
                
                        html.Div([ ], id='plot1'),
                        html.Div([ ], id='plot2')
                    ], style={'display': 'flex'}),

    ])
    #outer division ends
])

#layout ends
#TASK 4: Add the Ouput and input components inside the app.callback decorator.
#Place to add @app.callback Decorator
@app.callback([Output(component_id='plot1', component_property='children'),
               Output(component_id='plot2', component_property='children')],
               Input(component_id='place', component_property='value'))
                
#TASK 5: Add the callback function.   
#Place to define the callback function .
def reg_neighbourhood_display(input_neighbourhood):  

    y_r_data = df[df['neighbourhood group']==input_neighbourhood]
    #Plot one 
    est_data = y_r_data.groupby('room type')['host name'].count().reset_index(name = 'count')
    fig1 = px.pie(est_data, values='count', names='room type', title="{} : Accommodation Types".format(input_neighbourhood))   
    
    #Plot two 
    fig2 = px.box(y_r_data, x='room type', y='price', title='Distribution of Price per Accommodation in {}'.format(input_neighbourhood))
    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]
            
if __name__ == '__main__':
    app.run_server()
    