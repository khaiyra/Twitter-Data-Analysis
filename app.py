import os
import sys
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from wordcloud import WordCloud
import seaborn as sns
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join('sql')))
from add_data import db_execute_fetch

st.set_page_config(page_title="Twitter Data Analysis & Visualization", layout="wide")

def text_category(p):
    if p > 0:
        return 'positive'
    elif p < 0:
        return 'negative'
    else:
        return 'neutral'         
                               
def wordCloud(df):
    cleanText = ''
    for text in df['clean_text']:
        tokens = str(text).lower().split()

        cleanText += " ".join(tokens) + " "

    wc = WordCloud(width=650, height=450, background_color='white', min_font_size=5).generate(cleanText)
    st.title("Tweet Text Word Cloud")
    st.image(wc.to_array())
    return cleanText

# main
def main():
    st.title("Twitter Data Analysis & Visualization")
    st.subheader("_khaiyra")
    query = "select * from TweetInformation"
    df = db_execute_fetch(query, dbName="tweets", rdf=True)
    df['score'] = df['polarity'].apply(text_category)
    
    # Insert Check-Box to show the snippet of the data.
    if st.checkbox('Show Data Snippet'):
        st.write(df.head()) # print the first 5 rows of the data
        st.subheader('Data Summary')
        st.write('Shape of the dataframe: ',df.shape) # print the shape of the data
        st.write('Data decription: \n',df.describe())
        
        location = st.multiselect("choose Location of tweets", list(df['place'].unique()))
        if location:
            df = df[np.isin(df, location).any(axis=1)]
            st.write(df)
   
    # Visualization Section
    choose_viz = st.sidebar.selectbox("Choose Visualization",
        ["None","Top tweet locations", "Top twittler handles", "Sentiment chart", "Polarity graph", "Wordcloud"])
    
    st.title("Data Visualization")
    if(choose_viz == "Top tweet locations"):
        fig = px.bar(df.place.value_counts().head(5))
        st.plotly_chart(fig)
    elif(choose_viz == "Top twittler handles"):
        fig = px.bar(df['original_author'].value_counts().head(10))
        st.plotly_chart(fig)
    elif(choose_viz == "Sentiment chart"):
        fig = px.bar(df['score'])
        st.plotly_chart(fig)
    elif(choose_viz == "Polarity graph"):
        fig, ax = plt.subplots()
        ax.hist(df["polarity"], bins=20)
        st.plt(fig)
    elif(choose_viz == "Wordcloud"):
        wordCloud(df)
        
if __name__ == "__main__":
    main()