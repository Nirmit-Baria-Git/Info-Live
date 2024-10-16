import streamlit as st
import pyttsx3
from GoogleNews import GoogleNews
import speech_recognition as sr
import requests
from PIL import Image

# Setting up voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 175)

# Function to set female voice
def set_female_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

set_female_voice()

# Defining speak function for speaking the introduction
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Error: {e}")

# Defining listening function for listening to input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)  # Increased duration
        st.write("Listening... Please speak now.")
        
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)  # Increased timeout and phrase time limit
            st.write("Recognizing...")
            query = recognizer.recognize_google_cloud(audio, language='en-IN')
            st.write("Query:", query)
            return query.lower()
        except sr.WaitTimeoutError:
            st.error("Listening timed out. Please try again.")
            return ""
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand that. Please try again.")
            return ""
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return ""

def tell_news(news_type, news_list):
    st.write(f"{news_type} Headlines are as follows:")
    for news_item in news_list:
        headline = news_item['title']
        if headline:
            st.write(headline)

def fetch_news(news_type, search_query):
    google_news = GoogleNews(lang='en', region='IN')
    google_news.search(search_query)
    news_list = google_news.results()
    tell_news(news_type, news_list[:2])
    google_news.clear()

def main():
    st.title("Info-Live | AI News Reader")
    st.write("Welcome to InfoLive")
    
    lhs_image_url = "https://i.ibb.co/5LJrqkj/home-left.png"
    rhs_image_url = "https://i.ibb.co/fxTXQqS/home-right.png"
    lhs_image = Image.open(requests.get(lhs_image_url, stream=True).raw).resize((200, 600))
    rhs_image = Image.open(requests.get(rhs_image_url, stream=True).raw).resize((200, 600))
    
    col1, col2 = st.columns(2)
    col1.image(lhs_image)
    col2.image(rhs_image)
    
    if st.button("Start Listening to News"):
        speak("Welcome to InfoLive! Would you like to hear International, National, or Sports news? Or should I give you a general update?")
        response = listen()
        
        if "international" in response:
            fetch_news("International News", "World News")
        elif "national" in response:
            fetch_news("National News", "National News India")
        elif "sports" in response:
            fetch_news("Sports News", "Sports News")
        else:
            fetch_news("International News", "World News")
            fetch_news("National News", "National News India")
            fetch_news("Sports News", "Sports News")
            
    if st.button("Return to Home"):
        st.experimental_rerun()

if __name__ == "__main__":
    main()