import time
from google import genai
from google.genai import errors

client = genai.Client()

MODELS = ["gemini-3.8-flash", "gemini-3.5-flash"]

with open("faq.txt", encoding="utf-8") as f:
    faq_text = f.read()


def ask_ai(prompt):
    for attempt in range(3):
        for model in MODELS:
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return response.text.strip()
            except errors.ServerError:
                print("(Server busy hai, dobara koshish kar raha hoon...)")
            except errors.ClientError as e:
                print("(Model", model, "nahi chala:", e.code, ")")
        time.sleep(5)
    return None


print("AI FAQ Bot. Band karne ke liye 'quit' likho.")

while True:
    text = input("You: ")
    if text.lower() == "quit":
        break

    prompt = f"""Tum ek support bot ho.
Sirf neeche di gayi FAQ list se jawab do.
Agar jawab list mein nahi hai, to sirf ye ek word likho: NOT_FOUND

FAQ list:
{faq_text}

Sawaal: {text}"""

    answer = ask_ai(prompt)

    if answer is None:
        print("Bot: Abhi AI se jawab nahi mil raha, thodi der baad try karo.")
    elif "NOT_FOUND" in answer:
        print("Bot: Mujhe pata nahi, ye kisi insaan ko bhejna padega.")
    else:
        print("Bot:", answer)