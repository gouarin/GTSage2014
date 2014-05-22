import numpy as np
import scipy.io.wavfile as wav


def note(frequency, length, amplitude=1, sample_rate=44100):
    """
    renvoie la sinusoide correspondant a la note representee par
    la frequence
    """
    time_points = np.linspace(0, length, length*sample_rate)
    data = np.sin(2*np.pi*frequency*time_points)
    data = amplitude*data
    return data

def kn(n):
    """
    renvoie la frequence d'une touche d'un piano compose de 88 touches
    """
    K49 = 440
    return K49*2**((n-49.)/12)

def auclairdelalune():
    partition = [52,52,52,54,56,54,
                 52,56,54,54,52,
                 52,52,52,54,56,54,
                 52,56,54,54,52,
                 54,54,54,54,49,49,
                 54,52,51,49,47,
                 52,52,52,54,56,54,
                 52,56,54,54,52]
    time = .5
    song = None
    for p in partition:
        if song is None:
            song = note(kn(p), time)
        else:
            song = np.concatenate((song, note(kn(p), time)))
    return song

if __name__ == '__main__':
    song = auclairdelalune()
    scaled = np.int16(song/np.max(np.abs(song))*32767)
    wav.write('auclair.wav', 44100, scaled)
