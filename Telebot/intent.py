import asyncio
import json
import os
from typing import List, Tuple, Optional

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

FAQ_PATH = os.path.join(os.path.dirname(__file__), "faq.json")

class SemanticFAQ:
    """
    Семантический поиск ближайшего ответа по базе знаний.
    Загружает модель один раз, эмбеддинги кэширует.
    """
    def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.model_name = model_name
        self.model: Optional[SentenceTransformer] = None
        self.questions: List[str] = []
        self.answers: List[str] = []
        self.embeddings: Optional[np.ndarray] = None

    def load(self):
        with open(FAQ_PATH, "r", encoding="utf-8") as f:
            items = json.load(f)
        self.questions = [it["q"] for it in items]
        self.answers = [it["a"] for it in items]
        # Ленивое подключение модели (загрузка может занять время при первом запуске)
        self.model = SentenceTransformer(self.model_name)
        self.embeddings = self.model.encode(self.questions, convert_to_numpy=True, normalize_embeddings=True)

    def ensure_ready(self):
        if self.model is None or self.embeddings is None:
            self.load()

    def search(self, query: str, top_k: int = 1) -> Tuple[str, float]:
        self.ensure_ready()
        query_vec = self.model.encode([query], convert_to_numpy=True, normalize_embeddings=True)
        sims = cosine_similarity(query_vec, self.embeddings)[0]
        idx = int(np.argmax(sims))
        return self.answers[idx], float(sims[idx])

# Простейший фоллбек по ключевым словам — если модель не доступна
KEYWORD_FAQ = {
    ("лекция", "занят", "урок", "пары"): "Лекции проходят по понедельникам и средам с 10:00 до 12:00.",
    ("аудитор", "кабинет", "комната", "где"): "Аудитория: корпус A, кабинет 101.",
    ("экзам", "тест", "контрольн", "когда"): "Экзамен назначен на 15 августа в 14:00.",
    ("сегодня", "расписан", "пар"): "Сегодня пар нет. Следующие занятия — завтра с 10:00."
}

def keyword_fallback(text: str) -> Optional[str]:
    t = text.lower()
    for keys, ans in KEYWORD_FAQ.items():
        if any(k in t for k in keys):
            return ans
    return None
