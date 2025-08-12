"""
course_cs_full.py
Курс: Computer science для новичков
Фазы: 1 - Outcomes & Skills, 2 - Skill Modules, 3 - Final Review & Export
Версия без colorama, расширенный финальный тест с подсчётом и сохранением.
"""

import json
import textwrap
import os

# Переменные настроек
COURSE_TITLE = "Computer science для новичков"
MAX_WORDS = 500
CONFIRM = True  # спрашивать ли подтверждение после каждого этапа


# ======= Данные курса =======

OUTCOMES = [
    {"id": "1", "title": "Понимать базовые понятия информатики", "validation": "✅ понятия ясны"},
    {"id": "2", "title": "Уметь писать простые программы на Python", "validation": "✅ программы работают"},
    {"id": "3", "title": "Развивать алгоритмическое мышление", "validation": "✅ задачи решаются"},
    {"id": "4", "title": "Понимать алгоритмы и их эффективность", "validation": "✅ оценка дана"},
]

SKILLS = [
    {"id": "1.1", "title": "Определять базовые термины информатики", "outcome": "1"},
    {"id": "1.2", "title": "Различать виды данных", "outcome": "1"},
    {"id": "2.1", "title": "Писать простые скрипты на Python", "outcome": "2"},
    {"id": "2.2", "title": "Использовать условные операторы", "outcome": "2"},
    {"id": "3.1", "title": "Анализировать задачи", "outcome": "3"},
    {"id": "3.2", "title": "Выбирать стратегию решения", "outcome": "3"},
    {"id": "4.1", "title": "Понимать алгоритмы поиска", "outcome": "4"},
    {"id": "4.2", "title": "Оценивать сложность алгоритмов", "outcome": "4"},
]

ALIGNMENT = [
    {"outcome": "1", "skills": ["1.1", "1.2"], "justification": "Основы для понимания информатики."},
    {"outcome": "2", "skills": ["2.1", "2.2"], "justification": "Навыки кодирования и условных операторов."},
    {"outcome": "3", "skills": ["3.1", "3.2"], "justification": "Развитие алгоритмического мышления."},
    {"outcome": "4", "skills": ["4.1", "4.2"], "justification": "Понимание алгоритмов и сложности."},
]


def wait_continue():
    input("\nНажмите Enter для продолжения...")


def print_header(text):
    print("\n" + "=" * 80)
    print(text)
    print("=" * 80 + "\n")


# === PHASE 1 ===

def phase1_outcomes():
    print_header("PHASE 1.1 — Course Outcomes")
    print("| Outcome # | Proposed Outcome                  | Validation      |")
    print("|-----------|---------------------------------|-----------------|")
    for o in OUTCOMES:
        val = o.get("validation", "❌ не подтверждено")
        print(f"| {o['id']:<9}| {o['title']:<33}| {val:<15}|")
    if CONFIRM:
        wait_continue()


def phase1_skills():
    print_header("PHASE 1.2 — Key Skills")
    print("| Skill # | Skill Description                  | Outcome # |")
    print("|---------|----------------------------------|-----------|")
    for s in SKILLS:
        print(f"| {s['id']:<7}| {s['title']:<32}| {s['outcome']:<9}|")
    if CONFIRM:
        wait_continue()


def phase1_alignment():
    print_header("PHASE 1.3 — Outcome–Skill Alignment")
    print("| Outcome # | Outcome Description               | Supporting Skills | Justification                  |")
    print("|-----------|----------------------------------|-------------------|-------------------------------|")
    for a in ALIGNMENT:
        outcome = next(o["title"] for o in OUTCOMES if o["id"] == a["outcome"])
        skills_str = ", ".join(a["skills"])
        print(f"| {a['outcome']:<9}| {outcome:<32}| {skills_str:<17}| {a['justification']:<29}|")
    if CONFIRM:
        wait_continue()


# === PHASE 2 ===

def skill_module(skill_num, objective, content, claims, reasoning, practice_q, practice_a, test_q, test_a):
    print_header(f"Skill {skill_num}")
    print("Objective: " + objective + "\n")
    print(textwrap.fill(content, width=80) + "\n")
    print("Knowledge Claims:")
    for c in claims:
        print(f" - {c}")
    print("\nReasoning & Assumptions:")
    print(textwrap.fill(reasoning, width=80))

    if CONFIRM:
        wait_continue()

    print("\n--- Практика ---")
    ans = input(practice_q + " ").strip().lower()
    if ans == practice_a.lower():
        print("✅ Верно!")
    else:
        print(f"❌ Неверно. Правильный ответ: {practice_a}")

    if CONFIRM:
        wait_continue()

    print("\n--- Тест ---")
    ans = input(test_q + " ").strip().lower()
    if ans == test_a.lower():
        print("✅ Верно!")
    else:
        print(f"❌ Неверно. Правильный ответ: {test_a}")

    if CONFIRM:
        wait_continue()


def phase2_modules():
    print_header("PHASE 2 — Skill Modules")

    skill_module(
        "1.1",
        "Определять базовые термины информатики.",
        "Этот модуль поможет понять ключевые термины: алгоритм, данные, переменная, цикл. "
        "Знание этих понятий необходимо для изучения информатики и программирования.",
        [
            "[✅] Термины определены корректно — основа для понимания.",
            "[✅] Базовая терминология упрощает обучение последующим темам."
        ],
        "Предполагается, что студент ранее не имел опыта в информатике. "
        "Выбор терминов соответствует начальному уровню.",
        "Вопрос: Что такое 'переменная' в программировании?",
        "контейнер для данных",
        "Тест: Алгоритм — это?",
        "набор шагов"
    )

    skill_module(
        "1.2",
        "Различать виды данных.",
        "Модуль охватывает числовые, строковые и логические типы данных, "
        "показывает примеры и применение.",
        [
            "[✅] Типы данных определены ясно.",
            "[✅] Даны практические примеры."
        ],
        "Предполагается базовое знание чисел и текста, логика объяснена на бытовых примерах.",
        "Вопрос: Тип данных True/False называется?",
        "логический",
        "Тест: 42 — это тип данных?",
        "число"
    )

    skill_module(
        "2.1",
        "Писать простые скрипты на Python.",
        "Разберём базовый синтаксис Python, вывод на экран, операции с переменными, "
        "простые арифметические вычисления.",
        [
            "[✅] Python синтаксис изложен просто.",
            "[✅] Примеры кода легко повторить."
        ],
        "Опора на предыдущие знания о переменных и данных, даём минимальный набор команд.",
        "Вопрос: Команда для вывода текста в Python?",
        "print",
        "Тест: Как объявить переменную x=5?",
        "x=5"
    )

    skill_module(
        "2.2",
        "Использовать условные операторы.",
        "Изучим if, elif, else. Примеры: проверка числа, условия в программах.",
        [
            "[✅] Операторы описаны чётко.",
            "[✅] Есть бытовые примеры."
        ],
        "Берём минимальные условия и проверку значений для простоты.",
        "Вопрос: Какой оператор для ветвления?",
        "if",
        "Тест: Что делает else?",
        "иначе"
    )

    skill_module(
        "3.1",
        "Анализировать задачи.",
        "Учимся разбивать задачу на части, выявлять входные и выходные данные.",
        [
            "[✅] Методика анализа дана.",
            "[✅] Пример задачи разобран."
        ],
        "Берём бытовые задачи и переводим в алгоритмическую форму.",
        "Вопрос: Что определяем первым при анализе?",
        "входные данные",
        "Тест: Что после входных данных?",
        "выходные данные"
    )

    skill_module(
        "3.2",
        "Выбирать стратегию решения.",
        "Сравним полный перебор, жадные алгоритмы, поиск в глубину и ширину.",
        [
            "[✅] Даны стратегии.",
            "[✅] Есть критерии выбора."
        ],
        "Приводим примеры, объясняем плюсы и минусы каждого подхода.",
        "Вопрос: Какая стратегия ищет все варианты?",
        "полный перебор",
        "Тест: Жадный алгоритм всегда оптимален?",
        "нет"
    )

    skill_module(
        "4.1",
        "Понимать алгоритмы поиска.",
        "Разберём линейный и бинарный поиск на простых примерах.",
        [
            "[✅] Алгоритмы описаны ясно.",
            "[✅] Примеры с числами."
        ],
        "Объясняем через упорядоченные и неупорядоченные списки.",
        "Вопрос: Какой поиск быстрее в отсортированном массиве?",
        "бинарный",
        "Тест: Линейный поиск идёт по элементам?",
        "да"
    )

    skill_module(
        "4.2",
        "Оценивать сложность алгоритмов.",
        "Вводим Big O, сравниваем O(n), O(log n), O(1).",
        [
            "[✅] Концепция Big O объяснена.",
            "[✅] Есть примеры для сравнения."
        ],
        "Используем наглядные примеры из жизни и программирования.",
        "Вопрос: Что значит O(1)?",
        "константная",
        "Тест: O(n) растёт с увеличением n?",
        "да"
    )


# === PHASE 3 ===

PROGRESS_FILE = "course_progress.json"


def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_progress(progress):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def final_review():
    print_header("PHASE 3 — Итоговый тест и обзор")

    progress = load_progress()
    total_questions = 8
    correct_answers = 0

    questions = [
        ("Что такое алгоритм?", "набор шагов"),
        ("Какой тип данных хранит True/False?", "логический"),
        ("Как вывести текст в Python?", "print"),
        ("Какой оператор используется для ветвления?", "if"),
        ("Что определяем первым при анализе задачи?", "входные данные"),
        ("Как называется стратегия поиска всех вариантов?", "полный перебор"),
        ("Какой поиск быстрее в отсортированном массиве?", "бинарный"),
        ("Что значит O(1)?", "константная"),
    ]

    for i, (q, a) in enumerate(questions, 1):
        print(f"Вопрос {i}: {q}")
        ans = input("Ответ: ").strip().lower()
        if ans == a.lower():
            print("✅ Верно!\n")
            correct_answers += 1
            progress[f"q{i}"] = True
        else:
            print(f"❌ Неверно. Правильный ответ: {a}\n")
            progress[f"q{i}"] = False

    print(f"Результат: {correct_answers} из {total_questions} правильных.")
    if correct_answers == total_questions:
        print("Поздравляем! Вы успешно завершили курс.")
    else:
        print("Рекомендуется повторить сложные темы.")

    save_progress(progress)
    if CONFIRM:
        wait_continue()


# === Основная логика запуска ===

def main():
    print(f"Добро пожаловать в курс: {COURSE_TITLE}")
    if CONFIRM:
        input("Нажмите Enter, чтобы начать Phase 1 (Outcomes & Skills)...")

    phase1_outcomes()
    phase1_skills()
    phase1_alignment()

    if CONFIRM:
        input("Начинаем Phase 2 (Skill Modules)... Нажмите Enter...")

    phase2_modules()

    if CONFIRM:
        input("Переходим к итоговому тесту Phase 3... Нажмите Enter...")

    final_review()

    print("\nСпасибо за прохождение курса!")


if __name__ == "__main__":
    main()
