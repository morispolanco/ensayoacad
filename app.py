import streamlit as st
import json
import requests

def generate_article(topic, length):
    url = "https://proxy.tune.app/text/completions"
    headers = {
        "Authorization": f"sk-tune-{st.secrets['API_KEY']}",
        "Content-Type": "application/json"
    }
    data = {
        "temperature": 0.5,
        "prompt": f"Write an academic article about {topic}. The article should be approximately {length} words long.",
        "model": "meta/llama-3.1-405b-instruct",
        "stream": False,
        "max_tokens": 10000
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['text']

st.title("Academic Article Generator")

topic = st.text_input("Enter the topic for your academic article:")
length = st.slider("Select the approximate length of the article (in words):", 100, 2000, 500)

if st.button("Generate Article"):
    if 'API_KEY' not in st.secrets:
        st.error("API Key not found. Please set up your API_KEY in the Streamlit secrets.")
    else:
        with st.spinner("Generating article..."):
            article = generate_article(topic, length)
        
        st.subheader("Generated Article:")
        st.write(article)
        
        st.download_button(
            label="Download Article",
            data=article,
            file_name="generated_article.txt",
            mime="text/plain"
        )
