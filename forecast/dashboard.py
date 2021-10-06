# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from django_plotly_dash import DjangoDash
from dash import dcc
from dash import html 
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output,State
from .DP import DataProcessor 
from .Result import Results
from .Ped import Peds
import dash_bootstrap_components as dbc
import json
import numpy as np
from .s3 import SthreeController as SC
from django.conf import settings

#Dash


# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app = DjangoDash('horecast', add_bootstrap_links=True)


#Data
# with open('forecast/static/data/race_results_all.pickle',"rb") as r:
#     race_results = pickle.load(r)
# with open('forecast/static/data/peds_all.pickle',"rb") as p:
#     peds = pickle.load(p)
sc = SC(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY,settings.AWS_S3_REGION_NAME,settings.AWS_STORAGE_BUCKET_NAME)
race_results = sc.read_result()
peds = sc.read_peds()

r = Results(race_results)
p = Peds(peds)


# df = r.data.query('(race_park=="中京" & race_type=="ダート") & course_len==1800' ,engine='python')
df = r.data

df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
df.dropna(subset=["着順"], inplace=True)
df["着順"] = df["着順"].astype(int)
merge_peds = df.merge(p.peds,how="left",left_on="horse_id",right_on="horse_id")
merge_peds["種牡馬"] = merge_peds["peds_0"].str.split(expand=True)[0]

available_race_park= merge_peds["race_park"].unique()
available_race_type= merge_peds["race_type"].unique()
available_course_len= merge_peds["course_len"].unique()
available_jockey = merge_peds['騎手'].unique()
available_trainer = merge_peds['調教師'].unique()
available_stallion= merge_peds["種牡馬"].unique()
available_course_len = np.sort(available_course_len)


#グラフのレイアウト調整
RadioItems = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("競馬場を選択してください"),
                dcc.RadioItems(
                    id="select_race_park",
                    options=[{'label': i, 'value': i} for i in available_race_park],
                    value="札幌",
                    labelStyle={'display': 'inline-block'}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("レース種別を選択してください"),
                dcc.RadioItems(
                    id="select_race_type",
                    options=[{'label': i, 'value': i} for i in available_race_type],
                    value="芝",
                    labelStyle={'display': 'inline-block'}
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("距離を選択してください"),
                dcc.RadioItems(
                    id="select_course_len",
                    options=[{'label': i, 'value': i} for i in available_course_len],
                    value=2000,
                    labelStyle={'display': 'inline-block'}
                ),
            ]
        ),
        dbc.Button(
            "検索", id="search-button", className="mr-2", n_clicks=0
        ),
        dcc.Store(id='intermediate-value')
    ],
    body=True,
)




app.layout = dbc.Container(
    [   
       dbc.Row(
            [
                html.Div(
                    dbc.Col(RadioItems),
                )
            ],
            align="center",
            className="h-30"
        ),       
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                html.Div(
                    children=[
                        html.H1(id="data-title")
                    ],
                    style={"background-color": "white"}
                )
            ],
            className="h-30"
        ),
 

        dbc.Row(
            [
                dbc.Col(
                    [
                    dcc.Graph(
                        id='rank-frame',
                        figure={},
                    ),
                    ]
                    # スタイルシートを適用
                    # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
                    #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
                    #             }
                ),
            ],
            className="h-30"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                    dcc.Dropdown(
                        id='selected_jockey',
                        options=[{'label': i, 'value': i} for i in available_jockey],
                        value='',
                        multi=True
                    ),
                    dcc.Graph(
                        id='rank-jockey',
                        figure={},
                    ),
                    ]
                    # スタイルシートを適用
                    # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
                    #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
                    #             }
                ),
            ],
            className="h-30"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [    
                    dcc.Dropdown(
                        id='selected_trainer',
                        options=[{'label': i, 'value': i} for i in available_trainer],
                        value='',
                        multi=True
                    ),
                    dcc.Graph(
                        id='rank-trainer',
                        figure={},
                    ),
                    ]
                ),
            ],
            className="h-30"
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                    dcc.Dropdown(
                        id='selected_stallion',
                        options=[{'label': i, 'value': i} for i in available_stallion],
                        value='',
                        multi=True
                    ),
                    dcc.Graph(
                        id='rank-stallion',
                        figure={},
                    ),
                    ]
                    # スタイルシートを適用
                    # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
                    #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
                    #             }
                ),
            ],
            className="h-30"
        ),
    ]
)


@app.callback(
    Output('data-title', 'children'),
    [Input('search-button','n_clicks')],
    [State('select_race_park', 'value'),
    State('select_race_type', 'value'),
    State('select_course_len', 'value')]
)
def express_title(n_clicks,race_park,race_type,course_len):
    return f"{race_park}{race_type}{course_len}mデータ"



@app.callback(
    Output('intermediate-value', 'data'),
    [Input('search-button','n_clicks')],
    [State('select_race_park', 'value'),
    State('select_race_type', 'value'),
    State('select_course_len', 'value')]
)
def update_figure(n_clicks,race_park,race_type,course_len):

#Data
    race_results = sc.read_result()
    peds = sc.read_peds()

    r = Results(race_results)
    p = Peds(peds)





    # r = Results.read_pickle(['race_results_all.pickle'])
    # p = Peds.read_pickle(['peds_all.pickle'])
    # course_len = int(course_len)


    # df = r.data.query('(race_park=="中京" & race_type=="ダート") & course_len==1800' ,engine='python')
    df = r.data
    df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
    df.dropna(subset=["着順"], inplace=True)
    df["着順"] = df["着順"].astype(int)
    merge_peds = df.merge(p.peds,how="left",left_on="horse_id",right_on="horse_id")
    merge_peds["種牡馬"] = merge_peds["peds_0"].str.split(expand=True)[0]
    


    # df = merge_peds[(merge_peds["race_park"]==race_park & merge_peds["race_type"]==race_type) & merge_peds["course_len"]==course_len]
    df_race_park = merge_peds.query("race_park==@race_park")

    df_race_type = df_race_park.query("race_type==@race_type")

    # course_len = int(course_len)
    df = df_race_type.query("course_len==@course_len")
    print("course_len")
    print(course_len)
    print(df.head())
    df_1 = df['着順']
    df_2 = df['枠番']
    df_3 = df['騎手']
    df_4 = df['調教師']
    df_5 = df['種牡馬']

    datasets = {
        'df_1': df_1.to_json(orient='split', date_format='iso'),
        'df_2': df_2.to_json(orient='split', date_format='iso'),
        'df_3': df_3.to_json(orient='split', date_format='iso'),
        'df_4': df_4.to_json(orient='split', date_format='iso'),
        'df_5': df_5.to_json(orient='split', date_format='iso'),
    }
    
    return json.dumps(datasets)

@app.callback(
    Output('rank-frame', 'figure'),
    Input('intermediate-value', 'data')
)
def update_figure(jsonified_cleaned_data):
    datasets = json.loads(jsonified_cleaned_data)
    df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
    df_frame = pd.read_json(datasets['df_2'], orient='split',typ='series')
    
    df = pd.concat([df_rank,df_frame],axis=1)
    if len(df.index) == 0: 
        frame_number_chart = go.Figure()
        frame_number_chart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "該当するデータは存在しません",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return frame_number_chart
    else:
        pivot_f = pd.crosstab(df["枠番"],df["着順"],margins=True)
        win_rate_1_f = [pivot_f.T[horse_number].iloc[0]/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
        win_rate_2_f = [(pivot_f.T[horse_number].iloc[0]+pivot_f.T[horse_number].iloc[1])/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
        win_rate_3_f = [(pivot_f.T[horse_number].iloc[0]+pivot_f.T[horse_number].iloc[1]+pivot_f.T[horse_number].iloc[2])/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
        total = pivot_f.T.iloc[-1].tolist()[:-1]
        frame_numbers = pivot_f.T.columns.tolist()[:-1]

        df_f = pd.DataFrame({
            "枠番": frame_numbers,
            "勝率": win_rate_1_f,
            "連対率": win_rate_2_f,
            "複勝率": win_rate_3_f,
        })

    
        frame_number_chart = go.Figure()

        frame_number_chart.add_trace(go.Bar(name="勝率", x=df_f["枠番"], y=df_f["勝率"]))
        frame_number_chart.add_trace(go.Bar(name="連対率", x=df_f["枠番"], y=df_f["連対率"]))
        frame_number_chart.add_trace(go.Bar(name="複勝率", x=df_f["枠番"], y=df_f["複勝率"]))


        frame_number_chart.update_layout(height=400, width=1180, showlegend=True,
                                            autosize=False, title_text='枠番ごとの成績（2011年~2021年）')

        return frame_number_chart
    ################
@app.callback(
    Output('rank-jockey', 'figure'),
    [Input('intermediate-value', 'data'),
    Input('selected_jockey', 'value')]
)

def update_figure(jsonified_cleaned_data,selected_jockey):
    datasets = json.loads(jsonified_cleaned_data)
    df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
    df_jockey = pd.read_json(datasets['df_3'], orient='split',typ='series')
    df = pd.concat([df_rank,df_jockey],axis=1)
    if len(df.index) == 0: 
        jockey_chart = go.Figure()
        jockey_chart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "該当するデータは存在しません",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return jockey_chart
    else:
        pivot_j = pd.crosstab(df["騎手"],df["着順"],margins=True)
        pivot_j = pivot_j[pivot_j["All"]>=50]

        win_rate_1_j = [round(pivot_j.T[jockey].iloc[0]/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()[:-1]]
        win_rate_2_j = [round((pivot_j.T[jockey].iloc[0] + pivot_j.T[jockey].iloc[1])/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()[:-1]]
        win_rate_3_j = [round((pivot_j.T[jockey].iloc[0] + pivot_j.T[jockey].iloc[1] + pivot_j.T[jockey].iloc[2])/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()[:-1]]
        count = pivot_j.T.iloc[-1].tolist()[:-1]
        jockey = pivot_j.T.columns.tolist()[:-1]

        df_j = pd.DataFrame({
            "騎手": jockey,
            "勝率": win_rate_1_j,
            "連対率": win_rate_2_j,
            "複勝率": win_rate_3_j,
            "騎乗数": count
        })

        filtered_df = df_j.query("騎手 in @selected_jockey")

        # fig = px.bar(filtered_df, x="win_rate_1", y="jockey", orientation='h')

        jockey_chart = go.Figure()

        jockey_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["騎手"], x=filtered_df["複勝率"],orientation='h'))
        jockey_chart.add_trace(go.Bar(name="連対率", y=filtered_df["騎手"], x=filtered_df["連対率"],orientation='h'))
        jockey_chart.add_trace(go.Bar(name="勝率", y=filtered_df["騎手"], x=filtered_df["勝率"],orientation='h'))
                    # plot_bgcolor=colors['background'],
                    # paper_bgcolor=colors['background'],
                    # font_color=colors['text'],
                    # barmode='group',
        jockey_chart.update_layout(height=400, width=1180, showlegend=True,
                                        autosize=True, title_text='騎手ごとの成績（2011年~2021年）')
        return jockey_chart
    # ################
@app.callback(
    Output('rank-trainer', 'figure'),
    [Input('intermediate-value', 'data'),
    Input('selected_trainer', 'value')]
)

def update_figure(jsonified_cleaned_data,selected_trainer):
    datasets = json.loads(jsonified_cleaned_data)
    df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
    df_trainer = pd.read_json(datasets['df_4'], orient='split',typ='series')
    
    df = pd.concat([df_rank,df_trainer],axis=1)
    if len(df.index) == 0: 
        trainer_chart = go.Figure()
        trainer_chart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "該当するデータは存在しません",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return trainer_chart
    else:   
        pivot_t = pd.crosstab(df["調教師"],df["着順"],margins=True)
        pivot_t = pivot_t[pivot_t["All"]>=50]
        win_rate_1_t = [round(pivot_t.T[trainer].iloc[0]/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()[:-1]]
        win_rate_2_t = [round((pivot_t.T[trainer].iloc[0] + pivot_t.T[trainer].iloc[1])/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()[:-1]]
        win_rate_3_t = [round((pivot_t.T[trainer].iloc[0] + pivot_t.T[trainer].iloc[1] + pivot_t.T[trainer].iloc[2])/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()[:-1]]
        trainer = pivot_t.T.columns.tolist()[:-1]

        df_t = pd.DataFrame({
            "調教師": trainer,
            "勝率": win_rate_1_t,
            "連対率": win_rate_2_t,
            "複勝率": win_rate_3_t
        })

        filtered_df = df_t.query("調教師 in @selected_trainer")

        trainer_chart = go.Figure()

        trainer_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["調教師"], x=filtered_df["複勝率"],orientation='h'))
        trainer_chart.add_trace(go.Bar(name="連対率", y=filtered_df["調教師"], x=filtered_df["連対率"],orientation='h'))
        trainer_chart.add_trace(go.Bar(name="勝率", y=filtered_df["調教師"], x=filtered_df["勝率"],orientation='h'))
                    # plot_bgcolor=colors['background'],
                    # paper_bgcolor=colors['background'],
                    # font_color=colors['text'],
                    # barmode='group',
        trainer_chart.update_layout(height=400, width=1180, showlegend=True,
                                        autosize=True, title_text='調教師ごとの成績（2011年~2021年）')
        
        return trainer_chart
    # ################################################################

@app.callback(
    Output('rank-stallion', 'figure'),
    [Input('intermediate-value', 'data'),
    Input('selected_stallion', 'value')]
)

def update_figure(jsonified_cleaned_data,selected_stallion):
    datasets = json.loads(jsonified_cleaned_data)
    df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
    df_stallion = pd.read_json(datasets['df_5'], orient='split',typ='series')
    
    df = pd.concat([df_rank,df_stallion],axis=1)
    if len(df.index) == 0: 
        stallion_chart = go.Figure()
        stallion_chart.update_layout(
            xaxis =  { "visible": False },
            yaxis = { "visible": False },
            annotations = [
                {   
                    "text": "該当するデータは存在しません",
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                    "font": {
                        "size": 28
                    }
                }
            ]
        )
        return stallion_chart
    else:
        pivot_s = pd.crosstab(df["種牡馬"],df["着順"],margins=True)
        pivot_s = pivot_s[pivot_s["All"]>=50]
        win_rate_1_s = [round(pivot_s.T[stallion].iloc[0]/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()[:-1]]
        win_rate_2_s = [round((pivot_s.T[stallion].iloc[0] + pivot_s.T[stallion].iloc[1])/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()[:-1]]
        win_rate_3_s = [round((pivot_s.T[stallion].iloc[0] + pivot_s.T[stallion].iloc[1] + pivot_s.T[stallion].iloc[2])/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()[:-1]]
        stallion = pivot_s.T.columns.tolist()[:-1]

        df_s = pd.DataFrame({
            "種牡馬": stallion,
            "勝率": win_rate_1_s,
            "連対率": win_rate_2_s,
            "複勝率": win_rate_3_s,
        })

        filtered_df = df_s.query("種牡馬 in @selected_stallion")

        stallion_chart = go.Figure()

        stallion_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["種牡馬"], x=filtered_df["複勝率"],orientation='h'))
        stallion_chart.add_trace(go.Bar(name="連対率", y=filtered_df["種牡馬"], x=filtered_df["連対率"],orientation='h'))
        stallion_chart.add_trace(go.Bar(name="勝率", y=filtered_df["種牡馬"], x=filtered_df["勝率"],orientation='h'))   
        stallion_chart.update_layout(height=400, width=1180, showlegend=True,
                                        autosize=True, title_text='種牡馬ごとの成績（2011年~2021年）')
        
        return stallion_chart

