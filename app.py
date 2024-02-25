from dotenv import load_dotenv
load_dotenv()  # load all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API And get response
def get_gemini_repsonse(input, image, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input, image[0], prompt])
    return response.text

# Function to set up image data
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [{"mime_type": uploaded_file.type, "data": bytes_data}]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="NutriCraft", layout="wide")

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar
st.sidebar.title("Prompt and User Input:")
user_input = st.sidebar.text_input("User Input:")

# Main content
st.title("NutriCraft")
st.subheader("Craft Your Palate")  # Added subheading

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Submit")

# Input prompt explanation
input_prompt = """
You are an expert in nutrition. Analyze the food items from the image and provide information about their nutritional content. 
Include details such as calories, fat content, and any other relevant information.

You can structure the response in any suitable format.
"""

st.subheader("Input Prompt Example:")
st.write(input_prompt)

# If submit button is clicked
if submit:
    try:
        image_data = input_image_setup(uploaded_file)
        response = get_gemini_repsonse(user_input, image_data, input_prompt)
        
        # Save the user input and model response to the conversation history
        st.session_state.conversation_history.append({'user_input': user_input, 'model_response': response})
        
        st.subheader("The Response is")
        
        # Display conversation history
        for entry in st.session_state.conversation_history:
            st.write(f"User: {entry['user_input']}")
            st.write(f"Model: {entry['model_response']}")
            st.write("---")

    except FileNotFoundError as e:
        st.error(str(e))
