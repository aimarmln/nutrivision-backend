import tensorflow as tf
import pickle
import re

model = tf.keras.models.load_model('models_ml/sentiment_analysis_model.h5')

with open('models_ml/utils/tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

stopwords = [
    'terlalu', 'saya', 'lebih', 'sangat', 'untuk', 'dan', 'yang', 'buat', 'ini',
    'banget', 'pas', 'banyak', 'bisa', 'rasa', 'di', 'sampai', 'bikin', 'butuh',
    'tapi', 'agak', 'tidak', 'jadi', 'cepat', 'cukup', 'waktu', 'dengan', 'kayak',
    'siang', 'malam', 'lagi', 'orang', 'ada', 'kalau', 'ingin', 'harus', 'antara',
    'namun', 'dari', 'akan', 'semua', 'dalam', 'sekali', 'sama', 'tetap', 'padahal'
    'luar', 'masih', 'karena', 'jika', 'setelah', 'tetapi', 'sore', 'satu', 'atau', 
    'aja', 'ke', 'punya', 'saat', 'juga', 'akhir', 'cuma', 'rumah', 'mungkin', 'bagi', 
    'tanpa', 'beberapa', 'tiap', 'pernah', 'sendiri', 'pun', 'sering', 'bahkan', 
    'bukan', 'siap', 'nih', 'hampir', 'sudah', 'doang', 'asal', 'hanya', 'apalagi', 
    'dulu', 'deh', 'kira', 'walau', 'masuk', 'salah', 'pada', 'putih', 'oleh', 'mana', 
    'dapet', 'apa', 'jangan', 'bakal', 'itu', 'mereka', 'sebenarnya', 'sekitarnya', 
    'begitu', 'ya', 'siapa', 'kami', 'kamu', 'aku'
]

def preprocess_text(text):
    text = text.replace('-', ' ')  # Ubah '-' menjadi spasi
    text = text.lower() # Lowercasing
    text = re.sub(r'[^a-zA-Z\s]', '', text) # Menghapus karakter non-alphabet 
    tokens = text.split() # Tokenizing
    filtered_tokens = [word for word in tokens if word not in stopwords] # Hapus stopwords
    return ' '.join(filtered_tokens)

def analyze_sentiment(text):
    text = preprocess_text(text)
    text_seq = tokenizer.texts_to_sequences([text])
    text_pad = tf.keras.preprocessing.sequence.pad_sequences(text_seq, maxlen=32, padding='post')
    
    prob = float(model.predict(text_pad)[0][0]) 
    sentiment = 'Positive' if prob > 0.7 else 'Negative'

    return sentiment
