import streamlit as st
import pyttsx3
from GoogleNews import GoogleNews
import speech_recognition as sr
import joblib
from joblib import Memory
from PIL import Image
import base64

# Set up caching
memory = Memory(location='news_cache', verbose=0)

# Set up voice engine
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

# Define speak function for speaking the introduction
def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Error:", e)

# Define listening function for listening to input
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            recognizer.adjust_for_ambient_noise(source, duration=2.5)
            st.write("Listening...")
            audio = recognizer.listen(source, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            st.write("Timeout error. Please try again.")
            return ""
        try:
            st.write("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-IN')
            st.write("Query:", query)
            return query.lower()
        except sr.UnknownValueError:
            st.write("Sorry, I couldn't understand that. Please try again.")
            return ""
        except sr.RequestError as e:
            st.write("Could not request results; {0}".format(e))
            return ""

# Define a helper function for fetching news (outside the class)
@memory.cache
def fetch_news_cached(search_query, lang='en', region='IN'):
    google_news = GoogleNews(lang=lang, region=region)
    google_news.search(search_query)
    return google_news.results()[:2]

# Define NewsFetcher class
class NewsFetcher:
    def __init__(self, lang='en', region='IN'):
        self.lang = lang
        self.region = region

    def fetch_news(self, search_query):
        return fetch_news_cached(search_query, self.lang, self.region)

# Define tell_news function to both display and speak news
def tell_news(news_type, news_list):
    st.write(f"**{news_type} Headlines:**")
    speak(f"{news_type} Headlines are as follows:")
    for news_item in news_list:
        headline = news_item['title']
        if headline:
            st.write(headline)  # Display the headline
            speak(headline)  # Speak the headline

# Define ask_for_news_type function
def ask_for_news_type():
    speak("Welcome to InfoLive! Would you like to hear International, National, or Sports news? Or should I give you a general update?")
    response = listen()
    if "international" in response:
        return "international"
    elif "national" in response:
        return "national"
    elif "sports" in response:
        return "sports"
    else:
        return "general"

# Function to set background image
def set_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .reportview-container {{
            background: url(data:image/png;base64,{encoded_image})
        }}
        </style>
        """, 
        unsafe_allow_html=True
    )

# Main Function
def main():
    st.set_page_config(page_title="Info Live | Technovergence", page_icon=":newspaper:", layout="wide")
    
    # Set background image
    background_image_path = r"C:\\Users\\Dell\\Desktop\\Technovergence\\assets\\background.jpg"  # Use forward slashes
    set_background_image(background_image_path)

    # Add top-left and top-right images with small size
    top_left_image_path = r"C:\\Users\\Dell\\Desktop\\Technovergence\\assets\\info-live-logo.png"
    top_right_image_path = r"C:\\Users\\Dell\\Desktop\\Technovergence\\assets\\zsfc-logo.png"
    top_left_image = Image.open(top_left_image_path)
    top_right_image = Image.open(top_right_image_path)
   
    # Use columns to position the images at the top left and right
    col1, col2, col3 = st.columns([1, 4, 1])  # Adjust column widths as needed
    with col1:
        st.image(top_left_image, width=300)  # Set width to 360 pixels for a small size
    with col3:
        st.image(top_right_image, width=200)  # Set width to 360 pixels for a small size

    st.title("Info-Live | AI News Reader")
    st.markdown("<p style='text-align: center; font-size: 50px;'>Welcome to InfoLive!</p>", unsafe_allow_html=True)
    st.markdown("<style>h1 {text-align: center; color: #3498db;}</style>", unsafe_allow_html=True)
    st.markdown("<style>button {background-color: #3498db; color: white;}</style>", unsafe_allow_html=True)

    # Create an instance of NewsFetcher
    news_fetcher = NewsFetcher()

    # Ask for news type
    news_type = ask_for_news_type()

    # Fetch news based on user input
    if news_type == "international":
        news = news_fetcher.fetch_news("world news")
    elif news_type == "national":
        news = news_fetcher.fetch_news("india news")
    elif news_type == "sports":
        news = news_fetcher.fetch_news("sports news")
    else:
        news = news_fetcher.fetch_news("latest news")

    # Display and speak news
    tell_news(news_type, news)

if __name__ == "__main__":
    main()
