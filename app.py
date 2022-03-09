import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['id', 'name', 'date', 'manner_of_death', 'armed', 'age', 'gender',
       'race', 'city', 'state', 'signs_of_mental_illness', 'threat_level',
       'flee', 'body_camera', 'arms_category']

mycolumn='race'
myheading1 = f"Incident reported for {mycolumn}!"
mygraphtitle = '2015 to 2020 Police shooting database'
mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
mycolorbartitle = "No of incidents"
tabtitle = 'Police shooting'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/Malathy-Muthu/301-old-mcdonald'



########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/shootings.csv')

fig = go.Figure(data=go.Choropleth(
    locations=df['state'], # Spatial coordinates
    z = df[mycolumn].astype(float), # Data to be color-coded
    locationmode = 'USA-states', # set of locations match entries in `locations`
    colorscale = mycolorscale,
    colorbar_title = mycolorbartitle,
))

fig.update_layout(
    title_text = mygraphtitle,
    geo_scope='usa',
    width=1200,
    height=800
)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1),
    dcc.Graph(
        id='figure-1',
        figure=fig
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

############ Deploy
if __name__ == '__main__':
    app.run_server()