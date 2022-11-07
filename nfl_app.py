import pandas as pd
import numpy as np 
import altair as alt
import streamlit as st
import time 

st.title('NFL Replay')
st.subheader('Week 8')
colors = {
    'ARI':"#97233F", 
    'ATL':"#A71930", 
    'BAL':'#241773', 
    'BUF':"#00338D", 
    'CAR':"#0085CA", 
    'CHI':"#C83803", 
    'CIN':"#FB4F14", 
    'CLE':"#311D00", 
    'DAL':'#003594',
    'DEN':"#FB4F14", 
    'DET':"#0076B6", 
    'GB':"#203731", 
    'HOU':"#03202F", 
    'IND':"#002C5F", 
    'JAX':"#9F792C", 
    'KC':"#E31837", 
    'LA':"#003594", 
    'LAC':"#0080C6", 
    'LV':"#000000",
    'MIA':"#008E97", 
    'MIN':"#4F2683", 
    'NE':"#002244", 
    'NO':"#D3BC8D", 
    'NYG':"#0B2265", 
    'NYJ':"#125740", 
    'PHI':"#004C54", 
    'PIT':"#FFB612", 
    'SEA':"#69BE28", 
    'SF':"#AA0000",
    'TB':'#D50A0A', 
    'TEN':"#4B92DB", 
    'WAS':"#5A1414", 
    'football':'#CBB67C'
}
games = pd.read_csv('trimmed_games.csv',usecols=['nflId',
'gameId',
'playId',
'frameId',
'playDescription',
'possessionTeam',
'defensiveTeam',
'homeTeamAbbr',
'team',
'visitorTeamAbbr',
'x',
'y',
'displayName',
'officialPosition',
'pff_role',
'team_color'])


game_ids = games['gameId'].unique()

def play_select(x):
    return plays[plays['playId'] == x]['playDescription'].values[0]

def game_select(x):
    y = games[games['gameId'] == x].iloc[0]
    return f"{y['homeTeamAbbr']} vs {y['visitorTeamAbbr']}"

game = st.sidebar.selectbox('Pick a game',game_ids,index=0,format_func=game_select)

game_df = games.loc[games['gameId'] == game]
plays = game_df[['playId','playDescription']].drop_duplicates()


def build_chart(frame_df):
    play_title = frame_df[['playDescription','possessionTeam','defensiveTeam']].iloc[0]
    frame_chart = alt.Chart(frame_df).mark_circle().encode(
            x=alt.X('x',scale=alt.Scale(domain=(0,120))),
            y=alt.Y('y',scale=alt.Scale(domain=(0,53.3)),axis=None),
            color=alt.Color(
                'team',
                scale=alt.Scale(domain=frame_df.team.unique(),range=frame_df.team_color.unique())),
            tooltip=['displayName','officialPosition','pff_role',]).properties(
                    title=f"Offense - {play_title['possessionTeam']} Defense - {play_title['defensiveTeam']}",
                    width=640,
                    height=320,
                    background='#00B140')
    return frame_chart
    

def game_chart_play(game_df:pd.DataFrame(),play):
    plot_charts = []
    play_df = game_df.query(f'playId == {play}').drop_duplicates()
    ffdict = dict(tuple(play_df.groupby('frameId')))
    plot_charts = [build_chart(x) for i, x in ffdict.items()]
    return plot_charts

def chart_game(game_df, game = 2021102800,play = 189, frame = 1):
    frame_df = game_df.query(f'gameId == {game} and playId == {play} and frameId == {frame}')
    play_title = frame_df[['playDescription','possessionTeam','defensiveTeam']].iloc[0]
    frame_chart = alt.Chart(frame_df).mark_circle().encode(
        x=alt.X('x',scale=alt.Scale(domain=(0,120))),
        y=alt.Y('y',scale=alt.Scale(domain=(0,53.3)),axis=None),
        color=alt.Color(
            'team',
            scale=alt.Scale(domain=frame_df.team.unique(),range=frame_df.team_color.unique())),
        tooltip=['displayName','officialPosition','pff_role',]).properties(
                title=f"Offense - {play_title['possessionTeam']} Defense - {play_title['defensiveTeam']}",
                width=640,
                height=320,
                background='#00B140')
    return frame_chart
    
def reset_button():
    st.session_state['animate_nfl'] = False
    return


play = st.sidebar.selectbox('Pick a play',plays,index=0,format_func=play_select)
pb_speed = st.sidebar.slider('Playback Delay',min_value=0.05,max_value=0.9,value=0.25,step=.05)
start_plot = st.sidebar.checkbox('Start Animation', key='animate_nfl')

st.text('''
        Select a game and play to animate from NFL week 8. To animate the play, 
        check the Start Animation check box.
        ''')

if start_plot:
    charts = game_chart_play(game_df,play)
    st.caption(f"{plays[plays['playId'] == play]['playDescription'].values[0]}")
    game_plot = st.altair_chart(charts[0])
    num_charts = len(charts)
    i = 0
    while i < num_charts:
        game_plot = game_plot.altair_chart(charts[i])
        i +=1
        time.sleep(pb_speed)




