from flask import Flask, render_template, request
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from pymorphy3 import MorphAnalyzer

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = ' '.join(text.split())
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('russian'))
    tokens = [w for w in tokens if w not in stop_words]
    morph = MorphAnalyzer()
    lemmas = [morph.parse(w)[0].normal_form for w in tokens if not w.isdigit()]
    return lemmas

def analyze_text(lemmas):
    # Находим повторяющиеся слова
    counter = Counter(lemmas)
    common = counter.most_common(10)  # Топ-10 слов
    # Пример простой "ошибки": слова с частотой > 3 считаем повторяющимися
    repeated_words = [word for word, count in counter.items() if count > 3]
    return {
        'total_words': len(lemmas),
        'unique_words': len(set(lemmas)),
        'most_common': common,
        'repeated_words': repeated_words,
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    text = ""
    if request.method == 'POST':
        # Приоритет загрузка файла
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            text = file.read().decode('utf-8')
        else:
            text = request.form.get('text_input', '')

        lemmas = clean_text(text)
        analysis = analyze_text(lemmas)

    return render_template('index.html', analysis=analysis, text=text)

if __name__ == '__main__':
    app.run(debug=True)
