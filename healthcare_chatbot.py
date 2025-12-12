import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import numpy as np
import re

class HealthcareChatbot:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open("intents.json").read())
        self.words = pickle.load(open('words.pkl', 'rb'))
        self.classes = pickle.load(open('classes.pkl', 'rb'))
        self.model = load_model('chatbot_model.h5')
        
        # Health-related keywords for filtering
        self.health_keywords = [
            'symptom', 'disease', 'medicine', 'doctor', 'hospital', 'pain', 
            'fever', 'headache', 'treatment', 'diagnosis', 'health', 'medical',
            'illness', 'sick', 'appointment', 'prescription', 'medication',
            'therapy', 'surgery', 'infection', 'allergy', 'wellness'
        ]
        
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
            return "I'm sorry, I can only help with health-related questions. Could you please ask about symptoms, diseases, medications, or other health topics?"
            
        tag = intents_list[0]['intent']
        list_of_intents = intents_json['intents']
        
        for i in list_of_intents:
            if i['tag'] == tag:
                return random.choice(i['responses'])
        
        return "I'm sorry, I can only help with health-related questions."
    
    def is_health_related(self, user_input):
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in self.health_keywords)
    
    def get_bot_response(self, user_input):
        # Check if the input is health-related
        if not self.is_health_related(user_input):
            return "I'm a healthcare chatbot and can only assist with health-related questions. Please ask about symptoms, diseases, medications, treatments, or other health topics."
        
        # Predict intent and get response
        intents = self.predict_class(user_input)
        response = self.get_response(intents, self.intents)
        return response

def main():
    print("Healthcare Chatbot Initialized!")
    print("Ask me anything about health, symptoms, diseases, or medical topics.")
    print("Type 'quit' to exit.\n")
    
    chatbot = HealthcareChatbot()
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Bot: Thank you for using Healthcare Chatbot. Stay healthy!")
            break
        
        if user_input:
            response = chatbot.get_bot_response(user_input)
            print(f"Bot: {response}\n")

if __name__ == "__main__":
    main()
