import os
import requests
from config import PERSPECTIVE_API_KEY, DEV_MODE

# Simple fallback keyword-based detector for dev
KEYWORDS = [
    # Basic insults
    "stupid", "idiot", "useless", "hate", "die", "fool", "dumb", "suck", "trash",
    "jerk", "loser", "pathetic", "worthless", "garbage", "scum", "moron",
    "clown", "pig", "donkey", "dog", "ugly", "liar", "fake", "cheater", "coward",

    # Commands / aggression
    "shut up", "get lost", "go away", "drop dead", "get out", "buzz off",
    "fuck off", "leave me alone", "nobody likes you", "no one likes you",

    # Threats / violence
    "kill", "kill yourself", "go kill yourself", "i will kill you", "stab you",
    "shoot you", "beat you", "hurt you", "destroy you", "smash you",
    "break your neck", "burn you", "bury you", "wipe you out", "ruin you",

    # Strong insults / profanity
    "fuck", "fucking", "shit", "asshole", "dick", "bitch", "slut", "whore",
    "piss off", "crap", "damn", "hell", "screw you", "son of a bitch",

    # Negativity / hate
    "i hate you", "you disgust me", "you make me sick", "worst", "gross",
    "dirty", "filthy", "hopeless", "lazy", "ignorant", "nasty",

    # Self-harm related
    "i want to die", "kill me", "end myself", "end my life", "suicide",
    "hang myself", "i hate my life", "life sucks", "cut myself",
    "i want to end it", "no reason to live"
]
def _keyword_score(text: str) -> float:
    text = text.lower()
    hits = sum(text.count(k) for k in KEYWORDS)
    # normalize: 0..1
    return min(1.0, hits / 3.0)

def analyze_toxicity(text: str) -> float:
    """
    Returns toxicity score in [0,1].
    If PERSPECTIVE_API_KEY is configured and DEV_MODE is False, it calls Perspective API.
    Else returns a quick local heuristic score.
    """
    text = (text or "").strip()
    if not text:
        return 0.0

    if PERSPECTIVE_API_KEY and not DEV_MODE:
        url = "https://commentanalyzer.googleapis.com/v1/comments:analyze"
        data = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {"TOXICITY": {}}
        }
        try:
            r = requests.post(url, params={"key": PERSPECTIVE_API_KEY}, json=data, timeout=5)
            r.raise_for_status()
            resp = r.json()
            return float(resp["attributeScores"]["TOXICITY"]["summaryScore"]["value"])
        except Exception:
            # fallback if API fails
            return _keyword_score(text)
    else:
        return _keyword_score(text)
