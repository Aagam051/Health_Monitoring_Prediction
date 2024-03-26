import streamlit as st
import requests
import joblib

# Function to fetch data from Blynk
def fetch_blynk_data(auth_token):
    sensor_pins = {
        'Temp': 'v4',
        'Pulse': 'v8',
        'RR': 'v2',
        'Spo2': 'v0'
    }

    fetched_data = {}

    for sensor, pin in sensor_pins.items():
        response = requests.get(f'https://blynk.cloud/external/api/get?token={auth_token}&pin={pin}')
        if response.status_code == 200:
            try:
                data = response.json()
                fetched_data[sensor] = data[0] if isinstance(data, list) else data
            except ValueError:
                fetched_data[sensor] = response.text
                st.error(f"Invalid JSON response for sensor {sensor}: {response.text}")
        else:
            st.error(f"Failed to fetch data for sensor {sensor}: {response.status_code}")

    return fetched_data

# Function to make predictions
def make_predictions(input_test):
    model = joblib.load('model3.pkl')
    predictions = model.predict([input_test])
    return predictions

# Streamlit app
def main():
    st.title("Health Monitoring Prediction")

    auth_token = 'jDkN_S8Pe4y3Zxc5LIok8wRFXRvEBujT'

    if auth_token:
        fetched_data = fetch_blynk_data(auth_token)
        
        if fetched_data:
            st.write("Fetched sensor data:")
            st.write(fetched_data)
            
            temp_data = fetched_data.get('Temp', None)
            pulse_data = fetched_data.get('Pulse', None)
            rr_data = fetched_data.get('RR', None)
            spo2_data = fetched_data.get('Spo2', None)
            
            input_test = [temp_data, pulse_data, rr_data, spo2_data]

            # Define the input sequence
            input_sequence = ['Temp', 'Pulse', 'RR', 'Spo2', 'CVS', 'CNS', 'PA', 'RS', 'SC', 'WL', 'CRY', 'BW', 'GRUNTING', 'Icterus']

            # Fill in remaining features manually
            for feature in input_sequence[4:]:
                value = st.text_input(f"Enter value for {feature}: ")
                input_test.append(value)

            if st.button("Make Predictions"):
                predictions = make_predictions(input_test)
                st.write("Predictions:", predictions)
        else:
            st.warning("No data fetched. Please check your Blynk authentication token.")

if __name__ == "__main__":
    main()
