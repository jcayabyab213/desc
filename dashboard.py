import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__, meta_tags=[{'name':'viewport', 'content':'width=device-width'}])
app.title = 'Crime Dashboard'

df = pd.read_csv('laC.csv')

app.layout = html.Div([
        
    html.Div([
        html.H1('Los Angeles Crimes Dashboard'),
        html.Hr(),
        html.H3('Area Name:'),
        dcc.Dropdown(
            id="dropdown_area",
            options=[{"label": x, "value": x} for x in df.loc[:,'AREA_NAME'].unique()],
            value='',
            multi = True
        ),
        html.H3('Victim Descent:'),
        dcc.Dropdown(
            id="dropdown_descent",
            options=[{"label": x, "value": x} for x in df.loc[:,'Vict_Descent'].unique()],
            value='',
            multi = True
        ),
        html.H3('Crime Category:'),
        dcc.Dropdown(
            id="dropdown_crime",
            options=[{"label": x, "value": x} for x in df.loc[:,'crm_cat'].unique()],
            value='',
            multi = True
        ),
        html.H3('Year:'),
        dcc.RangeSlider(
            id='year-slider',
            min=2015,
            max=2019,
            value=[df['year'].min(), df['year'].max()],
            marks={str(Year): str(Year) for Year in [x for x in range(2015, 2020, 1)]},
            step= None,
        ), 
        
    ], className = 'controls'),


    html.Div([
        
        html.Div([
            dcc.Graph(
                     id='rbarchart',
                     className='chart_container'
                ), 
            html.Div([
                 html.Div([
                      html.H1('Area Names'),
                      html.Hr(),
                      html.H4('Shows what areas have the most and least crime occurences')
                 ], style={'margin-top':'63%',
                           'margin-left':'0',
                           'width':'100%'
                           }),
                
             ], className='c1_container'),
        ]),
        
        

        html.Div([
            html.Div([
                html.Img(src='https://ouch-cdn2.icons8.com/iWqGYKzvsDQAgJA7nCcJvJA0USjBlqrA1X7n2z4tDyQ/rs:fit:946:912/czM6Ly9pY29uczgu/b3VjaC1wcm9kLmFz/c2V0cy9zdmcvOTQz/LzM3MzhlNTRlLWNl/NzktNDkzNy04YjY2/LTIyZTZkZjNkNjZl/Mi5zdmc.png',
                         width=200, height=150),
            ], className='total_occ_container'),
            
            html.Div([
                html.H3('Total Crimes:'),
                html.H1(id='total_occurence'),
            ], className='textt_container'),
            
            html.Div([
                html.Img(src='https://ouch-cdn2.icons8.com/jdkzTz8EW2cJslmwMERb6gDxpusHfFo5VdVTVp0O9HA/rs:fit:912:912/czM6Ly9pY29uczgu/b3VjaC1wcm9kLmFz/c2V0cy9zdmcvNzgw/LzU1OWU5N2FlLTVh/MDYtNDIyNS1iNGZl/LWQzZWJmODc4NDM3/MC5zdmc.png',
                         width=200, height =150)
            ], className='total_occ_container'),
            
             html.Div([
                html.H3('Male Percentage:'),
                html.H1(id='male'),
            ], className='text_container'),
            
            html.Div([
                html.Img(src='https://ouch-cdn2.icons8.com/FsTsfXUG2v-vxNCG-Zs6X_j8gNlLHL9MSyIPKwxfhHs/rs:fit:526:912/czM6Ly9pY29uczgu/b3VjaC1wcm9kLmFz/c2V0cy9zdmcvNDY1/L2I5ZTQ0M2MxLWY2/ODUtNGRkNC1iMGQy/LThhYTUxYzc4ZGNj/Ni5zdmc.png',
                         width=200, height =150)
            ], className='total_occ_container'),
            
             html.Div([
                html.H3('Female Percentage'),
                html.H1(id='female'),
            ], className='text_container'),

         ], className='c4_container'),
                
        
        html.Div([
            dcc.Graph(
                     id='barchart',
                     className='chart_container'
                ), 
            html.Div([
                html.Div([
                      html.H1('Victim Descent'),
                      html.Hr(),
                      html.H4('Shows how many victim are the victims in terms of their race.')
                 ], style={'margin-top':'63%',
                           'margin-left':'0',
                           'width':'100%'
                           }),
             ], className='c3_container'),
        ]),
        
        html.Div([
            dcc.Graph(
                     id='donut',
                     className='chart_container'
                 ),
             html.Div([
                 html.Div([
                      html.H1('Crime Category'),
                      html.Hr(),
                      html.H4('Shows what crime categories are the most and least occured.')
                 ], style={'margin-top':'86%',
                           'margin-left':'0',
                           'width':'100%'
                           }),
             ], className='c2_container'),
        ]),
        
        html.Div([
            dcc.Graph(
                     id='map',
                     className='chart_container'
                 ),
             html.Div([
                 html.Div([
                      html.H1('Map'),
                      html.Hr(),
                      html.H4('Shows where in the L.A. that the crimes occured.')
                 ], style={'margin-top':'32%',
                           'margin-left':'0',
                           'width':'100%'
                           }),
             ], className='c5_container'),
        ]),

        

    ],className = 'main_content'), 
                           
    

], className='whole')

@app.callback(
    [Output("total_occurence", "children"),
     Output("male", "children"),
     Output("female", "children")
     ], 
    [Input('year-slider', 'value'),
     Input('dropdown_area', 'value'),
     Input('dropdown_descent', 'value'),
     Input('dropdown_crime', 'value'),
      ])
def count_total_occurence(year, area, desc, crime):
    
    if len(area) == 0:
        area = df['AREA_NAME'].unique()     
    if len(desc) == 0:
       desc = df['Vict_Descent'].unique()
    if len(crime) == 0:
        crime = df['crm_cat'].unique()
        
            
    xdf = df[df['Vict_Descent'].isin(desc)].copy()
    cdf = xdf[xdf['crm_cat'].isin(crime)]
    zdf = cdf[cdf['AREA_NAME'].isin(area)]
    
    ndf = zdf[(xdf['year'] >= int(year[0])) & (xdf['year'] <= int(year[1]))]
    
    total = ndf['total_crm'].sum()
    
    male = ndf[ndf['Vict_Sex'] == 'M'].shape[0]/ df.shape[0]
    female = ndf[ndf['Vict_Sex'] == 'F'].shape[0]/ df.shape[0]
    
    m = '{:.2f}'.format(male*100)
    f = '{:.2f}'.format(female*100)
    
    return total, m, f


@app.callback(
    Output("rbarchart", "figure"), 
    [Input('year-slider', 'value'),
     Input('dropdown_area', 'value'),
     Input('dropdown_descent', 'value'),
     Input('dropdown_crime', 'value'),
     ])
def update_rbar_chart(year, area, desc, crime):
    
    if len(area) == 0:
        area = df['AREA_NAME'].unique()     
    if len(desc) == 0:
       desc = df['Vict_Descent'].unique()
    if len(crime) == 0:
        crime = df['crm_cat'].unique()
        
            
    xdf = df[df['Vict_Descent'].isin(desc)].copy()
    cdf = xdf[xdf['crm_cat'].isin(crime)]
    zdf = cdf[cdf['AREA_NAME'].isin(area)]
    
    ndf = zdf[(xdf['year'] >= int(year[0])) & (xdf['year'] <= int(year[1]))]
    
     
    fig = px.histogram(ndf, y='AREA_NAME', x='total_crm', color='AREA_NAME', width=750, height=550).update_layout({
                                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                                })
    fig.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig.update_layout(transition_duration=500)

    return fig

@app.callback(
    Output("barchart", "figure"), 
    [Input('year-slider', 'value'),
     Input('dropdown_area', 'value'),
     Input('dropdown_descent', 'value'),
     Input('dropdown_crime', 'value'),
     ])
def update_bar_chart(year, area, desc, crime):
    
    if len(area) == 0:
        area = df['AREA_NAME'].unique()     
    if len(desc) == 0:
       desc = df['Vict_Descent'].unique()
    if len(crime) == 0:
        crime = df['crm_cat'].unique()
        
            
    xdf = df[df['Vict_Descent'].isin(desc)].copy()
    cdf = xdf[xdf['crm_cat'].isin(crime)]
    zdf = cdf[cdf['AREA_NAME'].isin(area)]
    
    ndf = zdf[(xdf['year'] >= int(year[0])) & (xdf['year'] <= int(year[1]))]
    
    fig2 = px.histogram(ndf, x='Vict_Descent', y='total_crm', color='Vict_Descent', width=750, height=550).update_layout({
                                                'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                                })
    
    fig2.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig2.update_layout(transition_duration=500)

    return fig2




@app.callback(
    Output("donut", "figure"), 
    [Input('year-slider', 'value'),
     Input('dropdown_area', 'value'),
     Input('dropdown_descent', 'value'),
     Input('dropdown_crime', 'value'),
     ])
def update_donut_chart(year, area, desc, crime):
    
    if len(area) == 0:
        area = df['AREA_NAME'].unique()     
    if len(desc) == 0:
       desc = df['Vict_Descent'].unique()
    if len(crime) == 0:
        crime = df['crm_cat'].unique()
        
            
    xdf = df[df['Vict_Descent'].isin(desc)].copy()
    cdf = xdf[xdf['crm_cat'].isin(crime)]
    zdf = cdf[cdf['AREA_NAME'].isin(area)]
    
    ndf = zdf[(xdf['year'] >= int(year[0])) & (xdf['year'] <= int(year[1]))]
    
    columns = ndf.groupby('crm_cat').sum()['total_crm'].index
    values = ndf.groupby('crm_cat').sum()['total_crm'].values
    
    fig3 = px.pie(df, 
                  columns,
                  values, 
                  hole=0.5,
                  width=550,
                  height = 550).update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })
                      
    fig3.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig3.update_layout(transition_duration=500)

    return fig3

@app.callback(
    Output("map", "figure"), 
    [Input('year-slider', 'value'),
     Input('dropdown_area', 'value'),
     Input('dropdown_descent', 'value'),
     Input('dropdown_crime', 'value'),
     ])
def update_map_chart(year, area, desc, crime):
    
    if len(area) == 0:
        area = df['AREA_NAME'].unique()     
    if len(desc) == 0:
       desc = df['Vict_Descent'].unique()
    if len(crime) == 0:
        crime = df['crm_cat'].unique()
        
            
    xdf = df[df['Vict_Descent'].isin(desc)].copy()
    cdf = xdf[xdf['crm_cat'].isin(crime)]
    zdf = cdf[cdf['AREA_NAME'].isin(area)]
    
    ndf = zdf[(xdf['year'] >= int(year[0])) & (xdf['year'] <= int(year[1]))]
    
    fig4 = px.scatter_mapbox(ndf, hover_name='AREA_NAME', lat="LAT", lon="LON", 
                             color='total_crm',
                             size = 'total_crm', 
                             mapbox_style="open-street-map", 
                             height=500,
                             width = 1368,
                             color_continuous_scale=px.colors.sequential.Rainbow, size_max=30, zoom=15).update_layout({
                                                                                            'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                                            'paper_bgcolor': 'rgba(0, 0, 0, 0)',
                                                                                            })
                                 
    fig4.update_layout(
       margin={
           't':0,
           'l':0,
           'r': 0,
           'b': 0} 
    )
                      
    fig4.update_layout(transition_duration=500)

    return fig4



if __name__ == '__main__':
    app.run_server(debug=True)