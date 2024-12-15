from datetime import datetime, timedelta

class NER_parser:

    # Основная функция для извлечения даты, времени и врача
    def parse(self, text):
        # Поиск типа запроса
        request = self.extract_response(text)
        # Поиск врача
        doctor = self.extract_doctor(text)
        # Поиск даты
        date, text = self.text_to_date(text)
        # Поиск времени
        time, text = self.text_to_time(text)

        if date:
            int_date = int(date.split(".")[0]) + (30 * int(date.split(".")[1])) # Дата в виде целого числа
            today_date = datetime.now().day + datetime.now().month * 30
            if today_date > int_date:
                year = datetime.now().year + 1 # Если дата уже прошла, то добавляем год
            else:
                year = datetime.now().year
        else:
            year = datetime.now().year # Если дата не найдена, используем текущий год

        if date:
            date = f"{date}.{year}"

        # return (response, doctor, date, time)
        return {'request' : request,
                'doctor' : doctor, 
                'date' : date, 
                'time'  : time, 
                # 'new_date' : None, 
                # 'new_time' : None,
                }
    
    # Функция для извлечения типа запроса
    def extract_response(self, text):
        # Словарь запросов
        responses = [
            "записаться", "записать", "запишите", "отменить", "отмените", "перенести", "перенесите"
            ]
        text = text.lower()
        response = None
        for resp in responses:
            if resp in text:
                if resp in ["записаться", "записать", "запишите"]:
                    response = "Запись"
                elif resp in ["отменить", "отмените"]:
                    response = "Отмена"
                else:
                    response = "Перенос"
        return response  

    # Функция для извлечения врача из текста
    def extract_doctor(self, text):
        # Словарь врачей
        doctors = [
            "хирург", "терапевт", "кардиолог", "невролог", "стоматолог", "офтальмолог",
            "отоларинголог", "педиатр", "уролог", "гинеколог", "эндокринолог", "химиотерапевт",
            "психолог", "дерматолог"
            ]
        text = text.lower()
        doctor = None
        for doctor_name in doctors:
            if doctor_name in text:
                doctor = doctor_name
                break
        return doctor

    # Функция для извлечения даты из текста
    def text_to_date(self, text):
        # Словарь для дней месяца с учётом склонений
        days = {
            "первое": 1, "первого": 1, "первым": 1,
            "второе": 2, "второго": 2, "вторым": 2,
            "третье": 3, "третего": 3, "третим": 3,
            "четвёртое": 4, "четвёртого": 4, "четвёртым": 4,
            "пятое": 5, "пятого": 5, "пятым": 5,
            "шестое": 6, "шестого": 6, "шестым": 6,
            "седьмое": 7, "седьмого": 7, "седьмым": 7,
            "восьмое": 8, "восьмого": 8, "восьмым": 8,
            "девятое": 9, "девятого": 9, "девятым": 9,
            "десятое": 10, "десятого": 10, "десятым": 10,
            "одиннадцатое": 11, "одиннадцатого": 11, "одиннадцатым": 11,
            "двенадцатое": 12, "двенадцатого": 12, "двенадцатым": 12,
            "тринадцатое": 13, "тринадцатого": 13, "тринадцатым": 13,
            "четырнадцатое": 14, "четырнадцатого": 14, "четырнадцатым": 14,
            "пятнадцатое": 15, "пятнадцатого": 15, "пятнадцатым": 15,
            "шестнадцатое": 16, "шестнадцатого": 16, "шестнадцатым": 16,
            "семнадцатое": 17, "семнадцатого": 17, "семнадцатым": 17,
            "восемнадцатое": 18, "восемнадцатого": 18, "восемнадцатым": 18,
            "девятнадцатое": 19, "девятнадцатого": 19, "девятнадцатым": 19,
            "двадцатое": 20, "двадцатого": 20, "двадцатым": 20,
            "двадцать первое": 21, "двадцать первого": 21, "двадцать первым": 21,
            "двадцать второе": 22, "двадцать второго": 22, "двадцать вторым": 22,
            "двадцать третье": 23, "двадцать третьего": 23, "двадцать третьим": 23,
            "двадцать четвёртое": 24, "двадцать четвёртого": 24, "двадцать четвёртым": 24,
            "двадцать пятое": 25, "двадцать пятого": 25, "двадцать пятым": 25,
            "двадцать шестое": 26, "двадцать шестого": 26, "двадцать шестым": 26,
            "двадцать седьмое": 27, "двадцать седьмого": 27, "двадцать седьмым": 27,
            "двадцать восьмое": 28, "двадцать восьмого": 28, "двадцать восьмым": 28,
            "двадцать девятое": 29, "двадцать девятого": 29, "двадцать девятым": 29,
            "тридцатое": 30, "тридцатого": 30, "тридцатым": 30,
            "тридцать первое": 31, "тридцать первого": 31, "тридцать первым": 31
            }

        # Словарь для месяцев с учётом склонений
        months = {
            "январь": 1, "января": 1, "январе": 1,
            "февраль": 2, "февраля": 2, "феврале": 2,
            "март": 3, "марта": 3, "марте": 3,
            "апрель": 4, "апреля": 4, "апреле": 4,
            "май": 5, "мая": 5, "мае": 5,
            "июнь": 6, "июня": 6, "июне": 6,
            "июль": 7, "июля": 7, "июле": 7,
            "август": 8, "августа": 8, "августе": 8,
            "сентябрь": 9, "сентября": 9, "сентябре": 9,
            "октябрь": 10, "октября": 10, "октябре": 10,
            "ноябрь": 11, "ноября": 11, "ноябре": 11,
            "декабрь": 12, "декабря": 12, "декабре": 12
            }
        text = text.lower()
        day = None
        month = None

        # Проверка на относительные даты
        if "сегодня" in text:
            date = datetime.now()
            text = text.replace("сегодня", "").strip()
        elif "послезавтра" in text:
            date = datetime.now() + timedelta(days=2)
            text = text.replace("послезавтра", "").strip()
        elif "завтра" in text:
            date = datetime.now() + timedelta(days=1)
            text = text.replace("завтра", "").strip()
        else:
            date = None

        if date:
            return date.strftime("%d.%m"), text

        # Находим день
        for key in sorted(days.keys(), key=len, reverse=True):
            if key in text:
                day = days[key]
                text = text.replace(key, "").strip() # Удаляем распознанный день из текста
                break
        # Находим месяц
        for key in sorted(months.keys(), key=len, reverse=True):
            if key in text:
                month = months[key]
                text = text.replace(key, "").strip() # Удаляем распознанный месяц
                break
        if day and month:
            return f"{day:02}.{month:02}", text
        return None, text

    # Преобразуем текстовое время в формат времени
    def text_to_time(self, text):
        # Словарь для чисел времени с учётом склонений
        times = {
            "один": 1, "одного": 1, "одним": 1,
            "два": 2, "двух": 2, "двумя": 2,
            "три": 3, "трех": 3, "тремя": 3,
            "четыре": 4, "четырех": 4, "четырьмя": 4,
            "пять": 5, "пяти": 5, "пятью": 5,
            "шесть": 6, "шести": 6, "шестью": 6,
            "семь": 7, "семи": 7, "семью": 7,
            "восемь": 8, "восьми": 8, "восьмью": 8,
            "девять": 9, "девяти": 9, "девятью": 9,
            "десять": 10, "десяти": 10, "десятью": 10,
            "одиннадцать": 11, "одиннадцати": 11, "одиннадцатью": 11,
            "двенадцать": 12, "двенадцати": 12, "двенадцатью": 12,
            "тринадцать": 13, "тринадцати": 13, "тринадцатью": 13,
            "четырнадцать": 14, "четырнадцати": 14, "четырнадцатью": 14,
            "пятнадцать": 15, "пятнадцати": 15, "пятнадцатью": 15,
            "шестнадцать": 16, "шестнадцати": 16, "шестнадцатью": 16,
            "семнадцать": 17, "семнадцати": 17, "семнадцатью": 17,
            "восемнадцать": 18, "восемнадцати": 18, "восемнадцатью": 18,
            "девятнадцать": 19, "девятнадцати": 19, "девятнадцатью": 19,
            "двадцать": 20, "двадцати": 20, "двадцатью": 20
            }

        # Словарь для минут (с учетом двухзначных чисел)
        minutes = {
            "ноль": 0, "пять": 5, "десять": 10, "пятнадцать": 15,
            "двадцать": 20, "двадцать пять": 25, "тридцать": 30,
            "тридцать пять": 35, "сорок": 40, "сорок пять": 45,
            "пятьдесят": 50, "пятьдесят пять": 55
            }
        text = text.lower()
        hour = None
        minute = None
        # Ищем время (часы) до слова "часов"
        if "час" in text:
            if "часов" in text:
                text = text.replace("часов", "час")
            time_text = text.split("час")[0].strip() # Обрезаем текст до "часов"
            for key in sorted(times.keys(), key=len, reverse=True):
                if key in time_text:
                    hour = times[key]
                    text = text.replace(time_text, "").strip() # Удаляем распознанные часы
                    break
    # Ищем минуты после слова "часов"
        if "минут" in text:
            for key in sorted(minutes.keys(), key=len, reverse=True):
                if key in text:
                    minute = minutes[key]
                    text = text.replace(key, "").strip() # Удаляем распознанные минуты
                    break
        if hour is not None:
            time_str = f"{hour:02}:00" # Начальный формат, если минут нет
            if minute is not None:
                time_str = f"{hour:02}:{minute:02}"
            return time_str, text
        return None, text

# # Пример текста
# text = "Отменить запись к хирургу двадцать пятого сентября на семь часов двадцать пять минут"

# # Извлечение даты, времени и врача
# parser = NER_parser()
# data = parser.parse(text)
# print(data)