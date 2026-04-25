# nutrivision-backend

Backend API untuk NutriVision berbasis Flask, SQLAlchemy, Alembic, JWT, dan integrasi model ML.

## Project Structure

```text
.
|-- .env
|-- .gitignore
|-- AGENTS.md
|-- README.md
|-- alembic.ini
|-- main.py
|-- requirements.txt
|-- app/
|   |-- __init__.py
|   |-- config.py
|   |-- database.py
|   |-- extensions.py
|   |-- constants/
|   |   |-- __init__.py
|   |   |-- chat.py
|   |   |-- comment.py
|   |   |-- food.py
|   |   |-- food_log.py
|   |   |-- recipe.py
|   |   `-- user.py
|   |-- middlewares/
|   |   `-- uuid_middleware.py
|   |-- ml/
|   |   |-- __init__.py
|   |   |-- sentiment_analyzer.py
|   |   |-- yolo_detector.py
|   |   |-- models/
|   |   |   |-- food_detection_model.pt
|   |   |   `-- sentiment_analysis_model.h5
|   |   `-- tokenizers/
|   |       `-- sentiment_tokenizer.pkl
|   |-- models/
|   |   |-- __init__.py
|   |   |-- chat_message.py
|   |   |-- chat_session.py
|   |   |-- comment.py
|   |   |-- food.py
|   |   |-- food_log.py
|   |   |-- recipe.py
|   |   |-- serving.py
|   |   `-- user.py
|   |-- repositories/
|   |   |-- comment_repository.py
|   |   |-- food_log_repository.py
|   |   |-- food_repository.py
|   |   |-- recipe_repository.py
|   |   |-- serving_repository.py
|   |   `-- user_repository.py
|   |-- routes/
|   |   |-- __init__.py
|   |   |-- auth_routes.py
|   |   |-- comment_routes.py
|   |   |-- food_logs_routes.py
|   |   |-- food_routes.py
|   |   |-- recipe_routes.py
|   |   `-- user_routes.py
|   |-- schemas/
|   |   |-- auth_schema.py
|   |   |-- food_log_schema.py
|   |   |-- food_schema.py
|   |   |-- recipe_comment_schema.py
|   |   |-- recipe_schema.py
|   |   `-- user_schema.py
|   |-- services/
|   |   |-- __init__.py
|   |   |-- auth_service.py
|   |   |-- comment_service.py
|   |   |-- food_log_service.py
|   |   |-- food_service.py
|   |   |-- recipe_service.py
|   |   `-- user_service.py
|   `-- utils/
|       |-- __init__.py
|       |-- enum.py
|       |-- errors.py
|       |-- logger.py
|       |-- recipe.py
|       |-- responses.py
|       |-- user.py
|       `-- validation.py
`-- migrations/
	|-- README
	|-- env.py
	|-- script.py.mako
	`-- versions/
		|-- 083b78b306dd_create_initial_nutrivision_schema.py
		|-- 0ceace46c2dd_add_full_text_search_to_foods.py
		|-- 559733462727_add_servings_table_and_update_food_logs.py
		`-- e8275cb76473_add_chat_session_messages.py
```

## Notes

- Struktur di atas menampilkan file dan folder utama project.
- Folder cache seperti `__pycache__/` dan metadata Git tidak ditampilkan agar dokumentasi tetap fokus.

Mantap — struktur kamu ini **sudah level production backend yang serius** 👍
Sekarang aku bantu kamu: **next step paling logis setelah chat_sessions + chat_messages sudah ada**

---

# 🧭 POSISI KAMU SEKARANG

Kamu sudah punya:

- Users ✔
- Food system ✔
- Serving system ✔
- Food logs ✔
- Chat sessions ✔ (baru ditambah)
- Chat messages ✔

👉 Artinya kamu sekarang masuk ke tahap:

# 🚀 NEXT STAGE: “AI CHAT INTELLIGENCE LAYER”

Bukan lagi DB / schema
tapi **cara chat bekerja end-to-end**

---

# 🧠 NEXT THINGS YOU HARUS BUILD (URUTAN BENAR)

## 1. 🔥 Chat Service Layer (WAJIB FIRST)

Buat:

```
app/services/chat_service.py
```

### Tugasnya:

- handle message masuk
- ambil session (timeout)
- simpan message
- panggil AI router
- route ke food / info / edit
- simpan response assistant
- update last_activity_at

👉 ini CORE SYSTEM kamu

---

## 2. 🧠 AI ROUTER (INTENT ENGINE)

```
app/services/ai_router.py
```

Output harus minimal:

```json
{
  "intent": "log_food | query | edit_food | unknown",
  "food": "ayam goreng",
  "amount": 2,
  "unit": "potong"
}
```

👉 ini otak NutriVision

---

## 3. 🍗 FOOD RESOLUTION ENGINE (INI PENTING BANGET)

```
app/services/food_resolution_service.py
```

### tugas:

ubah:

- "ayam 2 potong"
- "ayam 100 gram"
- "nasi 1 centong"

jadi:
👉 match ke `servings`

---

### logic penting:

```
food → foods table
unit → servings.serving_unit
amount → number_of_units
```

---

## 4. 🧠 SESSION MANAGER (TIMEOUT CORE)

```
app/services/session_service.py
```

Rules:

- kalau idle > 30 menit → session baru
- Redis optional tapi sangat disarankan

---

## 5. 📡 CHAT ROUTES (FLASK ENTRY POINT)

```
app/routes/chat_routes.py
```

Endpoint minimal:

### POST /chat

```json
{
  "user_id": "...",
  "message": "ayam 2 potong",
  "session_id": null
}
```

Response:

```json
{
  "session_id": "...",
  "reply": "Oke, ayam goreng 2 potong sudah dicatat",
  "intent": "log_food"
}
```

---

### GET /chat/sessions

list session user

---

### GET /chat/sessions/<id>/messages

chat history (pagination)

---

## 6. 🧾 CHAT REPOSITORY

```
app/repositories/chat_repository.py
```

functions:

- create_session
- get_session
- save_message
- get_messages
- update_last_activity

---

## 7. ⚡ REDIS (OPTIONAL TAPI SANGAT DISARANKAN)

```
session:{user_id} → session_id
```

TTL:

```
30 menit idle
```

---

# 🧠 STRUKTUR FLOW FINAL

```text id="flow1"
User message
   ↓
Flask /chat
   ↓
Session Service (timeout check)
   ↓
Chat Message saved
   ↓
AI Router (intent detection)
   ↓
IF log_food:
      → Food Resolution Service
      → Food Log DB
IF query:
      → LLM answer
IF edit:
      → update food log
   ↓
Save assistant message
   ↓
Return response
```

---

# 🔥 YANG PALING PENTING (DESIGN DECISION)

## 1. ChatSession itu bukan "chat room"

👉 tapi **container memory**

---

## 2. ChatMessage itu source of truth

👉 semua interaksi disimpan

---

## 3. AI tidak simpan data

👉 AI cuma classifier + extractor

---

## 4. Serving system kamu itu kunci utama

👉 ini yang bikin:

- “ayam 2 potong”
- “ayam 100 gram”

jadi bisa akurat

---

# 🚀 NEXT STEP (SETELAH INI)

Kalau kamu lanjut, urutan terbaik:

## Phase 1 (core chat)

- ChatService
- SessionService
- AI Router
- Chat Routes

## Phase 2 (food intelligence)

- FoodResolutionService
- fuzzy search food (TSVECTOR already good)

## Phase 3 (UX)

- pagination chat
- session list UI
- auto title session (AI generate)

## Phase 4 (upgrade AI)

- memory summarization
- context compression
- hybrid retrieval (last messages + food logs)

---

# 💡 JAWABAN SINGKAT: “LANJUTAN KAMU APA?”

👉 Kamu sekarang HARUS mulai dari:

### ✔ `chat_service.py`

karena itu pusat sistem

---

Kalau kamu mau, aku bisa bantu step berikutnya:

### 🔥 “FULL IMPLEMENTATION ChatService + AI Router + Session Redis ready production”

atau

### 🔥 “Food resolution system (ayam 2 potong vs gram conversion)”

tinggal bilang 👍
