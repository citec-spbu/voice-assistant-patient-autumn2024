#!/usr/bin/env python3
#этот скрипт реализует потоковую обработку аудио при помощи библиотеки Vosk и ffmpeg. Скрипт читает аудиоданные порциями по 4000 байт и передает их для распознавания, не дожидаясь загрузки полного файла.
import subprocess
import sys
from vosk import Model, KaldiRecognizer, SetLogLevel

SAMPLE_RATE = 16000

SetLogLevel(0)

# Загрузка модели для русского языка 
model = Model(lang="ru")

rec = KaldiRecognizer(model, SAMPLE_RATE)

# Проверка, был ли передан аргумент с путем к аудиофайлу
if len(sys.argv) < 2:
    print("Usage: python script.py <audio_file>")
    sys.exit(1)

# Открываем файл для записи финальных результатов
output_file = "transcription.txt"
with open(output_file, "w", encoding="utf-8") as text_file:
    # Использование ffmpeg для обработки аудиофайла
    with subprocess.Popen(["ffmpeg", "-loglevel", "quiet", "-i",
                           sys.argv[1],
                           "-ar", str(SAMPLE_RATE), "-ac", "1", "-f", "s16le", "-"],
                          stdout=subprocess.PIPE) as process:

        while True:
            data = process.stdout.read(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                result = rec.Result()
                print(result)  # Выводим в консоль
                # Записываем финальный результат в файл
                text_file.write(result + "\n")  
                text_file.flush()  # Обеспечиваем немедленную запись
            else:
                # Выводим промежуточный результат в консоль
                print(rec.PartialResult())  

        final_result = rec.FinalResult()
        print(final_result)  # Выводим финальный результат
        text_file.write(final_result + "\n")  # Записываем финальный результат в файл
