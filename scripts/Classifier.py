def classify_request(text):
    category = model.predict([text])[0]
    return category