import pyttsx3
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import datetime  

# Initialize the pyttsx3 engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to speak a given text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("How may I help you")

# Function to take voice input from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')  
        print(f"User said: {query}\n")
    except Exception as e:
        print("Please repeat that again...")
        return "None"
    return query


def sendEmail(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  
        server.ehlo()
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Replace with actual email and password
        server.sendmail('youremail@gmail.com', to, content)
        server.close()
    except Exception as e:
        print("Error:", e)
        speak("Sorry, I could not send the email.")

# Main function
if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower() 

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak('According to Wikipedia')
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://youtube.com")

        elif 'open google' in query:
            webbrowser.open("https://google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Sudrao21@gmail.com"  # Replace with the actual recipient email
                sendEmail(to, content)
                speak("The email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry, I could not send the email.")
