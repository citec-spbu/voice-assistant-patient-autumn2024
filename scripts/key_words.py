   
def analyze_keywords(file_path):
    # Словари ключевых слов для различных действий
    confirmation_keywords = ["да", "согласен", "подтверждаю", "ок", "запишите"]
    reschedule_keywords = ["перенести", "другой день", "перезаписать", "позже"]
    cancellation_keywords = ["отмена", "отказ", "не надо", "отмените", "нет"]

    # Результаты анализа
    analysis_results = {
        "confirmation": False,
        "reschedule": False,
        "cancellation": False
    }

    # Открытие файла для анализа
    with open(file_path, "r", encoding="utf-8") as f:
        transcript = f.read().lower()  # Приведение к нижнему регистру для корректного анализа

    # Поиск ключевых слов
    if any(word in transcript for word in confirmation_keywords):
        analysis_results["confirmation"] = True
    if any(word in transcript for word in reschedule_keywords):
        analysis_results["reschedule"] = True
    if any(word in transcript for word in cancellation_keywords):
        analysis_results["cancellation"] = True

    return analysis_results

result = analyze_keywords("transcript.txt")
print(result)
