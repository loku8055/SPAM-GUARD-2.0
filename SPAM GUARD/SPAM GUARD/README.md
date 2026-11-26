# 🛡️ SpamGuard — AI-Powered Email Spam Detection System

A high-performance, dual-architecture AI application featuring a **Django-powered web dashboard** and a **real-time Chrome extension** for Gmail protection. Built with **Naive Bayes + TF-IDF** for millisecond-latency classification.

---

## 📁 Project Architecture

```
.
├── spam_detector/              ← Backend Enterprise App
│   ├── manage.py
│   ├── requirements.txt
│   ├── ml_model/               ← ML Engineering Artifacts
│   │   ├── train_model.py      ← Training & Export Script
│   │   ├── model.pkl           ← Serialized NB Model
│   │   └── vectorizer.pkl      ← TF-IDF Vectorizer
│   ├── spam_app/               ← Core Logic & Templates
│   │   ├── predictor.py        ← Inference Logic
│   │   ├── views.py            ← Hybrid Controller (UI + API)
│   │   └── templates/          ← Premium UI Components
│   └── spam_detector/          ← Project Configuration
│
└── spam_extension/             ← Browser Extension (MV3)
    ├── manifest.json           ← Extension Metadata
    ├── background.js           ← Service Worker (Fetch & Notify)
    ├── content.js              ← Gmail DOM Injector
    ├── content.css             ← In-Gmail UI Styling
    └── popup/                  ← Manual Analysis UI
```

---

## 🚀 Setup & Deployment

### 1. Initialize Environment & Dependencies
```bash
cd spam_detector
pip install -r requirements.txt
```

### 2. Prepare ML Model
```bash
# This script will automatically download the 190k dataset from Kaggle and train the model
python ml_model/train_model.py
```

### 3. Database Sync & Admin Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

### 4. Start the Server
```bash
python manage.py runserver
```

### 5. Install Chrome Extension
1. Open Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer Mode** (top-right).
3. Click **Load Unpacked** and select the `spam_extension/` directory.

---

## ✨ Enterprise-Grade Features

### 💻 Web Application
- **State-of-the-Art UI/UX**: Features glassmorphism cards, animated ambient blobs, and staggered `slideUpFade` entrance animations.
- **Dynamic Theme Engine**: Persistent Dark/Light mode synchronization across the entire dashboard.
- **Privacy-Centric History**: Unauthenticated users viewing the Global History see **scrubbed data** with shimmering **Skeleton Loaders** and `🔒 ENCRYPTED TEXT` badges to ensure 100% data privacy.
- **Advanced Statistics**: Real-time analytics on spam/ham ratios and total classification volume.

### 🧩 Chrome Extension
- **Gmail Auto-Scan**: Automatically detects newly opened emails in Gmail and injects a sleek, interactive prompt asking to scan.
- **Contextual Warnings**: If spam is detected, the prompt morphs into a high-visibility red warning banner directly inside the Gmail UI.
- **Manual Analyzer**: A popup interface for analyzing any text snippet on the fly.
- **Native Notifications**: Triggers system-level Chrome notifications for high-confidence spam detections.

### 🧠 The Intelligence Engine
The system uses a **Multinomial Naive Bayes** classifier paired with a **TF-IDF Vectorizer**:
- **Dataset**: Trained on a massive **190,000+ email dataset** sourced from Kaggle for extreme robustness.
- **Auto-Kaggle Sync**: Integrated with `kagglehub` to automatically fetch and train on the latest industry-standard datasets.
- **N-Grams**: Uses (1, 2) n-gram range to capture context (e.g., "winner" vs "you are a winner").
- **Sublinear Scaling**: Improves performance on long-form email text.
- **Confidence Metrics**: Returns precise probability scores for both Spam and Ham categories.

---

## 🔌 API Documentation

| Method | Endpoint | Access | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Public | Main Dashboard & History |
| `POST` | `/predict/` | User | Web Form Classification |
| `POST` | `/classify/` | Public | JSON API for external integrations |
| `POST` | `/api/detect/` | Public | Extension-optimized detection API |
| `GET` | `/history/` | Public | JSON stream of recent detections |
| `GET` | `/antigravity/` | Public | Easter Egg: Redirect to XKCD/353 |

**Example API Payload:**
```json
POST /classify/
{ "text": "Win a $1000 gift card today!" }
```

**Response:**
```json
{
  "label": "spam",
  "confidence": 98.4,
  "confidence_level": "High",
  "created_at": "May 05, 2026 15:30"
}
```

---

## 🛠️ Technical Skills Gained
- **Python**: Backend development and ML application logic.
- **Django**: Building dynamic, secure, and scalable web applications.
- **Frontend**: Responsive UI design with HTML5, CSS3 (Glassmorphism), and JavaScript.
- **Security**: Implementation of user authentication and data scrubbing for privacy.
- **Version Control**: Project management using Git & GitHub.
- **QA & Debugging**: Solving complex integration issues and performance optimization.

---

## 🚀 Extensibility
To enhance the model's accuracy:
1. Append new training samples to the dataset in `ml_model/train_model.py`.
2. Re-run the training script.
3. The server will hot-reload the updated artifacts automatically upon the next request.

---
*Created By Lokapriya R.*
