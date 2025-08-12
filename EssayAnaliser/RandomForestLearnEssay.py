import pandas as pd
import re
from nltk.corpus import stopwords
from pymorphy3 import MorphAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from collections import defaultdict

# Загрузка данных (тексты отзывов о курсах и уроках)
df = pd.read_csv("moocs_stem_reviews.csv", sep=";", engine="python")

print(df.columns)  # посмотреть названия колонок

texts = df.iloc[:, 0].astype(str).tolist()  # берём первый столбец с отзывами

# Создаём метки на основе ключевых слов
positive_keywords = [
    "лучший", "отлично", "замечательный", "спасибо", "прекрасный", "хороший",
    "понравился", "отличная", "рекомендую", "супер", "классный", "потрясающий", "сойдет"
]

labels = [1 if any(word in text.lower() for word in positive_keywords) else 0 for text in texts]

# Предобработка текста
morph = MorphAnalyzer()
stop_words = set(stopwords.words('russian'))
stop_words.discard("не")
lemma_cache = defaultdict(str)

def lemmatize_token(token):
    if token not in lemma_cache:
        lemma_cache[token] = morph.parse(token)[0].normal_form
    return lemma_cache[token]

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    tokens = text.split()
    lemmas = [lemmatize_token(tok) for tok in tokens if len(tok) >= 2 and tok not in stop_words]
    return " ".join(lemmas)

cleaned_texts = [preprocess_text(t) for t in texts]

# Векторизация
vectorizer = TfidfVectorizer(max_df=0.9, min_df=1, ngram_range=(1,3), sublinear_tf=True)
X = vectorizer.fit_transform(cleaned_texts)

# Разделение данных
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Обучение модели
clf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced",
    max_features="sqrt",
    n_jobs=-1
)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

# Результаты
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, target_names=['Отрицательный', 'Положительный']))
