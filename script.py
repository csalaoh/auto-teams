import os
import sys
from openai import OpenAI

def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Hiba: Az OPENAI_API_KEY környezeti változó nincs beállítva.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    raw_messages = """
    - [10:15] Kovács Péter: Laci, holnap lesz a tanári értekezlet a teremben?
    - [11:30] Igazgatóság: Kérlek küldjétek be a heti óraterveket péntekig.
    - [14:00] Szülő (Nagy Anna): Érdeklődnék, hogy a jövő héten lesz-e szakkör?
    """

    print("Üzenetek elemzése az OpenAI modellel...")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Te egy iskolaigazgató-helyettes asszisztense vagy. Elemezd a kapott Teams üzeneteket, kategorizáld őket, és készíts egy tömör napi összefoglalót markdown formátumban."
                },
                {
                    "role": "user",
                    "content": f"Itt vannak a mai üzenetek:\n{raw_messages}"
                }
            ],
            temperature=0.3
        )
        
        # Ha ide eljut, létrejön a summary
        summary = response.choices[0].message.content
        print("\n--- NAPI ÖSSZEFOGLALÓ ---\n")
        print(summary)

    except Exception as e:
        print(f"\nHiba történt az OpenAI hívás közben: {e}")

if __name__ == "__main__":
    main()