import dash
import dash_core_components as dcc
from dash import html
# import dash_html_components as html # deprecated
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import pandas as pd

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['code', 'state', 'category', 'total exports', 'beef', 'pork', 'poultry',
       'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
       'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']

# get columns starting with total exports (item #4)
list_of_export_products = list_of_columns[3:]

# initiate chart with total exports
product = list_of_export_products[0]

myheading1 = "2011 US Agriculture Export Analytics"
mygraphtitle = "Exports by State"
topstatesmax = 5
mycolorscale = 'darkmint' # Note: The error message will list possible color scales.
mycolorbartitle = "Millions USD"
tabtitle = 'US Exports'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/Dangee/old-mcdonald'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2011-agriculture.csv')


# fig = go.Figure(data=go.Choropleth(
#     locations=df['code'], # Spatial coordinates
#     z = df[product].astype(float), # Data to be color-coded
#     locationmode = 'USA-states', # set of locations match entries in `locations`
#     colorscale = mycolorscale,
#     colorbar_title = mycolorbartitle,
# ))
#
# fig.update_layout(
#     title_text = mygraphtitle,
#     geo_scope='usa',
#     width=1024,
#     height=680
# )

########### Initiate the app
external_stylesheets = ['assets/my_bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1(myheading1, className="header"),
    html.Div(children=[
        html.Div(
            children=[html.H3(mygraphtitle),
            html.P("Select an export product: "),
            dcc.Dropdown(
                id="product-filter",
                options=[
                    {"label": product, "value": product}
                    for product in list_of_export_products
                ],
                value = list_of_export_products[0],
                clearable = False,
                className = "dropdown"
                ),
                html.Table(id='id-top-producers'),
                dcc.Graph(id='export-chart')
            ],
        className="chart"),
    ],
    className="card"
    ),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ],
    className = "wrapper"
)

########## Define Callback
@app.callback([Output('export-chart', 'figure'),
               Output('id-top-producers', 'children')],
              Input('product-filter', 'value'))

def update_chart(product):
    # ============= update map =============
    chart_data = df[['code','state', 'category', product]]
    export_chart_figure = go.Figure(data=go.Choropleth(
            locations=chart_data['code'], # Spatial coordinates
            z = chart_data[product].astype(float), # Data to be color-coded
            locationmode = 'USA-states', # set of locations match entries in `locations`
            colorscale = mycolorscale,
            colorbar_title = mycolorbartitle,
        ))

    export_chart_figure.update_layout(
        # title_text=mygraphtitle,
        geo_scope='usa',
        width=1024,
        height=680
    )

    # ============= update top producer table =========
    df_top = df[['state', product]].sort_values(product, ascending=False)

    top_producer_table = [
             html.H3(f"top {topstatesmax} producing states ({mycolorbartitle})"),
             html.Table(children=[
                 html.Tbody(
                     html.Tr([html.Th(col)
                              for col in df_top['state'].head(topstatesmax)
                              ])
                 ),
                 html.Tbody([
                     html.Tr([
                         html.Th(col)
                         for col in df_top[product].head(topstatesmax)
                     ])
                 ])
            ])
        ]

    return export_chart_figure, top_producer_table


############ Deploy
if __name__ == '__main__':
    app.run_server()
