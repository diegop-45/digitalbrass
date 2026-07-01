First make sure the microphone, midi output, and mouse are working.
There are great resources online, but I like to use LoopMidi to create a virtual midi port on my Windows computer, or alternatively connect it to a physical synthesizer.
Afterwards you will be asked:
“How many semitones would you like the fundamental frequency shifted” and “How many semitones would you like to transpose?”
The first (fundamental frequency) changes the fundamental frequency, similar to physically changing the size of the instrument. Trombone fundamental frequency corresponds to +0 meaning the player has to buzz a note as if it was on a trombone. Similarly, trumpet fundamental frequency corresponds to +12, and the player would have to buzz the mouthpiece as if it were a trumpet mouthpiece an octave higher. This CANNOT be changed after starting the program and requires a restart to change.
The second (transposition) changes the note that makes it to the midi controller AFTER the calculation for the note played is made (where it references the buzzed pitch compared to the valve combination). So if this semitone stat is set to +12, the buzzed pitch could be a Bb 2 (typically the first note learned on a trombone) then output as a Bb 3 (right below middle C). This CAN be changed after starting the program by pressing ‘t’ entering the number of semitones to change.

Known Issues:
There is currently no support for an air pressure sensor, though once I learn how to get a pressure sensor working (or someone else does pls) support will be added
Faster notes are given as a single note with multiple drops in volume for every tongue.  
I will make a better UI, add web/mobile support, and an executable once I get it to work smoother
