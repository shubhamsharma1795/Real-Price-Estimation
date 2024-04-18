import streamlit as st
import pandas as pd
import pickle
import json

# Load the trained model
model = pickle.load(open('banglore_home_prices_model.pickle', 'rb'))

# Load the column names for input
try:
    with open('columns(1).json', 'r') as f:
        columns = json.load(f)
except FileNotFoundError:
    st.error("Error: 'columns.json' file not found.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: Unable to parse 'columns.json' file. Make sure it's correctly formatted.")
    st.stop()

# Function to predict price
def predict_price(bhk, bathroom):
    input_data = [[bhk, bathroom]]
    input_df = pd.DataFrame(input_data, columns=['bhk', 'bathroom'])
    print("Input DataFrame:", input_df)  # Print input DataFrame for debugging
    prediction = model.predict(input_df)
    return prediction[0]

# Set background image
st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80%27") center;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and input fields
st.title('Bangalore Room Price Prediction')
bhk = st.number_input('Number of Bedrooms (BHK)', min_value=1, max_value=10, value=1, step=1)
bathroom = st.number_input('Number of Bathrooms', min_value=1, max_value=10, value=1, step=1)

# Predict price on button click
if st.button('Predict Price'):
    price = predict_price(bhk, bathroom)
    st.success('Predicted Price: ₹{:.2f}'.format(price))
