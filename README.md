# 🩺 Intelligent Health Assistant Chatbot

An advanced, AI-powered healthcare assistant designed to provide immediate, safe, and context-aware medical guidance. This hybrid chatbot combines the reasoning power of Large Language Models (LLMs) with strict rule-based safety protocols to ensure accurate and helpful responses.

## 🚀 Key Features

### 1. 🏥 **Symptom Analysis & Home Remedies**
The chatbot acts as a first-line digital consultant for common health issues.
- **Context-Aware Advice:** Understands specific symptoms like "tired eyes," "knee pain," or "flu."
- **Eye Care Specialist:** Includes specialized logic for **Dry Eyes** (hydration tips) and **Eye Pain** (strain relief).
- **Safety First:** Automatically detects emergencies (e.g., "chest pain", "difficulty breathing") and advises immediate medical attention.

### 2. 📊 **BMI Calculator**
A built-in utility to help users track their physical health.
- **How it works:** Users can say *"Calculate my BMI"* or *"I am 175cm and 70kg"*.
- **Output:** Instantly calculates Body Mass Index and categorizes it (Underweight, Normal, Overweight, Obese) with tailored health tips.

### 3. 📍 **Nearby Hospital & Clinic Locator**
Helps users find medical help quickly based on their location.
- **Smart Detection:** Recognizes Zip Codes (e.g., `226016`) and City names.
- **Actionable Results:** Generates a direct **Google Maps link** to hospitals in the specified area.
- **Example:** *"Where is the nearest clinic?"* -> *"Which city?"* -> *"Lucknow"* -> *[Link to Hospitals in Lucknow]*

### 4. 💊 **Medication Safety System**
- **OTC Only:** Recommends *only* Over-The-Counter remedies (e.g., Paracetamol, Ibuprofen) for mild symptoms.
- **Strict Guardrails:** NEVER recommends prescription drugs (antibiotics, steroids).
- **Disclaimers:** Every recommendation includes a mandatory safety warning to consult a pharmacist.

---

## 🛠️ Tech Stack

### **Backend**
- **Python 3.x:** The core logic and data processing.
- **Flask:** Lightweight web framework to serve the application and handle API requests.
- **Regex (Regular Expressions):** Used for precise pattern matching (BMI extraction, Zip Code detection).

### **AI & NLP**
- **LLM Integration:** Supports **OpenAI (GPT-3.5/4)** and **Google Gemini** for natural language understanding and empathetic responses.
- **Hybrid Logic:** Combines AI generation with hard-coded safety rules for maximum reliability.

### **Frontend**
- **HTML5 & CSS3:** Custom "Medical Theme" with soothing teal colors and floating background animations.
- **Vanilla JavaScript:** Handles the chat interface, message history, and the "Engagement Milestone" gamification feature.

---

## 📦 Libraries & Dependencies

The project relies on the following key Python libraries:

| Library | Purpose |
| :--- | :--- |
| `flask` | Web server and routing. |
| `openai` | Client for OpenAI API (GPT models). |
| `google-generativeai` | Client for Google Gemini API. |
| `python-dotenv` | Managing environment variables (API keys). |
| `requests` | Handling HTTP requests (if needed). |

---

## 🏃‍♂️ How to Run

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/AaminSingh/HealthChatbot.git
    cd HealthChatbot
    ```

2.  **Create a Virtual Environment (Optional but Recommended):**
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Keys:**
    - Create a `.env` file in the root directory.
    - Add your key: `OPENAI_API_KEY=your_key_here` or `GOOGLE_API_KEY=your_key_here`.

5.  **Run the Application:**
    ```bash
    python web_chatbot_llm.py
    ```

6.  **Open in Browser:**
    Visit `http://127.0.0.1:5000` to start chatting!

---

*⚠️ **Disclaimer:** This AI chatbot is for informational purposes only and does not replace professional medical advice, diagnosis, or treatment.* 
