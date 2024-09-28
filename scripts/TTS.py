import os
from gtts import gTTS
from playsound import playsound


# Модуль преобразования текста в речь
def text_to_speech(text):
    tts = gTTS(text=text, lang='ru')
    tts.save("response.mp3")
    playsound("response.mp3")
    os.remove("response.mp3")  # Удаляем файл после воспроизведения