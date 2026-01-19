import speech_recognition as sr
from gtts import gTTS
import os
import random
import requests

# ==========================
# SETTINGS
# ==========================

# OpenWeatherMap API
city = "Kakinada"
api_key = "YOUR_API_KEY"  

# Crop prices (dynamic simulation)
crop_prices = {
    "వరి": random.randint(2100, 2300),
    "మక్క": random.randint(1700, 1900),
    "పత్తి": random.randint(5900, 6100)
}

# ==========================
# VOICE INPUT
# ==========================

r = sr.Recognizer()

with sr.Microphone() as source:
    print("రైతన్న గారు, మీ ప్రశ్న చెప్పండి...")
    audio = r.listen(source)

try:
    # Convert speech to text (Telugu)
    text = r.recognize_google(audio, language="te-IN")
    print("మీరు అడిగింది:", text)

    response = ""

    # ==========================
    # CROP PRICE LOGIC
    # ==========================
    if "ధర" in text:
        if "వరి" in text:
            response = f"వరి ధర {crop_prices['వరి']} రూపాయలు"
        elif "మక్క" in text:
            response = f"మక్క ధర {crop_prices['మక్క']} రూపాయలు"
        elif "పత్తి" in text:
            response = f"పత్తి ధర {crop_prices['పత్తి']} రూపాయలు"
        else:
            response = "క్షమించండి, ఈ పంట ధర నాకు తెలియదు"

    # ==========================
    # WEATHER LOGIC
    # ==========================
    elif "వాతావరణం" in text or "ఈ రోజు" in text:
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            data = requests.get(url).json()
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            response = f"{city} వాతావరణం: {description}, ఉష్ణోగ్రత {temp} డిగ్రీలు"
        except:
            response = "వాతావరణం సమాచారం పొందలేకపోయాము"

    # ==========================
    # UNKNOWN QUESTION
    # ==========================
    else:
        response = "క్షమించండి, నేను అర్థం చేసుకోలేకపోయాను"

    # ==========================
    # VOICE OUTPUT
    # ==========================
    tts = gTTS(text=response, lang='te')
    tts.save("response.mp3")
    os.system("start response.mp3")

except:
    print("క్షమించండి, మళ్ళీ ప్రయత్నించండి")