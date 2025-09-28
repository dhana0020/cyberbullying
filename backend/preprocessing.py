import re
import nltk

try:
    nltk.data.find("tokenizers/punkt")
except:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except:
    nltk.download("stopwords")

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

STOPWORDS = set(stopwords.words("english"))

def preprocess_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"http\S+", "", text)                 # remove urls
    text = re.sub(r"[^a-zA-Z0-9\s']", " ", text)        # keep alnum and apostrophe
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    return " ".join(tokens)
