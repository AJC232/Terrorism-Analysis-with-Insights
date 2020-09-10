# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 19:14:15 2020

@author: hp 3006tx
"""
import pandas as pd
import dash
from dash.dependencies import Input , State, Output
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
import plotly.graph_objects as go
import plotly.express as px

# region country state city day month attacktype 
app = dash.Dash()
app.title = 'Terrorism Data Analysis'


def load_data():
   
# world data    
    globalterror = 'global_terror.csv'
    
    global df    
    df = pd.read_csv(globalterror)
    
    temp_list=sorted(df['country_txt'].unique().tolist())
    
    global country_list
    #country_list=[{"label":str(i),"value":str(i)} for i in temp_list]
    country_list = df.groupby("region_txt")["country_txt"].unique().apply(list).to_dict()

    global year_list
    year_list=sorted(df['iyear'].unique().tolist())     
    global year_dict
    year_dict = {str(i) : str(i) for i in year_list}
    
    month = {
               'January':1,
               'February':2,
               'March':3,
               'April':4,
               'May':5,
               'June':6,
               'July':7,
               'August':8,
               'September':9,
               'Octomber':10,
               'November':11,
               'December':12
            }   
    global month_list
    month_list = [{'label':key,'value':values} for key,values in month.items()]
    
    global date_list
    date_list = [i for i in  range(1,32) ]
    global region_list
    region_list=[{'label': str(i),'value':str(i)} for i in df['region_txt'].unique().tolist()]
    
    global state_list
    state_list=df.groupby("country_txt")["provstate"].unique().apply(list).to_dict()
    global city_list
    city_list=df.groupby("provstate")["city"].unique().apply(list).to_dict()
    
    global attacktype_list
    attacktype_list=[{'label': str(i), 'value':str(i)} for i in sorted(df['attacktype1_txt'].unique().tolist())]    


    
#Chart dropdown list
    global chart_dd_values
    chart_dd_values= {"Terrorist Organisation":'gname', 
                      "Target Nationality":'natlty1_txt', 
                      "Target Type":'targtype1_txt', 
                      "Type of Attack":'attacktype1_txt', 
                      "Weapon Type":'weaptype1_txt', 
                      "Region":'region_txt', 
                      "Country Attacked":'country_txt'
                     }
                             
    chart_dd_values = [{"label":keys, "value":value} for keys, value in chart_dd_values.items()]
 


def open_browser():
    webbrowser.open_new('http://127.0.0.1:8050/')
    

def create_app_ui():
     
    
    main_layout = html.Div(
    [  
       html.Div([
       html.Hr(),
       html.Hr(),
       html.Hr(),
       html.H1(id='Main_title', children='Terrorism Analysis with Insights'),
       html.Hr(),
       html.Hr(),
       html.Hr(),
       ],style={'background-image':'url(/assets/img1.jpg)'    
                 }
           ),
       dcc.Tabs(id='maintab',value='maptool',children=[
                  dcc.Tab(label='MAP-TOOL',id= 'MAP-TOOL',value='maptool',children=[
                      dcc.Tabs(id='subtab1',value='world',children=[
                     dcc.Tab(label='WORLD-MAP',id='WORLD-MAP',value='world'),
                     dcc.Tab(label='INDIA-MAP',id='INDIA-MAP',value='india')
                     ]),               
       html.Div([
       
       html.Br(),
       html.Br(),
       html.Br(), 
        

       dcc.Dropdown(
                     id='month_dropdown', 
                     options = month_list, 
                     placeholder='Select Month',
                     multi=True
                   ),             

        dcc.Dropdown(
                     id='date_dropdown', 
                     options = [{'label':'Select Month','value':'Select Month'}], 
                     placeholder='Select Date',
                     multi=True,
                   ),  

        dcc.Dropdown(
                     id='region_dropdown', 
                     options = region_list, 
                     placeholder='Select Region',
                     multi=True
                   ),
  
       dcc.Dropdown(
                     id='country_dropdown', 
                     options = [{'label': 'Select Region','value':'Select Region'}], #country_list, 
                     placeholder='Select Country',
                     multi=True           
                   ), 

       dcc.Dropdown(
                     id='state_dropdown', 
                     options = [{'label': 'Select Country','value':'Select Country'}], 
                     placeholder='Select State',
                     multi=True           
                   ),

       dcc.Dropdown(
                     id='city_dropdown', 
                     options = [{'label': 'Select State','value':'Select State'}], 
                     placeholder='Select City',
                     multi=True          
                   ),

        dcc.Dropdown(
                     id='attacktype_dropdown', 
                     options = attacktype_list, 
                     placeholder='Select Attack Type',
                     multi=True           
                    ),    
 
       html.H5(id='year_title', children='Select Year'),
       
       dcc.RangeSlider(
                   id='year_slider',
                   min=min(year_list),
                   max=max(year_list),
                   value=[min(year_list),max(year_list)],
                   marks=year_dict,
                   step=None
            ),
       html.Br(),
       ],style={'background-image':'url(/assets/img2.jpg)'    
                 }
)
                 ]), 
            dcc.Tab(label = "CHART-TOOL", id="CHART-TOOL", value="Chart", children=[
            dcc.Tabs(id = "subtab2", value = "WorldChart",children = [
            dcc.Tab(label="World Chart tool", id="WorldC", value="WORLD-CHART"),          
            dcc.Tab(label="India Chart tool", id="IndiaC", value="INDIA-CHART")]),
            html.Div([
            html.Br(),
            dcc.Dropdown(id="Chart_Dropdown",
                         options = chart_dd_values, 
                         placeholder="Select option", 
                         value = "region_txt"), 
            
            html.Br(),
            html.Br(),
            html.Hr(),
            dcc.Input(id="search", placeholder="Search Filter"),
            html.Hr(),
            html.Br(),
            ],style={'background-image':'url(/assets/img2.jpg)'}),
            html.Br(),
            dcc.RangeSlider(
                    id='cyear_slider',
                    min=min(year_list),
                    max=max(year_list),
                    value=[min(year_list),max(year_list)],
                    marks=year_dict,
                    step=None
                      ),
                  html.Br()
                  
              ]),
                  
                  
           ]),
         html.Div(id='graph_object',children='Loading..., Please wait' ''',style={'background-image':'url(/assets/img2.jpg)'}''')
    
                                                                          
        ])
    return main_layout


@app.callback(
    
           dash.dependencies.Output('graph_object','children'), 
           [
                dash.dependencies.Input('maintab','value'),
                dash.dependencies.Input('region_dropdown','value'),
                dash.dependencies.Input('country_dropdown','value'),
                dash.dependencies.Input('state_dropdown','value'),
                dash.dependencies.Input('city_dropdown','value'),
                dash.dependencies.Input('month_dropdown','value'),
                dash.dependencies.Input('date_dropdown','value'),
                dash.dependencies.Input('attacktype_dropdown','value'),
                dash.dependencies.Input('year_slider','value'),
                dash.dependencies.Input('cyear_slider', 'value'), 
    
                
                dash.dependencies.Input("Chart_Dropdown", "value"),
                dash.dependencies.Input("search", "value"),
                dash.dependencies.Input("subtab2", "value")
           ]
    )
def update_app_ui(tab,region_value,country_value,state_value,city_value,month_value,day_value,attacktype_value,year_value,cyear_value,chart_dd_value,search_value,subtab2_value):
  
  figure=None
     
  if tab == 'maptool':
     print('data type of country: '+str(type(country_value)))  
     print('data value of country: '+str((country_value)))
     print('data type of year: '+str(type(year_value)))
     print('data value of year: '+str((year_value)))
     
     #year
     year_range=range(year_value[0],year_value[1]+1)
     new_df=df[df['iyear'].isin(year_range)]

     #month
     if month_value==[] or month_value is None:
        pass
     else:
        if day_value==[] or day_value is None:
           new_df=new_df[new_df['imonth'].isin(month_value)] 
        else:    
           new_df=new_df[ new_df['imonth'].isin(month_value) &
                          new_df['iday'].isin(day_value) ]
     #region...
     if region_value==[] or region_value is None: 
        pass
     else:
         if country_value==[] or country_value is None:
            new_df=new_df[new_df['region_txt'].isin(region_value)]
         else:   
            if state_value==[] or state_value is None:              
              new_df=new_df[new_df['region_txt'].isin(region_value) &
                          new_df['country_txt'].isin(country_value) ]
            else:
              if city_value==[] or city_value is None:
                 new_df=new_df[new_df['region_txt'].isin(region_value) &
                               new_df['country_txt'].isin(country_value) &
                               new_df['provstate'].isin(state_value) ]
              else: 
                  new_df=new_df[new_df['region_txt'].isin(region_value) &
                               new_df['country_txt'].isin(country_value) &
                               new_df['provstate'].isin(state_value) &
                               new_df['city'].isin(city_value)]
     
     if attacktype_value == [] or attacktype_value is None:
            pass
     else:
         new_df = new_df[new_df["attacktype1_txt"].isin(attacktype_value)]             
  
     
  
     figure = go.Figure()
     
     if new_df.shape[0]:
        pass
     else: 
        new_df = pd.DataFrame(columns = ['iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'provstate',
               'city', 'latitude', 'longitude', 'attacktype1_txt', 'nkill'])
            
        new_df.loc[0] = [0, 0 ,0, None, None, None, None, None, None, None, None]
            
        
     mapFigure = px.scatter_mapbox(new_df,
                                      lat="latitude", 
                                      lon="longitude",
                                      color="attacktype1_txt",
                                      hover_name="city",
                                      hover_data=["region_txt", "country_txt", "provstate","city", "attacktype1_txt","nkill","iyear","imonth", "iday"],
                                      zoom=1,
                                      template='plotly_dark'
                                   )                       
     mapFigure.update_layout(mapbox_style="carto-darkmatter",
                                autosize=True,
                                height=680,
                                margin=dict(l=0, r=0, t=25, b=20),
                                legend=dict(orientation="h",
                                            yanchor="top",
                                            y=1,
                                            xanchor="center",
                                            x=1)
                          )
     
     figure=mapFigure
     
  elif tab=="Chart":
        figure = None
        
        
        year_range_c = range(cyear_value[0], cyear_value[1]+1)
        chart_df = df[df["iyear"].isin(year_range_c)]
        
        
        if subtab2_value == "WorldChart":
            pass
        elif subtab2_value == "IndiaChart":
            chart_df = chart_df[(chart_df["region_txt"]=="South Asia") &(chart_df["country_txt"]=="India")]
        if chart_dd_value is not None and chart_df.shape[0]:
            if search_value is not None:
                chart_df = chart_df.groupby("iyear")[chart_dd_value].value_counts().reset_index(name = "count")
                chart_df  = chart_df[chart_df[chart_dd_value].str.contains(search_value, case=False)]
            else:
                chart_df = chart_df.groupby("iyear")[chart_dd_value].value_counts().reset_index(name="count")
        
        
        if chart_df.shape[0]:
            pass
        else: 
            chart_df = pd.DataFrame(columns = ['iyear', 'count', chart_dd_value])
            
            chart_df.loc[0] = [0, 0,"No data"]
        chartFigure = px.area(chart_df, x="iyear", y ="count", color = chart_dd_value,template='plotly_dark')
        figure = chartFigure   
     
  return dcc.Graph(figure=figure)




@app.callback([Output("region_dropdown", "value"),
               Output("region_dropdown", "disabled"),
               Output("country_dropdown", "value"),
               Output("country_dropdown", "disabled")],
              [Input("subtab1", "value")])
def update_r(tab):
    region = None
    disabled_r = False
    country = None
    disabled_c = False
    if tab == "world":
        pass
    elif tab=="india":
        region = ["South Asia"]
        disabled_r = True
        country = ["India"]
        disabled_c = True
    return region, disabled_r, country, disabled_c

@app.callback(
                Output('date_dropdown','options'),
                [
                   Input('month_dropdown','value')  ]
    )
def update_date(month):
    
    option = [{'label': 'Select Month','value':'Select Month'}]
    if month:
        option= [{"label":m, "value":m} for m in date_list]
    return option


@app.callback(
    
            dash.dependencies.Output('country_dropdown','options'),
            [
               dash.dependencies.Input('region_dropdown','value') ]
    )
def update_country(region):
        
     option=[]
     
     if region is None:
         option= [{'label': 'Select Region','value':'Select Region'}]
         return option
     else:
         for i in region:
             if i in country_list.keys():
                 option.extend(country_list[i])
                  
     return [{'label':a,'value':a} for a in option]  

@app.callback(
    
           dash.dependencies.Output('state_dropdown','options'),
           [
               dash.dependencies.Input('country_dropdown','value') ]
    )
def update_state(country):
    
     option=[]
     
     if country is None:
         option=[{'label': 'Select Country','value':'Select Country'}]
         return option
     else:
         for i in country:
             if i in state_list.keys():
                 option.extend(state_list[i])
                  
                 
     return [{'label':a,'value':a} for a in option]

@app.callback(
    
           dash.dependencies.Output('city_dropdown','options'),
           [
               dash.dependencies.Input('state_dropdown','value') ]
    )
def update_city(state):
    
     option=[]
     
     if state is None:
         option=[{'label': 'Select State','value':'Select State'}]
         return option
     else:
         for i in state:
             if i in city_list.keys():
                 option.extend(city_list[i])
                  
                 
     return [{'label':a,'value':a} for a in option]
 

    
        
def main():
    print("Welcome to terrosism data analysis")

    load_data()
    open_browser()

    global app
    app.layout = create_app_ui()
    
    
    
    app.run_server()
    



    print("thanks for using my project")

    app = None
    df = None



if __name__ == '__main__':  
   main()