import random
import operator

from collections import Counter
from TheoryCollections.IntervalListUtilities import *
from IOMidi.Sequencer import *
from IOMidi.MidiToObjects import *

class Analyser:

    def __init__(self, p_sequencer, p_seed):
        random.seed(p_seed)
        self.sequencer = p_sequencer
        self.key_changes = Analyser.approximateKeyChanges(Sequencer.toDict(p_sequencer))

    #def selection(self):

    #def mutate(self):

    #def bread(self):

    #def initialize(self, p_size = 100):

    def candidate(self):
        old_sequencer = self.getSequencer()
        new_sequencer = Sequencer()

        for beat in Sequencer.toDict(old_sequencer)().keys():
            random_tone = random.choice(notes[0].getRelatives())
            random_intervals = random.choice(IntervalListUtilities.getPossibleIntervalList([item - notes[beat][0] for item in notes[beat]]))
            random_root = random.choice(Analyser.getKeyForBeat(beat).getDegrees())
            random_bass_triad_quality = random.choice([item[0] for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys()])
            random_extensions_quality = random.choice([item[0] for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys()])
            new_chord = Chord(random_tone, random_intervals, random_root, random_bass_triad_quality, random_extensions_quality)
            new_unused_prior_parts = []

            for part in new_chord.getParts():
                if len(unused_prior_parts) > 0:
                    viable_parts = [part for part in viable_parts if (part.getReferencePoint() - part.getReferencePoint()).getSemitones() <= (ACCIDENTAL_LIMIT * 2)]
                    random_part = random.choice(unused_prior_parts + [None])

                    if random_part is None:
                        new_voice = Voice()
                        new_voice.add(part)
                    else:
                        unused_prior_parts.pop(random_part)
                        random_part.getParentVoice().add(part)
                else:
                    new_voice = Voice()
                    new_voice.add(part)

                unused_prior_parts.append(part)

            new_sequencer[0].add(new_chord)
            unused_prior_parts += new_unused_prior_parts
            unused_prior_parts = [item for item in unused_prior_parts if beat - item.getAbsPosition() < 4]

        return new_notes

    @staticmethod
    def getKeyForBeat(p_beat, p_key_changes):
        keys = [p_key_changes[beat] for beat in p_key_changes.keys() if beat <= p_beat and beat + p_key_changes[beat]["range"] > beat]
        return keys[0] if len(keys) > 0 else None

    @staticmethod
    def approximateKeyChanges(p_notes, p_range = 4):
        beat_counter = 0
        key_dict = {}
        max_beat = max(p_notes.keys())

        for start_beat in range(0, max_beat + p_range, p_range):
            notes_in_range = dict((beat, p_notes[beat]) for beat in p_notes.keys() if beat >= start_beat and beat < start_beat + p_range)
            key_counter = Analyser.approximateKey(notes_in_range)
            prevalent_keys = list(dict(sorted(key_counter.iteritems(), key=operator.itemgetter(1), reverse=True)[:7]).keys())
            
            for key in prevalent_keys:
                assigned_scale = Scale(key, major)
                if all(item.simplify() in [item2.simplify() for item2 in assigned_scale.getReferencePoints()] for item in prevalent_keys): break

            if assigned_scale != key_dict.values()[-1]["scale"]:
                key_dict.update(Analyser.approximateKeyChanges(key_dict.keys()[-1]["notes"], key_dict.keys()[-1]["range"] / 2))
                key_dict.update(Analyser.approximateKeyChanges(notes_in_range, p_range / 2))
            else:
                key_dict[start_beat] = {"scale": assigned_scale, "notes": notes_in_range, "range": p_range}

        return key_dict

    @staticmethod
    def approximateKey(p_notes):
        return Counter(list(p_notes.values()))

    @staticmethod
    def normalizeBeats(p_notes):
        min_beat = min(p_notes.keys())

        for beat in p_notes.keys():
            p_notes[beat - min_beat] = p_note.pop(beat)

        return p_notes
    
    def getKeyChanges(self): return self.key_changes
    def getSequencer(self): return self.sequencer

    def setKeyChanges(self, p_key_changes): key_changes = p_key_changes
    def setSequencer(self, p_sequencer): self.sequencer = p_sequencer