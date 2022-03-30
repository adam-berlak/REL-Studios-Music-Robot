# [BUG] print(Ostinato(Chord(Scale(F, minor)[::3]), [5, 6, 5, 4, 3, 2, 1, 1, 8, 4, 5, 7, 6, 6, 5, 5]))
# [BUG] Chord(Scale(C, major)[::3]).transpose(-2)[5]
# [BUG] Chord(Scale(C, major)[::3])[::-3].get_root_position()
# [BUG] Scale(C, major)[::-1]
# [BUG] Scale(C, major)[::-2].get_name()
# Finish chord, go through all objects and ensure all methods call BL, update interface class
# When getting secondary chords maybe we should use the transpose method?
# Need to verify if adding the "and p_fixed_invert != P1" to the intervalsRelativeTo method doesnt break anything
# Candidates has empty sequencers for some reason and waltz still has min arg error
# [BUG] Test tone changes
# [BUG] When we reach the constructor for Scale the unaltered intervals become incorrect, need to fix this, also check if the unaltered intervals/reference point position is changed correctly for all methods
# [Feature] Chord(C7, "maj7") / Chord(G5, "dom7") => <Chord G5, B5, D6, F6, C7, E7, G7, B7> with child object built on C7 => <Chord, C7, E7, G7, B7>, the parent in this case is a chord part, when you alter the child we will need to reference the parent chords bass chord and build the new chord off of that, for this reason the parent chord must have a reference to the bass chord and the child chord
	# Maybe add new attribute to items to indicate if the item is added
	# Whenever reference point is a part we need to call getOriginalChord()
	# Create get original chord method to get chord without added items
# [Feature] modes are a result of transpositions so getModes() should use the transpose method
# [Feature] need to create getCache method
# [Feature] Need to add negative interval support for from string in fast interval
# [Functional Issue] Cant instantiate a Chord object without doing all the quality logic since this impacts the parent item
# [Functional Issue] Need to fix issue where if we derive unaltered intervals from the qualities of a chord, it assumes we are at root position
# [Code Cleanliness] Need to add support for instance methods, and update some methods like add interval to update the current instance, also add a copy method (This might be difficult with circular references, might need to look into how to do deepcopy with a circular reference)
# [Code Cleanliness] Chord has a p_nodulate_parent method
# [Code Cleanliness] Remove brackets from if statements
# [Done] [Code Cleanliness] Create wrapper/BL classes for classes in Scale and Chord
	# [Done] IntervalList
	# [Done] Chord
	# [Done] Scale
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
# [Code Cleanliness] Organize all classes to have methods in the order I have decided
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
# [Code Cleanliness] Make sure all BL methods are referencing other BL methods, we can do this by commenting out the non-bl methods and seeing which methods throw an error
# [Code Cleanliness] When creating new intervallist or subclasses of intervallist we need to use type(self)
# [Code Cleanliness] Update all methods to use the new GenericInterval object
# [Code Cleanliness] Range in Interval needs to work similarly to the one in IntervalList. IE in intervallist we should keep checking intervals even if the first item we check is not within bounds, and Range in Interval needs to return a sorted list, also change return variable name from new_numerals, also fix using 1 as step in both
# [Code Cleanliness] Need to ensure wrapper classes have the same arguments as the business logic classes
	# [Done] IntervalList
# [Code Cleanliness] Dont need deriveUnalteredIntervalsFromParent, we can just use intervalsRelativeTo
# [Code Cleanliness] Need to fix getGenericInterval because of the change for getReferencePointPosition() and replace instances of invertStatic() with new one, also need to replace size comparison with numerals again
# [Code Cleanliness] Updated all methods that create new interval lists in IntervalList, need to verify that the new attributes are correct
# [Code Cleanliness] for methods that check if sublist we need to add a parameter that can override this, and if we override we need to check if the intervallist has a parent
	# IntervalList
	# Scale
	# Chord
# [Outdated] [Code Cleanliness] rsub needs to flip which one is getting subbed
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# Generic Interval
# [Outdated] Issues with build when scale is rootless
# [Outdated] [Functional Issue] Interval.getRoof().getRoof() needs to be the same as Interval.getRoof()
# [Outdated] First element in Interval.inRange(1,4,3) is negative, need to update build logic as well to use the new range method I created
# [Outdated] Build Pitch Class is behaving weirdly with get_negative
# [Outdated] Need to fix buildPitchClass
# [Outdated] In fast interval we need to simplify the numeral when calling from string and also negate if the accidental sign is negative, also there was an infinite loop when we didnt have accidental sign
# [Outdated] Need to create a method for updating the list of attributes that are dependant on a reference point
# [Done] [BUG] [Possible Issue] Accidentals are weird Scale(C, major)[:30:m3]
# [Done] [BUG] Scale(C, [P1, P8, P15])
# [Done] [BUG] C_Major_Scale[5:6] / C_Major_Scale[5:8:3]
# [Done] [BUG] Scale(C, major)[::-1] infinite loop
# [Done] [Code Cleanliness] Remove references to build instead use getitem logic
# [Done] [Code Cleanliness] Need to add constants for flat/dim intervals
# [Done] [Code Cleanliness] Need to update how roof and floor is determines in Intervallist Scale and Object to match whats in get_negative()
# [Done] [Code Cleanliness] Make sure everything is using the Interval getSign() method
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] Need to update Chord and Scale so their addition attributes are also updated correctly when calling methods in IntervalList # Added all of these under the chord Overridden Business Logic Methods, scale has the same attributes as intervallist so we dont need to handle this
# [Done] [Code Cleanliness] Remove brackets from if statements
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] Add local variables for new objects
	# Should probably do this with the object methods as well
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] if case is not handled for sub call (-p_other).__add__(self)
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] if case is not handled for add call other add
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] if case is not handled for radd call add
	# [Done] Tone
	# [Done] Key
	# [Done] Note
	# [Done] Interval
	# [Done] IntervalList
	# [Done] Scale
	# [Done] Chord
	# [Done] Generic Interval
# [Done] [Code Cleanliness] intervallist has a p_intervals param not p_item_2
# [Done] [Code Cleanliness] Need to update constructors of Chord and Scale
# [Done] [Code Cleanliness] Tone shouldnt take a string as a parameter since these are defined in a dict, it should be an int referencing the key for the tone name in the dict
# [Done] [Code Cleanliness] type dict and intervals should not be attributes of intervallist since they are part of item
# [Done] [BUG] Chord(Scale(C, major)[::3]).get_negative()
# [Done] [BUG] Chord(C, "maj7") + 2
# [Done] update build
# [Done] Negative step for indexing we should increase the bounds of the IntervalList
# [Done] Need to add support for numeral notation for items for negative intervallists
# [Done] [Funtional Issue] When calling scale[::-2] we need to change the sign somehow
# [Done] Scale(C, major).get_parellel()[::2] roof is wrong, constructor needs to account for direction when verifying floor and roof, also need to fix flipIntervals
# [Done] [Functional Issue] Scale(C, major).get_negative()[-2][::-3]
# [Done] [Functional Issue] If we add a P8 to an IntervalList that has a floor of -P8 and a roof of P8 there will be an infinite loop
# [Done] [Functional Issue] If we build a scale on Intervals [-M7, -M6, -P5, -P4, -M3, -M2, P1] then roof would be incorrect, it should be P1 not P8: roof of -P1 should be P1 and vice versa for P1 and floor
# [Done] [BUG] Scale(C, major)[2][::].get_parellel()
# [Done] [BUG] Chord(Scale(C, major)[1:14:3]).get_quality() is wrong
# [Done] [BUG] Scale(C, major)[-3].build(Chord, "maj7").get_negative() and Scale(C, major)[4].build(Chord, "maj7").get_negative() are wrong, caused by the fact that we are comparing against numerals now instead of intervals
# [Done] [Functional Issue] P1 and -P1 need to be the same
# [Done] [Functional Issue] numeral 1 and -1 need to be same in getitem
# [Done] [BUG] Chord(Scale(C, melodic_minor_ascending)[::3]).get_parellel() infinite loop
# [Done] (Scale(C, major).get_negative()[::-2] + 1).getIntervals() are negative when they shouldnt be
# [Done] (Scale(C, major).get_negative()[::-2] + 1).getIntervals() 1 behaves like 2
# [Done] [BUG] Scale(C, major)[2][::].get_parellel() is wrong
# [Done] [Functional Issue] Need to fix generic interval method for Scale(C, major)[2][::].get_parellel()
# [Done] getitem doesnt use start or stop
# [Done] Need to put range logic in getitem for intervallist, add getParentIntervalListItem to tone/IptichedObject, when using slice open ended we check the numeral of floor and roof
# [Done] Chord(Scale(C, major)[5][::3]) results in error
# [Done] Most recent thing that I did: Change getRoot() to return an interval list, and updated all methods that call this. Need to create a new method for creating new objects without using getAttributes(), need to instead only return IntervalList objects in IntervalList and override the methods that should update new attributes. Also, getAttributes() should only contain attributes that arent in IntervalList, and we should default to whatever these are if the parent method is not overriden
# [Done] Need to update get_parellel logic to behave like the Chord version
# [Done] get_relative in chord does not behave the same as in a scale
# [Done] the configure reference item in chord needs cases for ipitchedobject and tone
# [Done] String to pitch class needs to return the key not the string for quality
# [Done] Need to update getParentChordStatic with new parameters for additional context
# [Done] Chord(Scale(C, major)[2][1,3,dim5,7]) errors
# [Done] Need to add attributes to get attributes for intervallist and simplify code
# [Done] error/infinite loop when trying to use range with m3 when indexing a Scale
# [Done] Scale has a variable named temp_var
# [Done] Scale(C, harmonic_major)[m3].getAlteration() is wrong
# [Done] If we add a b1 to a scale this is a valid scenerio since a child chord or scale might alter this degree, yet we assume the lowest an interval can be is a P1, need to add support for intervals below this, intervallist should have a root just like a chord for this scenerio, methods like normalizeIntervals need to be updated to account for this
# [Done] Dependancies, the root of the chord should be an interval and should be updated along with the unaltered intervals
# [Done] Need to use the input params of the Chord when trying to isolate the quality
# [Done] Right now we dont handle tones correctly with new Chord logic
# [Done] When we do degree arithmetic with Chord parts we set the current chord part as the parent item. chord parts shouldnt be parents
# [Done] When deciding whether we build a chord of a new scale thats based off the qualities or just stick to the main scale, we should base this off whether the unaltered intervals encompassed by the extension are different from the parent. We also need to add an extension parameter to the class
# [Done] Create getSign() method for Interval

import random
import sys

# Internal Dependancies


#from ai.analyser import *
#from io.sequencer import *
from theory.config import *
from theory.interval_list import *
from theory.scale import *
from theory.chord import *
from theory.interval import *
from theory.tone import *
from theory.key import *
from theory.note import *
from theory.ostinato import *

def main():
	
	'''
	Chord(Scale(F5, minor)[-3][::3])[3]{
		1: [5:4,2:8,-2:8,-2:8,-2:8,-2:4.5,-2:8,1:8]
		2: [0:4,5:4,1:4           ,0:4 ,1:4 ,1:4  ]
		3: [0:4,3:4,1:4           ,0:4 ,1:4 ,1:4  ]
		4: [0:2.5                 ,0:4 ,1:4 ,1:4  ]
		5: [1:2.5                 ,-2:2.5         ]
	} + Chord(Scale(F5, minor)[2][::3])[1]{
		1: [8:4,-5:8,2:8,3:8,-2:8,1:4.5,-2:8,1:4]
		2: [0:4,-2:2.5           ,0:4, -2+8:4,1:4]
		3: [0:4,1:2.5            ,0:4]
		4: [-2:2            ,-3:4,-4:2.5          ]
	}
	'''
	test_chord = Chord(Scale(C, major)[5][:8:3])
	test_chord_2 = test_chord.resolve_chord()
	print(Ostinato(Chord(Scale(C, major))[::3], [1, 5, 7, 5]))
	print(Ostinato(Chord(Scale(C, major))[::3], [1, 5, 7, 5]).transpose_BL(-2))
	to_json(Scale(C, major), {})
	Tone(0, -3) - C
	Key(Tone(0, -3), 4) - Key(C, 4)
	Scale(C, major)[2]
	Scale(C, major)[:30:m3]
	'''
	print(Chord(C4, "maj7").getItems()[1])
	Chord(C, "maj7")
	print(Chord(C, "maj7"))
	Key(C_flat, 4).get_relatives()
	P8.simplify()
	Key(Tone("E", -2), 4) - Key(Tone("C", -1), 4)
	Key(Tone("C", -1), 4) + Interval(3, 1)
	Key(Tone("C", 2), 4) - Key(Tone("C", -1), 4)
	B4.get_relatives()
	C4 < D4
	local_dir = "C:\\Users\\adamb\\github\\REL-Studios-Music-Robot\\IOMidi\\MidiFiles\\"
	chopin_waltz = Sequencer()
	chopin_waltz.fromMidi(local_dir + 'waltz_34_2.mid')
	Sequencer.toDict(chopin_waltz)
	Sequencer.flattenDict(Sequencer.toDict(chopin_waltz))

	candidates = []
	analyser = Analyser(chopin_waltz)

	for seed in range(10):
		candidates.append(analyser.candidate(seed))
	
	sequencer = Sequencer()
	sequencer.add(Note(C4, quarter_note), 1)
	sequencer.add(Note(D4, quarter_note), 2)
	sequencer.add(Note(E4, quarter_note), 3)
	sequencer.add(Note(F4, quarter_note), 4)
	sequencer.add(Note(G4, quarter_note), 5)
	sequencer.add(Note(A4, quarter_note), 6)
	sequencer.add(Note(B4, quarter_note), 7)
	sequencer.add(Note(C5, quarter_note), 8)
	sequencer.add(Chord(Note(C5, quarter_note), "maj7b5"), 9)
	sequencer.add(Chord(Note(A4, quarter_note), "min5").invert(), 10)
	sequencer.add(Chord(Note(G4, quarter_note), "min7b5"), 11)
	sequencer.toMidi(local_dir + "file-generated.mid")
	
	
	Scale(C, major)[1].build(Chord, 5, 3)
	#print(Chord(C4, "dom7b3")[1].move(3))
	Scale(C, major)[1].build(Chord, 7, 3)[3].move(-3)
	Scale(C, major)[1,2,3,5,6].rotate()
	Scale(C, major)[1,2,3,5,6].get_relativeScale()
	Scale(C, major)[2].build(Chord, [1, 10, 12])
	Scale(C, major)[2].build(Scale, [P1,M2,M3,P4,P5,M6,M7])
	Scale(C, major)[1].build(Chord, 7, 3).invert(2)
	print(Scale(C, major)[1].build(Chord, 7, 3)[0])
	Scale(C, major)[1].build(Chord, 7, 3).transpose(p_ignore_parent = True)
	Scale(C, major)[1].build(Chord, 7, 3).rotate(p_ignore_parent = True)
	Chord(C, "dom9b9")
	Scale(C, major)[1].build(Chord, "maj7addb3b4")
	Scale(C, major)[1,2,3,5,6][m3].getGenericInterval_BL()
	Scale(C, major)[1,2,m3,4,5].getIntervalsWhere_BL(p_ignore_parent = False)
	Scale(C, major).getIntervals()
	Scale(C, major)[m3].getParentScale().transpose_BL(2)
	Scale(C, major)[1,2,3,5,6][m3].getGenericInterval_BL()
	Scale(C, [P1, M2, m3, M3, P4, P5, M6, M7])[m3].getAlteration_BL()
	Scale(C, major)[m3].isTemp()
	Scale(C, major).remove(1).getTonicTone()
	Scale(C, major)[1,2,3,5,6][4]
	args = {"test": 123}
	Scale(C, major).get_parellelScale()
	print(Scale(C, major)[1,2,m3,5,6][m3].buildPitchClass_BL(2, 3))
	Scale(C, major)[1,2,m3,5,6].get_parellelScale()
	Scale(C, major)[1,2,m3,5,6].get_parellelScale()[2]
	
	Chord(C, "maj7").get_negative()
	str(Interval(0, -1))
	Scale(C, [-P1, -M2, -M3, -P4, -P5, -M6, -M7])
	Scale(C, [-m3, m3])[1]
	(Scale(C, [-m3, P1, m3]) - 2).getUnalteredIntervals()
	Scale(C, [-m3, P1, m3]).getGenericIntervals()
	Scale(C, [-m3, P1, m3])[2].next()
	Scale(C, [-m3, P1, m3]) - 2
	(Scale(C, [-m3, P1, m3]) + m2) + 2
	(Scale(C, [-m3, P1, m3]) - 2).getUnalteredIntervals()
	
	Scale(C, major)[1]
	IntervalListUtilities.newInvertStatic([-m3, P1, m3], 2, None, m3)
	test = Scale(C, major)[-3].build(Chord, "maj7")
	#test.get_negative()
	Scale(C, major)[1].build(Chord, "maj7").get_negative()
	Scale(C, major)[1].build(Chord, 7, 3)[2]
	(Scale(C, major)[1].build(Chord, 7, 3)[2] + 2).getParentChord()
	'''
	#Scale(C, [P1, M9, P15])[2].build(Chord, "maj7").getParentScale()

	C_Major_Scale = Scale(C, major)
	C_Major_Scale_2 = Scale(C, [P1, M2, M3, P4, P5, M6, M7])
	C_Major_Scale_3 = Scale(C, [2, 2, 1, 2, 2, 2, 1])
	C_Major_Scale_4 = Scale([C, D, E, F, G, A, B])
	str(Scale([C, D, E, F, G, A, B]))
	
	# Ways to build a Chord object with a Parent Scale
	C_M7 = C_Major_Scale[1].build(Chord, "maj7")
	#C_M7_2 = C_Major_Scale[1].build(Chord, 4, 3)
	C_M7_3 = C_Major_Scale[1].build(Chord, [P1, M3, P5, M7])
	#C_M7_4 = C_Major_Scale[1].build(Chord, [1, 3, 5, 7])
	C_M7_5 = Chord(C_Major_Scale[1] + C_Major_Scale[3] + C_Major_Scale[5] + C_Major_Scale[7])
	C_M7_6 = Chord(C_Major_Scale[1, 3, 5, 7])
	
	# Ways to build a Chord object without a Parent Scale
	C_M7_6 = Chord(C, "maj7")
	C_M7_7 = Chord(C, [P1, M3, P5, M7])
	C_M7_9 = Chord([C, E, G, B])
	
	# Naming Conventions
	C_Major_Scale.get_name()
	C_Major_Scale.get_cardinality()
	C_Major_Scale.get_mode_names()
	C_Major_Scale[1].get_name()
	C_Major_Scale[1].get_numeral()
	(C_Major_Scale + 2).get_name()
	
	C_M7.get_quality()
	#print(json.dumps(P1.toJson(), indent=4))
	C_M7.get_figured_bass()
	C_M7.get_numeral()
	
	# Arithmetic
	C_Major_Scale + 3																										# Rotates the Scale by a Generic Interval of 3
	C_Major_Scale + m3																										# Transposes the Scale by a Specfic Interval of m3
	C_Major_Scale[1] + 3																									# Returns a Scale-Degree 3 Generic Intervals above the Tonic
	C_Major_Scale[1] + m3																									# Returns a Scale-Degree m3 Specific Intervals above the Tonic
	C_Major_Scale[1] + C_Major_Scale[3]																						# Creates a new Scale containing C and E
	C_Major_Scale[1:2] + C_Major_Scale[4]																					# Adds an F to the Scale <Scale I=C, II=D>
	C_Major_Scale[1:4:3] + C_Major_Scale[5:8:3]																					# Adds the Scale <Scale I=G, II=A> to <Scale I=C, II=D, III=E> => <Scale I=C, II=D, III=E, V=G, VI=A>
	
	C_Major_Scale[3] - C_Major_Scale[1]																						# Returns the Specific Interval between Scale-Degrees 3 and 1 => 3
	
	E - C																													# Returns the Specific Interval between the Tones E and C => b6
	C + m3																													# Returns the Tone a m3 above the Tone C => Eb
	P1 + m3																													# Returns the Sum of the Specific Intervals P1 and m3 => b3
	
	# Chord Inversions and Sub-Setting
	C_64 = C_M7[1:6:3].invert(2)																								# Returns the Second Inversion of a Chord => <Chord I=G, IV=C, vi=E>
	C_64.get_inversion()																										# Returns the inversion number of the Chord in question => 2
	C_64.get_figured_bass()																									# Returns the Figure-Bass notation of the Chord in question => I 6/4
	C_53 = C_64.get_root_position()																							# Returns the First Inversion of the Chord in question => <Chord I=C, iii=E, V=G>
	
	# Resolving Chords and Voice Leading
	'''
	F_643 = C_M7.resolveChord()																								# Returns the result of resolving the Chord in question using Voice Leading Rules => <Chord I=C, iii=E, IV=F, vi=A>
	F_643.get_inversion()																									# Returns the inversion number of the Chord in question => 2
	G_643 = C_M7.resolveChordInto(C_Major_Scale[5].build(Chord, "maj7"))															# Returns the result of resolving the Chord in question into a specific Chord
	G_643.get_inversion()
	'''
	
	# Transformations7
	Ab_M7 = C_M7.get_negative()																							# Returns the Negative-Chord of the Chord in question => <Chord I=Ab, iii=C, V=Eb, bvii=G>
	C_m7 = C_M7.get_parellel()																							# Returns the Parallel-Chord of the Chord in question => <Chord i=C, biii=Eb, V=G, bVII=Bb>
	A_m7 = C_M7.get_relative()																							# Returns the Relative-Chord of the Chord in question => <Chord i=A, biii=C, V=E, bVII=G>
																								
	# Finding alternative Scales
	#C_M7.getPossibleParentScales()
	
	# Secondary Chords
	D_m7 = C_M7 + 2
	A_7 = D_m7.get_secondary_dominant()
	E_o7 = D_m7.get_secondary_sub_dominant()
	D_m5 = D_m7.get_secondary_tonic()
	E_dom7_b5 = D_m7.get_secondary_augmented_six()
	A_dom7_b5 = D_m7.get_secondary_tritone_substitution()
	
	# Complex Chord Building
	Chord(C, "mM11b5no9")
	Chord(C, "m9b5add6")
	Chord(C, "half-dim9sus4b9")
	

if __name__ == "__main__":
	main()