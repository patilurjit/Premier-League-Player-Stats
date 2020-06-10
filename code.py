import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

def main():
    image = Image.open("..\PL.jpg") #update the location of the image after cloning the repository
    st.image(image,use_column_width = True)

    ft_selection = st.sidebar.selectbox("Functionality Selection",('','Player Stat Comparison','Top Performers'),key = 'ft_selection')

    if ft_selection == 'Player Stat Comparison':

        st.title("Premier League Player Stats")
        st.subheader("Compare stats of Premier League Players")
        st.sidebar.title("Player Stat Comparison")

        st.sidebar.subheader("Select Stat Type")
        stat = st.sidebar.selectbox("Stat Types",('Standard Stats','Passing','Goal and Shot Creation','Defensive Actions','Miscellaneous'),key = 'stat')

        def load_data():
            data = pd.read_excel("..\PL.xlsx",sheet_name = stat) #update the location of the dataset after cloning the repository
            return data

        df = load_data()
        df.Age.astype(int)
        df.Born.astype(int)

        def select_features():
            if stat == 'Standard Stats':
                cols = ['Pos','Squad','Age','Matches Played','Starts','Minutes','Yellow Cards','Red Cards','Goals/90','Assists/90']
                return cols
            elif stat == 'Passing':
                cols = ['Pos','Squad','Age','90s','Attempted Passes','Pass Completion %','Pass Completion % (short)','Pass Completion % (medium)','Pass Completion % (long)']
                return cols
            elif stat == 'Goal and Shot Creation':
                cols = ['Pos','Squad','Age','90s','Shot Creating Actions','Shot Creating Actions/90','Goal Creating Actions','Goal Creating Actions/90','OG']
                return cols
            elif stat == 'Defensive Actions':
                cols = ['Pos','Squad','Age','90s','Tackles Won %','Number of times dribbled past','Shots Blocked','Interceptions','Clearances','Errors']
                return cols
            else:
                cols = ['Pos','Squad','Age','90s','Yellow Cards','Red Cards','Second Yellow Card','Fouls Committed','Fouls Drawn','Offsides','Crosses','Interceptions','Penalty Kicks Won','Penalty Kicks Conceded','Own Goals','Aerial Duels Won %']
                return cols

        cols = select_features()

        cols = select_features()

        list1 = df.Squad.unique()
        list1.sort()

        def team_data(club):
            data1 = df[df.Squad == club]
            return data1

        st.sidebar.subheader("Player 1")
        club1 = st.sidebar.selectbox("Team",list1,key = 'club1')

        team1 = team_data(club1)

        list2 = team1.Player.unique()
        list2.sort()

        player1 = st.sidebar.selectbox("Name",list2,key = 'player1')

        st.sidebar.subheader("Player 2")
        club2 = st.sidebar.selectbox("Team",list1,key = 'club2')

        team2 = team_data(club2)

        list3 = team2.Player.unique()
        list3.sort()

        player2 = st.sidebar.selectbox("Name",list3,key = 'player2')

        p1 = team1[team1['Player'] == player1]
        p1.drop('Rk',axis = 1,inplace = True)
        p1.set_index('Player',inplace = True)

        p2 = team2[team2['Player'] == player2]
        p2.drop('Rk',axis = 1,inplace = True)
        p2.set_index('Player',inplace = True)

        if st.sidebar.button("Compare",key = 'compare'):
            show1 = p1[cols].T
            show2 = p2[cols].T
            final = pd.concat([show1,show2],axis = 1)
            st.table(final)

    if ft_selection == 'Top Performers':

        st.title("Top Performers")
        st.sidebar.subheader("Select Stat")

        def load_data():
            data = pd.read_excel("..\PL.xlsx",sheet_name = "Miscellaneous") #update the location of the dataset after cloning the repository
            return data

        df = load_data()

        stats = st.sidebar.selectbox("Stats",('Goals','Assists','Yellow Cards','Red Cards','Fouls Committed','Fouls Drawn','Offsides','Crosses','Interceptions'),key = 'stats')

        def show_top(stat):
            df1 = df.sort_values(by=[stat],ascending = False)
            df2 = df1[['Player','Squad',stat]].head(10)
            list1 = np.arange(1,11)
            df2.set_index(list1,inplace = True)
            return df2

        show = show_top(stats)

        if st.sidebar.button("Show",key = 'show'):
            st.table(show)

if __name__ == '__main__':
    main()
