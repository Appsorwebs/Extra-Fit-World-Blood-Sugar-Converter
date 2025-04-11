import streamlit as st
from streamlit_option_menu import option_menu

def convert_blood_sugar(value, from_unit, to_unit):
    """Convert blood sugar between mg/dL and mmol/L"""
    if from_unit == to_unit:
        return value
    
    if from_unit == "mg/dL" and to_unit == "mmol/L":
        return round(value / 18, 1)
    elif from_unit == "mmol/L" and to_unit == "mg/dL":
        return round(value * 18)
    return value

def main():
    # Set page config
    st.set_page_config(
        page_title="Extra Fit Blood Sugar Converter",
        page_icon="🩸",
        layout="centered"
    )
    
    # Custom CSS for colorful UI
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    [data-testid="stHeader"] {
        background-color: #4a8bed;
        color: white;
    }
    .stButton>button {
        background-color: #4a8bed;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #3a7bd5;
        color: white;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #4a8bed;
        color: white;
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Dark/light mode toggle using Streamlit's theme API
    theme = st.selectbox("🌙 Theme", ["Light", "Dark"])
    if theme == "Dark":
        st.markdown("""
        <style>
        .stNumberInput>div>div>input,
        .stTextInput>div>div>input,
        .stSelectbox>div>div>select {
            color: white !important;
            background-color: #333333 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Set theme config
        st._config.set_option("theme.backgroundColor", "#1a1a1a")
        st._config.set_option("theme.secondaryBackgroundColor", "#333333")
        st._config.set_option("theme.textColor", "white")
    
    # App title and description
    st.title("🩸 Extra Fit Blood Sugar Converter")
    st.markdown("Convert between mg/dL and mmol/L blood glucose units")
    
    # Unit selection
    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From Unit", ["mg/dL", "mmol/L"], key="from_unit")
    with col2:
        to_unit = st.selectbox("To Unit", ["mmol/L", "mg/dL"], key="to_unit")
    
    # Value input
    value = st.number_input(
        f"Enter blood sugar value in {from_unit}",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        step=0.1
    )
    
    # Convert button
    if st.button("Convert"):
        result = convert_blood_sugar(value, from_unit, to_unit)
        st.success(f"Converted value: {result} {to_unit}")
        
        # Colorful interpretation guide
        st.markdown("### Interpretation Guide")
        if from_unit == "mg/dL":
            if value < 70:
                st.warning("Low blood sugar (Hypoglycemia)")
            elif 70 <= value < 100:
                st.success("Normal fasting level")
            elif 100 <= value < 126:
                st.warning("Prediabetes range")
            else:
                st.error("Diabetes range")
        else:  # mmol/L
            if value < 3.9:
                st.warning("Low blood sugar (Hypoglycemia)")
            elif 3.9 <= value < 5.6:
                st.success("Normal fasting level")
            elif 5.6 <= value < 7.0:
                st.warning("Prediabetes range")
            else:
                st.error("Diabetes range")
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed by <a href="https://appsorwebs.com" target="_blank" style="color:white;">Appsorwebs.com</a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
