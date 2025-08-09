import streamlit as st
import base64
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment
load_dotenv()

# Page config
st.set_page_config(
    page_title="SpiderBot 🕸️",
    layout="centered",
)

# Helper to load image and encode to base64
def get_base64_image(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Encode avatar image
avatar_base64 = get_base64_image("spiderman-icon.jpeg")

# Custom CSS with transparent overlay but keeping 'contain'
st.markdown(f"""
    <style>
    html, body, .stApp {{
        background: 
            linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)),  /* Dark transparent overlay */
            url("data:image/png;base64,{get_base64_image('spiderman-bg.jpg')}") no-repeat center center fixed;
        background-size: contain;
        background-color: #000000;
    }}

        .header-text {{
        font-family: 'Comic Sans MS', cursive;
        font-size: 40px;
        font-weight: bold;
        margin-top: 10px;
        color: #ffffff; /* White text */
        text-shadow: 2px 2px 4px #000000; /* Black shadow */
    }}

    .avatar-img {{
        border-radius: 50%;
        width: 90px;
        height: 90px;
        object-fit: cover;
    }}

    .stTextInput > label {{
        font-weight: bold;
        color: white;
    }}

    .chatbox {{
        font-size: 18px;
        color: white;
        padding: 15px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        margin-top: 20px;
        border: 2px solid #e60000;
    }}
    </style>
""", unsafe_allow_html=True)

# Avatar + Title layout
col1, col2 = st.columns([1, 4])

with col1:
    st.markdown(f"<img src='data:image/jpeg;base64,{avatar_base64}' class='avatar-img'>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='header-text'>🕸️Web of Knowledge🕷️</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# Ask prompt
st.markdown("<div style='margin-top: 4px;'></div>", unsafe_allow_html=True)
st.markdown("<p style='color:white; font-weight:bold;'>Ask anything SpiderBot 🧠:</p>", unsafe_allow_html=True)
question = st.text_input(label="", placeholder="Type your question here...")

# LLM setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.3,
)

# Prompt + Chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are SpiderBot, a helpful and honest AI with the wit of Spider-Man."),
    ("human", "Question: {question}")
])
output_parser = StrOutputParser()
chain = prompt | llm | output_parser

# Generate response
if question:
    with st.spinner("🕸️Swinging into action..."):
        try:
            response = chain.invoke({"question": question})
            st.markdown(f"<div class='chatbox'><b>🕷️ SpiderBot says:</b><br>{response}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Oops! Something went wrong:")
            st.exception(e)
