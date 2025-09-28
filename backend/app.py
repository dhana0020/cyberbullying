import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from preprocessing import preprocess_text
from toxicity import analyze_toxicity
from sentiment import analyze_sentiment
from decision import compute_risk_score, is_toxic
from database import log_message, fetch_flagged_messages
from alert import send_in_app_alert
from config import RISK_THRESHOLD, DEV_MODE

app = Flask(__name__)
CORS(app)

@app.route("/")
def health():
    return "✅ Cyberbullying Detection Backend Running"

@app.route("/monitor", methods=["POST"])
def monitor():
    """
    Expects JSON:
    { "user_id": "...", "message": "...", "timestamp": "..." }
    """
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    user_id = data.get("user_id", "unknown")
    message = data.get("message", "")
    timestamp = data.get("timestamp", "")

    clean = preprocess_text(message)
    toxicity_score = analyze_toxicity(clean)
    sentiment_score = analyze_sentiment(clean)

    # TODO: compute repetition_factor from DB/redis by counting recent offenses
    repetition_factor = 0.0

    risk_score = compute_risk_score(toxicity_score, sentiment_score, repetition_factor)
    flagged = is_toxic(risk_score)

    log_message(user_id, message, timestamp, risk_score)

    if flagged:
        send_in_app_alert(user_id, message, risk_score)

    return jsonify({"status": "processed", "risk_score": risk_score, "flagged": bool(flagged)}), 200

@app.route("/get-flagged-messages", methods=["GET"])
def get_flagged():
    # return messages with risk >= RISK_THRESHOLD (configurable)
    msgs = fetch_flagged_messages(limit=500, min_risk=RISK_THRESHOLD)
    return jsonify(msgs), 200

if __name__ == "__main__":
    # For development only
    app.run(host="127.0.0.1", port=5000, debug=True)

