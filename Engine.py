import STT
import NER
from datetime import datetime
import TTS
import requests

# лучше вводить 1 или 3
patient_id = int(input("Введите идентификатор пациента: "))
 
class Engine:

    def __init__(self):
        self.listener = STT.Listener()
        self.parser = NER.NER_parser()              
        self.vocalize = TTS.vocalize

        self.status = {
            'request' : None,
            'doctor' : None,
            'date' : None,
            'time'  : None,
            # 'new_date' : None, 
            # 'new_time' : None,
        }

    def date_to_words(self, date):
        day_list = ['первое', 'второе', 'третье', 'четвёртое',
            'пятое', 'шестое', 'седьмое', 'восьмое',
            'девятое', 'десятое', 'одиннадцатое', 'двенадцатое',
            'тринадцатое', 'четырнадцатое', 'пятнадцатое', 'шестнадцатое',
            'семнадцатое', 'восемнадцатое', 'девятнадцатое', 'двадцатое',
            'двадцать первое', 'двадцать второе', 'двадцать третье',
            'двадацать четвёртое', 'двадцать пятое', 'двадцать шестое',
            'двадцать седьмое', 'двадцать восьмое', 'двадцать девятое',
            'тридцатое', 'тридцать первое']
        month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
            'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
        date_list = date.split('.')
        return (day_list[int(date_list[0]) - 1] + ' ' +
            month_list[int(date_list[1]) - 1])
    

    def time_to_words(self, time):
        time_list = time.split(':')
        if time_list[1][0] == '0':
            time_list[1] = ' ноль ' + time_list[1][1:]
        return time_list[0] + ' ' + time_list[1]
    
    def get_doctors_by_specialization(self, specialization: str):
        url = "http://localhost:8000/doctors/specialization"
        params = {"specialization": specialization}
        
        try:
            # Отправляем GET-запрос на указанный URL с параметром specialization
            response = requests.get(url, params=params)
            
            # Проверяем успешный ответ
            if response.status_code == 200:
                doctors = response.json()  # Парсим ответ как JSON
                return doctors
            else:
                print(f"Ошибка: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def get_schedules_by_doctors_and_start_time(self, doctor_ids: list[int], start_time: datetime):
        url = "http://localhost:8000/schedules/filter"
        params = {
            "doctor_ids": doctor_ids,
            "start_time": start_time.isoformat()  # Преобразуем дату и время в строку формата ISO
        }
        
        try:
            # Отправляем GET-запрос с параметрами
            response = requests.get(url, params=params)
            
            # Проверяем успешный ответ
            if response.status_code == 200:
                schedules = response.json()  # Парсим ответ как JSON
                return schedules
            else:
                print(f"Ошибка: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def book_schedule(self, schedule_id: int):
        url = f"http://localhost:8000/schedules/{schedule_id}/book"  # URL для маршрута бронирования расписания
        data = {
            "schedule_id": schedule_id
        }

        try:
            # Отправляем POST-запрос с параметром schedule_id
            response = requests.put(url, json=data)

            # Проверяем успешный ответ
            if response.status_code == 200:
                schedule = response.json()  # Парсим ответ как JSON (обновленное расписание)
                print("Расписание успешно забронировано:", schedule)
                return schedule
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def create_appointment(self, patient_id: int, doctor_id: int, appointment_time: datetime):
        url = "http://localhost:8000/appointments"  # URL для создания записи о приеме

        # Создаем объект AppointmentBase с необходимыми данными
        appointment_data = {
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_time": appointment_time.isoformat()  # Преобразуем datetime в строку ISO 8601
        }

        try:
            # Отправляем POST-запрос с данными в теле запроса
            response = requests.post(url, json=appointment_data)

            # Проверяем успешный ответ
            if response.status_code == 200:
                appointment = response.json()  # Парсим ответ как JSON (созданный прием)
                print("Прием успешно создан:", appointment)
                return appointment
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def get_datetime(self, date_str, time_str):
        datetime_str = f"{date_str} {time_str}"

        datetime_format = "%d.%m.%Y %H:%M"

        appointment_datetime = datetime.strptime(datetime_str, datetime_format)
        return appointment_datetime
    
    def repeat(self):
        repeat = f"Пожалуйста, повторите запрос."
        print(repeat)
        self.vocalize(repeat, True)
        
        self.status = {
            'request' : None,
            'doctor' : None,
            'date' : None,
            'time'  : None,
            # 'new_date' : None, 
            # 'new_time' : None,
        }
        call.main()

    def main(self):
        while None in self.status.values():
            speech = next(self.listener.get_speech())
            entities = self.parser.parse(speech)
            for key in self.status:
                if self.status[key] is None and entities[key] is not None:
                    self.status[key] = entities[key]
            print(self.status.values())
            

        confirmation = f"Произведена {self.status['request']} \
            к {self.status['doctor']}у \
                на {self.date_to_words(self.status['date'])} \
                    в {self.time_to_words(self.status['time'])}. Верно?"
        print(confirmation)
        self.vocalize(confirmation, True)

        response = None
        while response is None:
            speech = next(self.listener.get_speech())
            response = self.parser.extract_yes_or_no(speech)
            print(response)
            
        if response:
            print("Получение докторов...")
            doctors = self.get_doctors_by_specialization(self.status['doctor'])
            if not doctors:
                self.vocalize("Извините, врачей с такой специализацией не найдено.", True)
                self.repeat()
                return
            
            print("Докторы: ", doctors)
            
            doctor_ids = [doctor["id"] for doctor in doctors]
            
            appoinment_time = self.get_datetime(self.status['date'], self.status['time'])
            schedules = self.get_schedules_by_doctors_and_start_time(doctor_ids, appoinment_time)
            if not schedules:
                self.vocalize("Извините, нет доступного расписания на это время.", True)
                self.repeat()
                return
            
            print("Встречи: ", schedules)
            
            schedule = schedules[0]
            bookedSchedule = self.book_schedule(schedule["id"])
            if not bookedSchedule:
                self.vocalize("Извините, нет доступного расписания на это время.", True)
                self.repeat()
                return

            appoinment = self.create_appointment(patient_id, schedule["doctor_id"], appoinment_time)

            if not appoinment:
                self.vocalize("Извините, не удалось назначить встречу.", True)
                print(f"Тип переменной patient_id: {type(patient_id).__name__}")
                # Пример вывода типа переменной
                print(f"Тип переменной doctor_ids: {type(schedule["doctor_id"]).__name__}")
                print(f"Тип переменной appoinment_time: {type(appoinment_time).__name__}")
                self.repeat()


                return

            goodbye = f"До свидания."
            print(goodbye)
            self.vocalize(goodbye, True)
            return
        else:
            self.repeat()


if __name__ == "__main__":
    call = Engine()
    call.main()
