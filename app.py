import streamlit as st 
import pickle
import pandas as pd

# Set the page configuration for a more immersive experience
st.set_page_config(page_title="IPL SATTABAAZAAR", layout="wide")

# Center the title by using HTML and adjust the font size by changing header levels
st.markdown("<h1 style='text-align: center;'>🏏 IPL SATTABAAZAAR</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>🎉 Predict the Winning Probability of Your Favorite IPL Team!</h3>", unsafe_allow_html=True)

# Define the teams and cities
teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore', 
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Capitals'
]

cities = [
    'Hyderabad', 'Bangalore', 'Mumbai', 'Indore', 'Kolkata', 'Delhi', 'Chandigarh', 
    'Jaipur', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban', 'Centurion', 
    'East London', 'Johannesburg', 'Kimberley', 'Bloemfontein', 'Ahmedabad', 
    'Cuttack', 'Nagpur', 'Dharamsala', 'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 
    'Abu Dhabi', 'Sharjah', 'Mohali', 'Bengaluru'
]

# Load the model
with open('pipe.pkl', 'rb') as file:
    pipe = pickle.load(file)

# Team selection with sidebar
st.sidebar.markdown("#### ⚔️ Team Selection")
batting_team = st.sidebar.selectbox("Select the Batting Team", sorted(teams), key='batting_team')
bowling_team = st.sidebar.selectbox("Select the Bowling Team", sorted(teams), key='bowling_team')

# Hosting city
st.sidebar.markdown("#### 🏟️ Match Details")
selected_cities = st.sidebar.selectbox('Select the Hosting City', cities, key='city')

# Target score input
target_score = st.sidebar.number_input('Enter Target Score', min_value=0, step=1, key='target_score')

# Display current match situation inputs with metrics
st.markdown("#### 📊 Current Match Situation")

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input('Current Score', min_value=0, step=1, key='current_score')
    st.metric("Runs Scored", score, delta=None)
with col4:
    overs = st.number_input('Overs Completed', min_value=0.0, max_value=20.0, step=0.1, key='overs_completed')
    st.metric("Overs", overs, delta=None)
with col5:
    wickets = st.number_input('Wickets Fallen', min_value=0, max_value=10, step=1, key='wickets_fallen')
    st.metric("Wickets Left", 10 - wickets, delta=None)

# Prediction button with animation
if st.button('🎯 Predict Probability'):
    runs_to_chase = target_score - score
    balls_remaining = 120 - (overs * 6)
    wickets_left = 10 - wickets
    current_run_rate = score / overs if overs != 0 else 0
    required_run_rate = (runs_to_chase * 6) / balls_remaining if balls_remaining != 0 else 0

    input_df = pd.DataFrame({
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [selected_cities],
        'runs_to_chase': [runs_to_chase],
        'balls_remaining': [balls_remaining],
        'wickets_left': [wickets_left],
        'target_score': [target_score],
        'current_run_rate': [current_run_rate],
        'required_run_rate': [required_run_rate]
    })

    # Show spinner during prediction
    with st.spinner('Calculating...'):
        result = pipe.predict_proba(input_df)
        loss = result[0][0]
        win = result[0][1]

    # Display results with progress bars and emojis
    st.markdown("#### 🎈 Prediction Results")
    st.success(f"🏆 {batting_team} Winning Probability: **{round(win * 100, 2)}%**")
    st.progress(win)
    st.error(f"⚔️ {bowling_team} Winning Probability: **{round(loss * 100, 2)}%**")
    st.progress(loss)

    # Visual separator
    st.markdown("---")

    # Fun encouragement messages
    if win > loss:
        st.balloons()
        st.markdown("🎉 **Great chance for the batting team!** Keep cheering! 🥳")
    else:
        st.markdown("⚠️ **Bowling team has the upper hand!** Time for a strategic comeback! 💪")
