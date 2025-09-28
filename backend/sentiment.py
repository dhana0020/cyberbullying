from textblob import TextBlob

# If TextBlob isn't available or its corpora aren't downloaded,
# this will still work for simple polarity.

def analyze_sentiment(text: str) -> float:
    """
    Return a sentiment risk in range [0,1]:
    - we map negative polarity -> higher risk.
    TextBlob polarity: [-1, +1]. We map negative polarity to [0,1].
    """
    if not text:
        return 0.0
    tb = TextBlob(text)
    polarity = tb.sentiment.polarity  # -1 .. +1
    # negative polarity should increase risk; positive reduces it
    risk = max(0.0, -polarity)  # 0..1
    return float(risk)
