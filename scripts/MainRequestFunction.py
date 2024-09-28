from STT import speech_to_text
from TTS import text_to_speech
from Classifier import classify_request
from NameTime import extract_name_and_time

# Основная функция обработки запросов
def handle_request(appointments, model):
    user_input = speech_to_text() # получаем запрос от пользователя
    
    if user_input:
        category = classify_request(user_input, model) # Классифицируем запрос

        if category == "запись на прием":
            # Извлекаем имя и время
            name, time = extract_name_and_time(user_input)
            if name and time:
                appointments[name] = time # Добавляем запись
                response = f"Вы записаны на {time}, {name}."
            else:
                response = "Пожалуйста, укажите ваше имя и время записи."

        elif category == "отмена записи":
            name, _ = extract_name_and_time(user_input)
            if name in appointments:
                del appointments[name] # Удаляем запись
                response = f"Ваша запись отменена, {name}"
            else:
                response = "Запись не найдена. Уточните ваше имя."
            
        elif category == "узнать есть ли такой врач":
            response = "Пожалуйста, уточните, какой врач вам нужен."

        elif category == "узнать адрес больницы":
            response = "Наш адрес: улица Ленина дом 10."

        else:
            response = "Извините, я не могу распознать ваш запрос."

        text_to_speech(response) # Озвучиваем ответ       
