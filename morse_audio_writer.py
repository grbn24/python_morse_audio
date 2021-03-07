"""This module adds functions to convert text to morse code, morse code to time sequence morse code, and time sequence morse code to audio files"""
import sys
import numpy as np
import wavio


CODE = {' ': '_',
	"'": '.----.',
	'(': '-.--.-',
	')': '-.--.-',
	',': '--..--',
	'-': '-....-',
	'.': '.-.-.-',
	'/': '-..-.',
	'0': '-----',
	'1': '.----',
	'2': '..---',
	'3': '...--',
	'4': '....-',
	'5': '.....',
	'6': '-....',
	'7': '--...',
	'8': '---..',
	'9': '----.',
	':': '---...',
	';': '-.-.-.',
	'?': '..--..',
	'A': '.-',
	'B': '-...',
	'C': '-.-.',
	'D': '-..',
	'E': '.',
	'F': '..-.',
	'G': '--.',
	'H': '....',
	'I': '..',
	'J': '.---',
	'K': '-.-',
	'L': '.-..',
	'M': '--',
	'N': '-.',
	'O': '---',
	'P': '.--.',
	'Q': '--.-',
	'R': '.-.',
	'S': '...',
	'T': '-',
	'U': '..-',
	'V': '...-',
	'W': '.--',
	'X': '-..-',
	'Y': '-.--',
	'Z': '--..',
	'_': '..--.-'}

def convert_to_morse_code(sen, print_morse = False):
    """Function converts string to morse code, returning morse code"""
    sen = sen.upper()
    encoded_sentence = ""
    for character in sen:
        if character != " ":
            encoded_sentence += CODE[character] + " "
        else:
            encoded_sentence += "/"
    if print_morse:
        print("Sentence in morse: " + encoded_sentence)
    return encoded_sentence

def convert_morse_to_time_seq(morse):
    """Function converts morse string to time sequence, where a 1 would be a sound, and a 0 would be no sound"""
    morse = morse.replace(" ", "0 0 0 ")
    morse = morse.replace("/", "0 0 0 0 0 0 0 ")
    morse = morse.replace(".", "1 0 ")
    morse = morse.replace("-", "1 1 1 0 ")
    out = np.fromstring(morse, sep=" ")
    return out

def write_morse_audio(aud, filename = "0_sentence.wav"):
    """Function writes time sequence where 1 is tone, and 0 is silence to a .wav audio file"""
    dt = 0.5        # seconds per timeunit
    rate = 44100    # samples per second
    rep = round(rate*dt)
    aud = np.repeat(aud, rep)
# # Parameters
    T = aud.size/rate           # sample duration (seconds)
    f = 4*440.0       # sound frequency (Hz)# Compute waveform samples
    t = np.linspace(0, T, aud.size, endpoint=False)
    x = np.sin(2*np.pi * f * t)# Write the samples to a file
    x = np.multiply(x,aud)
    wavio.write(filename, x, rate, sampwidth=3)

def mainfun(sen):
    write_morse_audio(convert_morse_to_time_seq(convert_to_morse_code(sen,print_morse=True)))
    words = sen.split(" ")
    n = 1
    for w in words:
        w_morse = convert_to_morse_code(w)
        write_morse_audio(convert_morse_to_time_seq(w_morse), filename=(str(n)+"_"+w+".wav"))
        n += 1

if __name__ == "__main__":
    sentence = "This is morse code"
    if len(sys.argv) > 1:
        s_list = sys.argv[1:]
        sentence = " ".join(map(str,s_list))
    mainfun(sentence)
    