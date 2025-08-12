import openai
from apikey import OPENAI_API_KEY


# Вставьте ваш OpenAI API ключ
openai.api_key = OPENAI_API_KEY

def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Ты — помощник студента."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        n=1,
        temperature=0.7,
    )
    answer = response['choices'][0]['message']['content'].strip()
    return answer

# Тестируем
if __name__ == "__main__":
    questions = [
        "Что такое машинное обучение?",
        "Объясни, как работает случайный лес.",
        "Как лучше подготовиться к экзамену по информатике?"
    ]

    for q in questions:
        print(f"Вопрос: {q}")
        print(f"Ответ: {get_gpt_response(q)}\n")
