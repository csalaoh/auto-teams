import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from openai import OpenAI

# 1. Ellenőrizzük az OpenAI kulcsot
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("Hiba: Az OPENAI_API_KEY környezeti változó nincs beállítva.")

client = OpenAI(api_key=api_key)

# 2. Üzenetek beolvasása külső fájlból
file_path = "teams_messages.txt"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        teams_messages = f.read()
else:
    teams_messages = "Nincsenek elérhető üzenetek a fájlban."

# 3. OpenAI hívás az összefoglalóhoz
prompt = f"""
Elemezd, kategorizáld és foglald össze az alábbi Microsoft Teams üzeneteket. 
Különítsd el a Sürgős / Fontos teendőket és a Szülői kérdéseket.

Üzenetek:
{teams_messages}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3,
)

summary_text = response.choices[0].message.content
print("Generált összefoglaló:")
print(summary_text)

# 4. E-mail küldés logikája
smtp_server = "smtp.gmail.com"
smtp_port = 587

sender_email = os.environ.get("EMAIL_USER")
sender_password = os.environ.get("EMAIL_PASSWORD")
receiver_email = os.environ.get("EMAIL_TO")

if sender_email and sender_password and receiver_email:
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Teams Napi Összefoglaló (Automata)"

    msg.attach(MIMEText(summary_text, "plain", "utf-8"))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("E-mail sikeresen elküldve!")
    except Exception as e:
        print(f"Hiba történt az e-mail küldés során: {e}")
else:
    print(
        "Figyelem: Az e-mail küldéshez szükséges környezeti változók hiányoznak."
    )