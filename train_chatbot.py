import random
import json
import pickle
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import numpy as np

# Download required NLTK data
print("Downloading NLTK data...")
try:
    nltk.download('punkt_tab', quiet=True)
    nltk.download('punkt', quiet=True)
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    print("NLTK data downloaded successfully!")
except Exception as e:
    print(f"NLTK download warning: {e}")

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Load intents file
intents = json.loads(open("intents.json").read())

words = []
classes = []
documents = []
ignore_letters = ["?", "!", ".", ","]

# Process the intents file
print("Processing intents...")
for intent in intents["intents"]:
    for pattern in intent["patterns"]:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent["tag"]))
        
    if intent["tag"] not in classes:
        classes.append(intent["tag"])

# Lemmatize and sort words
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

print(f"Found {len(words)} unique words and {len(classes)} classes")

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Prepare training data
print("Preparing training data...")
training = []
template = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)
    
    output_row = list(template)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffle training data
random.shuffle(training)

# ✅ FIX: Separate features and labels BEFORE creating numpy arrays
train_x = [item[0] for item in training]  # Extract feature vectors
train_y = [item[1] for item in training]  # Extract output vectors

# Convert to numpy arrays (this will work now!)
train_x = np.array(train_x)
train_y = np.array(train_y)

print(f"Training data shape: X={train_x.shape}, Y={train_y.shape}")

# Create the neural network model
print("Creating neural network model...")
model = Sequential()
model.add(Dense(256, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile the model
sgd = SGD(learning_rate=0.01, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Train the model
print("Training the model...")
hist = model.fit(train_x, train_y, epochs=200, batch_size=5, verbose=1)

# Save the model
model.save("chatbot_model.h5")

print("\n" + "="*60)
print("🎉 TRAINING COMPLETED SUCCESSFULLY! 🎉")
print("="*60)
print("Files created:")
print("✅ chatbot_model.h5")
print("✅ words.pkl") 
print("✅ classes.pkl")
print("\nNow you can run: python web_chatbot.py")
print("="*60)
