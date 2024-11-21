# YOUTUBE-DATA-HARVESTING
### USING PYTHON STREAMLIT AND SQL

## Abstract
The objective of this project is to create a Python Streamlit Dashboard 
in which the extraction of Youtube data is done through Google API
and stored in MySQL for further analytical purposes.

## Overview
### Data Harvesting
The Youtube Data can be harvested using Google API with the help of Google API client library and 
displayed as dataframes inthe Streamlit dashboard.

### Data warehousing
The obtained data is then Migrated to the native MySQl database.
It offers simple and seamless data storage and retrieval methods.
Induvidual tables are created for distinct information.

### Data Analysis and Visualisation
The data stored in the SQL db is then appropriately queried to retrieve essential data for analytical purposes.
Plotly graphs are created to visualize the data.


## Primary Packages Used

 ### Streamlit
 This Python library enables us to create a simple dashboard 
 natively without the purposes of HTML or CSS.
 It has variety if methods in its interface to ensure interactive User Experience.

 ### MySql python connector
 Here we use Mysql database to collect and store the extracted data.
 So to connect with the sql server natively, we use the Mysql python connector library.
 This connects to the sql database and enables us to query the DB directly from our codebase.
 
 ## Google API Client 
 To connect with Youtube Database and retrieve necessary data is done through Google's YouTube API.
 This API key can be obtained for free from https://console.cloud.google.com/ .
 It ensures seamless integration and data retrieval.
 The only constraint to be aware of is, a single API key can only perform 10K operations per day.

 ## Plotly
 This library is used to create interactive visualisations with the specified dataframes nativeky in python.
 It has variety of graphs and chart features to portray data and its behaviour.
 Though Matplotlib has higher preferances in terms of visualisation, they provide only static images.
 Hence to create an engaging and clean presentation, plotly is used here.

 ## How to use?
 - Once the streamlit runs, it redirects to the Home page.
 - In the sidebar, click the Data extraxtion and storage
 - Enter the channel id
 - Click VIEW DETAILS to take a look at the obtained data of the respective channel
 - Click MIGRATE TO SQL to store the data in the sql database
 - In the sidebar, click Data Analysis and Visusalisation
 - choose one of the 10 predefined queries to analyse and visualise the data.

   -----------------------------------------------------------------------
   
  



