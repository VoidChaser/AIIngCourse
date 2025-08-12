import openai
from apikey import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


def generate_questions(lecture_text, num_questions=5):
    prompt = (
        f"Ты — преподаватель. На основе следующего текста лекции сгенерируй "
        f"{num_questions} вопросов для проверки понимания материала. "
        f"Текст лекции:\n{lecture_text}\n\nВопросы:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7,
        n=1,
    )

    questions_text = response['choices'][0]['message']['content'].strip()
    questions = questions_text.split('\n')
    questions = [q.strip('-•0123456789. ') for q in questions if q.strip()]
    return questions

def generate_multiple_choice_question(question_text, options, correct_option):
    question = f"Вопрос: {question_text}\n"
    for idx, option in enumerate(options, start=1):
        question += f"{idx}. {option}\n"
    question += f"Правильный ответ: {correct_option}\n"
    return question

# # Пример
# mc_question = generate_multiple_choice_question(
#     "Что из перечисленного является языком программирования?",
#     ["HTML", "CSS", "Python", "SQL"],
#     "3"
# )

# print(mc_question)
#

if __name__ == "__main__":
    sample_lecture = (
        "Машинное обучение — это область искусственного интеллекта, которая "
        "дает компьютерам возможность учиться на данных без явного программирования. "
        "Основные методы включают обучение с учителем, обучение без учителя и обучение с подкреплением."
    )

    questions = generate_questions(sample_lecture, num_questions=5)
    print("Сгенерированные вопросы:")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
