import streamlit as st
import pandas as pd
import datetime
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

# Initialize geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Custom styling for dark mode
st.markdown(
    """
    <style>
    .reportview-container {
        background: #1e1e2f;
    }
    .main .block-container {
        background: #27293d;
        color: #c3c3c3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# HTML5 Geolocation
st.write(
    """
    <script>
    navigator.geolocation.getCurrentPosition(
        function(position) {
            document.getElementById('latitude').textContent = position.coords.latitude;
            document.getElementById('longitude').textContent = position.coords.longitude;
        }
    );
    </script>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("Expense Tracker")

# Sidebar
st.sidebar.header("Input Your Expense Details Here")

# Date and Time
date = st.sidebar.date_input(
    "Date", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2023, 12, 31)
)
time = st.sidebar.time_input("Time", datetime.time(8, 45))

# Expense Category
expense_category = st.sidebar.selectbox(
    "Expense Category",
    ["Food", "Transportation", "Entertainment", "Utilities", "Others"],
)

# Sub-Category
sub_category = st.sidebar.text_input("Sub-Category")

# Payment Method
payment_method = st.sidebar.selectbox(
    "Payment Method", ["Cash", "Credit Card", "Debit Card", "Mobile Payment"]
)

# Transaction Type
transaction_type = st.sidebar.radio("Transaction Type", ["One-time", "Recurring"])

# Vendor
vendor = st.sidebar.text_input("Vendor")

# Location using Google Maps
location_name = st.sidebar.text_input(
    "Location Name", ""
)  # Text input for location name

if location_name:
    location = geolocator.geocode(location_name)
else:
    lat = st.sidebar.text_input("Latitude", "")
    lon = st.sidebar.text_input("Longitude", "")
    location = (
        [float(lat), float(lon)] if lat and lon else [40.7128, -74.0060]
    )  # Default to New York

if location:
    if isinstance(location, list):
        m = folium.Map(location=location, zoom_start=12)
    else:
        m = folium.Map(location=[location.latitude, location.longitude], zoom_start=12)
else:
    m = folium.Map(
        location=[40.7128, -74.0060], zoom_start=12
    )  # Default to New York if location not found

location_coordinates = st.sidebar.empty()  # Placeholder for coordinates
folium_static(m)

# Currency
currency = st.sidebar.selectbox("Currency", ["USD", "EUR", "JPY", "GBP", "Others"])

# Exchange Rate
exchange_rate = st.sidebar.number_input(
    "Exchange Rate (Optional)", min_value=0.0, max_value=1000.0, step=0.01, value=1.0
)

# Notes
notes = st.sidebar.text_area("Notes")

# Submit Button
if st.sidebar.button("Submit"):
    # Create or load CSV
    try:
        df = pd.read_csv("expenses.csv")
    except FileNotFoundError:
        df = pd.DataFrame(
            columns=[
                "Date",
                "Time",
                "Expense Category",
                "Sub-Category",
                "Payment Method",
                "Transaction Type",
                "Vendor",
                "Location Coordinates",
                "Currency",
                "Exchange Rate",
                "Notes",
            ]
        )

    # Append new expense
    new_expense = {
        "Date": date,
        "Time": time,
        "Expense Category": expense_category,
        "Sub-Category": sub_category,
        "Payment Method": payment_method,
        "Transaction Type": transaction_type,
        "Vendor": vendor,
        "Location Coordinates": f"{location[0] if isinstance(location, list) else location.latitude}, {location[1] if isinstance(location, list) else location.longitude}",
        "Currency": currency,
        "Exchange Rate": exchange_rate,
        "Notes": notes,
    }
    df = df.append(new_expense, ignore_index=True)

    # Save to CSV
    df.to_csv("expenses.csv", index=False)
    st.success("Expense added successfully!")

# Display Data
if st.checkbox("Show Data"):
    try:
        df = pd.read_csv("expenses.csv")
        st.write(df)
    except FileNotFoundError:
        st.write("No data to display.")
