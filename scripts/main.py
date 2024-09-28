from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from MainRequestFunction import handle_request

#Словарь для хранения записей (электронная очередь)
appointments = {}

# Подготовка данных для классификации запросов
training_data = [
    ("Запишите меня на прием к врачу", "запись на прием"),
    ("Отмените запись", "отмена записи"),
    ("Есть ли у вас врач-кардиолог", "узнать есть ли такой врач"),
    ("Где находится больница", "узнать адрес больницы"),
    ("Отмена записи на прием", "отмена записи"),
    ("Какой у вас адрес", "узнать адрес больницы"),
]

# Разделение данных на примеры и метки
texts, labels = zip(*training_data)

# Построение моделиклассификации запросов
model = make_pipeline(TfidfVectorizer(), MultinomialNB())
model.fit(texts, labels)

handle_request(appointments=appointments, model=model)