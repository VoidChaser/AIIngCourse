# Пример сводных отзывов пяти студентов
feedback = [
    {"interface": 5, "helpfulness": 4, "difficulty": 3, "overall": 4, "comments": "Очень удобно, ИИ помогает быстро."},
    {"interface": 4, "helpfulness": 3, "difficulty": 4, "overall": 3, "comments": "Иногда подсказки неполные."},
    {"interface": 5, "helpfulness": 5, "difficulty": 2, "overall": 5, "comments": "Отличный курс, легко понимать."},
    {"interface": 3, "helpfulness": 4, "difficulty": 3, "overall": 3, "comments": "Интерфейс можно упростить."},
    {"interface": 4, "helpfulness": 4, "difficulty": 3, "overall": 4, "comments": "Хотелось бы больше примеров."},
]

# Анализ средней оценки по параметрам
def average_score(feedback, key):
    return sum(f[key] for f in feedback) / len(feedback)

print("Средняя оценка интерфейса:", average_score(feedback, "interface"))
print("Средняя оценка полезности подсказок:", average_score(feedback, "helpfulness"))
print("Средняя оценка сложности:", average_score(feedback, "difficulty"))
print("Средняя общая оценка:", average_score(feedback, "overall"))
