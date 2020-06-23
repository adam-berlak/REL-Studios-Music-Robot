import itertools
import statistics

from Configuration import *

class IntervalListUtilities:

    ########################
    # Scale Static Methods #
    ########################

    @staticmethod
    def isDistinct(p_intervals): 
        return (len([item.simplify().getNumeral() for item in p_intervals]) == len(set([item.simplify().getNumeral() for item in p_intervals])))

    @staticmethod
    def fromInt(p_int): 
        return IntervalListUtilities.decimalToPitchClass(p_int)

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
        return [item.simplify() for item in p_intervals]

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