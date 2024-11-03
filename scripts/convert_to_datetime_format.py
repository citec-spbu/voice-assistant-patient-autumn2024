import dateparser

def convert_to_datetime(predicted_text):
    datetime_obj = dateparser.parse(predicted_text, settings={'PREFER_DATES_FROM': 'future'})
    return datetime_obj.strftime("%Y-%m-%d %H:%M") if datetime_obj else None

# Пример использования
predicted_text = "2024-11-04 08:30"
print(convert_to_datetime(predicted_text))