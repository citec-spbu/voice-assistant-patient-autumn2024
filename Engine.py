import STT
import NER
import TTS
import TTS
import requests
from datetime import datetime

patient_id = 1

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
    
    def check_today_time(self, entities_vocab):
        dat = datetime.now()

        time1 = str(dat).split(" ")[1].split(".")[0]
        now_time = int(time1.split(":")[0]) * 60 + int(time1.split(":")[1])
        prepared_time = int(entities_vocab['time'].split(":")[0]) * 60 + int(entities_vocab['time'].split(":")[1])

        if prepared_time < now_time:
            self.vocalize("Выберите другое время", True)
            entities_vocab['date'] = None
            entities_vocab['time'] = None
            return entities_vocab
        return entities_vocab

    def time_to_words(self, time):
        time_list = time.split(':')
        if time_list[1][0] == '0':
            time_list[1] = ' 0 ' + time_list[1][1:]
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
        
    def get_booked_schedules_by_doctors_and_start_time(self, doctor_ids: list[int], start_time: datetime):
        url = "http://localhost:8000/schedules/filter/booked"
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
        
    def unbook_schedule(self, schedule_id: int):
        url = f"http://localhost:8000/schedules/{schedule_id}/unbook"  # URL для маршрута бронирования расписания
        data = {
            "schedule_id": schedule_id
        }

        try:
            # Отправляем POST-запрос с параметром schedule_id
            response = requests.put(url, json=data)

            # Проверяем успешный ответ
            if response.status_code == 200:
                schedule = response.json()  # Парсим ответ как JSON (обновленное расписание)
                print("Бронь с расписания успешно снята:", schedule)
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
                # print("Запись успешно создана:", appointment)
                return appointment
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def get_appointments(self):
        url = "http://localhost:8000/appointments"  # URL для создания записи о приеме

        try:
            # Отправляем POST-запрос с данными в теле запроса
            response = requests.get(url)

            # Проверяем успешный ответ
            if response.status_code == 200:
                appointments = response.json()  # Парсим ответ как JSON (созданный прием)
                #print("Встречи успешно получены:", appointments)
                return appointments
            else:
                print(f"Ошибка: {response.status_code}, {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе: {e}")
            return None
        
    def delete_appointment(self, appointment_id):
        url = f"http://localhost:8000/appointments/{appointment_id}"

        try:
            # Отправляем POST-запрос с данными в теле запроса
            response = requests.delete(url)

            # Проверяем успешный ответ
            if response.status_code == 200:
                success = response.json()  # Парсим ответ как JSON (созданный прием)
                return success
            elif response.status_code == 204:  # Успешное удаление без контента
                return True
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

        }
        call.main()
    
    def update_repeat(self):
        repeat = f"Пожалуйста, повторите заново новую дату и время."
        print(repeat)
        self.vocalize(repeat, True)

        self.status = {
            'request' : "Запись",
            'doctor' : self.status['doctor'], 
            'date' : None, 
            'time'  : None, 
        }
        call.main()


    def find_first_matching_appointment(self, appointments, doctors, patient_id, appointment_time):
        if isinstance(appointment_time, str):
            appointment_time = datetime.strptime(appointment_time, '%Y-%m-%d %H:%M:%S')
        
        appointment_time_str = appointment_time.strftime('%Y-%m-%dT%H:%M:%S')
        
        doctor_ids = [doctor["id"] for doctor in doctors]
        for appointment in appointments:
            if (appointment['patient_id'] == patient_id and
                appointment['doctor_id'] in doctor_ids and
                appointment['appointment_time'] == appointment_time_str):
                # print(appointment['patient_id'])
                # print(appointment['doctor_id'])
                # print(appointment['appointment_time'])
                return appointment
        return None
    
    def find_first_matching_appointment_by_schedule(self, appointments, schedule_id):
        for appointment in appointments:
            if appointment['schedule_id'] == schedule_id:
                return appointment
        return None
    
    def create(self, patient_id):
        print("Получение докторов...")
        doctors = self.get_doctors_by_specialization(self.status['doctor'])
        if not doctors:
            self.vocalize("Извините, врачей с такой специализацией не найдено.", True)
            self.repeat()
            return

        doctor_ids = [doctor["id"] for doctor in doctors]

        print("Получение доступных встреч...")
        appoinment_time = self.get_datetime(self.status['date'], self.status['time'])
        schedules = self.get_schedules_by_doctors_and_start_time(doctor_ids, appoinment_time)
        if not schedules:
            self.vocalize("Извините, нет доступного расписания на это время.", True)
            self.repeat()
            return
        
        schedule = schedules[0]
        bookedSchedule = self.book_schedule(schedule["id"])
        if not bookedSchedule:
            self.vocalize("Извините, нет доступного расписания на это время.", True)
            self.repeat()
            return

        print("Создание встречи...")
        appoinment = self.create_appointment(patient_id, schedule["doctor_id"], appoinment_time)

        if not appoinment:
            self.vocalize("Извините, не удалось назначить встречу.", True)
            self.repeat()
            return
        

            
    def cancel(self, patient_id):
        # Получение докторов
        print("Получение докторов...")
        doctors = self.get_doctors_by_specialization(self.status['doctor'])
        if not doctors:
            self.vocalize("Извините, врачей с такой специализацией не найдено.", True)
            self.repeat()
            return

        doctor_ids = [doctor["id"] for doctor in doctors]

        # Получение доступных встреч для отмены
        print("Получение доступных встреч...")
        appointment_time = self.get_datetime(self.status['date'], self.status['time'])
        schedules = self.get_booked_schedules_by_doctors_and_start_time(doctor_ids, appointment_time)
        if not schedules:
            self.vocalize("Извините, нет доступного расписания на это время.", True)
            self.repeat()
            return
        
        schedule = schedules[0]
        # Выполняем отмену бронирования
        unbooked_schedule = self.unbook_schedule(schedule["id"])
        if not unbooked_schedule:
            self.vocalize("Извините, расписание не удалось разбронировать.", True)
            self.repeat()
            return

        # Получение назначенных встреч
        print("Получение назначенных встреч...")
        appointments = self.get_appointments()

        # Ищем соответствующую запись
        found_appointment = self.find_first_matching_appointment(appointments, doctors, patient_id, appointment_time)
        if not found_appointment:
            self.vocalize("Не удалось найти вашу запись.", True)
            self.repeat()
            return
        
        # Удаляем запись
        deleted_appointment = self.delete_appointment(found_appointment["id"])
        if not deleted_appointment:
            self.vocalize("Не удалось удалить вашу запись.", True)
            self.repeat()
            return

    def main(self):
        while None in self.status.values():
            speech = next(self.listener.get_speech())
            entities = self.parser.parse(speech)
            for key in self.status:
                if self.status[key] is None and entities[key] is not None:
                    self.status[key] = entities[key]
                if (self.status['date'] is not None) and (self.status['time'] is not None):
                    current_date = str(datetime.now()).split(" ")[0]
                    year = current_date.split("-")[0]
                    month = current_date.split("-")[1]
                    day = current_date.split("-")[2]
                    cur_date = day + "." + month + "." + year
                    if self.status['date'] == cur_date:
                        self.status = self.check_today_time(self.status)
            print(self.status.values())
            self.goodbye_printed = False 

        confirmation = f"Производится {self.status['request']} \
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
            if self.status['request'] == "Перенос":
                self.cancel(patient_id)
                # self.vocalize(f"Старая вcтреча успешно отменена.", True)

                asknew = "Скажите новую дату и время."
                print(asknew)
                self.vocalize(asknew, True)
                self.status = {
                    'request' : "Запись",
                    'doctor' : self.status['doctor'], 
                    'date' : None, 
                    'time'  : None, 
                }
                while None in self.status.values():
                    speech = next(self.listener.get_speech())
                    entities = self.parser.parse(speech)
                    for key in self.status:
                        if self.status[key] is None and entities[key] is not None:
                            self.status[key] = entities[key]
                        if (self.status['date'] is not None) and (self.status['time'] is not None):
                            current_date = str(datetime.now()).split(" ")[0]
                            year = current_date.split("-")[0]
                            month = current_date.split("-")[1]
                            day = current_date.split("-")[2]
                            cur_date = day + "." + month + "." + year
                            if self.status['date'] == cur_date:
                                self.status = self.check_today_time(self.status)
                    print(self.status.values())

                confirmation = f"Производится {self.status['request']} \
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
                    if self.status['request'] == "Запись":
                        self.create(patient_id)
                else:
                    self.update_repeat()
                self.vocalize("Запись успешно перенесена.", True)
                print("Запись успешно перенесена.")
                return
           
            elif self.status['request'] == "Отмена": 
                self.cancel(patient_id)
                self.vocalize("Запись успешно отменена.", True)
                print("Запись успешно отменена.")
            else:
                self.create(patient_id)               
                self.vocalize("Запись успешно создана.", True)
                print("Запись успешно создана.")
                
            self.vocalize("До свидания.", True)
            print("До свидания.")
        else:
                self.repeat()
                
    
        


if __name__ == "__main__":
    call = Engine()
    call.main()
