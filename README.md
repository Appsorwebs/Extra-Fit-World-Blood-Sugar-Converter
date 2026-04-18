# Extra Fit Blood Sugar Converter

A powerful and colorful Streamlit web application for converting blood sugar levels between milligrams per deciliter (mg/dL) and millimoles per liter (mmol/L). Built with love for the Extra Fit World community.

## ✨ Features

- **Bidirectional Conversion** - Convert from mg/dL to mmol/L and vice versa
- **Interpretation Guide** - Understand your readings with clinical accuracy
- **Theme Toggle** - Light and Dark mode support
- **Reading History** - Save and track your readings
- **Reference Tables** - Clinical ranges for all glucose levels
- **Responsive Design** - Works on desktop and mobile
- **Accessibility** - Screen reader friendly

## 🚀 Quick Start

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run blood_sugar_converter.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Clinical Reference

| Status | mg/dL | mmol/L |
|--------|-------|----------|
| Low (Hypoglycemia) | < 70 | < 3.9 |
| Normal (Fasting) | 70-99 | 3.9-5.5 |
| Prediabetes | 100-125 | 5.6-6.9 |
| Diabetes | ≥ 126 | ≥ 7.0 |

## 🧪 Testing

Run the conversion tests:

```bash
python -m pytest tests/
```

Or manually:

```bash
python -c "
from blood_sugar_converter import convert_blood_sugar, get_interpretation

# Test conversions
assert convert_blood_sugar(100, 'mg/dL', 'mmol/L') == 5.6
assert convert_blood_sugar(5.5, 'mmol/L', 'mg/dL') == 99

# Test interpretations
assert 'Low' in get_interpretation(50, 'mg/dL')[0]
assert 'Normal' in get_interpretation(85, 'mg/dL')[0]
assert 'Prediabetes' in get_interpretation(110, 'mg/dL')[0]
assert 'Diabetes' in get_interpretation(130, 'mg/dL')[0]

print('All tests passed!')
"
```

## 📁 Project Structure

```
.
├── blood_sugar_converter.py  # Main application
├── requirements.txt          # Python dependencies
├── README.md               # This file
├── .gitignore             # Git ignore rules
└── tests/                # Test files
    └── test_converter.py
```

## 🔧 Configuration

### Streamlit Config

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true

[theme]
primaryColor = "#4a8bed"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
```

## ⚠️ Disclaimer

This tool is for informational purposes only. Always consult a healthcare professional for medical advice, diagnosis, or treatment.

## 📄 License

MIT License - See LICENSE file for details.

## 👨‍💻 Developed By

**Michael Anderson**
AI Cloud Engineer, Tech Entrepreneur
CEO @ [Appsorwebs Limited](https://appsorwebs.com)

- 🌐 Website: https://appsorwebs.com
- 📧 Email: contact@appsorwebs.com
- 🐙 GitHub: https://github.com/appsorwebs

---

🩸 Part of the **Extra Fit World** health and fitness community