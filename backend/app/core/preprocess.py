import re

def clean_text(text: str) -> str:
    # Lowercase
    text = text.lower()
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
    # Remove emojis (optional, keep for sentiment)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    return text