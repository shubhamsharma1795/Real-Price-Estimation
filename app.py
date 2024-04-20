import streamlit as st
import numpy as np
import json
import requests
import pickle

# Function to download the JSON file and load it from GitHub
@st.cache
def load_column_data():
    json_url = 'https://raw.githubusercontent.com/shubhamsharma1795/Real-Price-Estimation/main/columns.json'
    response = requests.get(json_url)
    response.raise_for_status()  # Will raise an exception if the download failed
    data = response.json()
    
    columns = data.get('columns', [])
    area_options = data.get('data_columns', [])
    
    if not columns or not area_options:
        raise ValueError("JSON file is missing 'columns' or 'data_columns' keys")
    
    return columns, area_options

# Function to load the pickled model
@st.cache(allow_output_mutation=True)
def load_pickled_model():
    # You need to provide the URL where your pickled model is stored
    model_url = 'https://drive.google.com/uc?id=1OMFIXo38RsVSbCYC8_PEyAEYYdTJq7qt'  # Update this URL
    model_path = 'banglore_home_price_model.pickle'
    response = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(response.content)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# Load your model (assuming URL is provided correctly)
model = load_pickled_model()
columns, area_options = load_column_data()

# Streamlit UI setup
st.title('Bangalore Home Price Prediction')
st.header('Input the details of the house')

# User inputs
area = st.selectbox('Area', area_options)
bathrooms = st.number_input('Number of Bathrooms', min_value=1, max_value=10, value=2)
sqft = st.number_input('Square Feet', min_value=300, max_value=10000, step=100, value=1000)
bedrooms = st.number_input('Bedrooms', min_value=1, max_value=10, value=2)

# Prediction button
if st.button('Predict Price'):
    # Prepare the input features according to the model's requirements
    input_features = np.array([[area, bathrooms, sqft, bedrooms]])  # Ensure correct order and preprocessing if necessary
    prediction = model.predict(input_features)
    predicted_price = prediction[0]
    
    st.success(f'The estimated price of the house is ₹{predicted_price:,.2f}')

# To run this app, save this script as `app.py` and execute `streamlit run app.py` in your terminal
