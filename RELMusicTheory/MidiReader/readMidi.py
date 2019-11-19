from mxm.midifile import MidiInFile, MidiToCode
test_file = 'mary.mid'
midiIn = MidiInFile(MidiToCode(), test_file)
midiIn.read()