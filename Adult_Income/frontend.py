import streamlit as st
import requests

API_URL = "http://localhost:8000/predict"

st.title("Adult Income Prediction")
st.markdown("### Enter your details below:")

# User Inputs
age = st.number_input("Age", min_value=17, max_value=100, value=30)

workclass = st.selectbox("Workclass", ['Government', 'Private', 'Unemployed'])

educational_num = st.number_input("Education Number (1–18)", min_value=1, max_value=18, value=13)

marital_status = st.selectbox("Marital Status", ['Divorced', 'Single', 'Married', 'Widow'])

occupation = st.selectbox("Occupation", [
    'Management', 'Professional', 'Services',
    'Manual Labor', 'Protective Services', 'Armed Forces', 'Other'])

relationship = st.selectbox("Relationship", [
    'Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried'])

race = st.selectbox("Race", [
    'White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black'])

gender = st.selectbox("Gender", ['Female', 'Male'])

capital_gain = st.number_input("Capital Gain", min_value=0.0, step=1.0, value=0.0)
capital_loss = st.number_input("Capital Loss", min_value=0.0, step=1.0, value=0.0)

hours_per_week = st.number_input("Hours per Week", min_value=1, max_value=99, value=40)

native_country = st.selectbox("Native Country", ['US', 'Non US'])

# Predict Button
if st.button("Predict Income Category"):
    # Ensure keys exactly match your FastAPI Pydantic model
    input_data = {
        "age": age,
        "workclass": workclass,
        "educational-num": educational_num,
        "marital_status": marital_status,
        "occupation": occupation,
        "relationship": relationship,
        "race": race,
        "gender": gender,
        "capital-gain": capital_gain,
        "capital-loss": capital_loss,
        "hours-per-week": hours_per_week,
        "native-country": native_country
    }

    try:
        response = requests.post(API_URL, json=input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"### Predicted Income Category: **{result['predicted_category']}**")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")
