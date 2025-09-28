# Minimal alerts: in-app (print) + optional email (commented)
def send_in_app_alert(user_id, message, risk_score):
    # in production you'd push websocket or show a popup in UI
    print(f"[IN-APP ALERT] user={user_id} risk={risk_score:.2f} message={message}")

# optional: implement send_alert_email() if you want SMTP alerts (configure credentials)
def send_alert_email(user_id, message, risk_score):
    # placeholder - implement using smtplib if needed
    pass
