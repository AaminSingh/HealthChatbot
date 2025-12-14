from flask import Flask, render_template, request, jsonify
from llm_chatbot import LLMHealthChatbot
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize LLM chatbot
# Choose your provider: "openai" or "gemini"
API_PROVIDER = os.getenv("LLM_PROVIDER", "openai")  # Default to OpenAI

try:
    chatbot = LLMHealthChatbot(api_provider=API_PROVIDER, use_fallback=True)
    if chatbot.api_available:
        print(f"✅ LLM Chatbot initialized with {API_PROVIDER.upper()} API")
    else:
        print(f"ℹ️  LLM Chatbot running in intelligent fallback mode (no API key)")
        print(f"   Add your {API_PROVIDER.upper()} API key to .env file for full AI capabilities")
except Exception as e:
    print(f"❌ Error initializing chatbot: {e}")
    print("Falling back to basic mode...")
    chatbot = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        user_message = request.json.get('message', '')
        
        if not user_message.strip():
            return jsonify({'response': 'Please enter a message.'})
        
        if chatbot:
            response = chatbot.get_bot_response(user_message)
        else:
            response = "Chatbot is currently unavailable. Please try again later."
        
        return jsonify({'response': response})
    
    except Exception as e:
        return jsonify({
            'response': f"I apologize, but I encountered an error. Please try again. If the issue persists, contact support."
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = "healthy" if chatbot else "degraded"
    return jsonify({'status': status, 'provider': API_PROVIDER})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
