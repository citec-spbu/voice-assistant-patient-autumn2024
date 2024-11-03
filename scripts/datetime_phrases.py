import random
from datetime import datetime, timedelta
import pandas as pd

# Функция для генерации текстовых описаний даты и времени
def generate_datetime_phrases(base_date):
    phrases = []

    # Формы для дней
    days = [
        ("сегодня", base_date),
        ("завтра", base_date + timedelta(days=1)),
        ("послезавтра", base_date + timedelta(days=2)),
        ("в понедельник", base_date + timedelta(days=(0 - base_date.weekday() + 7) % 7)),
        ("во вторник", base_date + timedelta(days=(1 - base_date.weekday() + 7) % 7)),
        ("в среду", base_date + timedelta(days=(2 - base_date.weekday() + 7) % 7)),
        ("в четверг", base_date + timedelta(days=(3 - base_date.weekday() + 7) % 7)),
        ("в пятницу", base_date + timedelta(days=(4 - base_date.weekday() + 7) % 7)),
        ("в субботу", base_date + timedelta(days=(5 - base_date.weekday() + 7) % 7)),
        ("в воскресенье", base_date + timedelta(days=(6 - base_date.weekday() + 7) % 7)),
    ]

    # Форматы для времени
    times = [
        ("утром", "08:00"),
        ("днём", "12:00"),
        ("вечером", "18:00"),
        ("ночью", "23:00"),
    ]

    # Час и минута
    hours = [f"{h:02}" for h in range(8, 22)]
    minutes = ["00", "15", "30", "45"]

    # Генерация текстов и меток
    for day_text, day_date in days:
        # Простые фразы со временем суток
        for time_text, time_fixed in times:
            phrases.append((f"{day_text} {time_text}", f"{day_date.strftime('%Y-%m-%d')} {time_fixed}"))

        # Случайное время, например "в восемь тридцать"
        for hour in hours:
            for minute in minutes:
                time_text = f"в {hour} {minute}" if minute != "00" else f"в {hour}"
                phrases.append((f"{day_text} {time_text}", f"{day_date.strftime('%Y-%m-%d')} {hour}:{minute}"))
        
    # Конкретные даты, такие как "четвертого ноября"
    for day in range(1, 29):
        for month, month_name in enumerate(["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"], start=1):
            for hour in hours:
                for minute in minutes:
                    day_date = datetime(base_date.year, month, day)
                    time_text = f"в {hour} {minute}" if minute != "00" else f"в {hour}"
                    phrases.append((f"{day} {month_name} {time_text}", f"{day_date.strftime('%Y-%m-%d')} {hour}:{minute}"))
    
    return phrases

# Генерация данных
base_date = datetime.now() # базовая дата для расчетов
dataset = generate_datetime_phrases(base_date)

# Сохранение в файл для использования в обучении
df = pd.DataFrame(dataset, columns=["Text", "Label"])
df.to_csv("datetime_dataset.csv", index=False, encoding="utf-8")

print(f"Датасет с {len(dataset)} фразами успешно создан и сохранен в 'datetime_dataset.csv'.")