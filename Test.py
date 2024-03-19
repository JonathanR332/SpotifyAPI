import streamlit as st
import requests
import base64
import pandas as pd
import numpy as np
import datetime
import plotly.express as px



#Setting the up Streamlit app title and heading
st.set_page_config(page_title='Spotify Artist Information', page_icon=':musical_note:')
st.title('Spotify Info Tool') #title can be changed later
st.header('Spotify Artist Information')
current_time = datetime.datetime.now()
st.write(f"Getting Current Data based on: {current_time}")



SPOTIFY_CLIENT_ID = '240acb518fed48a9aaf493ca9bfcee11' #Api Parameters
SPOTIFY_CLIENT_SECRET = '5becdbdc35544bc0822d668d5c9fca66'
AUTH_URL = 'https://accounts.spotify.com/api/token'
SEARCH_URL = 'https://api.spotify.com/v1/search'


search_term = st.text_input('Search for an artist:', '') # artist search term


def get_access_token(client_id, client_secret, auth_url): #Get Spotify API access token
    auth_str = client_id + ':' + client_secret
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()
    headers = {'Authorization': 'Basic ' + b64_auth_str}
    payload = {'grant_type': 'client_credentials'}
    response = requests.post(auth_url, headers=headers, data=payload)
    access_token = response.json()['access_token']
    return access_token

page_color = f""" 
<style>
 [data-testid="stAppViewContainer"] > .main {{
 background-color: #1DB954;}}
 [data-testid="stSidebar"] > div:first-child {{
 background-color: #74DCBE;}}
 [data-testid="stHeader"] {{
 background: rgba(0,0,0,0);
 }}
 </style>
"""
# green for spotify :)
st.markdown(page_color,unsafe_allow_html=True)


if st.button('Search'): 
    if not search_term: #Search function
        st.warning('Please enter an artist name to search.')
    else:
        access_token = get_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, AUTH_URL)
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': search_term, 'type': 'artist', 'market': 'US', 'limit': 10}
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        if response.status_code == 200:
            results = response.json()['artists']['items']
            if not results:
                st.warning('No results found for the given artist name.')
            else:
                for result in results:
                    st.write('Name:', result['name'])
                    st.write('Genres:', ', '.join(result['genres']))
                    st.write('Popularity:', result['popularity'])
                    st.write('Followers:', result['followers']['total'])
                    if result['images']:
                        st.image(result['images'][0]['url'], width=200)
                    if 'canadian hip hop' in result['genres']:
                        df = pd.DataFrame({'lat': [56.1304], 'lon': [-106.3468]}) #display maps to show users where the artist genre / is located from
                        st.map(df)
                    if 'canadian pop' in result['genres']:
                        df = pd.DataFrame({'lat': [56.1304], 'lon': [-106.3468]})
                        st.map(df)
                    if 'cali rap' in result['genres']:
                         df = pd.DataFrame({'lat': [36.7783], 'lon': [-119.4179]})
                         st.map(df)
                    if 'virginia hip hop' in result['genres']:
                        df = pd.DataFrame({'lat': [37.926868], 'lon': [-78.024902]})
                        st.map(df)
                    if 'british folk' in result['genres']:
                        df = pd.DataFrame({'lat': [51.509865], 'lon': [-0.118092]})
                        st.map(df)
                    else:
                        st.warning('No image available.')
        else:
            st.error('Error occurred while fetching data. Please try again later.')


agree = st.checkbox('Subscribe for daily chart updates?') #checkbox function
if agree:
        st.write("We've got you covered!")
        with st.form("Email Form"):
            fullName = st.text_input(label ='Full Name', placeholder="Please enter your full name")
            email = st.text_input(label ='Email Address', placeholder="Please enter your email address")
            submit_res = st.form_submit_button(label="Send")


st.sidebar.title("Radio") #radio buttons allowing users to search for either Artist, Album, or Track
options = ['Artist', 'Album', 'Track']
selected_option = st.sidebar.radio('Select an option to listen to:', options)
st.sidebar.write("You selected:", selected_option)

#spacers so users can breathe and have a certain amount of results
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")



st.header("Top Charts in History")

#loading the csv file
df = pd.read_csv("spotify_top_music.csv")
df = df[['title', 'artist', 'top genre', 'year', 'pop']]
df


st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")



st.text(" ")
st.text(" ")
st.text(" ")
st.text(" ")

st.text("Data Taken from 2018") #used what data i could find 
data = {
    'Artist': [
        'Ed Sheeran', 'Camilla Cabello', 'Post Malone', 'Eminem', 'Maroon5',
        'Sia', 'Daddy Yankee', 'Beyonce', 'J.Balvin', 'Dua Lipa', 'Selena Gomez',
        'Demi Lovato', 'Sam Smith', 'Coldplay', 'Marshmello', 'Luis Fonsi', 'Mariah Carey',
        'Imagine Dragons', 'Justin Bieber', 'Khalid'
    ],
    '2018': [
        53.4, 42.0, 39.6, 38.3, 37.5, 35.6, 35.4, 35.3, 35.3, 35.0, 34.8,
        34.7, 34.5, 34.4, 33.6, 33.6, 33.4, 32.3, 30.8, 30.7
    ]

}

df = pd.DataFrame(data)

st.dataframe(df.head(20))

popularity_options = ["2018"]
popularity_selected = st.selectbox("Select a popularity value", popularity_options)

inform = f"Popularity By Millions Chart:"

fig = px.line(df.head(20), x="Artist", y=popularity_selected, title=inform)

st.plotly_chart(fig, use_container_width=True) #creates a line graph based on the data of most streamed songs


#streamlit run C:\Users\....\....\...\Test.py
