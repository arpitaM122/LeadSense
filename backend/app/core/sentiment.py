from textblob import TextBlob

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity  # -1 (negative) to +1 (positive)
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"
    return {"sentiment": sentiment, "polarity": polarity, "subjectivity": subjectivity}