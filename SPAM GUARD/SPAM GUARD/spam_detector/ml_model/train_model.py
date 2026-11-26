"""
Train Naive Bayes + TF-IDF spam detection model using Kaggle dataset.
"""

import pickle
import numpy as np
import pandas as pd
import kagglehub
import os
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from pathlib import Path

# ── Fallback Dataset (Original) ────────────────────────────────────────────────
FALLBACK_SPAM = [
    "Congratulations! You've won a $1,000,000 lottery prize! Click here to claim now!",
    "FREE iPhone 15 Pro! You've been selected! Claim your prize immediately!",
    "URGENT: Your account will be suspended. Verify your details NOW or lose access forever.",
    "Make $5000 per week working from home! No experience needed! Limited spots!",
    "Hot singles in your area want to meet you tonight! Click here!",
]

FALLBACK_HAM = [
    "Hi John, can we reschedule tomorrow's 3pm meeting to Thursday? Works better for me.",
    "Please find the Q3 financial report attached. Let me know if you have questions.",
    "Reminder: Team standup at 10am tomorrow. Agenda includes sprint review and planning.",
]

def load_kaggle_data():
    """Downloads and loads the 190k Kaggle spam dataset."""
    try:
        dataset_name = "meruvulikith/190k-spam-ham-email-dataset-for-classification"
        print(f"Downloading latest dataset from Kaggle ({dataset_name})...")
        path = kagglehub.dataset_download(dataset_name)
        csv_path = os.path.join(path, "spam_Emails_data.csv")
        
        # Load the dataset
        df = pd.read_csv(csv_path)
        
        # Filter for valid labels and drop NaNs
        df = df[df['label'].str.lower().isin(['ham', 'spam'])].copy()
        df = df.dropna(subset=['label', 'text'])
        
        print(f"Loaded {len(df)} valid rows from Kaggle dataset.")
        
        # Map labels: ham -> 0, spam -> 1
        df['mapped_label'] = df['label'].str.lower().map({'ham': 0, 'spam': 1}).astype(int)
        return df['text'].astype(str).tolist(), df['mapped_label'].tolist()
    except Exception as e:
        print(f"Failed to load Kaggle data: {e}")
        print("Falling back to built-in dataset.")
        texts = FALLBACK_SPAM + FALLBACK_HAM
        labels = [1] * len(FALLBACK_SPAM) + [0] * len(FALLBACK_HAM)
        return texts, labels

def train_and_save_model():
    texts, labels = load_kaggle_data()
    
    # Combine with a few fallback samples to ensure core patterns are present
    texts.extend(FALLBACK_SPAM + FALLBACK_HAM)
    labels.extend([1] * len(FALLBACK_SPAM) + [0] * len(FALLBACK_HAM))

    print(f"Training on {len(texts)} samples...")

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        stop_words='english',
        sublinear_tf=True,
    )
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # Naive Bayes Classifier
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train_tfidf, y_train)

    # Evaluate
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    print("\nModel Training Complete!")
    print(f"   Accuracy: {accuracy:.2%}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['Ham', 'Spam'])}")

    # Save artifacts
    save_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(save_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    with open(os.path.join(save_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)

    print(f"Saved model.pkl and vectorizer.pkl to {save_dir}")
    return accuracy

if __name__ == '__main__':
    train_and_save_model()

