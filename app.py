import streamlit as st
import pickle
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

# Load model and vectorizer
model = pickle.load(open("Notebook/phishing_model.pkl", "rb"))
vectorizer = pickle.load(open("Notebook/vectorizer.pkl", "rb"))

# Text cleaning function
def clean_text(text):
    text = re.sub(r'[^a-zA-Z]', ' ', str(text))
    text = text.lower()

    words = [
        word for word in text.split()
        if word not in ENGLISH_STOP_WORDS
    ]

    return " ".join(words)

# Page settings
st.set_page_config(
    page_title="SMS Phishing Detector",
    page_icon="🛡️",
    layout="centered"
)

# Title
st.title("🛡️ SMS Phishing Detection System")
st.write("Detect whether an SMS message is legitimate or phishing/spam.")

# Input box
message = st.text_area(
    "Enter SMS Message",
    height=150,
    placeholder="Paste your SMS here..."
)

# Analyze button
if st.button("Analyze Message"):

    if not message.strip():
        st.warning("Please enter a message.")
    else:

        cleaned_message = clean_text(message)

        message_vector = vectorizer.transform([cleaned_message])

        prediction = model.predict(message_vector)

        probability = model.predict_proba(message_vector)

        spam_probability = probability[0][1] * 100
        ham_probability = probability[0][0] * 100

        st.subheader("Analysis Result")

        if prediction[0] == 1:
            st.error("🚨 Spam / Phishing Message Detected")
        else:
            st.success("✅ Legitimate Message")

        st.write(f"**Spam Probability:** {spam_probability:.2f}%")
        st.write(f"**Safe Probability:** {ham_probability:.2f}%")

        if spam_probability >= 90:
            st.error("Risk Level: Very High")
        elif spam_probability >= 70:
            st.warning("Risk Level: High")
        elif spam_probability >= 40:
            st.info("Risk Level: Medium")
        else:
            st.success("Risk Level: Low")