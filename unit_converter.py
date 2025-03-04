# Import necessary libraries
import streamlit as st  # For creating the web app
from datetime import datetime  # For timestamping conversions
import math  # For mathematical operations


st.markdown(
    """
    <style>
    div[data-baseweb="select"] > div {
        transition: all 0.3s ease-in-out;
    }
    div[data-baseweb="select"]:hover > div {
        transform: scale(1.02);
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        right: 10px;
        font-size: 14px;
        color: gray;
    }
    </style>
    <div class="footer">
        Developed by <b>Syed Ali Kazim Shah</b>
    </div>
    """,
    unsafe_allow_html=True
)



# Dictionary containing conversion factors for different categories
CONVERSION_FACTORS = {
    "Area": {
        "Square Millimeters": 1e-6,
        "Square Centimeters": 1e-4,
        "Square Meters": 1,
        "Hectares": 10000,
        "Square Kilometers": 1e6,
        "Square Inches": 0.00064516,
        "Square Feet": 0.092903,
        "Square Yards": 0.836127,
        "Acres": 4046.86,
        "Square Miles": 2.59e6
    },
    "Data Transfer Rate": {
        "Bits per Second": 1,
        "Kilobits per Second": 1e3,
        "Megabits per Second": 1e6,
        "Gigabits per Second": 1e9,
        "Terabits per Second": 1e12,
        "Bytes per Second": 1/8,
        "Kilobytes per Second": 1e3 / 8,
        "Megabytes per Second": 1e6 / 8,
        "Gigabytes per Second": 1e9 / 8,
        "Terabytes per Second": 1e12 / 8
    },
    "Digital Storage": {
        "Bits": 1,
        "Bytes": 8,
        "Kilobits": 1e3,
        "Kilobytes": 8e3,
        "Megabits": 1e6,
        "Megabytes": 8e6,
        "Gigabits": 1e9,
        "Gigabytes": 8e9,
        "Terabits": 1e12,
        "Terabytes": 8e12,
        "Petabytes": 8e15
    },
    "Energy": {
        "Joules": 1,
        "Kilojoules": 1e3,
        "Calories": 4.184,
        "Kilocalories": 4184,
        "Watt-hours": 3600,
        "Kilowatt-hours": 3.6e6,
        "BTU": 1055.06,
        "Electronvolts": 1.60218e-19
    },
    "Frequency": {
        "Hertz": 1,
        "Kilohertz": 1e3,
        "Megahertz": 1e6,
        "Gigahertz": 1e9
    },
    "Fuel Economy": {
        "Liters per 100 Kilometers": 1,
        "Miles per Gallon (US)": lambda x: 235.215 / x,
        "Miles per Gallon (UK)": lambda x: 282.481 / x
    },
    "Length": {
        "Millimeters": 0.001,
        "Centimeters": 0.01,
        "Meters": 1,
        "Kilometers": 1000,
        "Inches": 0.0254,
        "Feet": 0.3048,
        "Yards": 0.9144,
        "Miles": 1609.34,
        "Nautical Miles": 1852
    },
    "Mass": {
        "Grams": 1,
        "Kilograms": 1000,
        "Pounds": 453.592,
        "Ounces": 28.3495,
        "Tons (Metric)": 1e6
    },
    "Plane Angle": {
        "Degrees": 1,
        "Radians": math.pi / 180,
        "Gradians": 0.9
    },
    "Pressure": {
        "Pascals": 1,
        "Kilopascals": 1000,
        "Bars": 1e5,
        "Atmospheres": 101325,
        "Pounds per Square Inch": 6894.76
    },
    "Speed": {
        "Meters per Second": 1,
        "Kilometers per Hour": 1 / 3.6,
        "Miles per Hour": 1 / 2.237,
        "Feet per Second": 0.3048,
        "Knots": 1.852 / 3.6
    },
    "Temperature": "custom", 
    "Time": {
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400,
        "Weeks": 604800,
        "Months": 2.628e6,
        "Years": 3.154e7
    },
    "Volume": {
        "Milliliters": 0.001,
        "Liters": 1,
        "Cubic Meters": 1000,
        "Teaspoons": 0.004929,
        "Tablespoons": 0.014787,
        "Cups": 0.24,
        "Pints": 0.473176,
        "Quarts": 0.946353,
        "Gallons": 3.78541,
        "Cubic Inches": 0.016387,
        "Cubic Feet": 28.3168
    }
}

# Function to handle temperature conversions
def convert_temperature(value, from_unit, to_unit):
    # Dictionary of conversion formulas for temperature
    conversions = {
        ("Celsius", "Fahrenheit"): lambda x: (x * 9/5) + 32,
        ("Fahrenheit", "Celsius"): lambda x: (x - 32) * 5/9,
        ("Celsius", "Kelvin"): lambda x: x + 273.15,
        ("Kelvin", "Celsius"): lambda x: x - 273.15,
        ("Fahrenheit", "Kelvin"): lambda x: (x - 32) * 5/9 + 273.15,
        ("Kelvin", "Fahrenheit"): lambda x: (x - 273.15) * 9/5 + 32,
    }
    # Get the conversion formula based on the from_unit and to_unit
    return conversions.get((from_unit, to_unit), lambda x: x)(value)

# Function to handle general conversions
def convert(value, from_unit, to_unit, category):
    # Special case for temperature
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    # Special case for fuel economy
    if category == "Fuel Economy":
        return CONVERSION_FACTORS[category][to_unit](value)
    
    # Get the conversion factors for the from_unit and to_unit
    factor_from = CONVERSION_FACTORS[category].get(from_unit, 1)
    factor_to = CONVERSION_FACTORS[category].get(to_unit, 1)
    
    # Perform the conversion
    return value * (factor_from / factor_to)

# Main function to run the Streamlit app
def main():
    st.title("Unit Converter")
    
    # Dropdown to select the category of conversion
    categories = list(CONVERSION_FACTORS.keys())
    category = st.selectbox("Select Category", categories)
    
    # Dropdowns to select the units to convert from and to
    units = list(CONVERSION_FACTORS[category].keys())
    from_unit = st.selectbox("From", units)
    to_unit = st.selectbox("To", units)
    
    # Input field for the value to convert
    value = st.number_input("Enter Value", min_value=0.0, format="%.6f")

    # Initialize session state for result and history
    if "result" not in st.session_state:
        st.session_state.result = None
        st.session_state.result_text = ""

   
    if st.button("Convert"):
        result = convert(value, from_unit, to_unit, category)
        st.session_state.result = result
        st.session_state.result_text = f"{value} {from_unit} = {result:.6f} {to_unit}"

        st.subheader("Result")
        st.write(st.session_state.result_text)
        
        # Initialize history if it doesn't exist
        if "history" not in st.session_state:
            st.session_state.history = []
        # Add the conversion to the history
        st.session_state.history.append(
            f"{datetime.now().strftime('%H:%M:%S')} - {value} {from_unit} -→ {result:.6f} {to_unit}"
        )


    # Conversion history
    if "history" in st.session_state:
        st.subheader("Conversion History")
        for entry in st.session_state.history[-5:]:  # Show the last 5 entries
            st.text(entry)


if __name__ == "__main__":
    main()