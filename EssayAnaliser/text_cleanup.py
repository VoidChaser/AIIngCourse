import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer

# Необходимые загрузки (один раз)
nltk.download('punkt')
nltk.download('stopwords')


def clean_text(text):
    # 1. Приведение к нижнему регистру
    text = text.lower()

    # 2. Удаление пунктуации
    text = re.sub(r'[^\w\s]', '', text)

    # 3. Удаление лишних пробелов
    text = ' '.join(text.split())

    # 4. Токенизация
    tokens = word_tokenize(text)

    # 5. Удаление стоп-слов
    stop_words = set(stopwords.words('russian'))
    tokens = [w for w in tokens if w not in stop_words]

    # 6. Лемматизация
    morph = MorphAnalyzer()
    lemmas = [morph.parse(w)[0].normal_form for w in tokens]

    # 7. Удаление чисел (если нужно)
    lemmas = [w for w in lemmas if not w.isdigit()]

    return lemmas


# Пример использования
example_essay = """
Сегодня я хочу рассказать о важности экологии. Экология - это наука, изучающая взаимодействие живых организмов и окружающей среды.
"""

cleaned = clean_text(example_essay)
print(cleaned)
