import re
import pickle
import keras
from typing import Literal
from app.constants.comment import STOPWORDS, Sentiment

class SentimentAnalyzer:
    def __init__(self, model_path: str, tokenizer_path: str):
        self.model: keras.Model = keras.models.load_model(model_path, compile=False)

        with open(tokenizer_path, 'rb') as f:
            self.tokenizer = pickle.load(f)

    def analyze(self, text: str) -> Literal['Positive', 'Negative']:
        text = self._preprocess_text(text) # Preprocess the text

        text_seq = self.tokenizer.texts_to_sequences([text]) # Tokenize
        text_pad = keras.preprocessing.sequence.pad_sequences(
            text_seq,
            maxlen=32,
            padding='post'
        )

        prob = float(self.model.predict(text_pad, verbose=0)[0][0]) # Predict sentiment probability

        return Sentiment.POSITIVE if prob >= 0.5 else Sentiment.NEGATIVE
    
    def _preprocess_text(self, text: str) -> str:
        text = text.replace('-', ' ')  # Replace hyphens with spaces
        text = text.lower() # Lowercasing
        text = re.sub(r'[^a-zA-Z\s]', '', text) # Remove non-alphabet characters
        tokens = text.split() # Tokenizing
        filtered_tokens = [word for word in tokens if word not in STOPWORDS] # Remove stopwords
        return ' '.join(filtered_tokens)
    