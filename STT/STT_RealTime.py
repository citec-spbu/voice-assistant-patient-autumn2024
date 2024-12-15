import sys

import sounddevice as sd
import queue

from vosk import Model, KaldiRecognizer

class Listener:

    def __init__(self):
        device_info = sd.query_devices(None, "input")
        self.samplerate = int(device_info["default_samplerate"])
        self.model = Model(lang="ru")
        self.q = queue.Queue()

    
    def callback(self, indata, frames, time, status):
        """Этот метод вызывается для каждого блока аудио"""
        if status:
            print(status, file=sys.stderr)
        self.q.put(bytes(indata))

    def get_speech(self):
        with sd.RawInputStream(samplerate = self.samplerate, blocksize=8000, dtype="int16", channels=1, callback=self.callback):
            rec = KaldiRecognizer(self.model, self.samplerate)
            listen = True
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    # listen = False
                    yield result
