from enum import Enum

class Sentiment(str, Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'

    def __str__(self) -> str:
        return str(self.value)

STOPWORDS = [
    'terlalu', 'saya', 'lebih', 'sangat', 'untuk', 'dan', 'yang', 'buat', 'ini',
    'banget', 'pas', 'banyak', 'bisa', 'rasa', 'di', 'sampai', 'bikin', 'butuh',
    'tapi', 'agak', 'tidak', 'jadi', 'cepat', 'cukup', 'waktu', 'dengan', 'kayak',
    'siang', 'malam', 'lagi', 'orang', 'ada', 'kalau', 'ingin', 'harus', 'antara',
    'namun', 'dari', 'akan', 'semua', 'dalam', 'sekali', 'sama', 'tetap', 'padahal',
    'luar', 'masih', 'karena', 'jika', 'setelah', 'tetapi', 'sore', 'satu', 'atau', 
    'aja', 'ke', 'punya', 'saat', 'juga', 'akhir', 'cuma', 'rumah', 'mungkin', 'bagi', 
    'tanpa', 'beberapa', 'tiap', 'pernah', 'sendiri', 'pun', 'sering', 'bahkan', 
    'bukan', 'siap', 'nih', 'hampir', 'sudah', 'doang', 'asal', 'hanya', 'apalagi', 
    'dulu', 'deh', 'kira', 'walau', 'masuk', 'salah', 'pada', 'putih', 'oleh', 'mana', 
    'dapet', 'apa', 'jangan', 'bakal', 'itu', 'mereka', 'sebenarnya', 'sekitarnya', 
    'begitu', 'ya', 'siapa', 'kami', 'kamu', 'aku'
]
