"""
ML predictor - loads trained Naive Bayes + TF-IDF model and makes predictions.
"""

import pickle
import os
import numpy as np
from pathlib import Path

_model = None
_vectorizer = None


def _load_artifacts():
    global _model, _vectorizer
    if _model is None or _vectorizer is None:
        base = Path(__file__).resolve().parent.parent / 'ml_model'
        with open(base / 'model.pkl', 'rb') as f:
            _model = pickle.load(f)
        with open(base / 'vectorizer.pkl', 'rb') as f:
            _vectorizer = pickle.load(f)


def predict(text: str) -> dict:
    """
    Returns:
        {
          'label': 'spam' | 'ham',
          'confidence': float (0-100),
          'spam_probability': float (0-100),
          'ham_probability': float (0-100),
        }
    """
    _load_artifacts()

    tfidf = _vectorizer.transform([text])
    proba = _model.predict_proba(tfidf)[0]  # [ham_prob, spam_prob]

    ham_prob = round(proba[0] * 100, 2)
    spam_prob = round(proba[1] * 100, 2)

    if spam_prob >= 50:
        label = 'spam'
        confidence = spam_prob
    else:
        label = 'ham'
        confidence = ham_prob

    return {
        'label': label,
        'confidence': round(confidence, 2),
        'spam_probability': spam_prob,
        'ham_probability': ham_prob,
    }
