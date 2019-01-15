from plyer.facades import Audio
from plyer.utils import whereis_exe
import sounddevice
import multiprocessing
import threading
from scipy.io import wavfile


class LinuxAudio(Audio):
    sounddevice.default.samplerate = 44100
    sounddevice.default.channels = 2
    _data = None
    _count = None
    _file_path = '/home/manthan/Git/plyer/'
    _recording = None

    def _start(self):
        self.state = 'recording'
        self._recording = threading.Thread(target=self.__record, args=[lambda: self.state, ])
        self._recording.start()

    def __record(self, terminator):
        self._count = 0
        state = terminator()
        while state == 'recording':
            print(state)
            print(self._count)
            self._data = sounddevice.rec(int(10 * 44100), 44100, 2)
            sounddevice.wait()
            wavfile.write(str(self._file_path) + str(self._count) + '.wav', sounddevice.default.samplerate, self._data)
            self._count += 1

    def _stop(self):
        self.state = 'ready'
        # print('stopped')
        sounddevice.stop()
        wavfile.write(str(self._file_path) + str(self._count) + '.wav', sounddevice.default.samplerate, self._data)
        self._recording.join()


if __name__ == '__main__':
    recoder = LinuxAudio()
    recoder.start()
    # print(recoder._data)
    import time
    time.sleep(15)
    print('time to stop')
    recoder.stop()

