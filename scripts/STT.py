import speech_recognition as sr
from TTS import text_to_speech

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        text_to_speech("Здравствуйте, по какому вопросу вы обратились?")
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="ru-RU")
            return text
        except sr.UnknownValueError:
            text_to_speech("Не удалось распознать речь. Попробуйте еще раз.")
            return None
        except sr.RequestError as e:
            text_to_speech(f"Ошибка сервиса распознавания: {e}")
            return None