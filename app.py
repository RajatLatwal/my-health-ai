from dotenv import load_dotenv
import os
import streamlit as st
import pandas as pd
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the Gemini model
model = genai.GenerativeModel("gemini-2.5-pro")

# ---------------- Sidebar: BMI Calculator ----------------
st.sidebar.subheader("⚖️ BMI Calculator")

weight = st.sidebar.text_input("Weight (kg):")
height = st.sidebar.text_input("Height (cm):")

try:
    weight_num = pd.to_numeric(weight)
    height_num = pd.to_numeric(height)
    if weight_num > 0 and height_num > 0:
        bmi = weight_num / ((height_num / 100) ** 2)
        st.sidebar.markdown(f"**Your BMI is:** `{bmi:.2f}`")
    else:
        st.sidebar.info("Please enter valid positive numbers.")
except:
    st.sidebar.info("Enter numerical values to calculate BMI.")

st.sidebar.markdown("""
**BMI Categories:**
- 🟦 Underweight: BMI < 18.5  
- 🟩 Normal weight: 18.5 ≤ BMI < 25  
- 🟨 Overweight: 25 ≤ BMI < 30  
- 🟥 Obese: BMI ≥ 30
""")

# ---------------- Main Content ----------------
st.set_page_config(page_title="MyHealthify", layout="centered")
st.header(":green[MyHealthify]–Your Health & Fitness Guide 💊", divider="red")

user_input = st.text_input("Ask me anything about Health, Diseases, or Fitness:")

# Gemini Response Function
def guide_me_on(query):
    if not query.strip():
        return "⚠️ Please enter a health-related question."

    system_prompt = (
        "You are a certified Dietician, Health Coach, and Fitness Expert. "
        "Respond to health, disease, and fitness-related questions with empathy and clarity. "
        "If a query is outside the health domain, reply: "
        "'❌ I am a Healthcare Expert and can only answer questions related to Health, Fitness, and Diet.' "
        "If someone asks about medicines, say: "
        "'❌ I am an AI model and cannot recommend medication or provide diagnosis. Please consult a doctor.'\n\n"
    )

    full_prompt = system_prompt + query
    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating response: {e}"

# Button to submit query
if st.button("Submit"):
    answer = guide_me_on(user_input)
    st.subheader(":blue[Response:]")
    st.markdown(answer)
