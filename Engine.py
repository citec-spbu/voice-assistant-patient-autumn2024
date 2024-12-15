import STT
import NER
import TTS
from datetime import datetime

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
            entities_vocab['time'] = None
            return entities_vocab
        return entities_vocab

    def time_to_words(self, time):
        time_list = time.split(':')
        if time_list[1][0] == '0':
            time_list[1] = ' 0 ' + time_list[1][1:]
        return time_list[0] + ' ' + time_list[1]

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
                asknew = "Скажите новую дату и время."
                print(asknew)
                self.vocalize(asknew, True)
                self.status = {
                    'request' : "Запись",
                    'doctor' : self.status['doctor'], 
                    'date' : None, 
                    'time'  : None, 
                }
                call.main()
                return
            else:
                goodbye = f"До свидания."
                print(goodbye)
                self.vocalize(goodbye, True)
                return
        else:
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


if __name__ == "__main__":
    call = Engine()
    call.main()
