import streamlit as st
import pickle
import re
import string
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN # Changed to SimpleRNN

# 1. Setup & Downloads
nltk.download('stopwords', quiet=True)
stemmer = nltk.SnowballStemmer("english")
stopword = set(stopwords.words('english'))

# Constants based on your training
max_len = 300 
max_words = 5000

# 2. Data Cleaning Function
def data_cleaning(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('@', '', text)
    text = re.sub('ur.+', '', text)
    text = re.sub('ð.+', '', text)
    text = re.sub('\s[\s+]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    
    words = [word for word in text.split(' ') if word not in stopword]
    text = " ".join(words)
    words = [stemmer.stem(word) for word in text.split(' ')]
    text = " ".join(words)
    return text

# 3. Load Saved Artifacts 
@st.cache_resource
def load_artifacts():
    # Load Tokenizer
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
        
    # Rebuild Model Architecture with SimpleRNN
    model = Sequential()
    
    # ⚠️ CRITICAL: These numbers MUST match what you wrote in task.ipynb
    model.add(Embedding(input_dim=max_words, output_dim=100, input_length=max_len)) 
    model.add(SimpleRNN(100)) # If this fails, you might have used a different number (e.g., 64, 128)
    model.add(Dense(1, activation='sigmoid'))
    
    # Explicitly build the model with the expected input shape
    model.build(input_shape=(None, max_len))
    
    # Load the weights
    model.load_weights('.weights.h5')
    
    return tokenizer, model

tokenizer, model = load_artifacts()

# 4. Streamlit Web App Interface
st.title("Findings of Hate or Not Hate Tweets")
st.write("Enter tweet below.")

user_input = st.text_area("Input Text:")

if st.button("Predict"):
    if user_input:
        cleaned_text = data_cleaning(user_input)
        sequence = tokenizer.texts_to_sequences([cleaned_text])
        sequence_matrix = pad_sequences(sequence, maxlen=max_len)
        
        prediction = model.predict(sequence_matrix)
        
        score = prediction[0][0]
        if score >= 0.5:
            st.success(f"Positive / Class 1 (Score: {score:.4f})")
        else:
            st.error(f"Negative / Class 0 (Score: {score:.4f})")
    else:
        st.warning("Please enter some text first.")