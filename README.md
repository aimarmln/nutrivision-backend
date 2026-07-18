# NutriVision Backend

NutriVision Backend adalah REST API yang dibangun menggunakan **Flask** untuk mendukung fungsionalitas aplikasi NutriVision. Aplikasi ini mengintegrasikan berbagai fitur seperti pelacakan makanan (food logging), manajemen resep, sistem *serving*, serta lapisan kecerdasan buatan (AI) yang mendukung analisis gambar makanan menggunakan *machine learning* (YOLO) dan chatbot pintar menggunakan arsitektur agen (LangGraph & Groq).

## 🚀 Fitur Utama

- **Otentikasi & Manajemen Pengguna**: Sistem registrasi, login, dan keamanan berbasis token menggunakan JWT (JSON Web Tokens).
- **Manajemen Makanan & Resep**: CRUD data makanan, *serving*, dan resep masakan.
- **Catatan Makanan (Food Logging)**: Mencatat asupan nutrisi dan makanan harian pengguna.
- **Kecerdasan Buatan & Chatbot (AI Chat Intelligence)**: Fitur percakapan pintar untuk mencatat makanan secara otomatis melalui *natural language processing*. Didukung oleh LangGraph dan Groq API.
- **Integrasi Machine Learning**:
  - **YOLO Detector**: Untuk mendeteksi dan mengenali jenis makanan dari gambar.
  - **Sentiment Analyzer**: Menganalisis sentimen terkait komentar resep atau feedback menggunakan model deep learning (TensorFlow/Keras).
- **Caching & Manajemen Sesi**: Menggunakan Redis untuk optimasi sistem chat session dan timeout.

## 🛠️ Teknologi & Library

Proyek ini dibangun menggunakan pustaka modern Python, antara lain:

- **Framework**: `Flask` (v3.1.1)
- **Database & ORM**: `SQLAlchemy` (v2.0.35), `flask_sqlalchemy`
- **Migrasi Database**: `Alembic`
- **Keamanan**: `flask_jwt_extended`, `werkzeug`
- **Data & Validasi**: `pydantic`, `pandas`
- **Kecerdasan Buatan (AI/ML)**:
  - `tensorflow` (v2.18.0) & `ultralytics` (YOLO) untuk Machine Learning / Computer Vision.
  - LLM Integrations via LangChain, LangGraph, Groq, dan API Gemini.
- **Pengolahan Gambar**: `Pillow`
- **Utilitas**: `python-dotenv` untuk konfigurasi environment.

## 📁 Struktur Proyek (Project Structure)

Proyek ini dirancang dengan arsitektur berbasis *Repository & Service Layer* untuk menjaga *Clean Code* dan memisahkan tanggung jawab (Separation of Concerns).

```text
.
├── .env.example          # Template environment variable
├── alembic.ini           # Konfigurasi Alembic untuk migrasi database
├── main.py               # Entry point untuk menjalankan aplikasi Flask
├── requirements.txt      # Daftar dependensi package Python
├── app/                  # Direktori utama aplikasi
│   ├── __init__.py       # Inisialisasi app Flask (Application Factory)
│   ├── config.py         # Konfigurasi aplikasi dari environment
│   ├── database.py       # Setup koneksi database
│   ├── extensions.py     # Inisialisasi ekstensi pihak ketiga (JWT, DB, dll.)
│   ├── agent/            # State agent config dan LangGraph checkpointers
│   ├── constants/        # Konstanta sistem (chat, food, user, dll.)
│   ├── middlewares/      # Custom middleware Flask (mis. UUID middleware)
│   ├── ml/               # Model Machine Learning & logika prediksi (YOLO, Sentiment)
│   ├── models/           # Definisi schema/model database SQLAlchemy
│   ├── repositories/     # Layer akses langsung ke database
│   ├── routes/           # Blueprints/Controller Flask untuk API endpoints
│   ├── schemas/          # Schema Pydantic untuk validasi input/output API
│   ├── services/         # Layer business logic dari aplikasi
│   └── utils/            # Fungsi bantuan, enumerasi, logger, dan error handler
└── migrations/           # Skrip riwayat migrasi database Alembic
```

## ⚙️ Persyaratan Sistem (Prerequisites)

Sebelum menjalankan backend ini, pastikan sistem Anda telah memiliki:

- **Python 3.10+**
- **PostgreSQL** (sebagai database utama)
- **Redis** (berjalan pada port 6379, untuk session chat cache)
- Akun API pihak ketiga (Groq API, LangSmith, atau HuggingFace, sesuai kebutuhan fitur).

## 🚀 Cara Menjalankan Aplikasi (How to Start)

Ikuti langkah-langkah di bawah ini untuk mengatur dan menjalankan backend NutriVision di lingkungan lokal Anda.

### 1. Kloning Repositori & Persiapkan Virtual Environment

```bash
# Clone repo (sesuaikan dengan URL repo)
git clone <url-repo-anda>
cd nutrivision-backend

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate
```

### 2. Instalasi Dependensi

Pastikan virtual environment telah aktif, lalu jalankan:

```bash
pip install -r requirements.txt
```

### 3. Konfigurasi Environment Variables

Salin file template `.env.example` menjadi `.env` dan sesuaikan kredensial Anda.

```bash
cp .env.example .env
```

Buka file `.env` dan pastikan Anda mengatur beberapa variabel kunci:
- `SECRET_KEY` & `JWT_SECRET_KEY`: Gunakan string acak yang aman.
- `DATABASE_URL`: URI koneksi ke server PostgreSQL Anda (contoh: `postgresql+psycopg2://username:password@localhost:5432/nutrivision`).
- `CHECKPOINT_DB_URL`: URI koneksi PostgreSQL untuk checkpointer AI/LangGraph.
- `GROQ_API_KEY`: Kunci API LLM Anda.
- Konfigurasi Redis, Hugging Face Token, dan konfigurasi tambahan opsional jika diperlukan.

### 4. Setup & Migrasi Database

Sebelum menjalankan server, inisialisasi schema database dan tabel Anda. Pastikan server PostgreSQL sudah berjalan dan database `nutrivision` telah dibuat.

Jalankan migrasi menggunakan Alembic:

```bash
alembic upgrade head
```

### 5. Jalankan Server Development

Setelah semua setup selesai, Anda bisa menjalankan server Flask.

```bash
python main.py
```

Server backend akan berjalan di: `http://0.0.0.0:8000`

---
*Dibuat untuk backend system aplikasi NutriVision*
