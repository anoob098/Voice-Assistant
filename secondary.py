import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import datetime
import requests
import json
import pyjokes

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Choose voice (0 for male, 1 for female)

# Speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Greet the user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your AI assistant. How can I help you today?")

# Take microphone input from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Sorry, I didn't catch that. Please repeat.")
        speak("Sorry, I didn't catch that. Please repeat.")
        return "None"
    return query.lower()

# Send an email
def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Use environment variables for security
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
        speak("Email has been sent successfully!")
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I was unable to send the email.")

# Fetch weather details using OpenWeatherMap API
def getWeather(city_name):
    api_key = "your_openweathermap_api_key"  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "q=" + city_name + "&appid=" + api_key + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather = data["main"]
        temperature = weather["temp"]
        humidity = weather["humidity"]
        description = data["weather"][0]["description"]
        speak(f"The temperature in {city_name} is {temperature} degrees Celsius with {description} and humidity at {humidity} percent.")
    else:
        speak("Sorry, I couldn't fetch the weather details for that city.")

# Main function
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand()

        # Wikipedia search
        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia:")
                print(results)
                speak(results)
            except Exception as e:
                speak("Sorry, I couldn't find information on that topic.")

        # Open websites
        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("https://stackoverflow.com")

        # Get current time
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        # Send an email
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Who should I send it to?")
                recipient = takeCommand()
                to = f"{recipient}@gmail.com"  # Replace this logic with a contact list or exact address
                sendEmail(to, content)
            except Exception as e:
                print(e)
                speak("Sorry, I couldn't send the email.")

        # Fetch weather details
        elif 'weather' in query:
            speak("Which city's weather would you like to know?")
            city_name = takeCommand()
            getWeather(city_name)

        # Tell a joke
        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)
            print(joke)

        # Exit the assistant
        elif 'exit' in query or 'quit' in query:
            speak("Goodbye! Have a great day!")
            break

        else:
            speak("I'm sorry, I didn't understand that. Please try again.")
