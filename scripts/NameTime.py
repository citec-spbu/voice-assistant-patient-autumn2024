import re

# Функция для извлечения имени и времени записи из текста
def extract_name_and_time(text):
    # Извлечение имени и времени с помощью регулярных выражений
    name_match = re.search(r'([А-ЯЁ][а-яё]+)\s([А-ЯЁ][а-яё]+)', text)
    time_match = re.search(r'\b([01]?[0-9]|2[0-3]):[0-5][0-9]\b', text)

    name = name_match.group(0) if name_match else None
    time = time_match.group(0) if time_match else None

    return name, time