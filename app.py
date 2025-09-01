from dotenv import load_dotenv

load_dotenv() ## load all the environment variables from .env file

import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function to load Gemini 2.5 Flash model
model=genai.GenerativeModel("gemini-2.5-flash")

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        ## Read the file into bytes
        image_bytes=uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, # Get the mime type of the uploaded file
                "data": image_bytes
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
##Intializing the streamlit app

st.set_page_config(page_title="Multi Language Invoice Extractor",page_icon=":robot_face:")

st.header("Multi Language Invoice Extractor")
input=st.text_input("Input prompt: ", key="import")
uploaded_file=st.file_uploader("Upload an invoice",type=["pdf","png","jpeg","jpg"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption='Uploaded Invoice.', use_container_width='stretch')


submit=st.button("Tell me about this invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload an image as invoice and you will have to answer any questions based on the uploaded invoice image.
"""

## If submit button is pressed
if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input,image_data,input_prompt)
    st.subheader("The Response is: ")
    st.write(response)

