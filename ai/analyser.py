import random
import operator

from collections import Counter
from io.sequencer import *
from io.midi_to_objects import *
from theory.scale import *
from theory.chord import *
from theory.utilities import *

class Analyser:

    def __init__(self, p_sequencer, p_seed = 0):
        self.sequencer = p_sequencer
        self.key_changes = Analyser.approximateKeyChanges(Sequencer.flattenDict(Sequencer.toDict(p_sequencer)), 4, p_sequencer.getTimeDivision())

    #def selection(self):

    #def mutate(self):

    #def bread(self):

    #def initialize(self, p_size = 100):

    def candidate(self, p_seed = 0):
        # Need to debug issue for the breakpoint
        # Notes needs to be ordered
        random.seed(p_seed)
        old_sequencer = self.getSequencer()
        sequencer_notes = Sequencer.flattenDict(Sequencer.toDict(old_sequencer))
        new_notes = {}

        for beat in sequencer_notes.keys():
            notes = sequencer_notes[beat]
            notes.sort()
            random_tones = [random.choice(item.getRelatives()) for item in notes]
            random_root = random.choice(Analyser.getKeyForBeat(beat, self.getKeyChanges())["scale"].getDegrees())
            random_bass_triad_quality = random.choice([item[0] for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys()])
            random_extensions_quality = random.choice([item[0] for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys()])
            new_chord = Chord(random_tones, p_root = random_root, p_bass_triad_quality = random_bass_triad_quality, p_extensions_quality = random_extensions_quality)
            #print(new_chord)
            
            for part in new_chord.getParts():
                viable_antecedent_parts = [item2 for item in sequencer_notes.keys() for item2 in sequencer_notes[item] if item >= beat - (old_sequencer.getTimeDivision() * 4) and item < beat]
                viable_consequent_parts = [item2 for item in sequencer_notes.keys() for item2 in sequencer_notes[item] if item <= beat + (old_sequencer.getTimeDivision() * 4) and item > beat]
                part.setAntecedentParts(viable_antecedent_parts)
                part.setConsequentParts(viable_consequent_parts)

            new_notes[beat] = new_chord.getParts()

        new_sequencer = Sequencer(p_channels = {1: new_notes})
        return new_sequencer

    @staticmethod
    def getKeyForBeat(p_beat, p_key_changes):
        keys = [p_key_changes[beat] for beat in p_key_changes.keys() if beat <= p_beat and beat + p_key_changes[beat]["range"] > beat]
        return keys[0] if len(keys) > 0 else None

    @staticmethod
    def approximateKeyChanges(p_notes, p_range = 4, p_division = 480, p_before_context = None, p_after_context = None):
        beat_counter = 0
        key_dict = {}
        min_beat = min(p_notes.keys())
        max_beat = max(p_notes.keys())
        groups_size = int(p_division * p_range)
        start_beat = min_beat
        max_range = max_beat + groups_size

        while start_beat < max_range:
            notes_in_range = dict((beat, p_notes[beat]) for beat in p_notes.keys() if beat >= start_beat and beat < start_beat + groups_size)
            key_counter = Analyser.approximateKey(notes_in_range)
            prevalent_keys = key_counter.most_common(7)
            prevalent_keys = list(dict(key_counter.most_common(7)).keys())
            key_found = False
            
            if len(prevalent_keys) >= 7:
                for key in prevalent_keys:
                    assigned_scale = Scale(key, major)

                    if all(item.getTone().simplify() in [item2.getTone().simplify() for item2 in assigned_scale.getReferencePoints()] for item in prevalent_keys): 
                        key_found = True
                        break

            if not key_found:
                if prevalent_keys == []: 
                    key_dict[start_beat] = {"scale": list(key_dict.values())[-1]["scale"] if len(key_dict.values()) != 0 else p_before_context, "notes": {start_beat: []}, "range": p_range}

                elif p_after_context is not None and p_before_context is not None:
                    before_key_eval = len([item for item in p_before_context.getTones() if item not in prevalent_keys] + [item for item in prevalent_keys if item not in p_before_context.getTones()])
                    after_key_eval = len([item for item in p_after_context.getTones() if item not in prevalent_keys] + [item for item in prevalent_keys if item not in p_after_context.getTones()])

                    if after_key_eval >= before_key_eval:
                        key_dict[start_beat] = {"scale": p_before_context, "notes": notes_in_range, "range": p_range}

                    else: key_dict[start_beat] = {"scale": p_after_context, "notes": notes_in_range, "range": p_range}

                elif p_after_context is not None:
                    key_dict[start_beat] = {"scale": p_after_context, "notes": notes_in_range, "range": p_range}
                
                elif start_beat + groups_size >= max(p_notes.keys()):
                    key_dict[start_beat] = {"scale": list(key_dict.values())[-1]["scale"], "notes": notes_in_range, "range": p_range}
                else:
                    max_range += groups_size
                    groups_size *= 2
                    start_beat -= groups_size

            elif len(key_dict.values()) != 0 and list(key_dict.values())[-1]["scale"] != assigned_scale:
                key_dict.update(Analyser.approximateKeyChanges(list(key_dict.values())[-1]["notes"], list(key_dict.values())[-1]["range"] / 2, p_division, list(key_dict.values())[-1]["scale"], assigned_scale))
                key_dict.update(Analyser.approximateKeyChanges(notes_in_range, p_range / 2, p_division, list(key_dict.values())[-1]["scale"], assigned_scale))

            else: key_dict.update(Analyser.approximateKeyChanges(notes_in_range, p_range / 2, p_division, list(key_dict.values())[-1]["scale"] if len(key_dict.values()) != 0 else None, assigned_scale))


            start_beat += groups_size

        return key_dict
        
    @staticmethod
    def approximateKey(p_notes):
        return Counter([item2.getTone().simplify() if type(item2.getTone().simplify()) == Tone else item2.getTone().simplify()[0] for item in p_notes.values() for item2 in item])

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