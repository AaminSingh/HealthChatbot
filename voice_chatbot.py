import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import numpy as np
import speech_recognition as sr
import pyttsx3
import time

class VoiceHealthcareChatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open("intents.json").read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_model.h5')
        
        # Initialize speech components
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        
        # Configure speech settings
        self.engine.setProperty('rate', 175)
        self.engine.setProperty('volume', 1.0)
        
        # Health keywords for filtering
        self.health_keywords = [
            'symptom', 'disease', 'medicine', 'doctor', 'hospital', 'pain',
            'fever', 'headache', 'treatment', 'diagnosis', 'health', 'medical',
            'illness', 'sick', 'appointment', 'prescription', 'medication'
        ]
    
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()
    
    def listen(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = self.recognizer.listen(source)
        
        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand that."
    
    def is_health_related(self, user_input):
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in self.health_keywords)
    
    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words
    
    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        
        for w in sentence_words:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)
    
    def predict_class(self, sentence):
        bow = self.bag_of_words(sentence)
        res = self.model.predict(np.array([bow]))[0]
        
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        results.sort(key=lambda x: x[1], reverse=True)
        
        return_list = []
        for r in results:
            return_list.append({'intent': self.classes[r[0]], 'probability': str(r[1])})
        return return_list
    
    def get_response(self, intents_list, intents_json):
        if not intents_list:
            return "I can only help with health-related questions."
            
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        
        for i in list_of_intents:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        
        return "I can only help with health-related questions."
    
    def process_input(self, user_input):
        if not self.is_health_related(user_input):
            return "I'm a healthcare chatbot. Please ask about health topics only."
        
        intents = self.predict_class(user_input)
        response = self.get_response(intents, self.intents)
        return response
    
    def run(self):
        self.speak("Hello! I am your healthcare chatbot. How can I help you with your health questions today?")
        
        while True:
            user_input = self.listen()
            
            if user_input.lower() in ['quit', 'exit', 'goodbye']:
                self.speak("Thank you for using the healthcare chatbot. Stay healthy!")
                break
            
            response = self.process_input(user_input)
            print(f"Bot: {response}")
            self.speak(response)

if __name__ == "__main__":
    bot = VoiceHealthcareChatbot()
    bot.run()
