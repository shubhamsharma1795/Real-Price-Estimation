import streamlit as st
import pandas as pd
import pickle
import json

# Load the trained model
model = pickle.load(open('banglore_home_price_model.pickle', 'rb'))

# Load the column names for input
try:
    with open('columns.json', 'r') as f:
        columns = json.load(f)
except FileNotFoundError:
    st.error("Error: 'columns.json' file not found.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: Unable to parse 'columns.json' file. Make sure it's correctly formatted.")
    st.stop()

# Function to predict price
def predict_price(bhk):
    # Create a dictionary with dummy values for features used during training
    input_data = {
        '1st Block Jayanagar': 0,
        '1st Phase JP Nagar': 0,
        '2nd Phase Judicial Layout': 0,
        '2nd Stage Nagarbhavi': 0,
        # Add more features as needed
        'bhk': bhk
    }
    input_df = pd.DataFrame([input_data])
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

# Predict price on button click
if st.button('Predict Price'):
    price = predict_price(bhk)
    st.success('Predicted Price: ₹{:.2f}'.format(price))
