import streamlit as st
import datetime as dt
import os
import pandas as pd
import matplotlib.pyplot as plt
from individual_profile import getProfile
from trends import trends
import re


timestamp_format = "%Y-%m-%d %H:%M"


politics = pd.read_csv('final_data.csv', sep='|')


def autolabel(rects):

    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2., int(height),
                 '%d' % int(height),
                 ha='center', va='bottom')


def tweet_date(ts):
    result = dt.datetime.strptime(ts, timestamp_format)
    result = dt.datetime(result.year, result.month, 1)
    return result


politics['clean_tweet'] = politics['clean_tweet'].str.lower()


politics['date'] = politics['date'].apply(tweet_date)


def filter_tweets(filter_text='bjp'):
    df = politics[politics['clean_tweet'].str.contains(str.lower(filter_text))]
    return df




def tweets_by_date(in_df):

    unq_class = in_df.sentiment_class.unique()
    list_of_dict = []
    for j,_ in enumerate(unq_class):
        df = in_df.loc[in_df['sentiment_class'] == unq_class[j]]
        df = df.reset_index(drop=True)
        group_date = df.groupby('date')['date'].count()
        date_l = group_date.index.tolist()
        val_l = group_date.tolist()
        list_of_dict.append({
            "name": unq_class[j],
            "x": date_l,
            "y": val_l
        })

 
    return list_of_dict


def tweets_class(in_df):

    unq_class = in_df.sentiment_class.unique()
    labels = []
    vals = []
    for j,_ in enumerate(unq_class):
        df = in_df.loc[in_df['sentiment_class'] == unq_class[j]]
        len_df = len(df.index)
        labels.append(unq_class[j])
        vals.append(len_df)

    return vals, labels


def main():
    st.title('Social and Information Networks')
    st.subheader('Data analysis for Indian Politics')

    
    st.sidebar.title('Menu')
    menuItems = [
        'DashBoard',
        'Individual Analyzer',
        'Politicians Data',
        'Trends'
    ]

    item = st.sidebar.selectbox('', menuItems)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    github = '''[ Fork/Star on Github](https://github.com/abhayrpatel10/spartan)'''
    st.sidebar.info(github)

    if item == 'DashBoard':
        s='''
        The data is extracted from the various social media platform is assigned a sentiment score.The technique used to assign the score is VADER (Valence Aware Dictionary and sentiment Reasoner).The sentiment score is calculated from a lexicon rule based dictionary and  the data is plotted for visual representation

        ### Workflow
            Extracting data from social media - data mostly from twitter.(The data extracted is from end of 2017 to 2018 just before 2019 Indian elections)
            The data was filterer using keywords like India,Indian politics,bj,congress,ncp,nda,inc,election2019
            The data was cleaned - removal of links,stopwords
            Each tweet was asigned a sentiment score
            The graphs shown is the result of grouping keywords and the sentiment score
        '''
        st.markdown(s)

        keyword = st.text_input('Enter a political keyword', 'bjp')

       

        x, y = tweets_class(filter_tweets(keyword))
        ax = plt.bar(y, x)
        autolabel(ax)
        st.write(mpl_fig=ax)
        st.pyplot()

        

        startingRadius = 0.7 + (0.3* (len(x)-1))
        for i, _ in enumerate(len(x)):
            scenario =y[i]
            percentage = x[i]
            textLabel = scenario + ' ' + str(percentage)
            print(startingRadius)
            
            remainingPie = 100 - percentage

            donut_sizes = [remainingPie, percentage]

            plt.text(0.04, startingRadius + 0.07, textLabel, horizontalalignment='center', verticalalignment='center')
            plt.pie(donut_sizes, radius=startingRadius, startangle=90, colors=['#d5f6da', '#5cdb6f'],
                    wedgeprops={"edgecolor": "white", 'linewidth': 6})

            startingRadius-=0.3

        # equal ensures pie chart is drawn as a circle (equal aspect ratio)
        plt.axis('equal')

        # create circle and place onto pie chart
        circle = plt.Circle(xy=(0, 0), radius=0.35, facecolor='white')
        plt.gca().add_artist(circle)
        st.pyplot()
        



        

        
    elif item == 'Individual Analyzer':
        name=st.text_input('Name','narendramodi')
        getProfile(name)

    elif item=='Location based analyser':
        f=open('data.geojson')
        st.map(f)
    elif item=='Politicians Data':
        df=pd.read_csv('term-16.csv')
        df=df.drop(['sort_name','twitter','id','facebook','term','start_date','end_date','image','gender','wikidata','wikidata_group','wikidata_area'],axis=1)
        st.table(df)

    elif item=='Trends':
        trends()

        

if __name__ == "__main__":
    main()
