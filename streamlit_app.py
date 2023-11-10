import os
import shutil
import pymongo
from pymongo import MongoClient
import streamlit as st
import pickle
from prediction_validation_insertion import pred_validation
from predictFromModel import prediction
import pandas as pd
from application_logging.mongodb_logger import mongodb_logger


def main():
    st.title("Wafer Fault Sensor Prediction App")
    
    st.markdown("""
    ## **Dataset Information : **            
    **This dataset is provided by the client side.**""",True)
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Wafer Fault Sensor Prediction App </h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    
    os.makedirs("raw_data", exist_ok=True)
    st.write("Custom File Predict")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file is not None:
        st.sidebar.write("Uploaded File:", uploaded_file.name)
        file_path = os.path.join("raw_data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        try:
            path = "raw_data"
            pred_valid = pred_validation(path)
            pred_valid.prediction_validation()
            pred=prediction()

            result = pred.predictionfrommodel()

            st.write("Prediction results:")
            st.write(result)
            shutil.rmtree("raw_data")
        except Exception as e:
            shutil.rmtree("raw_data")
            raise e

    st.write("OR")

    if st.button("Default File Predict"):
        try:
            file_path = "default_file"
            pred_valid = pred_validation(file_path)
            pred_valid.prediction_validation()
            pred = prediction()
            result = pred.predictionfrommodel()
            logger = mongodb_logger()
            logger.insert_records_into_collection("wafer", "results", result)
            #print(result)
            st.write("Prediction results:")
            st.json(result)  # Display the result as JSON
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if st.button("About"):
        st.markdown("""**Built with ❤️ by Prakhar**""")
     
if __name__ == '__main__':
    main()
    
    

    
    

