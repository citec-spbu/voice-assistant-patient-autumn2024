<<<<<<< HEAD
# voice-assistant-patient-autumn2024
Голосовой помощник для работы с записью пациентов/получения фидбека по телефону
=======
# TTS (Text-to-Speech) block

`TTS (Text-to-Speech) block` - поддерживает генерацию аудио (потоковую и в файл) на основе переданного текста.

## Использование CLI

```bash
╰─➤  python TTS -t {string} -p {bool}

options:
  -t {string}, --text Текст который необходимо озвучить
  -p {bool}, --pronounce {True, False} Подтвердить озвучивание, в ином случае результат запишится в mp3

Примеры использования:
  python TTS -t "Привет"
```

## Пример вызова функции

```python
from TTS import vocalize

vocalize("Привет", True)
```
>>>>>>> 3947011 (Implemented TTS block. Initial commit with only TTS block)
