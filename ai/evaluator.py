class Evaluator:

    def __init__(self, p_tone_dict):
        self.tone_dict = p_tone_dict

    def evaluate(self):
        pass

    def eval_changed_keys(self):
    def eval_changed_chords(self):

    def eval_resolved_notes(self, p_parts):
        return sum(sum(Evaluator.eval_resolved_note(antecedent, consequent) for consequent in antecedent.getConsequentParts()) for antecedent in p_parts)

    def eval_resolved_degrees(self, p_parts):
        return sum(sum(Evaluator.eval_resolved_degree(antecedent, consequent) for consequent in antecedent.getConsequentParts()) for antecedent in p_parts)

    def eval_resolved_parts(self, p_parts):
        return sum(sum(Evaluator.eval_resolved_part(antecedent, consequent) for consequent in antecedent.getConsequentParts()) for antecedent in p_parts)

    def eval_resolved_chords(self, p_tone_dict):
        chords = [parts[0].getParentChord() for parts in p_tone_dict.values()]
        return sum(sum(Evaluator.eval_resolved_chord(antecedent, consequent) for consequent in antecedent.getConsequentParts()) for antecedent in chords)

    def eval_resolved_chord(self, p_antecedent_chord, p_consequent_chord):
        delta = abs((p_antecedent_chord.getRoot().getTone() - p_consequent_chord.getRoot().getTone()).simplify())
        return 1 if delta not in [P4, P5] else 0 

    def eval_resolved_note(self, p_antecedent, p_consequent):
        return 1 if p_antecedent.isChromatic() and abs((p_antecedent.getTone() - p_consequent.getTone()).getNumeral()) == 2 else 0

    def eval_resolved_degree(self, p_antecedent, p_consequent):
        return 1 if p_antecedent.isChromatic() and p_consequent.isChromatic() else 0

    def eval_resolved_part(self, p_antecedent, p_consequent):
        return 1 if p_antecedent.isEnharmonic() and p_consequent.isEnharmonic() else 0

    def eval_voice_leading_chord(self, p_antecedent_chord, p_consequent_chord):
        evaluation = 0

        evaluation += Evaluator.eval_parallel_octaves(p_antecedent_chord, p_consequent_chord)
        evaluation += Evaluator.eval_parallel_fifths(p_antecedent_chord, p_consequent_chord)
        evaluation += Evaluator.eval_doubled_altered(p_antecedent_chord)
        evaluation += Evaluator.eval_doubled_leading_tone(p_antecedent_chord)
        evaluation += Evaluator.eval_doubled_root(p_antecedent_chord)
        evaluation += Evaluator.eval_doubled_seventh(p_antecedent_chord)
        evaluation += Evaluator.eval_doubled_ninth(p_antecedent_chord)
        evaluation += Evaluator.eval_guide_tones(p_antecedent_chord)
        evaluation += Evaluator.eval_avoid_notes(p_antecedent_chord)
        evaluation += sum(Evaluation.eval_voice_leading_part(antecedent, consequent) for consequent in antecedent.getConsequentParts() for antecedent in p_antecedent_chord.getParts())

        return evaluation

    def eval_doubled_leading_tone(self, p_antecedent_chord):
        return 1 if len([part for part in p_antecedent_chord.getParts() if part.isLeadingTone()]) > 1 else 0

    def eval_doubled_root(self, p_antecedent_chord):
        return 1 if len([part for part in p_antecedent_chord.getParts() if part.getPositionInParentChord() == 1]) != 2 else 0

    def eval_doubled_seventh(self, p_antecedent_chord):
        return 1 if len([part for part in p_antecedent_chord.getParts() if part.getPositionInParentChord() == 7]) > 1 else 0

    def eval_doubled_ninth(self, p_antecedent_chord):
        return 1 if len([part for part in p_antecedent_chord.getParts() if part.getPositionInParentChord() == 9]) > 1 else 0

    def eval_voice_leading_part(self, p_antecedent, p_consequent):
        evaluation = 0

        evaluation += Evaluation.eval_resolved_seventh(antecedent, consequent)
        evaluation += Evaluation.eval_resolved_third(antecedent, consequent)
        evaluation += Evaluation.eval_skips_resolution_sixth(antecedent, consequent)
        evaluation += Evaluation.eval_fourth_against_bass(antecedent, consequent)
        evaluation += Evaluation.eval_augmented_fourth(antecedent, consequent)
        evaluation += Evaluation.eval_augmented_second(antecedent, consequent)

        return evaluation

    def eval_resolved_seventh(self, p_antecedent, p_consequent):
        return 1 if p_antecedent.getPositionInParentChord() == 7 and (p_antecedent.getKey() - p_consequent.getKey()).getNumeral() == -2 else -1

    def eval_resolved_third(self, p_antecedent, p_consequent):
        return 1 if p_antecedent.getPositionInParentChord() == 3 and (p_antecedent.getKey() - p_consequent.getKey()).getNumeral() == 2 else -1

    def eval_skips_resolution_sixth(self, p_antecedent, p_consequent):
        delta = p_antecedent.getKey() - p_consequent.getKey()
        direction = int(delta.getNumeral() / abs(delta.getNumeral()))
        greater_than_sixth = abs(p_antecedent.getKey() - p_consequent.getKey()).getNumeral() > 6
        changed_direction_list = []

        for item in p_consequent.getConsequentParts():
            delta_2 = p_item.getKey() - p_consequent.getKey()
            direction_2 = int(delta_2.getNumeral() / abs(delta_2.getNumeral()))
            changed_direction = direction != direction_2
            changed_direction_list.append(changed_direction)

        change_in_direction = any(item for item in changed_direction_list)
        return 1 if greater_than_sixth and not change_in_direction else -1

    def eval_fourth_against_bass(self, p_antecedent, p_consequent):
        return 0

    def eval_augmented_fourth(self, p_antecedent, p_consequent):
        return 1 if abs(p_antecedent.getKey() - p_consequent.getKey()) == aug4 else 0

    def eval_augmented_second(self, p_antecedent, p_consequent):
        return 1 if abs(p_antecedent.getKey() - p_consequent.getKey()) == aug2 else 0