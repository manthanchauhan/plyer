from plyer.facades import Audio
from plyer.utils import whereis_exe
import sounddevice
import multiprocessing
from scipy.io import wavfile


class LinuxAudio(Audio):
    sounddevice.default.samplerate = 48000
    sounddevice.default.channels = 2
    _data = None
    _count = None
    _max_size = 3600
    _file_path = '/home/manthan/Git/plyer/'

    def _start(self):
        self._state = 'recording'
        self._count = 0
        while :
            self._data = sounddevice.rec(int(10 * sounddevice.default.samplerate))
            sounddevice.wait()
            wavfile.write(str(self._file_path) + str(self._count) + '.wav', sounddevice.default.samplerate, self._data)
            self._count += 1

    def _stop(self):
        print('stopped')
        sounddevice.stop()
        wavfile.write(str(self._file_path) + str(self._count) + '.wav', sounddevice.default.samplerate, self._data)
        self._recording.terminate()


if __name__ == '__main__':
    recoder = LinuxAudio()
    recoder.start()
    import time
    time.sleep(15)
    recoder.stop()

