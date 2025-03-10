import streamlit as st
import re
import random
import string
import pyperclip  # For copying to clipboard
from datetime import datetime, timedelta

# Custom CSS for modern dark-light theme and responsive design
def inject_custom_css():
    st.markdown("""
    <style>
    /* Global styles for modern light theme */
    body {
        background-color: #f4f4f9 !important;
        color: #2d2d2d !important;
        font-family: 'Arial', sans-serif !important;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background-color: #ffffff !important;
        color: #333333 !important;
        border-right: 1px solid #e0e0e0 !important;
    }

    /* Input box styling */
    .stTextInput input {
        background-color: #ffffff !important;
        color: #333333 !important;
        border: 2px solid #6c757d !important;
        border-radius: 5px !important;
        padding: 8px !important;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus {
        border: 2px solid #007bff !important;
    }

    /* Button styling */
    .stButton button {
        background-color: #007bff !important;
        color: #ffffff !important;
        border-radius: 5px !important;
        border: none !important;
        padding: 12px 20px !important;
        font-weight: bold !important;
        cursor: pointer !important;
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #0056b3 !important;
    }

    /* Checkbox styling */
    .stCheckbox label {
        color: #333333 !important;
        cursor: pointer !important;
    }

    /* Progress bar styling */
    .stProgress > div > div > div {
        background-color: #28a745 !important;
    }

    /* Footer styling */
    .css-1q1n0ol {
        background-color: #f4f4f9 !important;
        color: #2d2d2d !important;
        padding: 10px !important;
        border-top: 1px solid #e0e0e0 !important;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .css-18e3th9 {
            padding: 1rem !important;
        }
        .stButton button {
            font-size: 14px !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)

# List of common passwords to blacklist
COMMON_PASSWORDS = ["password", "123456", "qwerty", "admin", "letmein", "welcome", "password123"]

# Function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")

    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")

    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")

    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")

    # Blacklist Check
    if password.lower() in COMMON_PASSWORDS:
        score = 0
        feedback.append("❌ Password is too common and easily guessable.")

    # Strength Rating
    if score == 4:
        feedback.append("✅ Strong Password!")
    elif score == 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")

    return score, feedback

# Function to generate a strong password
def generate_strong_password(length=12, use_uppercase=True, use_digits=True, use_special_chars=True):
    """Generate a strong password with customizable complexity."""
    characters = string.ascii_lowercase
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# Function to display password strength visually
def display_strength_meter(score):
    if score == 4:
        st.success("Strong Password")
    elif score == 3:
        st.warning("Moderate Password")
    else:
        st.error("Weak Password")

# Main Streamlit App
def main():
    # Inject custom CSS
    inject_custom_css()

    # Sidebar
    st.sidebar.title("🔐 Password Strength Meter")
    st.sidebar.markdown(""" 
    ### How to Use:
    1. Enter your password in the input box.
    2. Click **Check Strength** to evaluate your password.
    3. Use the **Generate Password** option to create a strong password.
    4. Copy the generated password to your clipboard.
    """)

    # Password Generator Settings in Sidebar
    st.sidebar.subheader("Password Generator Settings")
    password_length = st.sidebar.slider("Password Length", min_value=8, max_value=20, value=12)
    use_uppercase = st.sidebar.checkbox("Include Uppercase Letters", value=True)
    use_digits = st.sidebar.checkbox("Include Digits", value=True)
    use_special_chars = st.sidebar.checkbox("Include Special Characters", value=True)

    # Toggle to generate password
    generate_password = st.sidebar.checkbox("Generate a Password", value=False)

    # Main Layout
    st.title("🔐 Password Strength Meter")
    st.write("Evaluate and improve your password security.")

    # Conditional password input or generated password
    password = ""
    if not generate_password:
        # Show regular password input (password or visible based on toggle)
        password_visibility = st.checkbox("Show Password", value=False)
        if password_visibility:
            password = st.text_input("Enter your password:", type="default", key="visible_password")
        else:
            password = st.text_input("Enter your password:", type="password", key="hidden_password")
    else:
        # Generate and display a strong password
        password = generate_strong_password(
            length=password_length,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special_chars=use_special_chars
        )
        st.text_input("Generated Password:", value=password, disabled=True, key="generated_password")
        if st.button("Copy to Clipboard"):
            try:
                pyperclip.copy(password)
                st.success("✅ Password copied to clipboard!")
            except Exception as e:
                st.error("❌ Failed to copy to clipboard. Please install pyperclip using `pip install pyperclip`.")

    # Check Password Strength Button
    if st.button("Check Strength"):
        if not password:
            st.warning("Please enter a password or generate one.")
        else:
            score, feedback = check_password_strength(password)
            display_strength_meter(score)
            st.progress(score / 4)  # Progress bar for strength
            for message in feedback:
                st.markdown(f"- {message}")

    # Password Expiry Suggestion
    if password:
        expiry_days = 90  # Suggest changing password every 90 days
        expiry_date = datetime.now().date() + timedelta(days=expiry_days)
        st.info(f"💡 Consider changing your password by {expiry_date} for better security.")

# Run the app
if __name__ == "__main__":
    main()