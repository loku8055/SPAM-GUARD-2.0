# 🛡️ SpamGuard — Email Spam Detection System

A full-stack AI-powered spam classifier using **Naive Bayes + TF-IDF** (ML) and **Django** (web framework).

---

## 📁 Project Structure

```
spam_detector/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created on first run
│
├── spam_detector/          ← Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── spam_app/               ← Main Django app
│   ├── models.py           ← Prediction model (stores results)
│   ├── views.py            ← classify() + history() endpoints
│   ├── predictor.py        ← ML inference wrapper
│   ├── urls.py
│   ├── admin.py
│   └── templates/
│       └── spam_app/
│           └── index.html  ← Full UI
│
└── ml_model/               ← ML artifacts
    ├── train_model.py      ← Training script
    ├── model.pkl           ← Trained Naive Bayes model
    └── vectorizer.pkl      ← TF-IDF vectorizer
```

---

## 🚀 Setup & Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Train the ML model (first time only)

```bash
python ml_model/train_model.py
```

This generates `model.pkl` and `vectorizer.pkl` in the `ml_model/` directory.

### 3. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. (Optional) Create admin superuser

```bash
python manage.py createsuperuser
```

### 5. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

---

## 🔌 API Endpoints

| Method | URL          | Description                              |
|--------|--------------|------------------------------------------|
| GET    | `/`          | Main UI (classifier + history)           |
| POST   | `/classify/` | JSON API: `{"text": "your message"}`     |
| GET    | `/history/`  | Returns last 50 predictions as JSON      |
| GET    | `/admin/`    | Django admin panel                       |

### Example API call

```bash
curl -X POST http://127.0.0.1:8000/classify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You have won a prize!"}'
```

**Response:**
```json
{
  "id": 1,
  "label": "spam",
  "confidence": 84.3,
  "spam_probability": 84.3,
  "ham_probability": 15.7,
  "confidence_level": "High",
  "created_at": "May 05, 2026 10:30"
}
```

---

## 🧠 How It Works

### Machine Learning Pipeline

```
Raw Text
   ↓
TF-IDF Vectorizer
  • Converts text to numerical feature vectors
  • Uses unigrams + bigrams (ngram_range=(1,2))
  • Top 5000 features, sublinear TF scaling
   ↓
Multinomial Naive Bayes
  • Probabilistic classifier
  • P(spam|features) vs P(ham|features)
  • Returns probability for each class
   ↓
Prediction + Confidence Score
```

### Database Model (Prediction)

| Field            | Type    | Description                     |
|------------------|---------|---------------------------------|
| text             | Text    | The input email/message         |
| result           | Char    | 'spam' or 'ham'                 |
| confidence       | Float   | Winning class probability (%)   |
| spam_probability | Float   | P(spam) as percentage           |
| ham_probability  | Float   | P(ham) as percentage            |
| created_at       | DateTime| Timestamp of prediction         |

---

## 🔧 Extending the Model

To improve accuracy with your own data:

1. Add more labeled examples to `ml_model/train_model.py`
2. Re-run `python ml_model/train_model.py`
3. No server restart needed — model reloads automatically

**Recommended improvements:**
- Add more training samples (500+ per class for production)
- Try `ComplementNB` for better spam detection
- Use `GridSearchCV` to tune `alpha` parameter
- Add preprocessing (HTML stripping, URL normalization)
