import wavio
import numpy as np
import sys

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
 
def convertToMorseCode(sentence):
    sentence = sentence.upper()
    encodedSentence = ""
    for character in sentence:
        if character != " ":
            encodedSentence += CODE[character] + " "
        else:
            encodedSentence += "s" 
    print(encodedSentence)
    return encodedSentence

def convertMorseToAudio(morse):
    morse = morse.replace(" ", "0 0 0 ")
    morse = morse.replace("s", "0 0 0 0 0 0 0 ")
    morse = morse.replace(".", "1 0 ")
    morse = morse.replace("-", "1 1 1 0 ")
    out = np.fromstring(morse, sep=" ");
    print(out)
    return out
    

def writeMorseAudio(aud, filename = "0zin.wav"):
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

def mainfun(zin):
    writeMorseAudio(convertMorseToAudio(convertToMorseCode(zin)))
    woorden = zin.split(" ")
    n = 1
    for w in woorden:
        writeMorseAudio(convertMorseToAudio(convertToMorseCode(w)), filename=(str(n)+"_"+w+".wav"))
        print(w)
        n += 1

zin = "Ruimte Fuifje Alle Welpen Welkom Zomer"
if len(sys.argv) > 1:
    zin_list = sys.argv[1:]
    zin = " ".join(map(str,zin_list))
    print(type(zin_list))
mainfun(zin)
    