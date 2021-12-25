# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.

# from django_plotly_dash import DjangoDash
# from dash import dcc
# from dash import html 
# import plotly.express as px
# import plotly.graph_objects as go
# import pandas as pd
# from dash.dependencies import Input, Output,State
# from .DP import DataProcessor 
# from .Result import Results
# from .Ped import Peds
# import dash_bootstrap_components as dbc
# import json
# import numpy as np
# from .s3 import SthreeController as SC
# from django.conf import settings

# #Dash


# # app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app = DjangoDash('horecast', add_bootstrap_links=True)

# colors = {
#     'background': '#253237',
#     'text': '#EFFBFF'
# }

# #Data
# # with open('forecast/static/data/race_results_all.pickle',"rb") as r:
# #     race_results = pickle.load(r)
# # with open('forecast/static/data/peds_all.pickle',"rb") as p:
# #     peds = pickle.load(p)
# sc = SC(settings.AWS_ACCESS_KEY_ID,settings.AWS_SECRET_ACCESS_KEY,settings.AWS_S3_REGION_NAME,settings.AWS_STORAGE_BUCKET_NAME)
# race_results = sc.read_result()
# peds = sc.read_peds()

# r = Results(race_results)
# p = Peds(peds)


# # df = r.data.query('(race_park=="中京" & race_type=="ダート") & course_len==1800' ,engine='python')
# df = r.data

# df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
# df.dropna(subset=["着順"], inplace=True)
# df["着順"] = df["着順"].astype(int)
# merge_peds = df.merge(p.peds,how="left",left_on="horse_id",right_on="horse_id")
# merge_peds["種牡馬"] = merge_peds["peds_0"].str.split(expand=True)[0]

# available_race_park= merge_peds["race_park"].unique()
# available_race_type= merge_peds["race_type"].unique()
# available_course_len= merge_peds["course_len"].unique()
# available_jockey = ['藤岡康太', '藤懸貴志', '柴山雄一',  '丸田恭介', 
#        '吉田豊', '吉田隼人', '松山弘平',  
#        '横山和生',  '丹内祐次', '福永祐一',
#        '幸英明', '鮫島良太', '川須栄彦', '菱田裕二', '古川吉洋',
#        '大野拓弥', '北村友一', 
#        '伊藤工真', '国分優作', 
#        '荻野琢真', '池添謙一', '和田竜二', '横山典弘',
#        '中井裕二', '勝浦正樹', '藤岡佑介', '武豊', '小牧太', '内田博幸', '川田将雅',
#        '浜中俊', '国分恭介', 
#        '酒井学', '戸崎圭太', '岩田康誠',
#        '柴田大知', '長岡禎仁', '原田和真', 'Ｍ．デム',  '丸山元気', 'ルメール',
#        '三浦皇成',
#        '秋山真一', '津村明秀', 
#        '北村宏司', 
#        '松若風馬', '田辺裕信', '木幡初也', '石橋脩', 
#        '石川裕紀',
#        '鮫島克駿', 
#        '藤田菜七', '坂井瑠星', '野中悠太',
#        '横山武史', '江田照男', '川又賢治', '富田暁', 
#        '木幡巧也', '武藤雅', '西村淳也', 
#        '木幡育也', '斎藤新', '岩田望来',
#        '亀田温心', '藤井勘一',  '団野大成',  '泉谷楓真',
#        '菅原明良', '秋山稔樹',  '角田大和', '永島まな',
#        '小沢大仁',"平均"]
# available_trainer = [
#       '[西] 中内田充','[東] 手塚貴久','[西] 矢作芳人','[西] 友道康夫',
#        '[東] 国枝栄','[西] 清水久詞','[西] 安田隆行', '[西] 須貝尚介','[西] 斉藤崇史',
#        '[西] 音無秀孝', '[西] 武幸四郎', '[東] 堀宣行', '[東] 伊藤圭三',
#        '[西] 高野友和', '[東] 伊藤伸一','[西] 藤岡健一','[東] 田村康仁',
#        '[西] 池江泰寿','[西] 杉山晴紀', '[西] 松永幹夫', '[西] 西村真幸',
#        '[西] 池添学', '[西] 寺島良', '[西] 南井克巳',  '[西] 藤原英昭', '[西] 吉岡辰弥',
#        '[東] 斎藤誠','[東] 木村哲也','[東] 中舘英二','[西] 森秀行','[西] 武英智',
#        '[西] 西園正都','[西] 浅見秀一','[東] 萩原清','[西] 高柳大輔','[東] 藤沢和雄',  
#        '[西] 中竹和也','[西] 安田翔伍','[東] 和田勇介', '[東] 加藤征弘', '[西] 大久保龍',
#        '[西] 佐々木晶','[西] 本田優',  '[西] 大橋勇樹', '[東] 鹿戸雄一','[西] 橋口慎介',
#        '[東] 岩戸孝樹','[西] 上村洋行', '[西] 奥村豊','[西] 中尾秀正','[西] 岡田稲男',"平均"]
# available_stallion= ['ディープインパクト', 'ロードカナロア', 'ハーツクライ', 'キズナ', 'ルーラーシップ', 'キングカメハメハ',
#        'オルフェーヴル', 'ダイワメジャー', 'エピファネイア', 'ヘニーヒューズ', 'モーリス', 'スクリーンヒーロー',
#        'ドゥラメンテ', 'キンシャサノキセキ', 'ハービンジャー', 'ゴールドシップ', 'クロフネ', 'ブラックタイド',
#        'ジャスタウェイ', 'ヴィクトワールピサ', 'エイシンフラッシュ', 'リオンディーズ', 'シニスターミニスター',
#        'パイロ', 'ゴールドアリュール', 'アイルハヴアナザー', 'マジェスティックウォリアー', 'ディープブリランテ',
#        'サウスヴィグラス', 'ノヴェリスト', 'ステイゴールド', 'マクフィ', 'バゴ', 'ミッキーアイル',
#        'リアルインパクト', 'カレンブラックヒル', 'ディスクリートキャット', 'マツリダゴッホ', 'ホッコータルマエ',
#        'アドマイヤムーン', 'スマートファルコン', 'メイショウサムソン', 'トゥザグローリー',
#        'ストロングリターン', 'ワールドエース', 'エスポワールシチー', 'ダンカーク', 'メイショウボーラー',
#        'ネオユニヴァース',"平均"]
# available_course_len = np.sort(available_course_len)


# #グラフのレイアウト調整
# RadioItems = dbc.Card(
   
#     [
#         dbc.FormGroup(
#             [
#                 dbc.Label("競馬場を選択してください"),
#                 dcc.RadioItems(
#                     id="select_race_park",
#                     options=[{'label': i, 'value': i} for i in available_race_park],
#                     value="札幌",
#                     labelStyle={'display': 'inline-block'}
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("レース種別を選択してください"),
#                 dcc.RadioItems(
#                     id="select_race_type",
#                     options=[{'label': i, 'value': i} for i in available_race_type],
#                     value="芝",
#                     labelStyle={'display': 'inline-block'}
#                 ),
#             ]
#         ),
#         dbc.FormGroup(
#             [
#                 dbc.Label("距離を選択してください"),
#                 dcc.RadioItems(
#                     id="select_course_len",
#                     options=[{'label': i, 'value': i} for i in available_course_len],
#                     value=2000,
#                     labelStyle={'display': 'inline-block'}
#                 ),
#             ]
#         ),
#         dbc.Button(
#             "検索", id="search-button", className="mr-2", n_clicks=0,block=True,color="light"
#         ),
#         dcc.Store(id='intermediate-value')
#     ],
#     body=True,
#     style={'color':'#EFFBFF',"background-color": "#36474f"}
# )




# app.layout = html.Div(
    
#     dbc.Container(
#         [   
#         dbc.Row(
#                 [    
#                     html.Div(
#                         dbc.Col(RadioItems),  
#                     )
#                 ],
#                 align="center",
#                 className="h-30",
                
#             ),       
#             html.Br(),
#             html.Br(),
#             html.Br(),
#             html.Div(
#                 children=[
#                     html.H3("表示されるまでしばらく時間がかかります",
#                     style={
#                         'textAlign': 'center',# テキストセンター寄せ
#                         'color': colors['text'],# 文字色
#                     })
#                 ]
#             ),
#             html.Br(),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 [
#                     html.Div(
#                         children=[
#                             html.H1(id="data-title", 
#                             style={
#                             'textAlign': 'center',# テキストセンター寄せ
#                             'color': colors['text'],# 文字色
#                             })
#                         ],
#                     ),
#                     html.Br(),
#                     html.Br(),
#                 ],
#                 className="h-40"
#             ),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                         html.Br(),
#                         html.H2("枠順ごとの勝率・連対率・複勝率"),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Graph(
#                             id='rank-frame',
                            
#                             figure={},
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         html.Br(),
#                         ]
#                         # スタイルシートを適用
#                         # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
#                         #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
#                         #             }
#                     ),
#                 ],
#                 className="h-40",
#                 style={'color':'#EFFBFF',"background-color": "#36474f"}
#             ),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                         html.Br(),
#                         html.H2("騎手ごとの勝率・連対率・複勝率"),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Dropdown(
#                             id='selected_jockey',
#                             options=[{'label': i, 'value': i} for i in available_jockey],
#                             value='平均',
#                             multi=True,
#                             style=
#                                 { 
#                                     'color': '#000000'
#                                 } 
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Graph(
#                             id='rank-jockey',
#                             figure={},
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         ]
#                         # スタイルシートを適用
#                         # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
#                         #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
#                         #             }
#                     ),
#                 ],
#                 className="h-40",
#                 style={'color':'#EFFBFF',"background-color": "#36474f"}
#             ),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [   
#                         html.Br(), 
#                         html.H2("調教師ごとの勝率・連対率・複勝率"),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Dropdown(
#                             id='selected_trainer',
#                             options=[{'label': i, 'value': i} for i in available_trainer],
#                             value='平均',
#                             multi=True,
#                             style=
#                             { 
#                                 'color': '#000000'
#                             } 
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Graph(
#                             id='rank-trainer',
#                             figure={},
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         ]
#                     ),
#                 ],
#                 className="h-40",
#                 style={'color':'#EFFBFF',"background-color": "#36474f"}
#             ),
#             html.Br(),
#             html.Br(),
#             dbc.Row(
#                 [
#                     dbc.Col(
#                         [
#                         html.Br(),
#                         html.H2("種牡馬ごとの勝率・連対率・複勝率"),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Dropdown(
#                             id='selected_stallion',
#                             options=[{'label': i, 'value': i} for i in available_stallion],
#                             value='平均',
#                             multi=True,
#                             style=
#                             { 
#                                 'color': '#000000'
#                             } 
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         dcc.Graph(
#                             id='rank-stallion',
#                             figure={},
#                         ),
#                         html.Br(),
#                         html.Br(),
#                         ]
#                         # スタイルシートを適用
#                         # style={'background-color': '#ffffff', 'text-align': 'center', 'border-radius': '5px 0px 0px 5px', 'height': '700px', 'width': '1185px',
#                         #             'margin': '0px 0px 30px 10px', 'padding': '15px', 'position': 'relative', 'box-shadow': '4px 4px 4px lightgrey',
#                         #             }
#                     ),
#                 ],
#                 className="h-40",
#                 style={'color':'#EFFBFF',"background-color": "#36474f"}
#             ),
#             html.Br(),
#             html.Br(),
#         ],
#     ),style = {'backgroundColor': colors['background']}, # 背景色
# )


# @app.callback(
#     Output('data-title', 'children'),
#     [Input('search-button','n_clicks')],
#     [State('select_race_park', 'value'),
#     State('select_race_type', 'value'),
#     State('select_course_len', 'value')]
# )
# def express_title(n_clicks,race_park,race_type,course_len):
#     return f"{race_park}{race_type}{course_len}mデータ"



# @app.callback(
#     Output('intermediate-value', 'data'),
#     [Input('search-button','n_clicks')],
#     [State('select_race_park', 'value'),
#     State('select_race_type', 'value'),
#     State('select_course_len', 'value')]
# )
# def update_figure(n_clicks,race_park,race_type,course_len):

# #Data
#     race_results = sc.read_result()
#     peds = sc.read_peds()

#     r = Results(race_results)
#     p = Peds(peds)





#     # r = Results.read_pickle(['race_results_all.pickle'])
#     # p = Peds.read_pickle(['peds_all.pickle'])
#     # course_len = int(course_len)


#     # df = r.data.query('(race_park=="中京" & race_type=="ダート") & course_len==1800' ,engine='python')
#     df = r.data
#     df["着順"] = pd.to_numeric(df["着順"], errors="coerce")
#     df.dropna(subset=["着順"], inplace=True)
#     df["着順"] = df["着順"].astype(int)
#     merge_peds = df.merge(p.peds,how="left",left_on="horse_id",right_on="horse_id")
#     merge_peds["種牡馬"] = merge_peds["peds_0"].str.split(expand=True)[0]
    


#     # df = merge_peds[(merge_peds["race_park"]==race_park & merge_peds["race_type"]==race_type) & merge_peds["course_len"]==course_len]
#     df_race_park = merge_peds.query("race_park==@race_park")

#     df_race_type = df_race_park.query("race_type==@race_type")

#     # course_len = int(course_len)
#     df = df_race_type.query("course_len==@course_len")
#     df_1 = df['着順']
#     df_2 = df['枠番']
#     df_3 = df['騎手']
#     df_4 = df['調教師']
#     df_5 = df['種牡馬']

#     datasets = {
#         'df_1': df_1.to_json(orient='split', date_format='iso'),
#         'df_2': df_2.to_json(orient='split', date_format='iso'),
#         'df_3': df_3.to_json(orient='split', date_format='iso'),
#         'df_4': df_4.to_json(orient='split', date_format='iso'),
#         'df_5': df_5.to_json(orient='split', date_format='iso'),
#     }
    
#     return json.dumps(datasets)

# @app.callback(
#     Output('rank-frame', 'figure'),
#     Input('intermediate-value', 'data')
# )
# def update_figure(jsonified_cleaned_data):
#     datasets = json.loads(jsonified_cleaned_data)
#     df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
#     df_frame = pd.read_json(datasets['df_2'], orient='split',typ='series')
    
#     df = pd.concat([df_rank,df_frame],axis=1)
#     if len(df.index) == 0: 
#         frame_number_chart = go.Figure()
#         frame_number_chart.update_layout(
#             xaxis =  { "visible": False },
#             yaxis = { "visible": False },
#             annotations = [
#                 {   
#                     "text": "該当するデータは存在しません",
#                     "xref": "paper",
#                     "yref": "paper",
#                     "showarrow": False,
#                     "font": {
#                         "size": 28
#                     }
#                 }
#             ]
#         )
#         return frame_number_chart
#     else:
#         pivot_f = pd.crosstab(df["枠番"],df["着順"],margins=True)
#         win_rate_1_f = [pivot_f.T[horse_number].iloc[0]/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
#         win_rate_2_f = [(pivot_f.T[horse_number].iloc[0]+pivot_f.T[horse_number].iloc[1])/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
#         win_rate_3_f = [(pivot_f.T[horse_number].iloc[0]+pivot_f.T[horse_number].iloc[1]+pivot_f.T[horse_number].iloc[2])/pivot_f.T[horse_number].iloc[-1] for horse_number in pivot_f.T.columns.tolist()[:-1]]
#         total = pivot_f.T.iloc[-1].tolist()[:-1]
#         frame_numbers = pivot_f.T.columns.tolist()[:-1]

#         df_f = pd.DataFrame({
#             "枠番": frame_numbers,
#             "勝率": win_rate_1_f,
#             "連対率": win_rate_2_f,
#             "複勝率": win_rate_3_f,
#         })

    
#         frame_number_chart = go.Figure()

#         frame_number_chart.add_trace(go.Bar(name="勝率", x=df_f["枠番"], y=df_f["勝率"]))
#         frame_number_chart.add_trace(go.Bar(name="連対率", x=df_f["枠番"], y=df_f["連対率"]))
#         frame_number_chart.add_trace(go.Bar(name="複勝率", x=df_f["枠番"], y=df_f["複勝率"]))


#         frame_number_chart.update_layout(height=550, width=1100, showlegend=True,
#                                             autosize=False, title_text='枠番ごとの成績（2011年~2021年）')

#         return frame_number_chart
#     ################
# @app.callback(
#     Output('rank-jockey', 'figure'),
#     [Input('intermediate-value', 'data'),
#     Input('selected_jockey', 'value')]
# )

# def update_figure(jsonified_cleaned_data,selected_jockey):
#     datasets = json.loads(jsonified_cleaned_data)
#     df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
#     df_jockey = pd.read_json(datasets['df_3'], orient='split',typ='series')
#     df = pd.concat([df_rank,df_jockey],axis=1)
#     if len(df.index) == 0: 
#         jockey_chart = go.Figure()
#         jockey_chart.update_layout(
#             xaxis =  { "visible": False },
#             yaxis = { "visible": False },
#             annotations = [
#                 {   
#                     "text": "該当するデータは存在しません",
#                     "xref": "paper",
#                     "yref": "paper",
#                     "showarrow": False,
#                     "font": {
#                         "size": 28
#                     }
#                 }
#             ]
#         )
#         return jockey_chart
#     else:
#         pivot_j = pd.crosstab(df["騎手"],df["着順"],margins=True)
#         # pivot_j = pivot_j[pivot_j["All"]>=50]

#         win_rate_1_j = [round(pivot_j.T[jockey].iloc[0]/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()]
#         win_rate_2_j = [round((pivot_j.T[jockey].iloc[0] + pivot_j.T[jockey].iloc[1])/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()]
#         win_rate_3_j = [round((pivot_j.T[jockey].iloc[0] + pivot_j.T[jockey].iloc[1] + pivot_j.T[jockey].iloc[2])/pivot_j.T[jockey].iloc[-1],2) for jockey in pivot_j.T.columns.tolist()]
#         count = pivot_j.T.iloc[-1].tolist()
#         jockey = pivot_j.T.columns.tolist()

#         df_j = pd.DataFrame({
#             "騎手": jockey,
#             "勝率": win_rate_1_j,
#             "連対率": win_rate_2_j,
#             "複勝率": win_rate_3_j,
#             "騎乗数": count
#         })
#         df_j["騎手"].iloc[-1]='平均'
#         filtered_df = df_j.query("騎手 in @selected_jockey")

#         # fig = px.bar(filtered_df, x="win_rate_1", y="jockey", orientation='h')

#         jockey_chart = go.Figure()
#         jockey_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["騎手"], x=filtered_df["複勝率"]))
#         jockey_chart.add_trace(go.Bar(name="連対率", y=filtered_df["騎手"], x=filtered_df["連対率"]))
#         jockey_chart.add_trace(go.Bar(name="勝率", y=filtered_df["騎手"], x=filtered_df["勝率"]))
#         jockey_chart.update_traces(width=0.25,
#                   hovertemplate='%{y}: %{x:0.2f}%',
#                   texttemplate='%{x:0.2f}%',
#                   textposition='outside',
#                   orientation='h')
#                     # plot_bgcolor=colors['background'],
#                     # paper_bgcolor=colors['background'],
#                     # font_color=colors['text'],
#                     # barmode='group',
#         jockey_chart.update_layout(height=550, width=1100, showlegend=True,
#                                         autosize=True, title_text='騎手ごとの成績（2011年~2021年）',legend_traceorder='reversed')

#         return jockey_chart
#     # ################
# @app.callback(
#     Output('rank-trainer', 'figure'),
#     [Input('intermediate-value', 'data'),
#     Input('selected_trainer', 'value')]
# )

# def update_figure(jsonified_cleaned_data,selected_trainer):
#     datasets = json.loads(jsonified_cleaned_data)
#     df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
#     df_trainer = pd.read_json(datasets['df_4'], orient='split',typ='series')
    
#     df = pd.concat([df_rank,df_trainer],axis=1)
#     if len(df.index) == 0: 
#         trainer_chart = go.Figure()
#         trainer_chart.update_layout(
#             xaxis =  { "visible": False },
#             yaxis = { "visible": False },
#             annotations = [
#                 {   
#                     "text": "該当するデータは存在しません",
#                     "xref": "paper",
#                     "yref": "paper",
#                     "showarrow": False,
#                     "font": {
#                         "size": 28
#                     }
#                 }
#             ]
#         )
#         return trainer_chart
#     else:   
#         pivot_t = pd.crosstab(df["調教師"],df["着順"],margins=True)
#         # pivot_t = pivot_t[pivot_t["All"]>=50]
#         win_rate_1_t = [round(pivot_t.T[trainer].iloc[0]/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()]
#         win_rate_2_t = [round((pivot_t.T[trainer].iloc[0] + pivot_t.T[trainer].iloc[1])/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()]
#         win_rate_3_t = [round((pivot_t.T[trainer].iloc[0] + pivot_t.T[trainer].iloc[1] + pivot_t.T[trainer].iloc[2])/pivot_t.T[trainer].iloc[-1],2) for trainer in pivot_t.T.columns.tolist()]
#         trainer = pivot_t.T.columns.tolist()

#         df_t = pd.DataFrame({
#             "調教師": trainer,
#             "勝率": win_rate_1_t,
#             "連対率": win_rate_2_t,
#             "複勝率": win_rate_3_t
#         })
#         df_t["調教師"].iloc[-1]='平均'
#         filtered_df = df_t.query("調教師 in @selected_trainer")

#         trainer_chart = go.Figure()
#         trainer_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["調教師"], x=filtered_df["複勝率"]))   
#         trainer_chart.add_trace(go.Bar(name="連対率", y=filtered_df["調教師"], x=filtered_df["連対率"]))
#         trainer_chart.add_trace(go.Bar(name="勝率", y=filtered_df["調教師"], x=filtered_df["勝率"]))
#         trainer_chart.update_traces(width=0.25,
#                   hovertemplate='%{y}: %{x:0.2f}%',
#                   texttemplate='%{x:0.2f}%',
#                   textposition='outside',
#                   orientation='h')
#         trainer_chart.update_layout(height=550, width=1100, showlegend=True,
#                                         autosize=True, title_text='調教師ごとの成績（2011年~2021年）',legend_traceorder='reversed')
        
#         return trainer_chart
#     # ################################################################

# @app.callback(
#     Output('rank-stallion', 'figure'),
#     [Input('intermediate-value', 'data'),
#     Input('selected_stallion', 'value')]
# )

# def update_figure(jsonified_cleaned_data,selected_stallion):
#     datasets = json.loads(jsonified_cleaned_data)
#     df_rank = pd.read_json(datasets['df_1'], orient='split',typ='series')
#     df_stallion = pd.read_json(datasets['df_5'], orient='split',typ='series')
    
#     df = pd.concat([df_rank,df_stallion],axis=1)
#     if len(df.index) == 0: 
#         stallion_chart = go.Figure()
#         stallion_chart.update_layout(
#             xaxis =  { "visible": False },
#             yaxis = { "visible": False },
#             annotations = [
#                 {   
#                     "text": "該当するデータは存在しません",
#                     "xref": "paper",
#                     "yref": "paper",
#                     "showarrow": False,
#                     "font": {
#                         "size": 28
#                     }
#                 }
#             ]
#         )
#         return stallion_chart
#     else:
#         pivot_s = pd.crosstab(df["種牡馬"],df["着順"],margins=True)
#         # pivot_s = pivot_s[pivot_s["All"]>=50]
#         win_rate_1_s = [round(pivot_s.T[stallion].iloc[0]/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()]
#         win_rate_2_s = [round((pivot_s.T[stallion].iloc[0] + pivot_s.T[stallion].iloc[1])/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()]
#         win_rate_3_s = [round((pivot_s.T[stallion].iloc[0] + pivot_s.T[stallion].iloc[1] + pivot_s.T[stallion].iloc[2])/pivot_s.T[stallion].iloc[-1],2) for stallion in pivot_s.T.columns.tolist()]
#         stallion = pivot_s.T.columns.tolist()

#         df_s = pd.DataFrame({
#             "種牡馬": stallion,
#             "勝率": win_rate_1_s,
#             "連対率": win_rate_2_s,
#             "複勝率": win_rate_3_s,
#         })
#         df_s["種牡馬"].iloc[-1]='平均'
#         filtered_df = df_s.query("種牡馬 in @selected_stallion")

#         stallion_chart = go.Figure()
#         stallion_chart.add_trace(go.Bar(name="複勝率", y=filtered_df["種牡馬"], x=filtered_df["複勝率"])) 
#         stallion_chart.add_trace(go.Bar(name="連対率", y=filtered_df["種牡馬"], x=filtered_df["連対率"]))
#         stallion_chart.add_trace(go.Bar(name="勝率", y=filtered_df["種牡馬"], x=filtered_df["勝率"]))   
#         stallion_chart.update_traces(width=0.25,
#                   hovertemplate='%{y}: %{x:0.2f}%',
#                   texttemplate='%{x:0.2f}%',
#                   textposition='outside',
#                   orientation='h')

#         stallion_chart.update_layout(height=400, width=1100, showlegend=True,
#                                         autosize=True, title_text='種牡馬ごとの成績（2011年~2021年）',legend_traceorder='reversed')
        
#         return stallion_chart

