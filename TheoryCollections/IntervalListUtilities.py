import itertools
import statistics
import re

from Configuration import *

class IntervalListUtilities:

    @staticmethod
    def intervalsToTypeDict(p_intervals):
        new_type_dict = {}

        for item in p_intervals:
            new_type_dict[item] = item.getParentIntervalListItem().getAttributes()

        return new_type_dict

    @staticmethod
    def invertIntervals(p_intervals):
        new_intervals = [-item for item in p_intervals][::-1]
        start_interval = new_intervals[-1]
        while start_interval >= new_intervals[0]: start_interval -= P8
        new_intervals = [start_interval] + new_intervals[:-1]
        new_intervals = IntervalListUtilities.normalizeIntervals(new_intervals)
        return new_intervals

    @staticmethod
    def normalizeTypeDict(p_type_dict, p_bass_interval):
        new_type_dict = {}

        for item in p_type_dict.keys():
            new_type_dict[item - p_bass_interval] = p_type_dict[item]

        return new_type_dict

    @staticmethod
    def getPossiblePitchClasses(p_semitones_list, p_variability = ACCIDENTAL_LIMIT, p_system = DEFAULT_SYSTEM):
        possible_intervals = [item.getIntervalsForSemitones(p_semitones) for item in p_semitones_list]
        all_combinations = list(itertools.product(*possible_intervals))
        return all_combinations

    @staticmethod
    def getIntervalsForSemitones(p_semitones, p_variability = ACCIDENTAL_LIMIT, p_system = DEFAULT_SYSTEM):
        previous_list = IntervalListUtilities.getPossibleIntervals(IntervalListUtilities.getChromaticIntervals(), p_system, p_variability)
        octaves = 1

        while(previous_list[-1].getSemitones() <= p_semitones + 12):
            temp_list = previous_list[:]
            for intervals in previous_list[:12]: temp_list.append([item + (Interval(12, 8) * octaves) for item in intervals])
            previous_list = temp_list[:]
            octaves += 1

        return [item for item in previous_list if item.semitones() == p_semitones]

    @staticmethod
    def getPossibleIntervals(p_intervals = None, p_variability = ACCIDENTAL_LIMIT):
        result = []
        intervals = IntervalListUtilities.getUnalteredIntervals(p_system) if p_intervals is None else p_intervals

        for item in intervals:
            sublist = []

            for i in range(p_variability):
                sublist.add(item)
                sublist.add(Interval(item.getSemitones() - (i + 1), item.getNumeral()))
                sublist.add(Interval(item.getSemitones() + (i + 1), item.getNumeral()))

            result.append(sublist)

        result = IntervalListUtilities.sortIntervals(result)
        return result

    @staticmethod
    def getChromaticIntervals(p_system = DEFAULT_SYSTEM):
        unaltered_intervals = IntervalListUtilities.getUnalteredIntervals(p_system)
        result = [item for item in IntervalListUtilities.getPossibleIntervals(unaltered_intervals, 1) if item.getSemitones() not in UNALTERED_INTERVALS[p_system]] + unaltered_intervals
        result = IntervalListUtilities.sortIntervals(result)
        return result

    @staticmethod
    def getUnalteredIntervals(p_system = DEFAULT_SYSTEM):
        return [Interval(UNALTERED_INTERVALS[p_system][i], i + 1) for i in range(len(UNALTERED_INTERVALS[p_system]))]

    ########################
    # Scale Static Methods #
    ########################

    @staticmethod
    def isDistinct(p_intervals): 
        return (len([item.simplify().getNumeral() for item in p_intervals]) == len(set([item.simplify().getNumeral() for item in p_intervals])))

    @staticmethod
    def pitchClassToScaleSteps(p_intervals):
        result = []
        previous = P1

        for interval in p_intervals[1:]:
            result.append((interval - previous).getSemitones())
            previous = interval

        result.append(abs(p_intervals[-1].simplify().getSemitones() - 12))
        return result

    @staticmethod
    def pitchClassToDecimal(p_intervals): 
        return int(IntervalListUtilities.pitchClassToBinary(p_intervals), 2)

    @staticmethod
    def pitchClassToBinary(p_intervals):
        result = ""

        for i in range(12):
            if (len([item for item in p_intervals if i == item.getSemitones()]) == 0): result = result + "0"
            else: result = result + "1"

        return result[::-1]

    @staticmethod
    def decimalToPitchClass(p_integer, p_use_distinct_intervals = False): return IntervalListUtilities.binaryToPitchClass('{0:012b}'.format(p_integer))

    @staticmethod
    def binaryToPitchClass(p_binary): return IntervalListUtilities.scaleStepsToDistinctPitchClass(IntervalListUtilities.binaryToIntervalListUtilitiesSteps(p_binary))

    @staticmethod
    def binaryToIntervalListUtilitiesSteps(p_binary):
        binary = p_binary[len(p_binary)::-1]
        binary = (binary + binary[0])[1:]
        scale_steps = []
        semitones = 0

        for i in range(len(binary)):
            if (binary[i] == '0'): semitones = semitones + 1
            else:
                semitones = semitones + 1
                scale_steps.append(semitones)
                semitones = 0
        
        return scale_steps

    @staticmethod
    def scaleStepsToPitchClass(p_scale_steps, p_system = DEFAULT_SYSTEM):
        counter = 0
        possible_intervals_collection = [(P1, P1, P1)]

        for i in range(len(p_scale_steps) - 1):
            integer = p_scale_steps[i]
            counter = counter + integer
            possible_intervals_collection.append(Interval.getPossibleIntervals(counter))

        all_combinations = list(itertools.product(*possible_intervals_collection))

        min_combination = None
        min_repeat_size = 1000
        min_accidental_count = 1000
        min_sharp_count = 1000

        for combination in all_combinations:
            temp_repeat_size = statistics.mean([len(list(group)) for key, group in itertools.groupby([item.getNumeral() for item in combination])])
            temp_accidental_count = len([item for item in combination if item.getAccidental() != ACCIDENTALS[p_system][0]])
            temp_sharp_count = len([item for item in combination if ACCIDENTALS[p_system][1] in item.getAccidental()])

            if (temp_repeat_size < min_repeat_size):
                min_combination = combination
                min_repeat_size = temp_repeat_size
                min_accidental_count = temp_accidental_count

            if (temp_repeat_size == min_repeat_size and (temp_accidental_count < min_accidental_count or temp_sharp_count < min_sharp_count)):
                min_combination = combination
                min_accidental_count = temp_accidental_count
                min_sharp_count = temp_sharp_count

        return list(min_combination)

    @staticmethod
    def scaleStepsToDistinctPitchClass(p_scale_steps):
        result = [P1]
        semitones = 0

        for i in range(len(p_scale_steps) - 1):
            semitones = semitones + p_scale_steps[i]
            result.append(Interval(semitones, i + 2))

        if (len([item for item in result if len(item.getAccidental()) > ACCIDENTAL_LIMIT]) > 0): return IntervalListUtilities.scaleStepsToPitchClass(p_scale_steps)
        return result

    @staticmethod
    def simplifyIntervals(p_intervals):
        new_intervals = [item.simplify() for item in p_intervals]
        new_intervals = IntervalListUtilities.sortIntervals(new_intervals)
        return new_intervals

    @staticmethod
    def scaleIntervalsByOrder(p_intervals):
        result = []
        previous = -m2

        for interval in p_intervals:
            while (interval <= previous): interval = interval + P8
            previous = interval
            result.append(interval)

        return result

    @staticmethod
    def sortIntervals(p_intervals): 
        p_intervals.sort(key=lambda x: x.getNumeral())
        p_intervals.sort(key=lambda x: x.getSemitones())
        return p_intervals

    @staticmethod
    def normalizeIntervals(p_intervals): 
        return [item - p_intervals[0] for item in p_intervals]

    @staticmethod
    def tonesToPitchClass(p_tones): 
        return IntervalListUtilities.scaleIntervalsByOrder([tone - p_tones[0] for tone in p_tones])

    ########################
    # Chord Static Methods #
    ########################

    @staticmethod
    def intervalsToQuality(p_intervals, p_bass_triad_quality = None, p_extensions_quality = None, p_system = DEFAULT_SYSTEM):
        bass_triad_qualities = IntervalListUtilities.evaluateQualityAssignments(p_intervals, slice(None, 3, None), p_bass_triad_quality, p_system)
        extensions_qualities = IntervalListUtilities.evaluateQualityAssignments(p_intervals, slice(3, None, None), p_extensions_quality, p_system)
        possible_qualities = []

        for extensions_quality_data in extensions_qualities:
            for triad_quality_data in bass_triad_qualities:

                data = {
                    "Bass Triad Quality": triad_quality_data["Quality"], 
                    "Bass Triad Accidentals": triad_quality_data["Accidentals"], 
                    "Bass Triad Omissions": [item for item in triad_quality_data["Omissions"] if item[1].getNumeral() < max([x.getNumeral() for x in p_intervals if x])],
                    "Extensions Quality": extensions_quality_data["Quality"],                 
                    "Extensions Accidentals" : extensions_quality_data["Accidentals"], 
                    "Extensions Omissions": [item for item in extensions_quality_data["Omissions"] if item[1].getNumeral() < max([x.getNumeral() for x in p_intervals if x])],
                    "Extensions Size": max([x.getNumeral() for x in p_intervals if x])
                }

                evaluation = triad_quality_data["Evaluation"] + extensions_quality_data["Evaluation"]
                possible_qualities.append((data, evaluation))

        return min(possible_qualities, key=lambda x: x[1])[0]

    @staticmethod
    def evaluateQualityAssignments(p_chord_intervals, p_slice, p_quality = None, p_system = DEFAULT_SYSTEM):
        chord_qualities = []
        in_qualities = [item for item in CHORD_QUALITIES[p_system].keys() if p_quality in item] if p_quality is not None else CHORD_QUALITIES[p_system].keys() 

        for key in in_qualities:
            temp_in_chord_intervals = p_chord_intervals[p_slice]
            temp_chord_quality_chord = [item for item in CHORD_QUALITIES[p_system][key] if item is not None][p_slice]

            evaluation = 0
            temp_accidentals = []
            omitted_intervals = []

            for interval in temp_chord_quality_chord:
                if (interval.getNumeral() not in [item.getNumeral() for item in temp_in_chord_intervals]): 
                    omitted_intervals += [(OMISSION_NOTATION[p_system], interval)]
                    evaluation += 1
                else:
                    for item in [item for item in temp_in_chord_intervals if item.getNumeral() == interval.getNumeral()]:
                        if (item != interval):
                            temp_accidentals += [("", item)]
                            evaluation += 1

            chord_qualities.append({
                    "Quality": key, 
                    "Accidentals": temp_accidentals, 
                    "Omissions": omitted_intervals, 
                    "Evaluation": evaluation}
                )

        return chord_qualities

    @staticmethod
    def stringQualityToData(p_quality, p_system = DEFAULT_SYSTEM):
        regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
        quality_contents = re.search(re.compile(regex), p_quality)

        bass_triad_quality = quality_contents.group(1)
        extensions_quality = quality_contents.group(2)
        extensions_numeral = quality_contents.group(3)

        extensions_quality = bass_triad_quality if extensions_quality is None else extensions_quality

        regex_accidentals = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
        regex_optional_accidentals = "[" + regex_accidentals + "]*\d+"

        regex_alt = "[" + regex_accidentals + "]\d+"
        altered_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_alt), p_quality)]

        regex_sus = SUSPENDED_NOTATION[p_system] + regex_optional_accidentals
        sus_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_sus), p_quality)]

        regex_add = ADDITION_NOTATION[p_system] + regex_optional_accidentals
        add_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_add), p_quality)]

        regex_omit = OMISSION_NOTATION[p_system] + regex_optional_accidentals
        omitted_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_omit), p_quality)]

        data = {
                "Bass Triad Quality": bass_triad_quality, 
                "Bass Triad Accidentals": [item for item in altered_intervals if item.getNumeral() <= 5], 
                "Bass Triad Added": [item for item in add_intervals if item.getNumeral() <= 5],
                "Bass Triad Omissions": [item for item in omitted_intervals if item.getNumeral() <= 5], 
                "Extensions Quality": extensions_quality,                 
                "Extensions Accidentals" : [item for item in altered_intervals if item.getNumeral() > 5], 
                "Extensions Added" : [item for item in add_intervals if item.getNumeral() > 5], 
                "Extensions Omissions": [item for item in omitted_intervals if item.getNumeral() > 5], 
                "Suspended" : sus_intervals, 
                "Extensions Size": extensions_numeral
            }

        return data

    @staticmethod
    def stringToPitchClass(p_quality, p_system = DEFAULT_SYSTEM):
        data = IntervalListUtilities.stringQualityToData(p_quality, p_system)

        bass_triad_quality = data["Bass Triad Quality"]
        extensions_quality = data["Extensions Quality"]
        list_of_alt_intervals = data["Bass Triad Accidentals"] + data["Extensions Accidentals"]
        list_of_sus_intervals = data["Suspended"]
        list_of_add_intervals = data["Bass Triad Added"] + data["Extensions Added"]
        list_of_omi_intervals = data["Bass Triad Omissions"] + data["Extensions Omissions"]
        extensions_numeral = data["Extensions Size"]

        for quality_tuple in CHORD_QUALITIES[p_system].keys():
            if bass_triad_quality in quality_tuple: bass_triad_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][:3]
            if extensions_quality in quality_tuple: extensions_pitch_class = CHORD_QUALITIES[p_system][quality_tuple][3:]

        result = (bass_triad_pitch_class + extensions_pitch_class)[:int((int(extensions_numeral) + 1) / 2)]

        for altered_interval in list_of_alt_intervals:
            match = [item for item in result if item.getNumeral() == altered_interval.getNumeral()]
            if len(match) > 0: result[result.index(match[0])] = altered_interval

        result = result + list_of_sus_intervals
        if (len(list_of_sus_intervals) > 0 and 3 in [item.getNumeral() for item in result]): result.pop(result.index([item for item in result if item.getNumeral() == 3][0]))

        result = result + list_of_add_intervals
        result.sort(key=lambda x: x.getSemitones())
        
        for omitted_interval in list_of_omi_intervals:
            if omitted_interval in result: result.pop(result.index(omitted_interval)) 

        return result

    @staticmethod
    def identifyParentScale(p_bass_triad_quality, p_extensions_quality):
        result_scale = [item for item in IntervalListUtilities.simplifyIntervals(IntervalListUtilities.stringToPitchClassFast(p_bass_triad_quality)) if item.getNumeral() in (1, 3, 5)]
        result_scale += [item for item in IntervalListUtilities.simplifyIntervals(IntervalListUtilities.stringToPitchClassFast(p_extensions_quality)) if item.getNumeral() in (2, 4, 6, 7)]
        return IntervalListUtilities.sortIntervals(result_scale)

    @staticmethod
    def stringToPitchClassFast(p_quality):
        results = [item for item in CHORD_QUALITIES[DEFAULT_SYSTEM].keys() if p_quality in item]
        return [item for item in CHORD_QUALITIES[DEFAULT_SYSTEM][results[0]] if item is not None] if len(results) > 0 else None

    @staticmethod
    def findRoot(p_intervals):
        temp_delta = (len(p_intervals) - IntervalListUtilities.getInversionStatic(p_intervals))
        return p_intervals[temp_delta] if temp_delta != len(p_intervals) else p_intervals[0]

    @staticmethod
    def getParentChordStatic(p_intervals):
        return IntervalListUtilities.buildOnThirdsStatic(IntervalListUtilities.getRootPositionStatic(p_intervals))

    @staticmethod
    def invertStatic(p_intervals, p_inversion_number, p_fixed_invert = None):
        temp_fixed_move = p_fixed_invert if p_fixed_invert is not None else p_intervals[-1].roof()
        if p_inversion_number == 0: return p_intervals
        if p_inversion_number > 0: temp_new_intervals = IntervalListUtilities.normalizeIntervals(p_intervals[1:] + [p_intervals[0] + temp_fixed_move]) 
        if p_inversion_number < 0: temp_new_intervals = IntervalListUtilities.normalizeIntervals([p_intervals[-1] - temp_fixed_move] + p_intervals[:-1])
        return IntervalListUtilities.invertStatic(temp_new_intervals, p_inversion_number - (p_inversion_number/abs(p_inversion_number)), temp_fixed_move) if abs(p_inversion_number) != 1 else temp_new_intervals

    @staticmethod
    def getRootPositionStatic(p_intervals):
        duplicates_found = False
        previous = p_intervals
        smallest_inversion = previous
        min_intervals_sum = sum([item.getSemitones() for item in IntervalListUtilities.buildOnThirdsStatic(p_intervals)])
        fixed_invert = p_intervals[-1].roof()

        for i in range(len(p_intervals) - 1):
            temp_intervals = IntervalListUtilities.invertStatic(previous, 1, fixed_invert)
            temp_intervals_as_thirds = IntervalListUtilities.buildOnThirdsStatic(temp_intervals)
            temp_intervals_sums = sum([item.getSemitones() for item in temp_intervals_as_thirds])
            
            if (temp_intervals_sums < min_intervals_sum):
                duplicates_found = False
                smallest_inversion = temp_intervals
                min_intervals_sum = temp_intervals_sums
                
            elif (temp_intervals_sums == min_intervals_sum): duplicates_found = True
            previous = temp_intervals

        if (duplicates_found):
            return smallest_inversion

        return smallest_inversion

    @staticmethod
    def getInversionStatic(p_intervals):
        temp_counter = 0
        temp_fixed_invert = p_intervals[-1].roof()
        temp_first_inversion = IntervalListUtilities.getRootPositionStatic(p_intervals)
        temp_next_inversion = IntervalListUtilities.invertStatic(p_intervals, 1, temp_fixed_invert)

        while(temp_next_inversion != temp_first_inversion):
            temp_next_inversion = IntervalListUtilities.invertStatic(temp_next_inversion, 1, temp_fixed_invert)
            temp_counter += 1

        return (len(p_intervals) - temp_counter) - 1

    @staticmethod
    def buildOnThirdsStatic(p_intervals):
        return [item for item in IntervalListUtilities.rearrangeIntervalsAsThirds(p_intervals) if item != None]

    @staticmethod
    def getItemRepetitionCount(p_intervals): 
        result = 0

        for interval in p_intervals:
            repeats = len([item for item in p_intervals if item.simplify().getSemitones() == interval.simplify().getSemitones()])
            if (repeats > 1): result = result + repeats

        return result

    @staticmethod
    def rearrangeIntervalsAsThirds(p_intervals, p_system = DEFAULT_SYSTEM):
        new_interval_list = []

        for interval in p_intervals:
            possible_intervals = []

            while (((interval.getNumeral() - 1) % 2) != 0 and interval < P8): interval += P8
            if (((interval.getNumeral() - 1) % 2) != 0 and interval < P8): new_interval = interval + P8

            elif ((interval.getNumeral() - 1) % 2 != 0 and interval > P8 and interval < M13): 
                new_interval = interval
                while (new_interval > P8): new_interval -= P8

            elif (interval > M13):
                new_interval = interval
                while (new_interval > M13 or ((new_interval.getNumeral() - 1) % 2) != 0): new_interval -= P8

            else: new_interval = interval
            if (new_interval != P8): new_interval_list.append(new_interval)

        new_interval_list.sort(key=lambda x: x.getSemitones())
        previous_numeral = -1
        i = 0

        while (i < len(new_interval_list)):

            if (new_interval_list[i].getNumeral() - previous_numeral != 2):
                difference = new_interval_list[i].getNumeral() - previous_numeral

                for j in range(int((difference - 2)/2)):
                    new_interval_list.insert(i, None)
                    i += 1

            previous_numeral = new_interval_list[i].getNumeral()
            i += 1

        return new_interval_list

    @staticmethod
    def getPitchClassByQuality(p_quality, p_system = DEFAULT_SYSTEM):

        for key in CHORD_QUALITIES[p_system].keys():
            if p_quality in key: return CHORD_QUALITIES[p_system][key]

        return None