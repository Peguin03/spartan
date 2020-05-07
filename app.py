import streamlit as st
import datetime as dt
import os
import pandas as pd
import matplotlib.pyplot as plt
from gotpy import got3 as got
from induvidual_profile import getProfile


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

# creating plots

# line chart


def tweets_by_date(in_df):

    unq_class = in_df.sentiment_class.unique()
    list_of_dict = []
    for j in range(0, len(unq_class)):
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

    # return {
    #     "data": list_of_dict,
    #     "layout": {
    #         "title": "# Tweets over Time",
    #         "showlegend": True
    #     }
    # }
    return list_of_dict


def tweets_class(in_df):

    unq_class = in_df.sentiment_class.unique()
    labels = []
    vals = []
    for j in range(0, len(unq_class)):
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
        'Induvidual Analyser',
        'Location based analyser',
    ]

    item = st.sidebar.selectbox('', menuItems)
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    github = '''[ Fork/Star on Github](https://github.com/abhayrpatel10/COVID-19)'''
    st.sidebar.info(github)

    if item == 'DashBoard':

        keyword = st.text_input('Enter a political keyword', 'bjp')

        # l = tweets_by_date(filter_tweets(keyword))

        # ay = plt.scatter([data['x'] for data in l], [data['y'] for data in l])
        # ay = plt.plot([data['x'] for data in l], [data['y'] for data in l])

        # # autolabel(ay)
        # st.write(mpl_fig=ay)
        # st.pyplot()

        x, y = tweets_class(filter_tweets(keyword))
        ax = plt.bar(y, x)
        autolabel(ax)
        st.write(mpl_fig=ax)
        st.pyplot()
    elif item == 'Induvidual Analyser':
        name=st.text_input('Name','narendramodi')
        getProfile(name)
        

if __name__ == "__main__":
    main()
