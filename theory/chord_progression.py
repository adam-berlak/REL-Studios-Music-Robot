class Transformation:

    def __init__(self, p_antecident):
        self.invert_even_beats
        self.invert_odd_beats
        self.invert_middle
        self.invert_start_to_end

        self.anchor_even_beats
        self.anchor_odd_beats
        self.anchor_middle
        self.anchor_start_to_end

        self.transposition
        self.relative_substitution
        self.parallel_substitution
        self.negative_substitution

        self.continuation

    def get_consequent(self):

        if Transformation.FORCE_DECEPTIVE_RROGRESSION:
            # ENSURE THAT THE CHORD IN BEAT 2 RESOLVES BY FIFTH/FOURTH HARMONIC MOTION TO BEAT 3

        if not Transformation.ALLOW_DIMINISHED_CHORDS:
            # SCENARIO 1: ALLOW PARALLEL CORRECTION
            # SCENARIO 2: ALLOW RELATIVE SUBSTITUTION

        if Transformation.PRESERVE_TRANSPOSITION:
            # SCENARIO 1: WITH ODD BEAT AS ANCHOR HARMONY MUST MOVE IN THE SAME DIRECTION AS TRANSPOSITION
            # SCENARIO 2: WITH START AND END BEAT AS ANCHOR HARMONY MUST MOVE IN THE SAME DIRECTION AS TRANSPOSITION

        if Transformation.ESNURE_TONICIZED:
            # There is a lingo for this called Masculine and Feminine Cadences, feminine where the cadences appear on the odd beats
            # SCENARIO 1: STARTS WITH A 1 ENDS WITH A V
            # SCENARIO 2: STARTS WITH A V ENDS WITH A 1
            # SCENARIO 3: STARTS WITH A IV ENDS WITH A 1
            # SCENARIO X: STARTS WITH A X (NON TONIC CHORD) ENDS WITH A 1
            
            if Transformation.CORRECT_INVERSIONS:
                # TONIC MUST BE IN FIRST INVERSION UNLESS WE IT IS THE FIRST CHORD IN SCENARIO X

        if Transformation.ESNURE_HARMONIC_SMOOTHNESS:
            # ENSURE EVERY CHORD FLOWS VIA FIFTH/FORTH MOTION. 
            # IF WE CAN TRANSPOSE A SECTION OF MUSIC UP OR DOWN A THIRD WITHOUT CREATING A NINTH ACROSS THE MELODIC/HARMONIC LINE DO IT
                # SCENARIO 1: CHORDS: G-C-E-A. MELODY: F-E-D-C, THEN WE CAN REPLACE HARMONY WITH: CHORDS: G-C-G-C
                # SCENARIO 2: CHORDS: G-C-E-A. MELODY: D-C-B-A, THEN WE CAN REPLACE THE HARMONY WITH: CHORDS: G-C-G-A
                # SCENARIO 3: CHORDS: C-G-A-E. MELODY: C-B-A-G#, THEN WE CAN NOT REPLACE ANYTHING

        if Transformation.ENSURE_MELODIC_SMOOTHNESS:
            # ENSURE MELODY MOVES BY STEP
            # WHEN WE MIRROR THE HARMONIC MOVEMENT EXACTLY ON THE MELODIC LINE, THIS CAN CREATE LEAPS IN THE MELODY, WE CAN APPLY TRANSFORMATIONS THAT RETAIN TRANSPOSITION BUT ALSO CORRECT THIS ISSUE
                # CHORDS: C-D-B-C. MELODY: C-D-B-C, WE CAN CORRECT THIS IN TWO WAYS
                    # SCENARIO 1: C-B-B-A IF WE MOVE EVENS DOWN (THIS CREATES A NINTH ACROSS HARMONY AND MELODY)
                    # SCENARIO 2: E-D-D-C IF WE MOVE ODDS UP

        if Transformation.AVOID_NINTHS:
            # SCENARIO 1: WE APPLY TWO CHORDS TO THIS BEAT
            # SCENARIO 2: WE USE A DECEPTIVE CADENCE

        if self.continuation:

            if not self.SENTENCE_STRUCTURE: 
                # REPEAT BEAT 2 ON BEAT 3, BEAT 4 MUST BE A PAUSE

                if Transformation.AVOID_PAC:
                    # ENSURE THAT ALL MOTIFS AND NESTED MOTIFS BEHAVE ACCORDING TO 1-X

            else: 
                # FILL ANY GAPS IN ANTECIDENT, BEAT 4 MUST BE A PAUSE

                if Transformation.AVOID_PAC:
                    # IF A PERFECT AUTHENTIC CADENCE OCCURES PREMATURELY REPLACE IT WITH A DECEPTIVE CADENCE OR A CADENTIAL 6/4

                    # SCENARIO 1: STARTS WITH A 1 ENDS WITH A V: ONLY FIRST BEAT CAN BE A PAC
                    # SCENARIO 2: STARTS WITH A V ENDS WITH A 1: ONLY LAST BEAT CAN BE A PAC
                    # SCENARIO 3: STARTS WITH A IV ENDS WITH A 1: ONLY LAST BEAT CAN BE A PAC
                    # SCENARIO X: STARTS WITH A X (NON TONIC CHORD) ENDS WITH A 1: ONLY LAST BEAT CAN BE A PAC


        if Transformation.MODULATE_TO_START:
            # TAKE THE TRANSPOSITION TO THE CONSEQUENT AND DERIVE THE OPPOSITE DIRECTION, REPLACE BEAT 4 WITH THE SECOND HALF OF THIS CONSEQUENT

            # SCENARIO 1: FINAL CHORD BASS NOTE IS NOT THE FIFTH OR LEADING TONE

                # IF THE BEAT WE ARE REPLACING IS ALREADY A TRANSPOSITION OF ITS CORRESPONDING ANTECEDENT APPLY THE MODULATION TO THE SECOND HALF OF THAT INNER STRUCTURE

                if Transformation.FORCE_OFFBEAT_TRANSPOSITION:
                    # IF THIS IS TRUE THEN WE MODIFY BEAT 2-3 SUCH THAT IT MIRRORS THE RELATIONSHIP BETWEEN BEAT 4-1

            # SCENARIO 2: 
                # SCENARIO 1: FINAL CHORD IS A V CHORD: DO NOTHING
                # SCENARIO 2: FINAL CHORD MUST BE A DIMINISHED CHORD, DO A RELATIVE SUBSTITION
                # SCENARIO 3: THE FIFTH OF SOME CHORD IS BEING PLAYED IN THE BASS
                    # SECNARIO 1: IF THE NOTE IS THE ROOT OF THE V THEN DO A NEGATIVE SUBSTITION
                    # SCENARIO 2: NOT SURE ATM