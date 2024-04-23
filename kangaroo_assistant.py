import pyttsx3, datetime, requests, webbrowser, os, pyjokes
import speech_recognition as sr

BYEBYE = ["bye", "goodbye", "see you", "laters", "see ya",
          "quit", "exit"]


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    '''
    This function will take 'audio' as a string input and it will
    speak it out using the voice set by the "engine.setProperty(...)"
    line above.
    '''
    engine.say(audio)
    engine.runAndWait()
    
    
def wishMe():
    '''
    This function will first decide if it is morning, afternoon,
    evening or past midnight;
    
    Then, it will greet you with the appropriate phrase,
    followed by an introduction of the 'software', which is called
    KURAMA.
    '''
    hour = int(datetime.datetime.now().hour)
    
    if hour >= 4 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    elif hour >= 18 and hour <= 23:
        speak("Good evening!")
    else:
        speak("Hi there! It's past midnight.")
        
    speak("I am Electromagnetic Kangaroo V4.20, your personal assistant. How may I help you?")
    
    
def takeCommand():
    '''
    It takes microphone input from the user and it converts it
    to a string output
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
        
        print("Recognizing...")
    
    try:
        query = r.recognize_google(audio)
        print(f"User said: {query}\n")
        
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    
    return query


def get_wikipedia_summary(query):
    # Encode the query for URL
    encoded_query = requests.utils.quote(query)
    
    # Define the URL for the MediaWiki API search Endpoint
    search_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srsearch={encoded_query}"
    
    # Send a GET request to the API to search for the query
    search_response = requests.get(search_url)
    search_data = search_response.json()
    
    # Check if there are any search results
    search_results = search_data.get('query', {}).get('search', [])
    if not search_results:
        return f"No Wikipedia page found for '{query}'.\
            Please try again."
            
    closest_match = search_results[0]['title']
    speak(f"Wikipedia results for '{closest_match}':")
    # Get the title of the closest matching page
    
    # Define the URL for the MediaWiki API to retrieve the page content
    page_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&titles={closest_match}&exintro&explaintext"
    
    # Send a GET request to the API to retrieve the page content
    page_response = requests.get(page_url)
    page_data = page_response.json()
    
    # Extract the page content
    page_id = list(page_data['query']['pages'].keys())[0]
    extract = page_data['query']['pages'][page_id]['extract']
    
    # Split the content into sentences
    sentences = extract.split(". ")
    
    # Extract the first two sentences
    first_two = ". ".join(sentences[:2]) + "."
    print(first_two)
    speak(first_two)
    
    return True


def open_website(query):
    open_idx = query.find("open") + 4
    keyword = query[open_idx:].replace(" ", "").lower()
    

    url = f"https://www.{keyword}.com"
    
    try:
        response = requests.get(url)
        if response.status_code >= 200 and response.status_code < 300:
            speak(f"Sure. Opening {keyword}")
            webbrowser.open_new_tab(url)
            
        else:
            speak(f"Sorry, I couldn't find any website called {keyword}")
    
    except requests.RequestException:
            speak("Hmmmmm, something went wrong. Please try again.")
            
            
def tell_joke():
    while True:
                short_joke = pyjokes.get_joke(category='neutral')
                print(short_joke)
                speak(f"Sure! Here's one: {short_joke}")
                speak("Wanna hear another one?")
                answer = takeCommand()

                if answer in ["yes", "yeah", "yea", "sure"]:
                    pass
                else:
                    speak("Alright.")
                    break
    
    
    
if __name__ == "__main__":
    wishMe()
    while True:
        
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            query = query.replace("wikipedia", "").title()
            speak("Searching Wikipedia...")
            get_wikipedia_summary(query)
            
        if "open code" in query:
            code_path = "C:\\Users\\rubio\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            speak("Sure! Opening VSCode...")
            os.startfile(code_path)
        elif "open" in query:
            open_website(query)
            
        if "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"The time is {strTime}")
            
        if "the date" in query:
            strDate = datetime.date.today()
            speak(f"Today is {strDate}")
            
        if "joke" in query:
            tell_joke()
            
        if "who are you" in query:
            speak("As I said in the beginning, I am Electromagnetic Kangaroo V4.20\
                And I was created by Alex Rubio. I am here to help.")
            
        if any(value in query for value in BYEBYE):
            speak("Alright! See you later!")
            break