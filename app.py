import streamlit as st
import tensorflow as tf
import numpy as np
import json
import gdown

# URLs for your model and JSON file
json_url = 'https://drive.google.com/uc?id=1QUYGRnLQdd2v5B6TfQbIOJLGuRZuQpzS'
model_url = 'https://drive.google.com/uc?id=1OMFIXo38RsVSbCYC8_PEyAEYYdTJq7qt'

# Function to download model and JSON
@st.cache(allow_output_mutation=True)
def download_files():
    # Paths where files will be saved
    json_path = 'columns.json'
    model_path = 'bangalore_home_price_model.pickle'
    
    # Downloading files
    gdown.download(json_url, json_path, quiet=False)
    gdown.download(model_url, model_path, quiet=False)
    
    # Loading model and JSON
    model = tf.keras.models.load_model(model_path)
    with open(json_path, 'r') as file:
        data = json.load(file)
    
    return model, data['columns'], data['data_columns']

model, columns, area_options = download_files()

# Streamlit UI code (as above, including input fields and prediction button)
