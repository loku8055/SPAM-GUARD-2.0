# SpamGuard 2.0

SpamGuard 2.0 is a Django and Chrome Extension application that classifies email text as spam or ham using TF-IDF and Multinomial Naive Bayes.

## Problem

Users need a fast, accessible way to identify suspicious email content and reduce exposure to phishing or unsolicited messages.

## Tech Stack

- Python
- Django
- Scikit-learn
- TF-IDF
- Multinomial Naive Bayes
- Pandas
- NumPy
- SQLite
- HTML, CSS, and JavaScript
- Chrome Extension Manifest V3
- KaggleHub

## Features

- Web-based spam and ham text classification
- Chrome Gmail scanning and manual analysis
- JSON classification APIs
- User authentication
- Prediction history and dashboard statistics
- 50% probability threshold for spam classification
- Scrubbed global history text for unauthenticated users

## Project Structure

```text
spam_detector/
├── manage.py
├── requirements.txt
├── spam_detector/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── spam_app/
│   ├── models.py
│   ├── views.py
│   ├── predictor.py
│   ├── urls.py
│   └── templates/
└── ml_model/
    ├── train_model.py
    ├── model.pkl
    └── vectorizer.pkl

spam_extension/
├── manifest.json
├── background.js
├── content.js
├── content.css
└── popup.html
```

## How to Run

```bash
cd spam_detector
pip install -r requirements.txt
python ml_model/train_model.py
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

To load the Chrome extension:

1. Open `chrome://extensions/`.
2. Enable Developer Mode.
3. Select the `spam_extension` directory.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Main dashboard |
| `POST` | `/predict/` | Web form classification |
| `POST` | `/classify/` | JSON text classification |
| `POST` | `/api/detect/` | Chrome extension classification |
| `GET` | `/history/` | Recent prediction data |

Example request:

```bash
curl -X POST http://127.0.0.1:8000/classify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "Congratulations! You have won a prize!"}'
```

## Results

- The training script performs an 80/20 stratified train/test split with `random_state=42`.
- TF-IDF uses 5,000 features, unigram/bigram n-grams, English stop words, and sublinear TF.
- Multinomial Naive Bayes uses `alpha=0.1`.
- A message is classified as spam when its spam probability is at least 50%.
- Held-out accuracy: **Not recorded**
- Precision: **Not recorded**
- Recall: **Not recorded**
- F1-score: **Not recorded**
- Confusion matrix: **Not recorded**

The training script computes and prints these evaluation metrics when run, but the repository does not contain stored execution output.

## Screenshots to Add

- Main dashboard
- Spam prediction result
- Ham prediction result
- Prediction history
- Chrome extension popup
- Gmail warning banner
- Django login and registration screens
- Confusion matrix
- Precision-recall or ROC curve

## Future Improvements

- Store and publish reproducible evaluation metrics.
- Tune the classification threshold using validation data.
- Add cross-validation and a confusion matrix.
- Measure API latency and throughput.
- Add URL, HTML, and sender-domain preprocessing.
- Compare the classifier with Complement Naive Bayes and transformer-based models.
- Move secrets and environment-specific settings to environment variables.
