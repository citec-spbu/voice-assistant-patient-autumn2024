#!/usr/bin/env python3

# Требуемые пакеты: установите по инструкции на https://alphacephei.com/vosk/install, а также модуль `sounddevice` (установка: `pip install sounddevice`)
# Пример использования с русской моделью: `python test_microphone.py -m ru`
# Для справки: `python test_microphone.py -h`

import argparse
import queue
import sys
import sounddevice as sd

from vosk import Model, KaldiRecognizer

q = queue.Queue()

def int_or_str(text):
    """Помощник для парсинга аргументов."""
    try:
        return int(text)
    except ValueError:
        return text

def callback(indata, frames, time, status):
    """Этот метод вызывается для каждого блока аудио."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Параметры командной строки
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l", "--list-devices", action="store_true",
    help="показать список аудиоустройств и выйти")
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    "-f", "--filename", type=str, metavar="FILENAME",
    help="файл для сохранения записи и текста", default="transcript.txt")
parser.add_argument(
    "-d", "--device", type=int_or_str,
    help="входное устройство (ID или строка)")
parser.add_argument(
    "-r", "--samplerate", type=int, help="частота дискретизации")
parser.add_argument(
    "-m", "--model", type=str, help="языковая модель; например, en-us, ru; по умолчанию en-us")
args = parser.parse_args(remaining)

try:
    # Установка частоты дискретизации устройства
    if args.samplerate is None:
        device_info = sd.query_devices(args.device, "input")
        args.samplerate = int(device_info["default_samplerate"])
    
    # Выбор модели по аргументу или по умолчанию
    if args.model is None:
        model = Model(lang="ru")  # по умолчанию выбрана русская модель
    else:
        model = Model(lang=args.model)

    # Открытие файла для сохранения текста
    with open(args.filename, "w", encoding="utf-8") as text_file:

        # Запуск потока ввода аудио
        with sd.RawInputStream(samplerate=args.samplerate, blocksize=8000, device=args.device,
                dtype="int16", channels=1, callback=callback):
            print("#" * 80)
            print("Нажмите Ctrl+C для остановки записи")
            print("#" * 80)

            rec = KaldiRecognizer(model, args.samplerate)
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    print(result)
                    text_file.write(result + "\n")  # Запись полного результата в файл
                    text_file.flush()
                else:
                    print(rec.PartialResult())

except KeyboardInterrupt:
    print("\nЗапись завершена")
    parser.exit(0)
except Exception as e:
    parser.exit(type(e).__name__ + ": " + str(e))
 