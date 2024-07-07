import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Load the pre-trained model
pipe = pickle.load(open("pipe.pkl", "rb"))

# List of teams and cities
teams = [
    'Australia', 'India', 'Bangladesh', 'New Zealand', 'South Africa', 
    'England', 'West Indies', 'Afghanistan', 'Pakistan', 'Sri Lanka'
]

cities = [
    'Colombo', 'Mirpur', 'Johannesburg', 'Dubai', 'Auckland', 'Cape Town', 
    'London', 'Pallekele', 'Barbados', 'Sydney', 'Melbourne', 'Durban', 
    'St Lucia', 'Wellington', 'Lauderhill', 'Hamilton', 'Centurion', 
    'Manchester', 'Abu Dhabi', 'Mumbai', 'Nottingham', 'Southampton', 
    'Mount Maunganui', 'Chittagong', 'Kolkata', 'Lahore', 'Delhi', 'Nagpur', 
    'Chandigarh', 'Adelaide', 'Bangalore', 'St Kitts', 'Cardiff', 
    'Christchurch', 'Trinidad'
]

# Streamlit app title
st.title("Cricket Score Predictor")

# Creating columns for input fields
col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team', options=["Select batting team"] + sorted(teams), index=0)

with col2:
    bowling_team = st.selectbox('Select bowling team', options=["Select bowling team"] + sorted(teams), index=0)

# Select city
city = st.selectbox('Select city', options=["Select city"] + sorted(cities), index=0)

# Creating more columns for additional input fields
col3, col4, col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current Score', min_value=0, value=0)

with col4:
    overs = st.number_input('Overs done (works for over > 5)', min_value=0, max_value=20, value=0)

with col5:
    wickets = st.number_input('Wickets out', min_value=0, max_value=10, value=0)

# Input for runs scored in the last 5 overs
last_five = st.number_input('Runs scored in last 5 overs', min_value=0, value=0)

# Predict button
if st.button('Predict Score'):
    if batting_team == "Select batting team":
        st.error("Please select a batting team.")
    elif bowling_team == "Select bowling team":
        st.error("Please select a bowling team.")
    elif city == "Select city":
        st.error("Please select a city.")
    elif overs <= 5:
        st.error("Please enter overs greater than 5.")
    else:
        balls_left = 120 - (overs * 6)
        wickets_left = 10 - wickets
        crr = current_score / overs

        input_df = pd.DataFrame(
            {
                'batting_team': [batting_team], 
                'bowling_team': [bowling_team], 
                'city': [city], 
                'current_score': [current_score], 
                'balls_left': [balls_left], 
                'wickets_left': [wickets_left], 
                'crr': [crr], 
                'last_five': [last_five]
            }
        )

        result = pipe.predict(input_df)
        st.header("Predicted Score - " + str(int(result[0])))
