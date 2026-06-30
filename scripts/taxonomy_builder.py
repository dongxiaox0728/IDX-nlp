import os
import re
from collections import Counter

import nltk
import pandas as pd
from nltk.util import ngrams


INPUT_FILE = "data/processed/listing_sample.csv"
OUTPUT_FILE = "data/processed/top_bigrams.csv"


def download_nltk_resources():
    """
    Download tokenizer resources if they are not already installed.
    """
    try:
        nltk.data.find("tokenizers/punkt")
    except LookupError:
        nltk.download("punkt")


def clean_text(text):
    """
    Lowercase text and remove unnecessary characters.
    """
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_bigrams(text_series, top_n=200):
    """
    Extract the most common bigrams from listing remarks.
    """
    all_text = " ".join(text_series.dropna().astype(str))
    cleaned_text = clean_text(all_text)

    tokens = nltk.word_tokenize(cleaned_text)

    stop_words = {
        "the", "and", "for", "with", "this", "that", "you", "your",
        "are", "was", "were", "from", "has", "have", "had", "not",
        "but", "all", "can", "will", "home", "property", "house",
        "unit", "room", "rooms", "area", "main", "new"
    }

    tokens = [
        token for token in tokens
        if token not in stop_words and len(token) > 2
    ]

    bigram_list = list(ngrams(tokens, 2))
    freq = Counter(bigram_list)

    results = []

    for bigram, count in freq.most_common(top_n):
        phrase = " ".join(bigram)
        results.append({
            "bigram": phrase,
            "count": count
        })

    return pd.DataFrame(results)


def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"{INPUT_FILE} does not exist. "
            "Run scripts/data_loading.py first."
        )

    os.makedirs("data/processed", exist_ok=True)

    print(f"Reading {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE)

    if "remarks" not in df.columns:
        raise ValueError("The CSV file must contain a column named 'remarks'.")

    print("Extracting top bigrams...")
    bigram_df = extract_bigrams(df["remarks"], top_n=200)

    bigram_df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved top bigrams to {OUTPUT_FILE}")
    print()
    print("Top 20 bigrams:")
    print(bigram_df.head(20).to_string(index=False))


if __name__ == "__main__":
    download_nltk_resources()
    main()