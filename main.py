def load_faqs(path):
    faqs = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if "|" in line:
                question, answer = line.split("|", 1)
                faqs.append((question, answer))
    return faqs


IGNORE = {"how", "to", "the", "a", "is", "are", "what", "your", "do", "i", "my", "can", "you"}


def find_answer(user_text, faqs):
    user_words = set(user_text.lower().split()) - IGNORE
    best_answer = None
    best_score = 0
    for question, answer in faqs:
        q_words = set(question.lower().split()) - IGNORE
        score = len(user_words & q_words)
        if score > best_score:
            best_score = score
            best_answer = answer
    if best_score < 2:
        return None
    return best_answer

faqs = load_faqs("faq.txt")
print("FAQ Bot. Band karne ke liye 'quit' likho.")

while True:
    text = input("You: ")
    if text.lower() == "quit":
        break
    answer = find_answer(text, faqs)
    if answer:
        print("Bot:", answer)
    else:
        print("Bot: Mujhe pata nahi, ye kisi insaan ko bhejna padega.")