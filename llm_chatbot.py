import os
import re
from typing import Dict, Optional
import json

# Uncomment the API you want to use:
# Option 1: OpenAI
# import openai

# Option 2: Google Gemini
# import google.generativeai as genai

class LLMHealthChatbot:
    """Enhanced Healthcare Chatbot with LLM Integration"""
    
    # Emergency keywords that trigger immediate safety response
    EMERGENCY_KEYWORDS = [
        'chest pain', 'heart attack', 'stroke', 'unconscious', 'not conscious',
        'severe bleeding', 'bleeding heavily', 'can\'t breathe', 'cannot breathe',
        'difficulty breathing', 'suicide', 'suicidal', 'kill myself', 'overdose',
        'poisoning', 'poisoned', 'severe injury', 'choking', 'seizure',
        'allergic reaction', 'anaphylaxis', 'broken bone', 'severe burn'
    ]
    
    # Common health symptoms with fallback responses
    FALLBACK_RESPONSES = {
        'headache': {
            'answer': 'Headaches can be caused by stress, dehydration, poor sleep, or tension. They are very common and usually not serious.',
            'tips': [
                'Rest in a quiet, dark room',
                'Stay well-hydrated (8-10 glasses of water daily)',
                'Practice relaxation techniques like deep breathing',
                'Maintain regular sleep schedule',
                'Avoid excessive screen time'
            ],
            'remedies': [
                'Apply a cold compress to your forehead',
                'Gently massage your temples in circular motions',
                'Try peppermint or lavender essential oil aromatherapy',
                'Drink ginger tea to reduce inflammation'
            ]
        },
        'cough': {
            'answer': 'A cough is your body\'s way of clearing irritants from your airways. It can be caused by colds, allergies, or respiratory infections.',
            'tips': [
                'Stay hydrated to thin mucus',
                'Use a humidifier to keep air moist',
                'Avoid smoke and strong odors',
                'Get plenty of rest',
                'Elevate your head while sleeping'
            ],
            'remedies': [
                'Honey and warm water: Mix 1-2 tablespoons in warm water',
                'Steam inhalation: Breathe in warm, moist air',
                'Saltwater gargle: Mix 1/2 teaspoon salt in warm water',
                'Ginger tea: Steep fresh ginger for 10 minutes'
            ]
        },
        'stomach': {
            'answer': 'Stomach discomfort can result from indigestion, gas, stress, or dietary choices. It\'s usually temporary and manageable.',
            'tips': [
                'Eat smaller, more frequent meals',
                'Avoid spicy, fatty, or acidic foods',
                'Stay upright after eating',
                'Manage stress through relaxation',
                'Keep a food diary to identify triggers'
            ],
            'remedies': [
                'Peppermint tea: Soothes digestive system',
                'Ginger: Chew small pieces or make tea',
                'Warm compress on stomach for comfort',
                'Chamomile tea: Reduces inflammation'
            ]
        },
        'dizzy': {
            'answer': 'Dizziness can be caused by dehydration, low blood sugar, sudden movements, or inner ear issues. It\'s important to sit down when feeling dizzy.',
            'tips': [
                'Sit or lie down immediately if dizzy',
                'Stay well-hydrated throughout the day',
                'Avoid sudden movements or standing quickly',
                'Eat regular, balanced meals',
                'Limit caffeine and alcohol'
            ],
            'remedies': [
                'Deep breathing exercises: Breathe slowly and deeply',
                'Ginger tea: Helps with balance',
                'Stay seated until dizziness passes',
                'Drink water with a pinch of salt and sugar'
            ]
        },
        'fever': {
            'answer': 'Fever is your body\'s natural response to fighting infection. A mild fever (under 102°F/39°C) is usually not dangerous.',
            'tips': [
                'Rest and stay in bed',
                'Drink plenty of fluids',
                'Wear light clothing',
                'Keep room temperature comfortable',
                'Monitor temperature regularly'
            ],
            'remedies': [
                'Cool compress: Apply to forehead and wrists',
                'Lukewarm bath: Not cold, to avoid shivering',
                'Herbal tea: Chamomile or elderflower',
                'Stay hydrated with water and clear broths'
            ]
        },
        'cold': {
            'answer': 'The common cold is a viral infection affecting your nose and throat. It usually resolves on its own within 7-10 days.',
            'tips': [
                'Get plenty of rest and sleep',
                'Drink warm fluids',
                'Use saline nasal drops',
                'Wash hands frequently',
                'Avoid close contact with others'
            ],
            'remedies': [
                'Chicken soup: Warm, nutritious, and soothing',
                'Honey and lemon in warm water',
                'Steam inhalation with eucalyptus',
                'Gargle with warm salt water'
            ]
        },
        'sore throat': {
            'answer': 'A sore throat is often caused by viral infections, allergies, or dry air. It typically improves within a few days.',
            'tips': [
                'Stay hydrated with warm beverages',
                'Avoid shouting or straining voice',
                'Use a humidifier at night',
                'Rest your voice when possible',
                'Avoid irritants like smoke'
            ],
            'remedies': [
                'Warm salt water gargle: 3-4 times daily',
                'Honey and lemon tea: Soothes throat',
                'Warm herbal teas: Chamomile or licorice root',
                'Ice chips or popsicles: Numb the pain'
            ]
        },
        'knee': {
            'answer': 'Knee pain can result from overuse, minor injuries, strain, or inflammation. It\'s one of the most common joint complaints.',
            'tips': [
                'Rest and avoid activities that worsen the pain',
                'Wear supportive, cushioned footwear',
                'Maintain a healthy weight to reduce joint stress',
                'Perform low-impact exercises like swimming',
                'Strengthen quadriceps and hamstring muscles'
            ],
            'remedies': [
                'R.I.C.E Method: Rest, Ice (20 mins every 2-3 hours), Compression (elastic bandage), Elevation',
                'Gentle stretching: Hamstring and quad stretches',
                'Turmeric tea: Natural anti-inflammatory',
                'Warm compress after first 48 hours for chronic pain'
            ]
        },
        'tired eyes': {
            'answer': 'Eye strain (asthenopia) is common with prolonged screen time, reading, or poor lighting. Your eyes need regular breaks to recover.',
            'tips': [
                'Follow the 20-20-20 rule during screen time',
                'Ensure proper lighting when reading or working',
                'Get 7-8 hours of quality sleep nightly',
                'Adjust screen brightness to match surroundings',
                'Keep screen at arm\'s length, slightly below eye level'
            ],
            'remedies': [
                '20-20-20 Rule: Every 20 minutes, look 20 feet away for 20 seconds',
                'Warm compress: Place over closed eyes for 5-10 minutes',
                'Blink exercises: Consciously blink 10 times slowly',
                'Chamomile tea bags: Cool and place on closed eyes'
            ]
        },
        'dry eyes': {
            'answer': 'Dry eyes occur when your tears aren\'t able to provide adequate lubrication for your eyes. This is common in air-conditioned environments or after long screen use.',
            'tips': [
                'Blink more frequently when using screens',
                'Follow the 20-20-20 rule',
                'Use a humidifier to add moisture to the air',
                'Position your computer screen below eye level',
                'Stay hydrated by drinking plenty of water'
            ],
            'remedies': [
                'Artificial tears (preservative-free eye drops)',
                'Warm compress to unclog oil glands',
                'Omega-3 fatty acid supplements (consult doctor)',
                'Eyelid massage with warm washcloth'
            ]
        },
        'eye pain': {
            'answer': 'Mild eye pain can be due to strain or dryness. However, severe or sharp pain requires medical attention.',
            'tips': [
                'Rest your eyes immediately',
                'Avoid bright lights and screens',
                'Do not rub your eyes',
                'Check if a foreign object is in the eye (wash with water)',
                'Wear sunglasses outdoors'
            ],
            'remedies': [
                'Cold compress for inflammation or minor injury',
                'Warm compress for styes or strain',
                'Over-the-counter lubricating eye drops',
                'Rest in a dark room'
            ]
        },
        'back': {
            'answer': 'Back pain is very common and usually caused by muscle strain, poor posture, or sudden movements. Most cases improve with self-care.',
            'tips': [
                'Maintain good posture when sitting and standing',
                'Use ergonomic chairs with lumbar support',
                'Lift objects properly using your legs, not your back',
                'Stay active with low-impact exercises',
                'Strengthen core muscles to support your spine'
            ],
            'remedies': [
                'Alternate heat and cold: Ice first 48 hours, then heat therapy',
                'Gentle stretching: Cat-cow pose, child\'s pose from yoga',
                'Epsom salt bath: Soak for 20 minutes to relax muscles',
                'Proper sleep position: Use pillow between knees if side-sleeping'
            ]
        }
    }
    
    SYSTEM_PROMPT = """You are a knowledgeable, empathetic, and cautious AI health assistant specialized in providing symptom-specific advice. Your role is to provide general health information while prioritizing user safety and accuracy.

CRITICAL INSTRUCTION - CONTEXTUAL ACCURACY:
Before generating any response, you MUST:
1. Identify the EXACT body part or symptom mentioned by the user (e.g., "knee", "eyes", "stomach")
2. Generate advice ONLY for that specific body part/symptom
3. NEVER use cached or default answers for different body parts
4. If the user asks about "knee pain", talk ONLY about knees, NOT headaches or other body parts

BROAD SYMPTOM RECOGNITION - Treat these as VALID health queries:
**Pain/Discomfort**: Knee, back, hand, stomach, head, chest, neck, shoulder, ankle, wrist, hip, elbow, foot, eye pain
**Sensory Issues**: Dizziness, tired eyes, eye strain, dry eyes, blurred vision, ringing ears, numbness, tingling
**Respiratory**: Cough, shortness of breath, wheezing, congestion, runny nose, sore throat
**Digestive**: Nausea, vomiting, diarrhea, constipation, bloating, heartburn, indigestion
**General**: Fever, fatigue, weakness, chills, sweating, sleep problems, anxiety

NEW FEATURE INSTRUCTIONS:

1. MEDICATION RECOMMENDATIONS (SAFETY CRITICAL):
- You may suggest common Over-The-Counter (OTC) remedies for mild symptoms (e.g., Paracetamol/Acetaminophen for fever, Ibuprofen for pain, Antacids for heartburn).
- CONSTRAINT: NEVER recommend prescription-only drugs (antibiotics, steroids, strong painkillers).
- MANDATORY DISCLAIMER: Every medication mention must end with: "Please read the label carefully and consult a pharmacist, especially if you have allergies or are on other medications."

2. BMI CALCULATOR:
- If the user asks to calculate BMI and provides height/weight, calculate it: Weight(kg) / Height(m)^2.
- Return the value and category: Underweight (<18.5), Normal (18.5-24.9), Overweight (25-29.9), Obese (30+).
- If user asks "Check my BMI" without data, ask: "Sure, please tell me your height (in cm or m) and weight (in kg)."

3. NEARBY CLINICS:
- If user asks for nearby hospitals/clinics and provides a city, generate this link: https://www.google.com/maps/search/hospitals+near+[City]
- If no city is provided, ask: "Which city or zip code are you currently in?"

RESPONSE FORMAT - Use HTML formatting for the response. Use <strong> for headers, <ul> and <li> for lists, and <br> for line breaks.

**1. Acknowledgment:**
"I understand you are experiencing [INSERT EXACT SYMPTOM USER MENTIONED]."

**2. Potential Causes:**
List 2-4 common non-emergency causes specific to that body part/symptom.

**3. Home Remedies:**
Provide 2-3 SPECIFIC remedies for THAT EXACT SYMPTOM/BODY PART. Examples:
- For knee pain: R.I.C.E method (Rest, Ice, Compression, Elevation)
- For tired eyes: Follow the 20-20-20 rule (every 20 mins, look 20 feet away for 20 seconds)
- For stomach discomfort: Ginger tea, peppermint, BRAT diet (bananas, rice, applesauce, toast)
- For headache: Cold compress, hydration, rest in dark room

**4. When to See a Doctor:**
List 2-3 specific red flags for THAT condition.

FEW-SHOT EXAMPLES TO LEARN FROM:

Example 1:
User: "My eyes feel tired"
AI Response:
"I understand you are experiencing tired eyes (eye strain).<br><br><strong>Potential Causes:</strong><ul><li>Prolonged screen time without breaks</li><li>Poor lighting conditions</li><li>Inadequate sleep</li><li>Uncorrected vision problems</li></ul><strong>Home Remedies:</strong><ul><li><strong>20-20-20 Rule</strong>: Every 20 minutes, look at something 20 feet away for 20 seconds</li><li><strong>Warm Compress</strong>: Apply a warm, damp cloth over closed eyes for 5-10 minutes</li><li><strong>Adjust Screen Settings</strong>: Reduce brightness, increase font size, use blue light filters</li><li><strong>Get Adequate Sleep</strong>: Aim for 7-8 hours nightly</li></ul><strong>When to See a Doctor:</strong><ul><li>If eye strain persists despite rest and adjustments</li><li>If you experience vision changes, pain, or headaches</li><li>If symptoms are accompanied by light sensitivity</li></ul><br><em>⚠️ I am an AI, not a doctor. Please consult a medical professional for proper diagnosis and treatment.</em>"

Example 2:
User: "I have knee pain"
AI Response:
"I understand you are experiencing knee pain.<br><br><strong>Potential Causes:</strong><ul><li>Overuse or strain from physical activity</li><li>Minor injury or sprain</li><li>Arthritis or joint inflammation</li><li>Poor posture or improper footwear</li></ul><strong>Home Remedies:</strong><ul><li><strong>R.I.C.E Method</strong>: Rest, Ice (20 mins every 2-3 hours), Compression (wrap with elastic bandage), Elevation (keep knee raised)</li><li><strong>Gentle Stretching</strong>: Perform low-impact exercises like hamstring and quadriceps stretches</li><li><strong>Anti-inflammatory Foods</strong>: Include turmeric, ginger, and omega-3 fatty acids in your diet</li><li><strong>Proper Footwear</strong>: Wear supportive shoes to reduce knee stress</li></ul><strong>When to See a Doctor:</strong><ul><li>If pain is severe or accompanied by swelling, redness, or warmth</li><li>If you cannot bear weight on the leg</li><li>If pain persists for more than a few days or worsens</li></ul><br><em>⚠️ I am an AI, not a doctor. Please consult a medical professional for proper diagnosis and treatment.</em>"

MANDATORY SAFETY RULES:
1. NEVER diagnose specific medical conditions
2. NEVER recommend prescription medications or dosages
3. ALWAYS end with disclaimer: "⚠️ I am an AI, not a doctor. Please consult a medical professional for proper diagnosis and treatment."
4. For non-health questions, respond: "I can only assist with health-related questions. Please ask about symptoms, wellness, or medical topics."

TEMPERATURE CONTROL: This prompt is designed to work with temperature=0.3 for focused, accurate responses."""

    def __init__(self, api_provider: str = "openai", api_key: Optional[str] = None, use_fallback: bool = True):
        """
        Initialize the LLM Health Chatbot
        
        Args:
            api_provider: Either "openai" or "gemini"
            api_key: API key for the chosen provider (or set via environment variable)
            use_fallback: If True, use fallback responses when API is unavailable
        """
        self.api_provider = api_provider.lower()
        self.use_fallback = use_fallback
        self.api_available = False
        
        if api_key:
            self.api_key = api_key
        elif self.api_provider == "openai":
            self.api_key = os.getenv("OPENAI_API_KEY")
        elif self.api_provider == "gemini":
            self.api_key = os.getenv("GEMINI_API_KEY")
        else:
            raise ValueError("Invalid API provider. Choose 'openai' or 'gemini'")
        
        # Only require API key if fallback is disabled
        if not self.api_key:
            if not use_fallback:
                raise ValueError(f"API key not found for {api_provider}. Set environment variable or pass api_key parameter.")
            else:
                print(f"⚠️  No API key found for {api_provider}. Using intelligent fallback mode.")
                self.api_available = False
        else:
            try:
                self._initialize_client()
                self.api_available = True
            except Exception as e:
                print(f"⚠️  Failed to initialize {api_provider} client: {e}")
                if use_fallback:
                    print("Using intelligent fallback mode.")
                    self.api_available = False
                else:
                    raise
    
    def _initialize_client(self):
        """Initialize the appropriate API client"""
        if self.api_provider == "openai":
            import openai
            openai.api_key = self.api_key
            self.client = openai
        elif self.api_provider == "gemini":
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel('gemini-pro')
    
    def detect_emergency(self, user_input: str) -> bool:
        """
        Detect if user input contains emergency keywords
        
        Args:
            user_input: The user's message
            
        Returns:
            True if emergency keywords detected, False otherwise
        """
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in self.EMERGENCY_KEYWORDS)
    
    def get_emergency_response(self) -> str:
        """
        Return emergency response message
        
        Returns:
            Emergency response string
        """
        return """🚨 <strong>MEDICAL EMERGENCY DETECTED</strong> 🚨<br><br>This sounds like a serious medical emergency. I cannot provide diagnosis or treatment advice for this situation.<br><br><strong>IMMEDIATE ACTION REQUIRED:</strong><ul><li>📞 Call 911 (or your local emergency number) RIGHT NOW</li><li>🏥 Or go to the nearest Emergency Room immediately</li></ul>Do not wait. Do not delay. Your safety is the top priority.<br><br>If you're having a medical emergency, please put down your device and call for help immediately."""
    
    def is_health_related(self, user_input: str) -> bool:
        """
        Determine if user input is health-related
        
        Args:
            user_input: The user's message
            
        Returns:
            True if health-related, False otherwise
        """
        health_keywords = [
            # Symptoms
            'pain', 'hurt', 'ache', 'sore', 'tired', 'fatigue', 'dizzy', 'nausea',
            'fever', 'cough', 'cold', 'flu', 'sick', 'ill', 'symptom',
            # Body parts
            'head', 'eye', 'eyes', 'ear', 'nose', 'throat', 'chest', 'stomach',
            'knee', 'back', 'hand', 'foot', 'neck', 'shoulder', 'arm', 'leg',
            # Medical terms
            'medicine', 'medication', 'doctor', 'hospital', 'health', 'medical',
            'treatment', 'diagnosis', 'disease', 'condition', 'injury',
            # Wellness
            'sleep', 'diet', 'exercise', 'wellness', 'nutrition', 'mental', 'stress',
            'anxiety', 'depression', 'weight', 'fitness',
            # Sensations
            'blurred', 'vision', 'strain', 'swelling', 'redness', 'numbness',
            'tingling', 'burning', 'itching', 'bleeding'
        ]
        
        user_input_lower = user_input.lower()
        return any(keyword in user_input_lower for keyword in health_keywords)
    
    def get_llm_response(self, user_input: str) -> str:
        """
        Get response from LLM API with health validation
        
        Args:
            user_input: The user's health question
            
        Returns:
            AI-generated response
        """
        # Check if question is health-related
        if not self.is_health_related(user_input):
            return "I can only assist with health-related questions. Please ask about symptoms, wellness, medications, or medical topics."
        
        # If API is not available, use fallback
        if not self.api_available and self.use_fallback:
            symptom = self.detect_symptom(user_input)
            if symptom:
                return self.format_fallback_response(symptom)
            else:
                return self._get_generic_health_response(user_input)
        
        try:
            if self.api_provider == "openai":
                return self._get_openai_response(user_input)
            elif self.api_provider == "gemini":
                return self._get_gemini_response(user_input)
        except Exception as e:
            # Fallback to intelligent response on API error
            if self.use_fallback:
                symptom = self.detect_symptom(user_input)
                if symptom:
                    return self.format_fallback_response(symptom)
                else:
                    return self._get_generic_health_response(user_input)
            return f"I apologize, but I encountered an error processing your request. Please try again or consult a healthcare professional."
    
    def _get_generic_health_response(self, user_input: str) -> str:
        """
        Provide a generic but helpful health response when no specific symptom is detected
        
        Args:
            user_input: The user's message
            
        Returns:
            Generic health response
        """
        return """Thank you for your health question. While I can provide general information, I'd like to help you better.<br><br><strong>Could you tell me more about:</strong><ul><li>What specific symptoms are you experiencing?</li><li>When did they start?</li><li>How severe are they on a scale of 1-10?</li></ul><strong>Common topics I can help with:</strong><ul><li>Headaches, coughs, colds, and flu symptoms</li><li>Stomach issues and digestive health</li><li>Fever and sore throat</li><li>General wellness and prevention tips</li><li>Home remedies for minor ailments</li></ul>Please describe your symptoms in more detail, and I'll provide specific advice, actionable tips, and home remedies.<br><br><em>⚠️ I am an AI, not a doctor. For serious concerns or symptoms that persist, please consult a medical professional.</em>"""
    
    def _get_openai_response(self, user_input: str) -> str:
        """Get response from OpenAI API with optimized parameters"""
        response = self.client.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" for better quality
            messages=[
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,  # LOW temperature for focused, accurate responses
            max_tokens=800,
            top_p=0.9  # Additional control for deterministic outputs
        )
        return response.choices[0].message.content.strip()
    
    def _get_gemini_response(self, user_input: str) -> str:
        """Get response from Google Gemini API with optimized parameters"""
        full_prompt = f"{self.SYSTEM_PROMPT}\n\nUser Question: {user_input}"
        
        # Configure generation with low temperature
        generation_config = {
            'temperature': 0.3,  # LOW temperature for focused responses
            'top_p': 0.9,
            'top_k': 40,
            'max_output_tokens': 800,
        }
        
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        return response.text.strip()
    
    def calculate_bmi(self, height_cm: float, weight_kg: float) -> str:
        """Calculate BMI and return formatted response"""
        try:
            height_m = height_cm / 100
            bmi = weight_kg / (height_m * height_m)
            bmi = round(bmi, 1)
            
            if bmi < 18.5:
                category = "Underweight"
                advice = "It seems you are underweight. Consider consulting a nutritionist for a balanced diet plan."
            elif 18.5 <= bmi <= 24.9:
                category = "Normal weight"
                advice = "Great! You are in a healthy weight range. Keep maintaining a balanced diet and regular exercise."
            elif 25 <= bmi <= 29.9:
                category = "Overweight"
                advice = "You are in the overweight range. Regular exercise and a balanced diet can help manage your weight."
            else:
                category = "Obese"
                advice = "Your BMI indicates obesity. It is recommended to consult a healthcare provider for personalized advice."
                
            return f"<strong>Your BMI is {bmi} ({category}).</strong><br><br>{advice}<br><br><em>Note: BMI is a general screening tool and does not measure body fat directly or account for muscle mass.</em>"
        except Exception:
            return "I couldn't calculate your BMI. Please ensure you provided valid numbers."

    def handle_bmi_request(self, user_input: str) -> Optional[str]:
        """Check if user wants BMI calculation and process it"""
        # Check for explicit BMI intent
        if re.search(r'\b(bmi|body mass index)\b', user_input.lower()):
            # Try to extract numbers
            # Look for patterns like "175 cm" or "1.75 m" and "70 kg"
            height_match = re.search(r'(\d+(?:\.\d+)?)\s*(cm|centimeters?|m|meters?)', user_input.lower())
            weight_match = re.search(r'(\d+(?:\.\d+)?)\s*(kg|kilograms?)', user_input.lower())
            
            if height_match and weight_match:
                height_val = float(height_match.group(1))
                height_unit = height_match.group(2)
                weight_val = float(weight_match.group(1))
                
                # Convert height to cm if in meters
                if 'm' in height_unit and 'cm' not in height_unit:
                    height_val *= 100
                    
                return self.calculate_bmi(height_val, weight_val)
            else:
                return "Sure, I can calculate your BMI. Please tell me your <strong>height</strong> (in cm or m) and <strong>weight</strong> (in kg).<br>Example: <em>'I am 175cm tall and weigh 70kg'</em>"
        return None

    def handle_hospital_request(self, user_input: str) -> Optional[str]:
        """Check if user wants to find nearby hospitals"""
        user_input_lower = user_input.lower()
        
        # Helper to generate link
        def generate_link(loc):
            search_query = f"hospitals+near+{loc.replace(' ', '+')}"
            link = f"https://www.google.com/maps/search/{search_query}"
            return f"Here is a list of medical facilities near <strong>{loc}</strong>:<br><br><a href='{link}' target='_blank' style='color: #00bfa5; font-weight: bold; text-decoration: none;'>📍 Click here to view Hospitals in {loc} on Google Maps</a><br><br><em>Please call ahead to confirm availability.</em>"

        # 1. Check for Zip Codes (Strong signal for follow-up)
        # Matches 5 or 6 digit numbers (e.g., 226016, 90210)
        zip_match = re.search(r'\b(\d{5,6})\b', user_input)
        if zip_match:
            return generate_link(zip_match.group(1))

        # 2. Check for explicit location context "in [City]" or "at [City]"
        # This helps catch "I am in London" even if they don't say "hospital" again
        location_match = re.search(r'\b(?:in|at|near|my city is)\s+([a-zA-Z\s]+)', user_input_lower)
        
        # 3. Standard Intent Check (User explicitly asks for hospital)
        if re.search(r'\b(hospital|clinic|doctor|medical center|emergency room)\b', user_input_lower):
            # If they provided location in the same sentence: "Hospital in London"
            if location_match:
                return generate_link(location_match.group(1).strip())
            
            # If intent is clear but no location found: "Find a hospital"
            if re.search(r'\b(find|search|where|nearest|nearby)\b', user_input_lower):
                return "I can help you find a nearby medical facility. <strong>Which city or zip code are you currently in?</strong>"
        
        # 4. Catch-all for "in [City]" if it looks like a location answer to a previous question
        # We filter out common non-location words to avoid false positives like "in pain"
        if location_match:
            location = location_match.group(1).strip()
            ignored_words = ['pain', 'trouble', 'danger', 'bed', 'hospital', 'clinic', 'emergency', 'need', 'love', 'doubt', 'general', 'particular', 'mind', 'fact']
            if location not in ignored_words and len(location) > 2:
                return generate_link(location)

        return None

    def get_bot_response(self, user_input: str) -> str:
        """
        Main method to get chatbot response with safety checks
        
        Args:
            user_input: The user's message
            
        Returns:
            Appropriate bot response
        """
        # First, check for emergencies
        if self.detect_emergency(user_input):
            return self.get_emergency_response()
            
        # Check for BMI request
        bmi_response = self.handle_bmi_request(user_input)
        if bmi_response:
            return bmi_response
            
        # Check for Hospital/Clinic request
        hospital_response = self.handle_hospital_request(user_input)
        if hospital_response:
            return hospital_response
        
        # If not emergency or special feature, get LLM response
        return self.get_llm_response(user_input)
    
    def detect_symptom(self, user_input: str) -> Optional[str]:
        """
        Enhanced symptom detection with specific body part recognition
        
        Args:
            user_input: The user's message
            
        Returns:
            Detected symptom key or None
        """
        user_input_lower = user_input.lower()
        
        # PRIORITY 1: Check exact symptom keywords first
        symptom_patterns = {
            'headache': ['headache', 'head pain', 'head ache', 'head hurts', 'migraine'],
            'cough': ['cough', 'coughing'],
            'stomach': ['stomach', 'belly', 'tummy', 'abdominal', 'nausea', 'vomit'],
            'dizzy': ['dizzy', 'dizziness', 'lightheaded', 'vertigo'],
            'fever': ['fever', 'temperature', 'hot', 'chills'],
            'cold': ['cold', 'flu', 'runny nose', 'sneezing', 'congestion'],
            'sore throat': ['sore throat', 'throat hurt', 'throat pain', 'swallow hurt'],
            'knee': ['knee'],
            'tired eyes': ['tired eye', 'eye strain', 'eyes tired', 'eyes feel tired', 'eye fatigue'],
            'dry eyes': ['dry eye', 'eyes dry', 'dryness in eye', 'keep eyes hydrated', 'hydrate eyes'],
            'eye pain': ['eye pain', 'eye hurt', 'pain in eye', 'eyes hurt', 'hurting eyes'],
            'back': ['back pain', 'back hurt', 'back ache', 'lower back', 'upper back']
        }
        
        # Check each symptom pattern
        for symptom_key, patterns in symptom_patterns.items():
            if any(pattern in user_input_lower for pattern in patterns):
                return symptom_key
        
        # PRIORITY 2: Check for other body part mentions that aren't in fallback
        # These will be handled by LLM with specific guidance
        body_parts = ['hand', 'ear', 'neck', 'shoulder', 'ankle', 'wrist', 'hip', 'elbow', 'foot']
        
        for part in body_parts:
            if part in user_input_lower and any(word in user_input_lower for word in 
                ['pain', 'hurt', 'ache', 'sore', 'tired', 'strain', 'stiff']):
                # Return None to force LLM response with specific guidance
                return None
        
        return None
    
    def format_fallback_response(self, symptom_key: str) -> str:
        """
        Format a fallback response using the three-part structure
        
        Args:
            symptom_key: Key from FALLBACK_RESPONSES
            
        Returns:
            Formatted response string
        """
        data = self.FALLBACK_RESPONSES[symptom_key]
        
        response = f"<strong>Direct Answer:</strong><br>{data['answer']}<br><br>"
        response += "<strong>Actionable Tips:</strong><ul>"
        for tip in data['tips']:
            response += f"<li>{tip}</li>"
        response += "</ul><strong>Home Remedies:</strong><ul>"
        for remedy in data['remedies']:
            response += f"<li>{remedy}</li>"
        response += "</ul><br><em>⚠️ I am an AI, not a doctor. Please consult a medical professional for proper diagnosis and treatment.</em>"
        
        return response


# Example usage function
def test_chatbot():
    """Test function to demonstrate usage"""
    # Initialize with your preferred provider
    # Option 1: OpenAI
    # chatbot = LLMHealthChatbot(api_provider="openai", api_key="your-openai-key")
    
    # Option 2: Gemini
    # chatbot = LLMHealthChatbot(api_provider="gemini", api_key="your-gemini-key")
    
    # Option 3: Fallback mode (for testing without API key)
    chatbot = LLMHealthChatbot(use_fallback=True)
    
    # Test queries
    test_queries = [
        "I have knee pain",
        "My eyes feel tired",
        "I have a mild headache. What should I do?",
        "I'm experiencing chest pain",  # Emergency test
        "How can I improve my sleep quality?"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        response = chatbot.get_bot_response(query)
        print(f"Bot: {response}\n")
        print("-" * 80)


if __name__ == "__main__":
    test_chatbot()
