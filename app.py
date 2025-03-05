import streamlit as st
from pint import UnitRegistry
from currency_converter import CurrencyConverter

# Initialize unit registry
ureg = UnitRegistry()
currency_converter = CurrencyConverter()

# Define unit categories and units
unit_categories = {
    "Length": ["meter", "centimeter", "kilometer", "mile", "inch", "foot", "yard"],
    "Mass": ["gram", "kilogram", "pound", "ounce", "ton"],
    "Speed": ["meter per second", "kilometer per hour", "mile per hour"],
    "Temperature": ["celsius", "fahrenheit", "kelvin"],
    "Time": ["second", "minute", "hour", "day"],
    "Currency": ["USD", "EUR", "GBP", "INR", "PKR", "CAD"]
}

def convert_units(category, value, from_unit, to_unit):
    try:
        if category == "Currency":
            try:
                return currency_converter.convert(value, from_unit, to_unit)
            except Exception:
                st.error("Error converting currency. Please check your internet connection.")
                return None
        elif category == "Temperature":
            if from_unit == "celsius" and to_unit == "fahrenheit":
                return (value * 9/5) + 32
            elif from_unit == "fahrenheit" and to_unit == "celsius":
                return (value - 32) * 5/9
            elif from_unit == "celsius" and to_unit == "kelvin":
                return value + 273.15
            elif from_unit == "kelvin" and to_unit == "celsius":
                return value - 273.15
        else:
            return (value * ureg(from_unit)).to(to_unit).magnitude
    except Exception as e:
        st.error(f"Error converting units: {str(e)}")
        return None

# Streamlit UI
st.title("🔄 Universal Unit Converter")
st.write("Convert between various units like length, mass, speed, temperature, time, and currency.")

# Unit category selection
category = st.selectbox("Select a category:", options=list(unit_categories.keys()))

# Unit selection and input
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    from_unit = st.selectbox("From:", options=unit_categories[category], key="from_unit")
with col2:
    value = st.number_input("Value", value=1.0, key="value")
with col3:
    to_unit = st.selectbox("To:", options=unit_categories[category], key="to_unit")

# Convert button
if st.button("Convert"):
    result = convert_units(category, value, from_unit, to_unit)
    if result is not None:
        st.success(f"{value} {from_unit} = {result:.4f} {to_unit}")
