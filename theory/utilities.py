import itertools
import statistics
import re

from theory.config import *

class Utilities:

    # not used
    @staticmethod
    def flip_intervals(p_intervals):
        new_intervals = [item * -1 for item in p_intervals]
        new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    @staticmethod
    def intervals_relative_to(p_interval, p_intervals, p_fixed_invert = None):
        fixed_invert = p_fixed_invert if p_fixed_invert is not None else (p_intervals[-1].roof() - p_intervals[0].floor())
        new_intervals = [item - p_interval for item in p_intervals]

        while new_intervals[0] < Interval(0, 0) and fixed_invert != P1:
            new_intervals = new_intervals[1:] + [new_intervals[0] + fixed_invert]

        new_intervals = Utilities.simplify_intervals(new_intervals)
        new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    @staticmethod
    def derive_unaltered_intervals_from_parent(p_parent_item, p_fixed_invert = None):
        parent_item_position = p_parent_item.get_interval()
        parent_item_unaltered_intervals = p_parent_item.get_parent_interval_list().get_unaltered_intervals()
        new_intervals = Utilities.intervals_relative_to(parent_item_position, parent_item_unaltered_intervals, p_fixed_invert)
        return new_intervals

    # not used
    @staticmethod
    def get_new_unaltered_intervals(p_intervals):
        new_unaltered_intervals = []

        for item in p_intervals:
            if item.get_parent_interval_list_item() is not None and item.get_parent_interval_list_item().get_parent_interval_list() is not None:
                if item.get_parent_interval_list_item().isUnAltered():
                    new_item = item.simplify()

                elif item.get_parent_interval_list_item().isAltered():
                    new_item = item.simplify() + item.get_parent_interval_list_item().getAlteration()
                    
                if new_item not in new_unaltered_intervals: 
                    new_unaltered_intervals.append(new_item)

        new_unaltered_intervals = Utilities.sort_intervals(new_unaltered_intervals)
        return new_unaltered_intervals

    @staticmethod
    def get_valid_unaltered_intervals(p_intervals, p_unaltered_intervals):
        intervals_by_numeral = {}
        new_intervals = p_unaltered_intervals[:]

        for item in p_intervals:
            intervals_by_numeral[item.simplify().get_numeral()] = [item2 for item2 in p_intervals if item2.simplify().get_numeral() == item.simplify().get_numeral()]
        
        for item in intervals_by_numeral.keys():
            has_duplicates = len(set([item2.simplify() for item2 in intervals_by_numeral[item]])) != len([item2 for item2 in intervals_by_numeral[item]])
            needs_unaltered = len([item2 for item2 in new_intervals if item2.simplify().get_numeral() == item]) == 0
            
            if has_duplicates: 
                min_interval = min(intervals_by_numeral[item], key=lambda x: abs(x.get_accidental_as_semitones_BL()))

                for item2 in new_intervals:
                    if item2 in intervals_by_numeral[item] and item2 != min_interval:
                        new_intervals.remove(item2)

            if needs_unaltered:
                min_interval = min(intervals_by_numeral[item], key=lambda x: abs(x.get_accidental_as_semitones_BL()))
                new_intervals.append(min_interval.simplify())

        new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    # not used
    @staticmethod
    def get_unaltered_intevals_type_dict(p_intervals, p_type_dict):
        intervals_by_numeral = {}

        for item in p_intervals:
            intervals_by_numeral[item.simplify().get_numeral()] = [item2 for item2 in p_intervals if item2.simplify().get_numeral() == item.simplify().get_numeral()]

        new_type_dict = p_type_dict
        
        for item in intervals_by_numeral.keys():
            unaltered_same_numeral = [item2 for item2 in intervals_by_numeral[item] if item2 in p_type_dict.keys() and p_type_dict[item2]["p_unaltered"] == True]
            needs_unaltered = len(unaltered_same_numeral) == 0

            if needs_unaltered: 
                min_interval = min(intervals_by_numeral[item], key=lambda x: abs(x.get_accidental_as_semitones_BL()))

                for item in p_intervals:
                    if item.simplify() == min_interval:
                        if min_interval in new_type_dict.keys():
                            new_type_dict[min_interval]["p_unaltered"] = True

                        else: new_type_dict[min_interval] = {"p_unaltered": True}

            else:
                min_interval = min(unaltered_same_numeral, key=lambda x: abs(x.get_accidental_as_semitones_BL()))

                for item2 in intervals_by_numeral[item]:
                    if item2 not in new_type_dict.keys(): 
                        new_type_dict[item2] = {}
                    
                    if item2.simplify() == min_interval.simplify():
                        new_type_dict[item2]["p_unaltered"] = True

                    else: new_type_dict[item2]["p_unaltered"] = False

        return new_type_dict

    @staticmethod
    def intervals_to_type_dict(p_intervals):
        new_type_dict = {}

        for item in p_intervals:
            if item.get_parent_interval_list_item() is not None:
                new_type_dict[item] = item.get_parent_interval_list_item().get_attributes()

        return new_type_dict

    @staticmethod
    def normalize_type_dict(p_type_dict, p_bass_interval):
        new_type_dict = {}

        for item in p_type_dict.keys():
            new_type_dict[item - p_bass_interval] = p_type_dict[item]

        return new_type_dict

    # not used
    @staticmethod
    def get_possible_pitch_classes(p_semitones_list, p_variability = ACCIDENTAL_LIMIT, p_system = DEFAULT_SYSTEM):
        possible_intervals = [Utilities.get_intervals_for_semitones(item) for item in p_semitones_list]
        all_combinations = list(itertools.product(*possible_intervals))
        return all_combinations

    @staticmethod
    def get_intervals_for_semitones(p_semitones, p_variability = ACCIDENTAL_LIMIT, p_system = DEFAULT_SYSTEM):
        previous_list = Utilities.get_possible_intervals(Utilities.get_chromatic_intervals(), p_system, p_variability)
        octaves = 1

        while previous_list[-1].get_semitones() <= p_semitones + 12:
            temp_list = previous_list[:]

            for intervals in previous_list[:12]: 
                temp_list.append([item + (Interval(12, 8) * octaves) for item in intervals])

            previous_list = temp_list[:]
            octaves += 1

        return [item for item in previous_list if item.semitones() == p_semitones]

    @staticmethod
    def get_possible_intervals(p_intervals = None, p_variability = ACCIDENTAL_LIMIT):
        new_intervals = []
        intervals = Utilities.get_unaltered_intervals(p_system) if p_intervals is None else p_intervals

        for item in intervals:
            sublist = []

            for i in range(p_variability):
                sublist.append(item)
                sublist.append(Interval(item.get_semitones() - (i + 1), item.get_numeral()))
                sublist.append(Interval(item.get_semitones() + (i + 1), item.get_numeral()))

            new_intervals.append(sublist)

        #new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    @staticmethod
    def get_chromatic_intervals(p_system = DEFAULT_SYSTEM):
        unaltered_intervals = Utilities.get_unaltered_intervals(p_system)
        new_intervals = [item for item in Utilities.get_possible_intervals(unaltered_intervals, 1) if item.get_semitones() not in UNALTERED_INTERVALS[p_system]] + unaltered_intervals
        new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    @staticmethod
    def get_unaltered_intervals(p_system = DEFAULT_SYSTEM):
        return [Interval(UNALTERED_INTERVALS[p_system][i], i + 1) for i in range(len(UNALTERED_INTERVALS[p_system]))]

    ########################
    # Scale Static Methods #
    ########################

    @staticmethod
    def is_distinct(p_intervals): 
        return (len([item.simplify().get_numeral() for item in p_intervals]) == len(set([item.simplify().get_numeral() for item in p_intervals])))

    ########################
    # Chord Static Methods #
    ########################

    @staticmethod
    def string_quality_to_data(p_quality, p_system = DEFAULT_SYSTEM):
        regex = (("(" + str([item for representations in CHORD_QUALITIES[p_system] for item in representations]).replace('\'', "").replace(" ", "").replace(',', "|").replace('+', "\+")[1:][:-1] + ")") * 2) + "*(\d+)"
        quality_contents = re.search(re.compile(regex), p_quality)

        bass_triad_quality = quality_contents.group(1)
        extensions_quality = quality_contents.group(2)
        extensions_numeral = quality_contents.group(3)

        extensions_quality = bass_triad_quality if extensions_quality is None else extensions_quality

        bass_triad_quality = [key for key in CHORD_QUALITIES[p_system] if bass_triad_quality in key][0]
        extensions_quality = [key for key in CHORD_QUALITIES[p_system] if extensions_quality in key][0]
        
        regex_accidentals = str([item for item in ACCIDENTALS[p_system].values()]).replace('\'', "").replace(' ', "").replace(',', "")[1:][:-1]
        regex_optional_accidentals = "[" + regex_accidentals + "]*\d+"

        regex_alt = "(\d+[" + regex_accidentals + "]*(?!(?<![" + regex_accidentals + "])\d*|[" + regex_accidentals + "]*" + SUSPENDED_NOTATION[p_system][::-1] + "|" + ADDITION_NOTATION[p_system][::-1] + "|" + OMISSION_NOTATION[p_system][::-1] + "))"
        altered_intervals = [Interval.stringToInterval(item[::-1]) for item in re.findall(re.compile(regex_alt), p_quality[::-1])]

        regex_sus = SUSPENDED_NOTATION[p_system] + regex_optional_accidentals
        sus_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_sus), p_quality)]

        regex_add = ADDITION_NOTATION[p_system] + regex_optional_accidentals
        add_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_add), p_quality)]

        regex_omit = OMISSION_NOTATION[p_system] + regex_optional_accidentals
        omitted_intervals = [Interval.stringToInterval(item) for item in re.findall(re.compile(regex_omit), p_quality)]

        data = {
                "Bass Triad Quality": bass_triad_quality, 
                "Bass Triad Accidentals": [item for item in altered_intervals if item.get_numeral() <= 5], 
                "Bass Triad Added": [item for item in add_intervals if item.get_numeral() <= 5],
                "Bass Triad Omissions": [item for item in omitted_intervals if item.get_numeral() <= 5], 
                "Extensions Quality": extensions_quality,                 
                "Extensions Accidentals" : [item for item in altered_intervals if item.get_numeral() > 5], 
                "Extensions Added" : [item for item in add_intervals if item.get_numeral() > 5], 
                "Extensions Omissions": [item for item in omitted_intervals if item.get_numeral() > 5], 
                "Suspended" : sus_intervals, 
                "Extensions Size": extensions_numeral
            }

        return data

    @staticmethod
    def string_to_pitch_class(p_quality, p_system = DEFAULT_SYSTEM):
        data = Utilities.string_quality_to_data(p_quality, p_system)
        bass_triad_quality = data["Bass Triad Quality"]
        extensions_quality = data["Extensions Quality"]
        list_of_alt_intervals = data["Bass Triad Accidentals"] + data["Extensions Accidentals"]
        list_of_sus_intervals = data["Suspended"]
        list_of_add_intervals = data["Bass Triad Added"] + data["Extensions Added"]
        list_of_omi_intervals = data["Bass Triad Omissions"] + data["Extensions Omissions"]
        extensions_numeral = data["Extensions Size"]
        
        bass_triad_pitch_class = CHORD_QUALITIES[p_system][bass_triad_quality][:3]
        extensions_pitch_class = CHORD_QUALITIES[p_system][extensions_quality][3:]

        result = (bass_triad_pitch_class + extensions_pitch_class)[:int((int(extensions_numeral) + 1) / 2)]

        for altered_interval in list_of_alt_intervals:
            match = [item for item in result if item.get_numeral() == altered_interval.get_numeral()]
            if len(match) > 0: result[result.index(match[0])] = altered_interval

        result = result + list_of_sus_intervals
        if len(list_of_sus_intervals) > 0 and 3 in [item.get_numeral() for item in result]: result.pop(result.index([item for item in result if item.get_numeral() == 3][0]))

        result = result + list_of_add_intervals
        result.sort(key=lambda x: x.get_semitones())
        
        for omitted_interval in list_of_omi_intervals:
            if omitted_interval in result: result.pop(result.index(omitted_interval)) 

        return result

    @staticmethod
    def string_to_pitch_class_fast(p_quality):
        new_intervals = CHORD_QUALITIES[DEFAULT_SYSTEM][p_quality]
        new_intervals = [item for item in new_intervals if item is not None] if len(new_intervals) > 0 else None
        return new_intervals

    # not used
    @staticmethod
    def get_pitch_class_by_quality(p_quality, p_system = DEFAULT_SYSTEM):
        for key in CHORD_QUALITIES[p_system].keys():
            if p_quality in key: 
                return CHORD_QUALITIES[p_system][key]

        return None

    @staticmethod
    def get_item_repetition_count(p_intervals): 
        result = 0

        for interval in p_intervals:
            repeats = len([item for item in p_intervals if item.simplify().get_semitones() == interval.simplify().get_semitones()])
            
            if repeats > 1: 
                result += repeats

        return result

    # Transformation

    @staticmethod
    def simplify_intervals(p_intervals):
        new_intervals = [item.simplify() for item in p_intervals]
        new_intervals = Utilities.sort_intervals(new_intervals)
        return new_intervals

    @staticmethod
    def scale_intervals_by_order(p_intervals, p_fixed_invert = P8):
        result = []
        previous = -m2

        for interval in p_intervals:
            while interval <= previous: 
                interval = interval + p_fixed_invert

            previous = interval
            result.append(interval)

        return result

    @staticmethod
    def sort_intervals(p_intervals): 
        p_intervals.sort()
        return p_intervals

    # not used
    @staticmethod
    def new_normalize_intervals(p_intervals, p_reference_point_position = P1):
        delta = p_intervals[0] + p_reference_point_position
        new_intervals = [item - delta for item in p_intervals]
        return new_intervals

    @staticmethod
    def normalize_intervals(p_intervals): 
        return [item - p_intervals[0] for item in p_intervals]

    @staticmethod
    def invert_intervals(p_intervals, p_fixed_invert = P8):
        new_intervals = [-item for item in p_intervals][::-1]
        return new_intervals

   # not used
    @staticmethod
    def new_invert_static(p_intervals, p_inversion_number = 1, p_fixed_invert = None, p_reference_point_position = P1):
        temp_fixed_move = p_fixed_invert if p_fixed_invert is not None else (p_intervals[-1].roof() - p_intervals[0].floor())
        new_intervals = p_intervals[:]

        if p_inversion_number == 0: 
            return p_intervals

        else:
            remove_p1 = False

            if P1 not in new_intervals:
                new_intervals.append(P1)
                new_intervals = Utilities.sort_intervals(new_intervals)
                remove_p1 = True
        
            index = new_intervals.index(P1)

            if p_inversion_number > 0: 
                new_intervals = new_intervals[1:] + [new_intervals[0] + temp_fixed_move]
                new_reference_point_position = new_intervals[index] - new_intervals[0]

            elif p_inversion_number < 0: 
                new_intervals = [new_intervals[-1] - temp_fixed_move] + new_intervals[:-1]
                new_reference_point_position = new_intervals[index] - new_intervals[0]

        sign = p_inversion_number / abs(p_inversion_number)
        new_intervals = Utilities.new_normalize_intervals(new_intervals, new_reference_point_position)

        if remove_p1:
            new_intervals = [item for item in new_intervals if item != P1]

        return Utilities.new_invert_static(new_intervals, p_inversion_number - sign, temp_fixed_move, new_reference_point_position)

    @staticmethod
    def invert_static(p_intervals, p_inversion_number = 1, p_fixed_invert = None):
        temp_fixed_move = p_fixed_invert if p_fixed_invert is not None else (p_intervals[-1].roof() - p_intervals[0].floor())

        if p_inversion_number == 0: 
            return p_intervals

        elif p_inversion_number > 0: 
            temp_new_intervals = Utilities.normalize_intervals(p_intervals[1:] + [p_intervals[0] + temp_fixed_move])

        elif p_inversion_number < 0: 
            temp_new_intervals = Utilities.normalize_intervals([p_intervals[-1] - temp_fixed_move] + p_intervals[:-1])
        
        return Utilities.invert_static(temp_new_intervals, p_inversion_number - (p_inversion_number/abs(p_inversion_number)), temp_fixed_move) if abs(p_inversion_number) != 1 else temp_new_intervals

    @staticmethod
    def build_on_thirds_static(p_intervals):
        return [item for item in Utilities.re_arrange_intervals_as_thirds(p_intervals) if item != None]

    @staticmethod
    def re_arrange_intervals_as_thirds(p_intervals, p_system = DEFAULT_SYSTEM):
        new_interval_list = []

        for interval in p_intervals:
            possible_intervals = []

            while (((interval.get_numeral() - 1) % 2) != 0 and interval < P8) or interval < P1: 
                interval += P8

            while (((interval.get_numeral() - 1) % 2) != 0 and interval > P8) or interval > M13: 
                interval -= P8

            new_interval = interval

            if new_interval != P8: 
                new_interval_list.append(new_interval)

        new_interval_list = Utilities.sort_intervals(new_interval_list)
        previous_numeral = -1
        i = 0

        while i < len(new_interval_list):
            if new_interval_list[i].get_numeral() - previous_numeral != 2:
                difference = new_interval_list[i].get_numeral() - previous_numeral

                for j in range(int((difference - 2)/2)):
                    new_interval_list.insert(i, None)
                    i += 1

            previous_numeral = new_interval_list[i].get_numeral()
            i += 1

        return new_interval_list

    # Heuristics

    @staticmethod
    def pitch_class_to_scale_steps(p_intervals):
        result = []
        previous = P1

        for interval in p_intervals[1:]:
            result.append((interval - previous).get_semitones())
            previous = interval

        result.append(abs(p_intervals[-1].simplify().get_semitones() - 12))
        return result

    @staticmethod
    def pitch_class_to_decimal(p_intervals): 
        return int(Utilities.pitch_class_to_binary(p_intervals), 2)

    @staticmethod
    def pitch_class_to_binary(p_intervals):
        result = ""
        intervals_simplified = Utilities.simplify_intervals(p_intervals)

        for i in range(12):
            if len([item for item in intervals_simplified if i == item.get_semitones()]) == 0: 
                result += "0"

            else: result += "1"

        return result[::-1]

    @staticmethod
    def decimal_to_pitch_class(p_integer, p_use_distinct_intervals = False): 
        return Utilities.binary_to_pitch_class('{0:012b}'.format(p_integer))

    @staticmethod
    def binary_to_pitch_class(p_binary): 
        return Utilities.scales_steps_to_distinct_pitch_class(Utilities.binary_to_scale_steps(p_binary))

    @staticmethod
    def binary_to_scale_steps(p_binary):
        binary = p_binary[len(p_binary)::-1]
        binary = (binary + binary[0])[1:]
        scale_steps = []
        semitones = 0

        for i in range(len(binary)):
            if binary[i] == '0': 
                semitones += 1
            else:
                semitones += 1
                scale_steps.append(semitones)
                semitones = 0
        
        return scale_steps

    @staticmethod
    def scale_steps_to_pitch_class(p_scale_steps, p_system = DEFAULT_SYSTEM):
        counter = 0
        possible_intervals_collection = [(P1, P1, P1)]

        for i in range(len(p_scale_steps) - 1):
            integer = p_scale_steps[i]
            counter = counter + integer
            possible_intervals_collection.append(Interval.get_possible_intervals(counter))

        all_combinations = list(itertools.product(*possible_intervals_collection))
        min_combination = None
        min_repeat_size = 1000
        min_accidental_count = 1000
        min_sharp_count = 1000

        for combination in all_combinations:
            temp_repeat_size = statistics.mean([len(list(group)) for key, group in itertools.groupby([item.get_numeral() for item in combination])])
            temp_accidental_count = len([item for item in combination if item.get_accidental_BL() != ACCIDENTALS[p_system][0]])
            temp_sharp_count = len([item for item in combination if ACCIDENTALS[p_system][1] in item.get_accidental_BL()])

            if temp_repeat_size < min_repeat_size:
                min_combination = combination
                min_repeat_size = temp_repeat_size
                min_accidental_count = temp_accidental_count

            if temp_repeat_size == min_repeat_size and (temp_accidental_count < min_accidental_count or temp_sharp_count < min_sharp_count):
                min_combination = combination
                min_accidental_count = temp_accidental_count
                min_sharp_count = temp_sharp_count

        return list(min_combination)

    @staticmethod
    def scales_steps_to_distinct_pitch_class(p_scale_steps):
        result = [P1]
        semitones = 0

        for i in range(len(p_scale_steps) - 1):
            semitones = semitones + p_scale_steps[i]
            result.append(Interval(semitones, i + 2))

        if len([item for item in result if len(item.get_accidental_BL()) > ACCIDENTAL_LIMIT]) > 0: 
            return Utilities.scale_steps_to_pitch_class(p_scale_steps)

        return result

    # not used
    @staticmethod
    def tones_to_pitch_class(p_tones): 
        return Utilities.scale_intervals_by_order([tone - p_tones[0] for tone in p_tones])

    @staticmethod
    def identify_parent_scale(p_bass_triad_quality, p_extensions_quality, p_extensions_size = 14):
        result_scale = []
        extension_size = 14 if p_extensions_size is None else p_extensions_size

        if p_bass_triad_quality is not None:
            indeces = (1, 3, 5) if p_extensions_quality is not None else (1, 2, 3, 4, 5, 6, 7)
            result_scale += [item.simplify() for item in Utilities.string_to_pitch_class_fast(p_bass_triad_quality) if item.simplify().get_numeral() in indeces and item.get_numeral() <= extension_size]

        if p_extensions_quality is not None:
            indeces = (2, 4, 6, 7) if p_bass_triad_quality is not None else (1, 2, 3, 4, 5, 6, 7)
            result_scale += [item.simplify() for item in Utilities.string_to_pitch_class_fast(p_extensions_quality) if item.simplify().get_numeral() in indeces and item.get_numeral() <= extension_size]
        
        new_intervals = Utilities.sort_intervals(result_scale)
        return new_intervals

    # not used
    @staticmethod
    def find_root(p_intervals):
        temp_delta = (len(p_intervals) - Utilities.get_inversion_static(p_intervals))
        root_position = p_intervals[temp_delta] if temp_delta != len(p_intervals) else p_intervals[0]
        new_intervals = [P1, root_position]
        return new_intervals

    @staticmethod
    def get_inversion_static(p_intervals):
        temp_counter = 0
        temp_fixed_invert = p_intervals[-1].roof() - p_intervals[0].floor()
        temp_first_inversion = Utilities.get_root_position_static(p_intervals)
        temp_next_inversion = Utilities.invert_static(p_intervals, 1, temp_fixed_invert)

        while temp_next_inversion != temp_first_inversion:
            temp_next_inversion = Utilities.invert_static(temp_next_inversion, 1, temp_fixed_invert)
            temp_counter += 1

        return (len(p_intervals) - temp_counter) - 1

    @staticmethod
    def get_parent_chord_static(p_intervals, p_root = None, p_bass_triad_quality = None, p_extensions_quality = None, p_fixed_invert = None, p_system = DEFAULT_SYSTEM):
        data = Utilities.get_root_position_static(p_intervals, p_root, p_bass_triad_quality, p_extensions_quality, p_fixed_invert, p_system)
        data["Parent Chord"] = Utilities.build_on_thirds_static(data["Root Position"])
        return data

    @staticmethod
    def get_root_position_static(p_intervals, p_root = None, p_bass_triad_quality = None, p_extensions_quality = None, p_fixed_invert = None, p_system = DEFAULT_SYSTEM):
        if p_root is not None:
            new_intervals = Utilities.intervals_relative_to(p_root[1], p_intervals)
            new_intervals = Utilities.normalize_intervals(new_intervals)

            data = {
                "Root": p_root,
                "Root Position": new_intervals
            }

            return data

        elif p_bass_triad_quality is not None or p_extensions_quality is not None:
            eval_bass_triad = lambda x: Utilities.evaluate_quality_assignments(Utilities.build_on_thirds_static(x), slice(None, 3, None), p_bass_triad_quality if p_bass_triad_quality is not None else p_extensions_quality, p_system)[0]["Evaluation"]
            eval_extensions = lambda x: Utilities.evaluate_quality_assignments(Utilities.build_on_thirds_static(x), slice(3, None, None), p_extensions_quality if p_extensions_quality is not None else p_bass_triad_quality, p_system)[0]["Evaluation"]
            eval_function = lambda x: eval_bass_triad(x) + eval_extensions(x)

        else:
            eval_function = lambda x: sum([item.get_semitones() for item in Utilities.build_on_thirds_static(x)])

        if len(set([item.get_numeral() for item in p_intervals])) == 7:
            data = {
                "Root": [P1, P1],
                "Root Position": p_intervals
            }

            return data

        duplicates_found = False
        previous = p_intervals
        index = 0
        smallest_inversion = previous
        min_intervals_sum = eval_function(p_intervals)
        fixed_invert = p_intervals[-1].roof() - p_intervals[0].floor() if p_fixed_invert is None else p_fixed_invert

        for i in range(len(p_intervals) - 1):
            temp_intervals = Utilities.invert_static(previous, 1, fixed_invert)
            temp_intervals_sums = eval_function(temp_intervals)
            
            if temp_intervals_sums < min_intervals_sum:
                index = i + 1
                duplicates_found = False
                smallest_inversion = temp_intervals
                min_intervals_sum = temp_intervals_sums
                
            elif temp_intervals_sums == min_intervals_sum: 
                duplicates_found = True
                
            previous = temp_intervals

        data = {
            "Root": [P1, p_intervals[index]],
            "Root Position": smallest_inversion
        }

        return data

    @staticmethod
    def intervals_to_quality(p_intervals, p_bass_triad_quality = None, p_extensions_quality = None, p_system = DEFAULT_SYSTEM):
        bass_triad_qualities = Utilities.evaluate_quality_assignments(p_intervals, slice(None, 3, None), p_bass_triad_quality, p_system)
        extensions_qualities = Utilities.evaluate_quality_assignments(p_intervals, slice(3, None, None), p_extensions_quality, p_system)
        possible_qualities = []

        for extensions_quality_data in extensions_qualities:
            for triad_quality_data in bass_triad_qualities:

                data = {
                    "Bass Triad Quality": triad_quality_data["Quality"], 
                    "Bass Triad Accidentals": triad_quality_data["Accidentals"], 
                    "Bass Triad Omissions": [item for item in triad_quality_data["Omissions"] if item[1].get_numeral() < max([x.get_numeral() for x in p_intervals if x])],
                    "Extensions Quality": extensions_quality_data["Quality"],                 
                    "Extensions Accidentals" : extensions_quality_data["Accidentals"], 
                    "Extensions Omissions": [item for item in extensions_quality_data["Omissions"] if item[1].get_numeral() < max([x.get_numeral() for x in p_intervals if x])],
                    "Extensions Size": max([x.get_numeral() for x in p_intervals if x])
                }

                evaluation = triad_quality_data["Evaluation"] + extensions_quality_data["Evaluation"]
                if triad_quality_data["Quality"] != extensions_quality_data["Quality"]: evaluation += 1
                possible_qualities.append((data, evaluation))

        return min(possible_qualities, key=lambda x: x[1])[0]

    @staticmethod
    def evaluate_quality_assignments(p_chord_intervals, p_slice, p_quality = None, p_system = DEFAULT_SYSTEM):
        chord_qualities = []
        in_qualities = [p_quality] if p_quality is not None else CHORD_QUALITIES[p_system].keys() 

        for key in in_qualities:
            temp_in_chord_intervals = p_chord_intervals[p_slice]
            temp_chord_quality_chord = [item for item in CHORD_QUALITIES[p_system][key] if item is not None][p_slice]

            evaluation = 0
            temp_accidentals = []
            omitted_intervals = []

            for interval in temp_chord_quality_chord:
                if interval.get_numeral() not in [item.get_numeral() for item in temp_in_chord_intervals]: 
                    omitted_intervals += [(OMISSION_NOTATION[p_system], interval)]
                    evaluation += 1
                    
                else:
                    for item in [item for item in temp_in_chord_intervals if item.get_numeral() == interval.get_numeral()]:
                        if item != interval:
                            temp_accidentals += [("", item)]
                            evaluation += 1

            chord_qualities.append({
                    "Quality": key, 
                    "Accidentals": temp_accidentals, 
                    "Omissions": omitted_intervals, 
                    "Evaluation": evaluation
                    })

        return chord_qualities