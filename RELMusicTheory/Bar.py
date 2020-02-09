import binascii

class Measure:

    def __init__(self, p_time_signature = (4, 4), p_current_beat = 0.0, p_contents = []):
        self.time_signature = p_time_signature
        self.current_beat = p_current_beat
        self.contents = p_contents

    def placeNotes(self, p_notes):
        self.placeNotesAt(p_notes, self.getCurrentBeat())
        self.setCurrentBeat(self.getCurrentBeat() + (p_notes.getDuration() * 4))

    def placeNotesAt(self, p_notes, p_beat): self.getContents()[p_beat] += p_notes

    def getTimeSignature(self): return self.time_signature
    def getCurrentBeat(self): return self.current_beat
    def getContents(self): return self.contents

    def setTimeSignature(self, p_time_signature): self.time_signature = p_time_signature
    def setCurrentBeat(self, p_current_beat): self.current_beat = p_current_beat
    def setContents(self, p_contents): self.contents = p_contents

class Note:
    
    def __init__(self, p_key, p_duration):
        self.key = p_key
        self.duration = p_duration

class MidiFile:

    bytes_read = 0

    '''
    def midiToComposition(self, p_file_name):
        (header, track_data) = self.parseMidiFile(p_file_name)

        if header[2]['fps']:
            print "Don't know how to parse this yet"
            return c

        ticks_per_beat = header[2]['ticks_per_beat']

        for track in track_data:

            metronome = 1
            thirtyseconds = 8
            meter = (4, 4)
            
            for items in track:
                (deltatime, event) = items
                duration = float(deltatime) / (ticks_per_beat * 4.0)
                duration = 1.0 / duration

                if (event['event'] == 8 and deltatime == 0): pass
                elif (event['event'] == 9): Note(Key.intToKey(event['param1'] % 12), )
                elif (event['event'] == 10): pass
                elif (event['event'] == 11): pass
                elif (event['event'] == 12): pass
    '''

    def parseMidiFile(self, p_file_name):

        try: f = open(p_file_name, 'rb')
        except: print("Failed to open file")
        
        header_data = self.parseHeaderData(f)
        tracks = header_data[1]
        events_list = []

        while(tracks > 0):
            events = self.parseTrack(f)
            events_list.append(events)
            tracks -= 1

        f.close()
        return (header_data, events_list)

    def parseHeaderData(self, p_fp):
        meta = p_fp.read(4)
        chunk_size = self.bytesToInt(p_fp.read(4))
        format_type = self.bytesToInt(p_fp.read(2))
        number_of_tracks = self.bytesToInt(p_fp.read(2))
        time_division = self.parseTimeDivision(p_fp.read(2))

        next_read = (chunk_size - 6) / 2
        p_fp.read(int(next_read))

        self.bytes_read += (16 + next_read)

        return (format_type, number_of_tracks, time_division)

    def bytesToInt(self, p_bytes): return int(binascii.b2a_hex(p_bytes), 16)

    def parseTimeDivision(self, p_bytes):
        value = self.bytesToInt(p_bytes)
        if not value & 0x8000: return {'fps': False, 'ticks_per_beat': value & 0x7FFF}
        else:
            SMPTE_frames = (value & 0x7F00) >> 2
            clock_ticks = (value & 0x00FF) >> 2
            return {'fps': True, 'SMPTE_frames': SMPTE_frames, 'clock_ticks': clock_ticks}

    def parseTrack(self, p_fp):
        events_list = []
        chunk_size = self.parseTrackHeader(p_fp)

        while(chunk_size > 0):
            (delta_time, chunk_delta_1) = self.parseVarbyteAsInt(p_fp)
            (event, chunk_delta_2) = self.parseMidiEvent(p_fp)
            chunk_size -= (chunk_delta_1 + chunk_delta_2)
            events_list.append([delta_time, event])

        return events_list

    def parseTrackHeader(self, p_fp):
        x = p_fp.read(4)
        chunk_size = self.bytesToInt(p_fp.read(4))

        self.bytes_read += 8
        
        return chunk_size

    def parseVarbyteAsInt(self, p_fp, p_return_bytes_read = True):
        result = 0
        bytes_read = 0
        r = 0x80

        while(r & 0x80):
            r = self.bytesToInt(p_fp.read(1))

            if r & 0x80: result = (result << 7) + (r & 0x7F)
            else: result = (result << 7) + r

            bytes_read += 2

        if (not p_return_bytes_read): return result
        else: return (result, bytes_read)

    def parseMidiEvent(self, p_fp):
        chunk_size = 0
        ec = self.bytesToInt(p_fp.read(1))

        chunk_size += 1
        self.bytes_read += 1

        event_type = (ec & 0xf0) >> 4
        channel = ec & 0x0f

        if (event_type < 8): print('Unknown event type')

        if (event_type == 0x0f):
            meta_event = self.bytesToInt(p_fp.read(1))
            (length, chunk_delta) = self.parseVarbyteAsInt(p_fp)
            data = p_fp.read(length)

            chunk_size += 1 + chunk_delta + length
            self.bytes_read += 1 + length

            return ({'event': event_type, 'meta_event': meta_event, 'data': data}, chunk_size)

        elif (event_type in [12, 13]):
            param1 = self.bytesToInt(p_fp.read(1))

            chunk_size += 1
            self.bytes_read += 1

            return ({'event': event_type, 'channel': channel, 'param1': param1}, chunk_size)
        
        else:
            param1 = self.bytesToInt(p_fp.read(1))
            param2 = self.bytesToInt(p_fp.read(1))

            chunk_size += 2
            self.bytes_read += 2

            return ({'event': event_type, 'channel': channel, 'param1': param1, 'param2': param2}, chunk_size)