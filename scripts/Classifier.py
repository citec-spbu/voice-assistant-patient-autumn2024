# Классификатор для обработки запросов
def classify_request(text, model):
    category = model.predict([text])[0]
    return category