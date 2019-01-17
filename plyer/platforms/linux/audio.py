from plyer.facades import Audio
# from plyer.utils import whereis_exe
import pyaudio
import wave
import threading


class LinuxAudio(Audio):
    _chunk = 1024
    _format = pyaudio.paInt16
    _channels = 2
    _rate = 44100
    _file_path = '/home/manthan/Git/plyer/recording'
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


def instance():
    return LinuxAudio()

if __name__ == '__main__':
    recoder = LinuxAudio()
    recoder.start()
    import time
    time.sleep(3)
    recoder.stop()

