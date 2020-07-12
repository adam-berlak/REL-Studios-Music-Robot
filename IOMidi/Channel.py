class Channel:

    def __init__(self, p_number = 0, p_beats = {}):
        self.current_time = 0
        self.number = p_number
        self.beats = Channel.fromDict(p_beats) if p_beats is not {} else []

    def __getitem__(self, p_index):
        if p_index not in [beat.getTime() for time in self.getBeats()]: 
            self.getBeats().add(Beat(p_index))

        return self.getBeats()[p_index]        

    @staticmethod
    def fromDict(p_beats):
        new_beats = []

        for beat in p_beats.keys():
            new_beats.append(Channel.Beat(beat, p_beats[beat]))

        return new_beats

    @staticmethod
    def toDict(p_channel):
        new_beats = {}

        for beat in p_channel.getBeats():
            new_beats[beat.getTime()] = beat.getNotes()

        return new_beats

    def updateCurrentTime(self, p_current_time):
        self.current_time = p_current_time

    def add(self, p_music_object, p_time = None):
        current_time = p_time if p_time is not None else self.getCurrentTime()
        if current_time not in self.getBeats(): self.getBeats().append(Sequencer.Channel.Beat(current_time))
        self.get(current_time).add(p_music_object)
        self.updateCurrentTime(current_time + max([note.getDuration() for note in toMidiData(p_music_object)]))

    def get(self, p_time): 
        beats = [item for item in self.getBeats() if item.getTime() == p_time]
        return beats[0] if len(beats) > 0 else None

    def getBeats(self): return self.beats
    def getNumber(self): return self.number
    def getCurrentTime(self): return self.current_time

    def setBeats(self, p_beats): self.beats = p_beats
    def setNumber(self, p_number): self.number = p_number
    def setCurrentTime(self, p_current_time): self.current_time = p_current_time

    class Beat:

        def __init__(self, p_time, p_notes = []):
            self.time = p_time
            self.notes = p_notes

        def add(self, p_music_object):
            for item in toMidiData(p_music_object):
                item.setParentSequencer(self)
                self.getNotes().append(item)

        def getTime(self): return self.time
        def getNotes(self): return self.notes

        def setTime(self, p_time): self.time = p_time
        def setNotes(self, p_notes): self.notes = p_notes