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
        self._recording = threading.Thread(target=self.__record, args=(lambda: self.state, ))
        self._recording.start()

    def __record(self, terminator):
        self._count = 0
        while terminator() == 'recording':
            print('recording {:d}'.format(self._count))
            self._data = sounddevice.rec(int(60 * 44100), 44100, 2)
            sounddevice.wait()
            print('recorded {:d}'.format(self._count))
            wavfile.write(str(self._file_path) + str(self._count) + '.wav', sounddevice.default.samplerate, self._data)
            self._count += 1
        print('written {:d}'.format(self._count))
        # self._recording.join()

    def _stop(self):
        self.state = 'ready'
        print('stopping')
        sounddevice.stop()
        print('stopped')
        self._recording.join()
        # print(self._data)


if __name__ == '__main__':
    recoder = LinuxAudio()
    recoder.start()
    import time
    time.sleep(1)
    recoder.stop()

