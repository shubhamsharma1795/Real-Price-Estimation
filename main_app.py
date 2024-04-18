import streamlit as st
from flask import Flask, render_template, request, jsonify
import pickle
import json
import threading

# Load the trained model from the pickle file
with open('banglore_home_price_model.pickle', 'rb') as f:
    model = pickle.load(f)

# Load column information from the JSON file
with open('columns.json', 'r') as f:
    column_info = json.load(f)

# Get the feature names from the JSON file
feature_names = column_info['data_columns']

# Create a Streamlit app
def run_streamlit_app():
    st.title('Bangalore Room Price Prediction')

    # Input fields for the user
    bhks = st.number_input('Enter number of bedrooms (bhks):', min_value=0, step=1, value=1)
    bathrooms = st.number_input('Enter number of bathrooms:', min_value=0, step=1, value=1)

    # Create a dictionary of the user input
    input_data = {
        'bhks': bhks,
        'bathrooms': bathrooms,
    }

    # Convert input_data to a list based on the feature names
    input_list = [input_data.get(feature) for feature in feature_names if feature in input_data]

    # Make a prediction based on the user input
    if st.button('Predict Price'):
        prediction = model.predict([input_list])
        st.write(f'Predicted Price: ₹{prediction[0]:,.2f}')

# Create a Flask app
app = Flask(__name__)

@app.route('/')
def index():
    # Render the homepage of your Flask app
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.get_json()

    # Extract features from the data
    bhks = data.get('bhks')
    bathrooms = data.get('bathrooms')

    # Convert input data to a list based on the feature names
    input_list = [bhks, bathrooms]

    # Make a prediction based on the input data
    prediction = model.predict([input_list])
    
    # Return the prediction as a JSON response
    return jsonify({'predicted_price': prediction[0]})

# Define the main function
def main():
    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=lambda: app.run(debug=True, port=5000))
    flask_thread.start()

    # Run the Streamlit app
    run_streamlit_app()

if __name__ == '__main__':
    main()
