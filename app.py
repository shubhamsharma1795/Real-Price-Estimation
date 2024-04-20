import streamlit as st
import numpy as np
import json
import gdown
import pickle

# Function to download the JSON file
@st.cache
def load_column_data():
    json_url = 'https://drive.google.com/uc?id=1QUYGRnLQdd2v5B6TfQbIOJLGuRZuQpzS'
    json_path = 'columns.json'
    gdown.download(json_url, json_path, quiet=False)
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data['columns'], data['data_columns']

# Function to load the pickled model
@st.cache(allow_output_mutation=True)
def load_pickled_model():
    model_url = 'https://drive.google.com/uc?id=1OMFIXo38RsVSbCYC8_PEyAEYYdTJq7qt'
    model_path = 'bangalore_home_price_model.pickle'
    gdown.download(model_url, model_path, quiet=False)
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

model = load_pickled_model()
columns, area_options = load_column_data()

# Streamlit UI setup
st.title('Bangalore Home Price Prediction')
st.header('Input the details of the house')

# User inputs
area = st.selectbox('Area', area_options)  # Dynamic area options from JSON
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
