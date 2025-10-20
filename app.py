import streamlit as st
import requests
from datetime import datetime

# --- Title ---
st.title("🚕 TaxiFareModel Frontend")

st.markdown("""
## Welcome!

Use this app to get a **taxi fare prediction** using the model API.

Fill in the ride details below 👇
""")

# --- User Inputs ---
st.header("Ride details")

# ✅ تصحيح إدخال التاريخ والوقت
pickup_date = st.date_input("📅 Pickup date", datetime.now().date())
pickup_time = st.time_input("⏰ Pickup time", datetime.now().time())
pickup_datetime = datetime.combine(pickup_date, pickup_time)

pickup_longitude = st.number_input("📍 Pickup longitude", value=-73.985428)
pickup_latitude = st.number_input("📍 Pickup latitude", value=40.748817)
dropoff_longitude = st.number_input("🏁 Dropoff longitude", value=-73.985428)
dropoff_latitude = st.number_input("🏁 Dropoff latitude", value=40.758896)
passenger_count = st.number_input("👥 Number of passengers", min_value=1, max_value=8, value=1)

# --- API URL ---
st.markdown("### API URL")
url = st.text_input("Enter your API endpoint", "https://taxifare.lewagon.ai/predict")

# --- Button ---
if st.button("💰 Get Fare Prediction"):
    # Build parameters dictionary
    params = {
        "pickup_datetime": pickup_datetime.strftime("%Y-%m-%d %H:%M:%S"),
        "pickup_longitude": pickup_longitude,
        "pickup_latitude": pickup_latitude,
        "dropoff_longitude": dropoff_longitude,
        "dropoff_latitude": dropoff_latitude,
        "passenger_count": int(passenger_count)
    }

    # Display parameters
    st.json(params)

    # --- API Call ---
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise error if not 200
        prediction = response.json()

        st.write("### 🔍 Raw API Response:")
        st.json(prediction)

        # ✅ معالجة المفاتيح المحتملة للـ prediction
        fare = (
            prediction.get("fare_amount") or
            prediction.get("fare") or
            prediction.get("prediction") or
            prediction.get("result")
        )

        if fare is not None:
            st.success(f"💵 Predicted fare: ${float(fare):.2f}")
        else:
            st.warning("⚠️ API response doesn't contain a 'fare_amount' key.")
            st.info("Check your API response structure.")

    except Exception as e:
        st.error(f"❌ Error calling API: {e}")
        st.info("Check your API URL or input values.")

# --- Footer ---
st.markdown("""
---
Made with love ❤️
👩‍💻 Author: Renad 🥰
""")
