import os

# Danger: do not commit actual API keys to git
PERSPECTIVE_API_KEY = os.getenv("PERSPECTIVE_API_KEY", "")
DEV_MODE = os.getenv("DEV_MODE", "true").lower() in ("1", "true", "yes")
RISK_THRESHOLD = float(os.getenv("RISK_THRESHOLD", "0.5"))
