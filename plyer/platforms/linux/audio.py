from plyer.facades import Audio
import pyaudio
import wave
import threading


class LinuxAudio(Audio):
    _chunk = 1024
    _format = pyaudio.paInt16
    _channels = 2
    _rate = 44100
    _frames = []
    _recording = None

    def _start(self):
        self._recording = threading.Thread(target=self.__record, args=())
        self._recording.start()

    def __record(self):
        self._frames = []
        p = pyaudio.PyAudio()
        stream = p.open(format=self._format,
                        channels=self._channels,
                        rate=self._rate,
                        input=True,
                        frames_per_buffer=self._chunk,
                        )
        while self.state == 'recording':
            data = stream.read(self._chunk)
            self._frames.append(data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    def _save(self, filename):
        p = pyaudio.PyAudio()
        if not filename.endswith('.wav'):
            filename = filename + '.wav'
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self._channels)
        wf.setsampwidth(p.get_sample_size(self._format))
        wf.setframerate(self._rate)
        wf.writeframes(b''.join(self._frames))
        wf.close()

    def _stop(self):
        self._save(self._file_path)

    def _play(self):
        play_thread = threading.Thread(target=self.__play, args=())
        play_thread.start()

    def __play(self):
        p = pyaudio.PyAudio()
        with wave.open(self._file_path + '.wav', 'rb') as audio_file:
            stream = p.open(format=p.get_format_from_width(audio_file.getsampwidth()),
                            channels=audio_file.getnchannels(),
                            rate=audio_file.getframerate(),
                            output=True
                            )
            data = audio_file.readframes(self._chunk)
            while len(data) != 0 and self.state == 'playing':
                stream.write(data)
                data = audio_file.readframes(self._chunk)
            stream.stop_stream()
            stream.close()
        p.terminate()


def instance():
    return LinuxAudio()
