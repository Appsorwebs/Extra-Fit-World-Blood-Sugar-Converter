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


def get_interpretation(value, unit):
    """Return interpretation based on blood sugar value and unit"""
    if unit == "mg/dL":
        if value < 70:
            return "Low blood sugar (Hypoglycemia)", "warning", "#FFA500"
        elif value < 100:
            return "Normal fasting level", "success", "#28a745"
        elif value < 126:
            return "Prediabetes range", "warning", "#FFA500"
        else:
            return "Diabetes range", "error", "#DC3545"
    else:
        if value < 3.9:
            return "Low blood sugar (Hypoglycemia)", "warning", "#FFA500"
        elif value < 5.6:
            return "Normal fasting level", "success", "#28a745"
        elif value < 7.0:
            return "Prediabetes range", "warning", "#FFA500"
        else:
            return "Diabetes range", "error", "#DC3545"


def main():
    st.set_page_config(
        page_title="Extra Fit Blood Sugar Converter",
        page_icon="🩸",
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.session_state.setdefault("theme", "Light")
    st.session_state.setdefault("page", "Converter")

    theme = st.session_state.theme

    light_css = """
    <style>
    .stButton>button {
        background-color: #4a8bed;
        color: white !important;
        border-radius: 10px;
        padding: 10px 24px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3a7bd5;
        color: white !important;
    }
    div.stButton>button p {
        color: white !important;
    }
    </style>
    """

    dark_css = """
    <style>
    html, body, .stApp {
        background-color: #0E1116 !important;
    }
    [data-testid="stMarkdown"], h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #FAFAFA !important;
    }
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input {
        background-color: #262730 !important;
        color: #FAFAFA !important;
        border: 1px solid #4A4A4A !important;
    }
    [data-testid="stSelectbox"] > div > div {
        background-color: #262730 !important;
        color: #FAFAFA !important;
    }
    [data-testid="stSelectbox"] > div > div > div {
        color: #FAFAFA !important;
    }
    .stExpander {
        background-color: #262730 !important;
    }
    .stExpander summary {
        color: #FAFAFA !important;
    }
    div[data-testid="stExpanderContent"] {
        background-color: #1C1C1C !important;
    }
    table {
        color: #FAFAFA !important;
    }
    th, td {
        border-color: #4A4A4A !important;
        color: #FAFAFA !important;
    }
    .stButton>button {
        background-color: #4A8BED !important;
        color: white !important;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #3A7BD5 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1C1C1C !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #FAFAFA !important;
    }
    [data-testid="stSidebar"] label {
        color: #FAFAFA !important;
    }
    </style>
    """

    st.markdown(dark_css if theme == "Dark" else light_css, unsafe_allow_html=True)

    selected = option_menu(
        None,
        ["Converter", "History", "About"],
        icons=["arrow-left-right", "clock-history", "info-circle"],
        default_index=0,
        orientation="horizontal",
    )
    st.session_state.page = selected

    if selected == "Converter":
        converter_page()
    elif selected == "History":
        history_page()
    else:
        about_page()


def converter_page():
    with st.sidebar:
        st.header("Settings")
        theme_choice = st.selectbox(
            "Theme",
            ["Light", "Dark"],
            index=0 if st.session_state.theme == "Light" else 1,
            key="theme_select",
        )
        if theme_choice != st.session_state.theme:
            st.session_state.theme = theme_choice
            st.rerun()

        st.divider()

        st.subheader("Quick Info")
        st.info("""
        **Conversion Formula:**
        - mg/dL → mmol/L: ÷ 18
        - mmol/L → mg/dL: × 18
        """)

    st.title("🩸 Extra Fit Blood Sugar Converter")
    st.markdown("Convert between **mg/dL** and **mmol/L** blood glucose units")

    col1, col2 = st.columns(2)
    with col1:
        from_unit = st.selectbox("From Unit", ["mg/dL", "mmol/L"], key="from_unit")
    with col2:
        to_unit = st.selectbox("To Unit", ["mmol/L", "mg/dL"], key="to_unit")

    value = st.number_input(
        f"Enter blood sugar value in {from_unit}",
        min_value=0.0,
        max_value=1000.0,
        value=100.0,
        step=0.1,
        help="Enter a value between 0 and 1000",
    )

    if st.button("Convert", type="primary"):
        result = convert_blood_sugar(value, from_unit, to_unit)
        st.success(f"## Converted value: {result} {to_unit}")

        st.markdown("### 📊 Interpretation Guide")
        interpretation, status, color = get_interpretation(value, from_unit)

        if status == "warning":
            st.warning(f"⚠️ {interpretation}")
        elif status == "success":
            st.success(f"✅ {interpretation}")
        else:
            st.error(f"🔴 {interpretation}")

        with st.expander("📋 View reference ranges", expanded=True):
            st.markdown(f"""
            | Status | mg/dL | mmol/L |
            |--------|-------|----------|
            | Low (Hypoglycemia) | < 70 | < 3.9 |
            | Normal (Fasting) | 70-99 | 3.9-5.5 |
            | Prediabetes | 100-125 | 5.6-6.9 |
            | Diabetes | ≥ 126 | ≥ 7.0 |
            """)

        save_reading = st.checkbox("Save this reading", value=False)
        if save_reading:
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append(
                {
                    "value": value,
                    "from_unit": from_unit,
                    "result": result,
                    "to_unit": to_unit,
                    "interpretation": interpretation,
                    "timestamp": "Just now",
                }
            )
            st.toast("Reading saved!", icon="💾")


def history_page():
    st.title("📜 Reading History")

    if "history" not in st.session_state or not st.session_state.history:
        st.info(
            "No readings saved yet. Convert a value and check 'Save this reading' to save it here."
        )
        return

    for i, reading in enumerate(reversed(st.session_state.history)):
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 2])
            with col1:
                st.metric("From", f"{reading['value']} {reading['from_unit']}")
            with col2:
                st.metric("To", f"{reading['result']} {reading['to_unit']}")
            with col3:
                st.caption(reading.get("timestamp", ""))
            st.caption(f"**{reading['interpretation']}**")
            st.divider()

    if st.button("Clear History", type="secondary"):
        st.session_state.history = []
        st.rerun()


def about_page():
    st.title("ℹ️ About")

    st.markdown("""
    ### 🩸 EXTRA FIT WORLD MEMBERS BLOOD SUGAR PERSONAL CALCULATOR

    👨‍💻 Developed By  
    Michael Anderson  
    AI Cloud Engineer, Tech Entrepreneur  
    CEO @ Appsorwebs Limited

    🌐 Website: https://appsorwebs.com  
    📧 Email: contact@appsorwebs.com  
    🐙 GitHub: https://github.com/appsorwebs

    ### Blood Sugar Converter
    
    A simple and powerful tool for converting blood glucose levels between the two most common units:
    
    - **mg/dL** - Milligrams per deciliter (used in United States)
    - **mmol/L** - Millimoles per liter (used in UK, Canada, Australia, and most other countries)
    
    ### Conversion Formulas
    
    - mg/dL → mmol/L: `value ÷ 18`
    - mmol/L → mg/dL: `value × 18`
    
    ### Clinical Reference
    
    | glucose-level | mg/dL | mmol/L | Meaning |
    |--------------|-------|--------|---------|
    | Low | < 70 | < 3.9 | Hypoglycemia |
    | Normal | 70-99 | 3.9-5.5 | Normal fasting |
    | Prediabetes | 100-125 | 5.6-6.9 | Pre-diabetes |
    | Diabetes | ≥ 126 | ≥ 7.0 | Diabetes |
    
    ### ⚠️ Important Disclaimer
    
    This tool is for **informational purposes only**. Always consult a healthcare professional for medical advice, diagnosis, or treatment. Do not make medical decisions based solely on this converter.
    """)

    st.caption("🩸 Extra Fit World - Blood Sugar Converter v1.0.0")


if __name__ == "__main__":
    main()
