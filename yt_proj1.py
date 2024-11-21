#Youtube Data Harvesting using Python and SQL
#AUTHOR: Ameen Abdullah S

import googleapiclient.discovery
import pandas as pd
import mysql.connector
import re
import streamlit as st
# import matplotlib.pyplot as plt
import plotly.express as px


from streamlit_option_menu import option_menu

#establishing connection with youtube Api
api_service_name = "youtube"
api_version = "v3"
api_Key="AIzaSyAHm_8PPT8nQSmcieO-CiF4OLuNSgvVYXU"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_Key)

#Establishing Connection With MySql Database

from mysql import connector
connection = connector.connect(
    host='localhost',
    user='root',
    password='mysql@716'
)
cursor=connection.cursor()

#creating a dedicated DB for Youtube data
cursor.execute('create database if not exists youtube')
cursor.execute('use youtube')


#Function to fetch channel data
def fetch_channel_data(channel_id):
    channel_data=[]
    chan_request = youtube.channels().list(
    part="snippet,contentDetails,statistics",
    id=channel_id)
    chan_response = chan_request.execute()

    for i in chan_response['items']:
        c_data= dict(
            channel_name=i['snippet']['title'],
            channel_id=i["id"],
            channel_description=i['snippet']['description'],
            channel_thumbnail=i['snippet']['thumbnails']['default']['url'],
            channel_playlist_id=i['contentDetails']['relatedPlaylists']['uploads'],
            channel_subscribers=i['statistics']['subscriberCount'],
            channel_video_count=i['statistics']['videoCount'],
            channel_views=i['statistics']['viewCount'],
            channel_publishedAt=i['snippet']['publishedAt'].replace("T"," ").replace("Z"," "))
        channel_data.append(c_data) 
    return channel_data 


#Function to fetch video Id
def fetch_video_id(channel_id):
    video_ids=[]
    try:
        request=youtube.channels().list(part="contentDetails",id=channel_id)
        response=request.execute()
        playlist_id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        next_page_token=None
        while True:
            request_videoid=youtube.playlistItems().list(part="contentDetails,snippet",playlistId= playlist_id,maxResults=50,pageToken=next_page_token)
            response_videoid=request_videoid.execute()
            for i in range(len(response_videoid['items'])):
                video_ids.append(response_videoid['items'][i]['snippet']['resourceId']['videoId'])
                next_page_token=response_videoid.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return video_ids

def time_dur_convert(duration):
    match = re.match(r'^PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?$', duration)
    if not match:
        return None

    hours = int(match.group(1)) if match.group(1) else 00
    minutes = int(match.group(2)) if match.group(2) else 00
    seconds = int(match.group(3)) if match.group(3) else 00

    return (f'{hours}:{minutes}:{seconds}')


def fetch_video_data(video_ids):
    video_data=[]
    try:
        for video_id in video_ids:
            vid_request= youtube.videos().list(part="snippet,contentDetails,statistics",id=video_id)
            vid_response=vid_request.execute()

            for i in vid_response['items']:
                    v_data=dict(
                            channel_id=i['snippet']['channelId'],
                            channel_name=i['snippet']['channelTitle'],
                            video_id=i['id'],
                            video_name=i['snippet']['title'],
                            video_description=i['snippet']['description'],
                            thumbnail=i['snippet']['thumbnails']['default']['url'],
                            video_publishedAt=i['snippet']['publishedAt'].replace("T"," ").replace("Z"," "),
                            video_duration=time_dur_convert(i['contentDetails']['duration']),
                            view_count=i['statistics']['viewCount'],
                            like_count=i['statistics'].get('likeCount'),
                            favorite_count=i['statistics'].get('favoriteCount'),
                            comment_count=i['statistics']['commentCount'],
                            caption_status=i['contentDetails']['caption'] 
                            )
                    video_data.append(v_data)

    except:
        pass
    return  video_data
           
#Function to fetch comment data
def fetch_comment_data(video_ids):
    comments_data=[]
    try:
        for video_id in video_ids:
            cmt_request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100)
            cmt_response = cmt_request.execute()

            for i in cmt_response['items']:
                com_data=dict(
                            video_id=i['snippet']['videoId'],
                            comment_id=i['snippet']['topLevelComment']['id'],
                            comment_text=i['snippet']['topLevelComment']['snippet']['textDisplay'],
                            comment_author=i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            comment_publishedAt=i['snippet']['topLevelComment']['snippet']['publishedAt'].replace("T"," ").replace("Z"," ")) #replace to convert UCT format to normal
                comments_data.append(com_data)
    except:
        st.error("No comments posted (or) Comment Section Has been disabled for some videos")
    return comments_data

#function to fetch playlist details

def fetch_playlist_data(channel_id):
    playlist_data=[]
    next_page_token=None
    try:
        while True:
            pl_request = youtube.playlists().list(
                        part="snippet,contentDetails",
                        channelId=channel_id,
                        maxResults=50
                    )
            pl_response = pl_request.execute()
        
            for i in pl_response['items']:
                data=dict(
                    channel_id=i['snippet']['channelId'],
                    channel_name=i['snippet']['channelTitle'],
                    playlist_id=i['id'],
                    playlist_name=i['snippet']['title'],
                    playlist_publishedAt=i['snippet']['publishedAt'].replace("T"," ").replace("Z"," "),
                    videos_count=i['contentDetails']['itemCount'])
                playlist_data.append(data)
                nextPageToken=pl_response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return playlist_data


#Creating StreamLit web page

st.set_page_config(page_title="Youtube Data Harvesting",
                    layout='wide',
                    initial_sidebar_state='expanded'
                )

with st.sidebar:
    choice =option_menu("Main Menu",
                        ["Home","Data Extraction And Storage","Data Analysis And Visualisation"],
                        icons=["house","upload","bar-chart"],
                        menu_icon="menu-up",
                       orientation="vertical")
    
#if the user chooses Home Page, the following data will be displayed.
if choice=='Home':
    st.title(":cyclone: :red[YouTube] Data Harvesting")
    st.header("Using :blue[Python Streamlit] and :blue[MySql]")
    st.subheader(":dart: :blue[Objective]")
    st.markdown("To create a Streamlit application that allows users to access and analyze data from multiple YouTube channels. ")    
    st.subheader(":male-technologist: :blue[Approach]")
    st.markdown(":pushpin: Building a Dashboard using :orange[Streamlit]")
    st.markdown(":pushpin: Data Extraction from Youtube through :orange[Google's Api]")           
    st.markdown(":pushpin: Data warehousing using :orange[MySql]")
    st.markdown(":pushpin: Data Analysis And Visualisation")

#if the user selects Data extraction and storage, the following script will run
if choice=='Data Extraction And Storage':
    st.title(":cloud: :blue[Data Extraction And Storage]")
    st.markdown(":pushpin: Enter the :blue[channel ID] in the Text Box")
    st.markdown(":pushpin: Click on :blue[Display Channel Data] to view the details")
    st.markdown(":pushpin: Click on :blue[Migrate Data to MySQL] to upload the channel data to MySQL DataBase")
    with st.expander("But..How to get the youtube channel ID?? :scream:"):
        st.write(":white_check_mark: Go to any YT channel's Home page")
        st.write(":white_check_mark: Click the :blue['more'] button below the channel description")
        st.write(":white_check_mark: Click :blue[Share channel] and choose :blue['copy channel ID]'")

    C_ID = st.text_input("**Enter the channel ID :**")

    if st.button("View details"): # Shows the channel information from Youtube
        with st.spinner('Loading...Please Wait for a moment...'):
            try:
                st.subheader(':blue[CHANNEL DETAILS]')
                c_details = fetch_channel_data(channel_id=C_ID)
                st.write(':blue[Channel Name] :', c_details[0]['channel_name'])
                st.write(':blue[Description] :', c_details[0]['channel_description'])
                st.write(':blue[Subscribers] :', c_details[0]['channel_subscribers'])
                st.write(':blue[Overall Views Count] :', c_details[0]['channel_views'])

                p_details=fetch_playlist_data(channel_id=C_ID)
                v_details=fetch_video_data(video_ids=fetch_video_id(channel_id=C_ID))
                com_details=fetch_comment_data(video_ids=fetch_video_id(channel_id=C_ID))

                st.subheader('DATAFRAMES:-')
                st.write(':blue[Channel Data]')
                st.dataframe(c_details)
                st.write(':blue[Playlist Data]')
                st.dataframe(p_details)
                st.write(':blue[Video Data]')
                st.dataframe(v_details)
                st.write(':blue[Comments Data]')
                st.dataframe(com_details)
            except:
                 st.error("Invalid Channel ID or Insufficient API Requests.")
    
    if st.button("Migrate Data to MySQL"):

        with st.spinner("Migration Initiated...Please dont quit or close the page."):
            
            try:
                #Query to Create Channel table
                cursor.execute('''create table if not exists Channel(
                               channel_name VARCHAR(100),
                               channel_id VARCHAR(50) PRIMARY KEY,
                               channel_description LONGTEXT,
                               channel_playlist_id VARCHAR(50), 
                               channel_subscribers BIGINT,
                               channel_video_count BIGINT,
                               channel_views BIGINT,
                               channel_publishedAt TIMESTAMP
                               )''')
                #Query to create Playlist Table
                cursor.execute('''create table if not exists Playlist(
                               playlist_id VARCHAR(50) PRIMARY KEY,
                               playlist_name VARCHAR(100),
                               channel_id VARCHAR(50),
                               channel_name VARCHAR(100),
                               videos_count BIGINT,
                               playlist_publishedAt TIMESTAMP
                               )''')
                #Query to create Video Table
                cursor.execute('''create table if not exists Video(
                               video_id VARCHAR(50) PRIMARY KEY,
                               video_name VARCHAR(255),
                               channel_id VARCHAR(50),
                               channel_name VARCHAR(100),
                               video_description LONGTEXT,
                               thumbnail VARCHAR(255),
                               video_publishedAt TIMESTAMP,
                               video_duration TIME,
                               view_count BIGINT,
                               like_count BIGINT,
                               favorite_count BIGINT,
                               comment_count BIGINT,
                               caption_status VARCHAR(20)
                               )''')
                #query to create comment table
                cursor.execute('''create table if not exists Comments(
                               video_id VARCHAR(50),
                               comment_id VARCHAR(50),
                               comment_text LONGTEXT,
                               comment_author VARCHAR(100),
                               comment_publishedAt TIMESTAMP
                               )''')
                
                #the obtained data is now transformed to pandas dataframe for ease of access while inserting into sql tables AND for visualisation
            
                # df_channel=pd.DataFrame(c_details,index=[0]) #Data frame for channel data
                # df_video=pd.DataFrame(v_details)
                # df_playlist=pd.DataFrame(p_details) #Data frame for playlist datails) #Data frame for video data
                # df_comments=pd.DataFrame(com_details)
                
                df_channel=pd.DataFrame(fetch_channel_data(channel_id=C_ID))
                df_video=pd.DataFrame(fetch_video_data(video_ids= fetch_video_id(channel_id=C_ID)))
                df_playlist=pd.DataFrame(fetch_playlist_data(channel_id=C_ID))
                df_comments=pd.DataFrame(fetch_comment_data(video_ids=fetch_video_id(channel_id=C_ID)))
                
                
                #Uploading the data frames into Sql by executing insert queries

                #Migrating channel data
                for col,row in df_channel.iterrows():
                    channel_query='''insert into Channel(channel_name, channel_id,channel_description,channel_playlist_id,
                                channel_subscribers,channel_video_count,channel_views,channel_publishedAt)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
                    values1=(row['channel_name'],row['channel_id'],row['channel_description'],row['channel_playlist_id'],row['channel_subscribers'],row['channel_video_count'],row['channel_views'],row['channel_publishedAt'])
                    cursor.execute(channel_query,values1)
                connection.commit()
                

                #Migrating Playlist data
                # cursor=connection.cursor() 
                for col,row in df_playlist.iterrows():
                    playlist_query='''insert into Playlist(playlist_id,playlist_name,channel_id,channel_name,
                                videos_count,playlist_publishedAt)
                                VALUES(%s,%s,%s,%s,%s,%s)'''
                    values2=(row['playlist_id'],row['playlist_name'],row['channel_id'],row['channel_name'],row['videos_count'],row['playlist_publishedAt'])
                    cursor.execute(playlist_query,values2)
                connection.commit()
                
                #migrating video data
                for col,row in df_video.iterrows():
                    video_query='''insert into Video(video_id,video_name,channel_id,channel_name,video_description,
                                thumbnail,video_publishedAt,video_duration,view_count,like_count,favorite_count,comment_count,caption_status)
                                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
                    values3=(row['video_id'],row['video_name'],row['channel_id'],row['channel_name'],row['video_description'],row['thumbnail'],row['video_publishedAt'],row['video_duration'],row['view_count'],row['like_count'],row['favorite_count'],row['comment_count'],row['caption_status'])
                    cursor.execute(video_query,values3)
                connection.commit()
                
                #migrating comments data
                for col,row in df_comments.iterrows():
                    comment_query='''insert into Comments(video_id,comment_id,comment_text,comment_author,comment_publishedAt)
                                    VALUES(%s,%s,%s,%s,%s)'''
                    values4=(row['video_id'],row['comment_id'],row['comment_text'],row['comment_author'],row['comment_publishedAt'])
                    cursor.execute(comment_query,values4)
                connection.commit()

                st.success("Data Successfully Migrated")
            except:
                  st.error("An error occured")
                  st.caption("Avoid Migrating duplicates (re-uploading data) OR Try again after some time.")

    #if the user chooses data analysis and visualisation, the following script will get executed
if choice=='Data Analysis And Visualisation':
        st.header(':chart_with_upwards_trend::blue[Data Analysis And Visualisation]')
        st.subheader(':orange[Select a query to analyse the data]')

        Queries = ['Choose any one from below',
        '1.What are the names of all the videos and their corresponding channels?',
        '2.Which channels have the most number of videos, and how many videos do they have?',
        '3.What are the top 10 most viewed videos and their respective channels?',
        '4.How many comments were made on each video, and what are their corresponding video names?',
        '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
        '6.What is the total number of likes for each video, and what are their corresponding video names?',
        '7.What is the total number of views for each channel, and what are their corresponding channel names?',
        '8.What are the names of all the channels that have published videos in the year 2022?',
        '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
        '10.Which videos have the highest number of comments, and what are their corresponding channel names?']


        q_choice=st.selectbox(' ',options=Queries)
        #query 1
        if q_choice==Queries[1]:
            cursor.execute('select video_name,channel_name from Video order by channel_name')
            out=cursor.fetchall()
            q1=pd.DataFrame(out,columns=['Video Name','Channel Name'])
            st.dataframe(q1)
        #query 2
        if q_choice==Queries[2]:
            cursor.execute(''' select distinct channel_name, count(video_id) from Video group by channel_name order by count(video_id)  desc''')
            out=cursor.fetchall()
            q2=pd.DataFrame(out,columns=['Channel Name','Video Count'])
            st.dataframe(q2)
            st.text(" ")
            st.subheader(":blue[Visualisation]")
            st.text(" ")
            st.markdown(':green[HIGHEST VIDEO COUNT]')
            st.text(" ")
            st.bar_chart(q2,x='Channel Name',y='Video Count',horizontal=True,color='Channel Name',height=250)
        #query 3
        if q_choice==Queries[3]:
            cursor.execute(''' select channel_name, video_name, view_count from Video
                                order by view_count desc''')
            out=cursor.fetchall()
            q3=pd.DataFrame(out,columns=['Channel Name','Video Name','Views'])
            st.dataframe(q3)
            st.text(" ")
            st.subheader(":blue[Visualisation]")
            st.text(" ")
            st.markdown(':green[HIGHEST VIEW COUNT]')
            st.text(" ")
            st.bar_chart(q3,x='Channel Name',y='Views',color='Channel Name',height=500,horizontal=False)
        #query 4
        if q_choice==Queries[4]:
            cursor.execute('select video_name, comment_count from Video order by comment_count desc')
            out=cursor.fetchall()
            q4=pd.DataFrame(out,columns=['Video Name','Comment Count'])
            st.dataframe(q4)
        #query 5
        if q_choice==Queries[5]:
            cursor.execute('''select video_name, like_count, channel_name  from Video
                                    order by like_count desc limit 100''')
            out=cursor.fetchall()
            q5=pd.DataFrame(out,columns=['Video Name','Likes','Channel Name'])
            st.dataframe(q5)
            st.text(" ")
            st.subheader(":blue[Visualisation]")
            st.text(" ")
            st.markdown(':green[HIGHEST LIKE COUNT]')
            st.bar_chart(q5,x='Channel Name',y='Likes',horizontal=True,height=250,color='Channel Name')
        #query 6
        if q_choice==Queries[6]:
            cursor.execute('select video_name,like_count from Video order by like_count desc')
            out=cursor.fetchall()
            q6=pd.DataFrame(out,columns=['Video Name','Like Count'])
            st.dataframe(q6)
        #query 7
        if q_choice==Queries[7]:
            cursor.execute('select channel_name, channel_views as total_views from Channel order by channel_views desc')
            out=cursor.fetchall()
            q7=pd.DataFrame(out,columns=['Channel Name','Total Views'])
            st.dataframe(q7)
            st.text('')
            st.subheader(":blue[Visualisation]")
            st.text('')
            st.markdown(':green[Highest Channel View Count]')
            st.text('')
            st.bar_chart(q7,x='Channel Name',y='Total Views',horizontal=True,color='Channel Name',height=250)
        #query 8
        if q_choice==Queries[8]:
            cursor.execute('select channel_name,video_name,video_publishedAt from video where video_publishedAt like "2022%"')
            out=cursor.fetchall()
            q8=pd.DataFrame(out,columns=['Channel Name','Video Name','Published At'])
            st.dataframe(q8)

        #query 9
        if q_choice==Queries[9]:
            cursor.execute('''select  channel_name, time_format(sec_to_time(avg(time_to_sec(time(video_duration)))),"%H:%i:%s") as Duration
                           from Video group by channel_name''')
            out=cursor.fetchall()
            q9=pd.DataFrame(out,columns=['Channel Name','Duration'])
            st.dataframe(q9)
            st.text('')
            st.subheader(":blue[Visualisation]")
            st.text('')
            st.markdown('Average Duration of Videos')
            st.text('')
            st.bar_chart(q9,x='Channel Name',y='Duration',horizontal=False,color='Channel Name',height=500)
        #query 10
        if q_choice==Queries[10]:
            cursor.execute('''select video_name,comment_count,channel_name from Video
                                    order by comment_count desc''')
            out=cursor.fetchall()
            q10=pd.DataFrame(out,columns=['Video Name','Comment Count','Channel Name'])
            st.dataframe(q10)
            st.text('')
            st.subheader(":blue[Visualisation]")
            st.text('')
            st.markdown('Highest Comments')
            st.text('')
            st.bar_chart(q10,x='Channel Name',y='Comment Count',horizontal=False,color='Channel Name',height=500)
            

        #End of source code