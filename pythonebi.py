#Python 3.11
#The FFT Analysis is adapted from Matt Zucker's ("mzucker" functions) July 2016 Python Tuner Here:
#https://github.com/mzucker/python-tuner/blob/master/tuner.py
#I don't know how that part works on the python side of things so go check it out if you're interested!
print("Press Q to exit")
print("This program uses the keyboard 1,2,3,4 as valves, then you can buzz with a mouthpiece to control pitch")
import time
import mido
import numpy
import pyaudio
import keyboard
import python-rtmidi
outtone = 0
fundamental_note = 0
overtones = [fundamental_note, fundamental_note + 12, fundamental_note + 19, fundamental_note + 24,
             fundamental_note + 28, fundamental_note + 31, fundamental_note + 34, fundamental_note + 36,
             fundamental_note + 38, fundamental_note + 40]
skip = False
port = 0
loud = 0
freq = 0
pressure = 0
wheel = 0
info = False
msmt = False
oldtone = 0
midiport = 'Unknown'
rega = float(1.82876e-11)
regb = float(-0.00000950606)
regc = float(-1.78068)
c0 = 16
c7 = 2093
def number_to_freq(n): return 440 * 2.0 ** ((n - 69) / 12.0)
def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP
#######################################################

print("Make sure your MIDI device, microphone, and mouse are all connected before proceeding.")
ask = input("Would you like information (Fundamental Tone, Buzzing Pitch, Buzzing Volume)? Y/N:").lower()
if ask == "y" or ask == "yes":
    info = True
    print("Info On!")
if ask == "s" or ask == "skip":
    #Skip sequence skips all the options steps and sets the transposition and fundamental frequency transposition factor to 0, turns on info, and opens port #1 (the second port)
    info = True
    skip = True
    inst = 0
    transp = 0
    port = 1
if info is False:
    print("Info Off!")
def mzucker_audiostart():
    ######################################################################
    # Author:  Matt Zucker
    # Date:    July 2016
    # License: Creative Commons Attribution-ShareAlike 3.0
    #          https://creativecommons.org/licenses/by-sa/3.0/us/
    ######################################################################
    global imin,imax, buf, num_frames, FRAME_SIZE, FREQ_STEP, stream, window

    NOTE_MIN = 0
    NOTE_MAX = 127
    FSAMP = 22050  # Sampling frequency in Hz
    FRAME_SIZE = 2048   # How many samples per frame?
    FRAMES_PER_FFT = 16  # FFT takes average across how many frames?

    SAMPLES_PER_FFT = FRAME_SIZE * FRAMES_PER_FFT
    FREQ_STEP = float(FSAMP) / SAMPLES_PER_FFT

    ######################################################################
    # Ok, ready to go now.

    # Get min/max index within FFT of notes we care about.
    # See docs for numpy.rfftfreq()
    def note_to_fftbin(n): return number_to_freq(n) / FREQ_STEP

    imin = max(0, int(numpy.floor(note_to_fftbin(NOTE_MIN - 1))))
    imax = min(SAMPLES_PER_FFT, int(numpy.ceil(note_to_fftbin(NOTE_MAX + 1))))

    # Allocate space to run an FFT.
    buf = numpy.zeros(SAMPLES_PER_FFT, dtype=numpy.float32)
    num_frames = 0

    # Initialize audio
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                    channels=1,
                                    rate=FSAMP,
                                    input=True,
                                    frames_per_buffer=FRAME_SIZE)

    stream.start_stream()

    # Create Hanning window function
    window = 0.5 * (1 - numpy.cos(numpy.linspace(0, 2 * numpy.pi, SAMPLES_PER_FFT, False)))

    # Print initial text
    print('Sampling at', FSAMP, 'Hz with max resolution of', FREQ_STEP, 'Hz')

    # As long as we are getting data:
mzucker_audiostart()
def init_port_check():
    global port
    while True:
        print("Finding ports...")
        if len(midiport) == 0:
            print("No Ports Found, Please Check Ports and Restart Program")
        elif len(midiport) > 0:
            for number, letter in enumerate(midiport):
                print((int(number) + 1), letter)
            desired_port = int(input("Enter desired midi port WHOLE NUMBER (1-16): "))
            if 0 < desired_port < (int(len(midiport)) + 1) and (type(desired_port) == int):
                port = desired_port - 1
                print("Using Port #", desired_port, "| Port Name:", midiport[port], "| Mido Port #", port)
                break
            else:
                print("Invalid Port Number, Please Retry")
midiport = mido.get_output_names()
def test_chord():
    msg = mido.Message('note_on', channel=0, note=36, velocity=64)
    outport.send(msg)
    msg = mido.Message('note_on', channel=0, note=43, velocity=64)
    outport.send(msg)
    time.sleep(0.5)
    for i in range(4):
        msg = mido.Message('note_on', channel=0, note=(60 + 7 * i), velocity=64)
        outport.send(msg)
        time.sleep(0.05)
        msg = mido.Message('note_on', channel=0, note=(64 + 7 * i), velocity=64)
        outport.send(msg)
        time.sleep(0.05)
    msg = mido.Message('note_off', channel=0, note=85, velocity=64)
    outport.send(msg)
    time.sleep(0.25)
    for i in range(4):
        msg = mido.Message('note_off', channel=0, note=(81 - 7 * i), velocity=64)
        outport.send(msg)
        msg = mido.Message('note_off', channel=0, note=(85 - 7 * i), velocity=64)
        outport.send(msg)
    msg = mido.Message('note_off', channel=0, note=36, velocity=64)
    outport.send(msg)
    msg = mido.Message('note_off', channel=0, note=43, velocity=64)
    outport.send(msg)
if skip is False:
    global outport
    init_port_check()
    outport = mido.open_output(midiport[int(port)])
    test_chord()
    print("How many semitones would you like the fundamental frequency shifted from standard Bb Trombone? See README for more information")
    inst = input("Please enter an INTEGER value:")
    print("How many semitones would you like to transpose?")
    transp = input("Please enter an INTEGER value:")
elif skip is True:
    outport = mido.open_output(midiport[port])
#Functions
def mzucker_analysis():
    global pressure, freq, playing, num_frames
    # Shift the buffer down and new data in
    buf[:-FRAME_SIZE] = buf[FRAME_SIZE:]
    buf[-FRAME_SIZE:] = numpy.frombuffer(stream.read(FRAME_SIZE), numpy.int16)

    # Run the FFT on the windowed buffer
    fft = numpy.fft.rfft(buf * window)

    # Get frequency of maximum response in range
    freq = (numpy.abs(fft[imin:imax]).argmax() + imin) * FREQ_STEP

    # Console output once we have a full buffer
    num_frames += 1
    #Regression for Pyaudio volume to MIDI 1-127
    loudness = abs(max(fft))
    pressure = int(rega * numpy.square(loudness) + regb * loudness + regc)
    if pressure > 125:
        pressure = 127
    if pressure < 7 or freq < c0 or freq > c7:
        pressure = 0
        playing = False
def pos_checks():
    global fundamental_note, outtone
    if keyboard.is_pressed('1'):
        valve1 = True
    else:
        valve1 = False
    if keyboard.is_pressed('2'):
        valve2 = True
    else:
        valve2 = False
    if keyboard.is_pressed('3'):
        valve3 = True
    else:
        valve3 = False
    if keyboard.is_pressed('4'):
        valve4 = True
    else:
        valve4 = False
    #Turns the valve combinations into the fundamental tone for the overtone series
    #34 is the midi note for pedal Bb and each valve brings down the fundamental tone a certain number of semitones plus the user given transposition factor (inst).
    fundamental_note = 34 - (2 * int(valve1) + int(valve2) + 3 * int(valve3) + 5 * int(valve4)) + int(inst)
    #This is an array representing the overtone series up to the 10th harmonic
    #For Bb (All valves open/1st position) this would be: Pedal Bb, Low Bb, F, (Now above the staff) Bb, D, F, Ab, (Now really high) Bb, C, and D
    overtones = [fundamental_note, fundamental_note + 12, fundamental_note + 19, fundamental_note + 24,
                 fundamental_note + 28, fundamental_note + 31, fundamental_note + 34, fundamental_note + 36,
                 fundamental_note + 38, fundamental_note + 40]
    if freq > 0:
        # Changes buzzed frequency to note
        semitone = round(numpy.log2(freq / 440) * 12) + 69
        #Finds closest overtone note to buzzed note (semitone) and outputs it as outtone
        outtone = int(min(overtones, key=lambda x: abs(x - semitone)) + int(transp))
    elif freq == 0:
        semitone = 0
        outtone = 0
    if info is True:
        print("Fundamental:", fundamental_note, "Sounds as:", semitone, "Playing?", playing)
def midiupdates():
    global outtone, pressure, playing
    #The reason why the start message for the next note happens here as opposed to during the audio analysis is because the note needs to be refrenced with pos_checks() first
    if pressure > 7 and playing is False:
        playing = True
        newmsg = mido.Message('note_on', channel=0, note=outtone, velocity=pressure)
        outport.send(newmsg)
        if info is True:
            print("New Output", newmsg)
    if playing is False or outtone != oldtone or (pressure < oldpressure - 16):
        endmsg = mido.Message('note_off', channel=0, note=outtone, velocity=64)
        outport.send(endmsg)
        endmsg = mido.Message('note_off', channel=0, note=oldtone, velocity=64)
        outport.send(endmsg)
        playing = False
        if info is True:
            print("Changing Message")
    if playing is True:
        updates = mido.Message('aftertouch', channel=0, value=pressure)
        outport.send(updates)
        if info is True:
            print("Updating as", updates, "On Note:", outtone)
print("Starting Midi Output")
while True:
    oldtone = outtone
    oldpressure = pressure
    mzucker_analysis()
    pos_checks()
    if pressure > 7:
        midiupdates()
    if keyboard.is_pressed('p'):
        outport.panic()
    if keyboard.is_pressed('t'):
        transp = input("Enter Number of Semitones to Transpose:")
        print(transp)
    if keyboard.is_pressed('q'):
        break
stream.stop_stream()
stream.close()
outport.panic()
outport.close()
print("Program ended. Close this window once finished.")
