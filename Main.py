# TODO:
# COMPLETED: Support #/b notes and assign accidentals correctly
# COMPLETED: Print Roman Numerals
# COMPLETED: Support Non-heptatonic Scales
# COMPLETED: Find solution to multiplying scale for chords to support degrees of > 12 Semitone intervals :: Solution: Chord inherits from scale, it is a scale object but has additional methods like resolve etc. but it also has its own degrees
# COMPLETED: fix building chords with skips greater or less than three
# COMPLETED: Fix notation for non-triadic chords
# COMPLETED: Fix Numeral Addition
# COMPLETED: Remove reliance on Interval objects, instead use semitones as is, interval objects only required for printing and interfacing
# COMPLETED: Automate creation of Interval objects within Scale so that it is always accurate, and have a fixed amount of intervals available for interfacing
# COMPLETED: Add support for subtraction, find better way of looping through degrees IE cycle
# COMPLETED: Fix arithmetic with degrees such that adding a generic interval includes the principle degree, IE C + 3 = E as opposed to F
# COMPLETED: Fix stringToPitchClass
# COMPLETED: Move unaltered_intervals dictionary into constants
# COMPLETED: Add support for stringToInterval in interval class
# COMPLETED: Using buildWithIntervals method should change the parent scale of the resulting scale object if it includes intervals not in the parent, but only if the scale object is a chord
# COMPLETED: Fix Degree addition problem
# COMPLETED: Add support for sus chords in stringToPitchClass method
# COMPLETED: Create a Scale.Dictionary.py file for holding thousands of Scale definitions
# COMPLETED: Create simplify method for Tone and change minimize to simplify in Interval
# COMPLETED: Add full support for sub for Tone class
# COMPLETED: Fix [Interval] in Scale method. It should check each rotation of the Scale
# COMPLETED: Add support for buildWithGenericIntervals
# COMPLETED: If you call a super method in chord, and that super method uses a method thats overridden super is ineffective (Check if class is a subclass)
# COMPLETED: If you build a chord on a Scale Degree that contains Tones not in the principle degree, they should ONLY be added if parent scale degree are not distinct, otherwise they should be transformed
# COMPLETED: All Degree objects should have a parent degree when a parent degree is established for the Root Degree *Added findInParent method*
# COMPLETED: Simplify invert method
# COMPLETED: Created getParallelChord() and transformChordTo() methods
# COMPLETED: Adding a specific interval to a scale degree should not add a new interval to the scale unless it is not distinct
# COMPLETED: Fixed getSecondaryDominant()
# COMPLETED: Get Numeral should return only the numeral
# COMPLETED: getFirstInversion() is not consistant *Checks if duplicates of same number of Nones are found, in which case we just return self*
# COMPLETED: Fix negative intervals and avoid interval with 0 semitones and numerals
# COMPLETED: Fix numeral representation *Fixed, when calling super in invert, the recursive add/sub calls the subclass add and sub after one repeat*
# COMPLETED: Fix adding interval not in chord to chord without context
# COMPLETED: Might need to scale by order for gen intervals in move
# COMPLETED: Tone simplify should return a list of Tones with multiple simple names
# COMPLETED: Printing of negative Intervals
# COMPLETED: Diminished and Augmented chords arent neccissarily built on Thirds so I need to find a new way to identify qualities
# COMPLETED: scaleIntervalsByOrder() should be le and not lt. Also when you use move if new degree already exists in chord it should be removed
# COMPLETED: Support voice leading rules in configuration
# COMPLETED: Add support for chord inversions and sus notes in printQuality()
# COMPLETED: Get parallel key of scale
# COMPLETED: Printing quality of AmM7 is wrong
# COMPLETED: Need to fix scaleStepsToPitchClass so it doesnt include the Intervals array
# COMPLETED: getNegativeChord needs to use first inversion
# COMPLETED: Support invert for chords larger than M13
# COMPLETED: In distanceFromNext() check if it works with scales larger than 7 degrees
# COMPLETED: Resulting Chord from ResolveChord should use same accidentals as inputed chord
# COMPLETED: BUGS TO FIX: next() and previous() for Intervals with mutliple accidentals should work differently *Removed Next and Previous*
# COMPLETED: GetNegativeScale() parameter can be Generic or Specific Interval, and refers to the start of reflection not axis point
# COMPLETED: New Algorithm for Deriving Parallel Scale and Relative Scale:
	# - Go a fifth above root of Scale, invert Scale pitch class, and build a new scale
	# - Go to same scale root a fifth below and build a new scale
	# - Find the mode of the original scale that matches the same pitch class, this is the parallel scale
	# - If scale does not have a reflection axis then the scale has no relative scale
# COMPLETED: Fix the add/sub methods in Key
# COMPLETED: Bug when adding m3 + 6

# LONG-TERM GOAL: Create and fix issues in UnitTest
# LONG-TERM GOAL: Add try-catch statements of invalid inputs 

# NEW FEATURES: Should be able to get a version of an interval with minimal accidentals IE: bb4 = b3
# NEW FEATURES: Change name for the Tone class within the Keyboard object to Key, allow it to play sounds
# NEW FEATURES: Use Diatonic and Generic Intervals together
# NEW FEATURES:
 
''' New Chord Object
		- Chord built on Scale Degrees instead of Intervals
		- When adding a Generic Interval that does not exist to a Chord Degree, a new Chord with that Degree is produced with Non-Harmonic Tone Boolean set True
		- This mirrors Interval Arithmetic in Scale Objects, insteading of "Chromatic Tone" boolean we have "Non-Harmonic Tone" boolean. 
		- Degrees that are both Chromatic and Non-Harmonic and resolve into a Chord Tone have Appoggiatura Boolean set True
		- If any of the Booleans are set to True, the associated degree will be removed from the parent object and the parent object will return to its original state
		- As an example: C_maj_7[1] + [1, 2, -b1, 2, -2] => "[C, D, Db, D, C]"
		- In such a case C is a Harmonic Tone, D is a Non-Harmonic Tone, and Db is a Chromatic Tone
		- This allows for indexing Chords with real Generic intervals IE C_maj_7[3] => "E"
		- When describing a piece in a Sequencer we can now use the highest level of abstraction, a Chord Degree
		- Thus any given Tone in the Sequencer object has a Parent Scale, a Parent Chord, and several booleans that describe its nature
'''

# BUGS TO FIX: [BUG] Key -> Midi Note offset by an octave
# BUGS TO FIX: [BUG] getting closest distance of chord doesnt work for keys because of subtraction, also adding M2 to B in CMAJ7 chord issue?
# BUGS TO FIX: [BUG] C# Octave higher when converted to midi
# BUGS TO FIX: [BUG] int + Interval doesnt work
# BUGS TO FIX: Feature: Allow style for accientals IE b/flat
# BUGS TO FIX: [BUG] Weird behavior when adding generic interval of 0 to a scale
# BUGS TO FIX: Diatonic Interval != Generic Interval
# BUGS TO FIX: Invert calls super of Chord Degree
# BUGS TO FIX: Maybe change how indexing works for Chord
# BUGS TO FIX: Add logic when adding an Interval to a Degree parent scale should change
# BUGS TO FIX: Change how sub works for Key Class
# BUGS TO FIX: Support decimal to pitch class in build
# BUGS TO FIX: Dont use contains for checking if interval in scale, because contains will rotate scale
# BUGS TO FIX: Transform should return degree instead of Scale or Chord
# BUGS TO FIX: Too many overrided methods in Chord, indexing should retrieve parent scale degree instead
# BUGS TO FIX: Transform should either take int or Accidental
# BUGS TO FIX: Override Interval add in Chord Degree
# BUGS TO FIX: [BUG] Possibly fix slice for Chord
# BUGS TO FIX: Possibly change how findInParent returns self if no parent defined
# BUGS TO FIX: In Chord, for all methods that access parentDegree() perfom a check
# BUGS TO FIX: [BUG] Add limitations on getFirstInversion() and getInversion() so that it doesnt loop forever
# BUGS TO FIX: [BUG] Remove hardcoded chord quality names from Chord class
# BUGS TO FIX: [BUG] If you build a Chord on a Chord degree with specific intervals how does it behave
# BUGS TO FIX: [BUG] Check if sub-setting Chords and rotating/added maintains the parent degree
# BUGS TO FIX: Retrieving numeral relative to parent should go down the chain of all parents

# Potenitial Issues: 
# - Fixed a bug where findInParent does not work when scale has degrees greater than a P8, reason: findInParent simplifies the interval that it is searching for
#	Shouldn't be an issue for chords even though they are a subclass of Scale because a Chord cannot be a Parent

# CHANGE-LOG
# 01/28/2020 - Scale 		 :: [BUG] Fixed Interval arithmetic on Degrees with Keys as Tones
# 01/28/2020 - Scale/Chord 	 :: [BUG] Added check for None value in parameter for Chord/Scale.setParentDegree() / Simplified Code
# 01/28/2020 - Scale 		 :: [BUG] Changed interval arithmetic logic for Scale Objects
# 01/28/2020 - Interval 	 :: Added floor/roof support for negative intervals
# 01/28/2020 - Chord 		 :: [BUG] Removed hardcoded 'no' in Chord.getQuality()
# 01/29/2020 - Scale 		 :: Changed parameter of Scale.getNegativeScale() + others from p_axis_point to p_reflection_point, method now takes an interval
# 01/30/2020 - Configuration :: Added missing Tone Constants from keyboard_tones array in Configuration
# 01/30/2020 - Key			 :: [BUG] Fixed add/sub for Key Class
# 01/30/2020 - Tone			 :: Subtracting a Tone from an identical Tone now returns P8 instead of P1
# 01/30/2020 - Chord		 :: Added p_reflection_point parameter to Chord.getRelativeChord() / Chord.getParallelChord() / Chord.getNegativeChord()
# 02/07/2020 - Scale		 :: [BUG] Changed behavior of Scale.getModes() to fix missing modes
# 02/07/2020 - Key			 :: [BUG] Fixed issue with Key addition/subtraction
# 02/07/2020 - Scale		 :: [BUG] You can now use multiple indices on Scales
# 02/07/2020 - Scale		 :: [BUG] Adding a Specific Interval to a Scale now also transposes the Parent Degree/ParentScale
# 02/15/2020 - Scale		 :: Added support for Degree arithmetic for Scales built on Key objects
# 02/16/2020 - Scale		 :: [BUG] Fixed type() bug in Scale + Degree method
# 03/01/2020 - Scale		 :: [BUG] now you cannot add an Interval to a scale if it already exists in the scale
# 03/01/2020 - Interval		 :: [BUG] Interval.Simplify() now works with negative intervals
# 05/26/2020 - Scale		 :: [BUG] getDegreeByInterval() now uses simplify() to fix issue where parent scale has intervals greater than M7
# 05/26/2020 - Chord		 :: [BUG] getFirstInversion() now sets previous as the new chord before the new chord is arranged by triads, fixes issue where certain inversions are skipped
# 06/01/2020 - Chord		 :: [BUG] Created static methods for inversion logic so it can be used in Chord constructors
# 06/01/2020 - Chord		 :: [BUG] Changed non-static inversion methods so that they now reference static methods to reduce duplicate code
# 06/01/2020 - Chord		 :: [BUG] Added negative inversion functionality so now you can invert chords in the opposite direction
# 06/01/2020 - Chord		 :: [BUG] Fixed issue in Inversion logic where the result is one more than it should be. First inversion is not the same as root position
# 06/01/2020 - Chord		 :: [BUG] Updated getNegativeChord() method in lieu of the changes made to the getInversion() logic
# 06/01/2020 - Chord		 :: [BUG] Added fixed_invert attribute to chord that ensures a chord is inverted by the same amount each time
# 06/01/2020 - Chord		 :: [BUG] getFirstInversion() now works with chords that are not built on thirds
# 06/01/2020 - Chord		 :: [BUG] Changed name of getFirstInversion() to getRootPosition() since they are not the same thing
# 06/01/2020 - Chord		 :: [BUG] Created get..Data() methods for Chord quality logic that returns a struct
# 06/01/2020 - Chord		 :: [BUG] Updated getParentChordQualityData() so that it doesn't get derive the parent chord within this method, and changed the name of the method
# 06/01/2020 - Chord		 :: [BUG] Created a new getParentChordQualityData() method that uses context of the Chord
# 06/07/2020 - Scale		 :: [FTR] Added chromatic and omitted attributes to Scale.Degree object
# 06/07/2020 - Scale		 :: [FTR] Organized constructor of Scale object
# 06/07/2020 - Scale		 :: [FTR] Added new attribute to Scale object called type_dict that uses Pythons Parameter Destruction to specify degree types
# 06/07/2020 - Scale		 :: [FTR] Updated Scale.Degree add/sub logic with integers to only count degrees that are not-chromatic as diatonic 
# 06/07/2020 - Scale		 :: [FTR] Scale.getName() method now only uses non-omitted Intervals
# 06/07/2020 - Scale		 :: [BUG] Third parameter in Scale has been removed, now p_item_1 is used to pass a Scale.Degree
# 06/07/2020 - Scale		 :: [BUG] Updated formatting of Scale.Degree.build() class and got rid of setParentDegree() call
# 06/07/2020 - Chord		 :: [FTR] Chord.configureParentDegree() now has an optional parameter called p_modulate_parent that decides whether the parent should be altered based on the new degree or if they should be chromatic
# 06/07/2020 - Scale		 :: [FTR] You can now choose if an added interval is considered chromatic or omitted
# 06/07/2020 - Chord		 :: [FTR] Chord.configureParentDegree() now assigns chromatic attribute to true for any intervals added to the parent scale
# 06/07/2020 - Scale		 :: [FTR] Changed Scale add/sub logic so that if you index an interval that does not belong to the Scale the interval will be chromatic
# 06/13/2020 - Tone		     :: [BUG] Fixed subtraction issue
# 06/13/2020 - Scale		 :: [BUG] Fixed issue in findInParent(), we now add to the degree instead of using getDegreeByInterval()
# 06/27/2020 - Scale		 :: [BUG] Fixed issue where Degree attributes are not maintained when transposing a Scale

# GOALS AND MILESTONES IN ORDER:
# Need to add logic to Chord Build logic where you can choose whether a new note should be considered Chromatic or Diatonic. IE secondary dominants/chromatic chords.
# The above change should be accompanied by a change in how the Scale add logic works aswell
#	- [Done] Scale Degrees now have a boolean Chromatic and Omitted
#	- [Done] In print logic for Scale degrees with omitted boolean as true should be ignored
#	- Should chromatic intervals be considered diatonic? IE a major scale with a chromatic b3 should be a 3? Or should we only be able to access this via specific intervals?
#		- [Done] If the latter we need to add a getDiatonicDegrees() method to the Scale object
#		- [Done] Changed logic in add and getitem to use this new method if we are adding a generic interval otherwise we will use the normal getDegrees()
#		- [Done] We might need to change the way resolveChord() works in the Chord object
# Add attributes and methods into Chord.Degree object that keep track of non-harmonic, and altered tones
#	- These arent attributes since they can be derived using the parent chord root
# For now DecimalToPitchClass wont try and identify omitted intervals, instead we should add logic to the subset logic of Scales whereby omitted degrees now have the boolean set to true
# Add the ability to get the Quality/Parent Chord of rootless chord voicings. Right now it will print an error

# TASK: Fix inheritence for Chord
# [Done] Create new intervalList object that Scale and Chord Inherit from and fix any bugs
# Remove unneccessary methods in Scale class and fix bugs
# [Done] Instead of using __method__logic() for the business logic of IntervalList and Item we should use method_BL(), the double underscore prefix causes an issue where we cant reference business logic in a subclass from outside the object, it is private
# [Done] Now we can uncomment the overriden methods in Chord
# [Done] Need to figure out a system for overriding __add__() so that it makes added intervals chromatic
# [Done] Need to add override methods for chromatic logic for Scale class
# Updating getitem and add has an issue, when we sub identical tones we get difference of 8

# Code Cleanliness
# Sub should replicate add logic in Key
# Ensure consistant use of temp in variable names
# Create a new assert equals for every outlier bug I fix
# Derived attributes shouldnt be in getters and setters section
# Fix Cammel Case
# If scale and chord dont call business logic why are we using type when creating new objects, one implies inheritence support the other does not
# Ensure parent degree is maintained for all new chords, scales and intervalLists
# Ensure all use of if doesnt use open and close brackets
# Ensure all method groups appear in the same order
# replace self.getParentDegree().getParentScale() with self.getParentScale()
# Ensure all non-wrapper methods in IntervalList are using the business logic methods
# Get rid of unnecessary methods in Scale
# Get rid of unnecessary methods in Chord
# Chord should not be using __add__ in its business logic. If we cant override of add_BL with the new logic we have created we need to go in IntervalList and make sure we can
# [Done] Sub should replicate add logic in Tone
# [Done] In Scale, we shouldnt be referencing Part, but instead Item and use method names with Part as wrappers
# [Done] In Chord, we shouldnt be referencing Part, but instead Item and use method names with Part as wrappers
# [Done] In IntervalList, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] In Scale, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] In Chord, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] getComponents() should be getItems()
# [Done] Ensure consistant use of getitem_BL over [] in Scale 
# [Done] Ensure consistant use of getitem_BL over [] in Chord 
# [Done] Ensure consistant use of getitem_BL over [] in IntervalList 
# [Done] Ensure consistant use of add_BL and sub_BL over +/- in Scale 
# [Done] Ensure consistant use of add_BL and sub_BL over +/- in Chord (If we want to use the overriden add logic in the Chord BL I am now using __add__, in the future if I want to update this add logic I need to go through and replace any references of add_Bl that I might need to) Might need to rethink how we do this, should be referencing either __add__ or add_BL consistantly, we need to be able to change how numeral arithmetic works dynamically, or dont use add when accessing degrees
# [Done] Ensure consistant use of add_BL and sub_BL over +/- in IntervalList 
# [Done] Make sure whenever we check instance of lists we check length first in IntervalList (Check if all references of 0 check len first)
# [Done] Make sure whenever we check instance of lists we check length first in Chord (Check if all references of 0 check len first)
# [Done] Make sure whenever we check instance of lists we check length first in Scale (Check if all references of 0 check len first)

# Optional Features and Bug Fixes that can be delayed
# Interval / Tone :: next and previous logic in interval and tone wont work for items with accidental greater than 2
# Interval / Tone :: ACCIDENTAL_LIMIT should limit the accidentals users can use in Interval and Tone
# Tone :: fix D_flat.getRelatives()
# Tone :: Tone + Semtiones arithmetic doest work for intervals where the next interval has less semitones than the current interval
# Interval :: Intervals with 0 numeral print incorrectly
# Interval :: Fix printing of aug1
# Interval :: Add Interval - Semtiones 
# Interval :: Interval + Semitones arithmetic doesnt work for intervals where the next interval has less semitones than the current interval
# IntervalList :: getAttributes type_dict is incorrect when you add an interval thats below P1 since all intervals above get changed
# IntervalList :: type_dict is incorrect when using transform if we are transforming the first item
# Unalterted Tones and Tone Names should be combined
# IntervalList :: fix Contains logic
# IntervalList :: Need to test new version of transform method for both Chord and IntervalList
# IntervalList :: Issue, if we specify type_dict in getAttributes but we use a modified interval list then the assignments in type dict will not make sense, one solution is to add logic for updating the type dict and generate a new one
# IntervalList :: Check that transform for Chord and Scale work as intended
# IntervalList :: Adding an interval that has same numeral as the tonic of a scale or chord will modulate the tonic, it should be chromatic
# IntervalListUtilities :: binaryToIntervalListUtilitiesSteps Should have the name fixed
# Chord / Scale :: We don't need a reference to the Intervals list aswell as the individual Intervals with the Degree objects in both Chord and Scale
# Chord / Scale :: Remove all instances of setParentDegree()
# Scale :: Scale Degree arithmetic does not retain parentItem if set
# Scale :: Update Scale so all new Scale objects pass the attributes of the current Scale and Scale.Degrees as parameters
# Scale :: Create a method for deriving omitted intervals
# Scale :: Remove wrappers for the Scale class
# Scale	:: Add logic in Scale.Degree shouldn't modulate the parent Scale
# Chord :: Chord slice should use generic intervals
# Chord :: Printing of negative interval are wrong when running through resolve chord
# Chord :: Chord(C4, "dom7b3")[1].move(3) is wrong
# Chord :: When the abs in new_accidental = (abs(p_other.getSemitones()) - (semitones_count - 1)) * sign is removed in Tone __add__ method there is an error in move()
# Chord :: getItem_BL logic is flawed when used in Chord because it calls the build_BL method which is flawed, build_BL needs to build on the parent Scales degree
# Chord :: When we were overridding build_BL methods in chord the indexing logic in IntervalList would call it causing an error, this was fixed but I should revisit this to figure out why the exception occured
# Chord :: GetInversion() only gets the inversion of the current chord not the parentChord()
# Chord :: Fix getFiguredBass()
# Chord :: getSecondaryDominant() in chord should be using the transform() method
# Chord :: Instead of passing a chords getAttributes() results we should be overriding this
# Chord :: Update transform in Chord.Degree
# Chord :: Update Chord so all new Chord objects pass the attributes of the current chord as parameters
# Chord :: root attribute of Chords should be an Interval instead of a TonedObject
# Chord :: Parent Chord should contain omitted intervals that are associated with a degree. The degree should have an omitted boolean
# Chord :: next() and previous() in Chord should not return parent scale degrees
# [Done] Chord(C4, "dom7")[9] is wrong
# [Done] when specifying a fixed invert parameter in chord it must be greater than the last interval otherwise we will use the roof of the last interval
# [Done] when using setParentItem() in IntervalList it should also update the tone
# [Done] getTypeDict() should be generated based on items
# [Done] we dont need an add and sub method, we can merge them into one method for IntervalList
# [Done] get rid of buildIntervalList() method
# [Done] Create get logic for interval, integer and degree in one method
# [Done] Add a method to both the Scale Object and Chord Object that will generate the degree objects. We can override this in the Chord object and change the name of Chord.Degree to Chord.Part
# [Done] Create a new object that contains most of the logic in Scale. Scale will be a subclass of this object and will have only scale specific methods. Chord will also be a subclass of this object
# [Done] Build method in Scale doesnt need to have all these cases, we should be able to simply specify a dictionary of parameters
# [Done] Chord addInterval will cause an error because a chord does not have a type_dict for degrees, for now there is a conditional in the scale, but change this later

# Dependancies
import random
import sys

# Internal Dependancies
from Configuration import *

from AITheoryAnalyser.Analyser import *
from TheoryCollections.IntervalList import *
from TheoryCollections.Scale import *
from TheoryCollections.Chord import *
from TheoryComponents.Interval import *
from TheoryComponents.Tone import *
from TheoryComponents.Key import *
from TheoryComponents.Note import *
from IOMidi.Sequencer import *

def main():

	#Chord(C4, "dom7")[-2]

	P1 + 2
	
	local_dir = "C:\\Users\\adamb\\github\\REL-Studios-Music-Robot\\RELMusicTheory\\IOMidi\\MidiFiles\\"
	'''
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

	C in Scale(C4, major)
	P1.transform(2) + 2
	Scale(C, major).addInterval(dim1)
	sequencer = Sequencer()
	sequencer.fromMidi(local_dir + "untitled.mid")
	Sequencer.toDict(sequencer)
	print(Sequencer.toDict(sequencer)[4][0][1])
	analyser = Analyser(sequencer, 20)
	
	D_flat.getRelatives()
	C - 4
	C + 1
	'''
	# Ways to build a Scale object
	C_Major_Scale = Scale(C, major)
	C_Major_Scale_2 = Scale(C, [P1, M2, M3, P4, P5, M6, M7])
	C_Major_Scale_3 = Scale(C, [2, 2, 1, 2, 2, 2, 1])
	C_Major_Scale_4 = Scale([C, D, E, F, G, A, B])

	Chord(C4, "maj7")[2, 4, 6]
	Chord(C4, "maj9b9")[9].findInParent()
	
	# Ways to build a Chord object with a Parent Scale
	C_M7 = C_Major_Scale[1].build(Chord, "maj7")
	C_M7_2 = C_Major_Scale[1].build(Chord, 4, 3)
	C_M7_3 = C_Major_Scale[1].build(Chord, [P1, M3, P5, M7])
	C_M7_4 = C_Major_Scale[1].build(Chord, [1, 3, 5, 7])
	C_M7_5 = Chord(C_Major_Scale[1] + C_Major_Scale[3] + C_Major_Scale[5] + C_Major_Scale[7])
	C_M7_6 = Chord(C_Major_Scale[1, 3, 5, 7])
	
	# Ways to build a Chord object without a Parent Scale
	C_M7_6 = Chord(C, "maj7")
	C_M7_7 = Chord(C, [P1, M3, P5, M7])
	C_M7_9 = Chord([C, E, G, B])
	
	# Naming Conventions
	C_Major_Scale.getName()
	C_Major_Scale.getCardinality()
	C_Major_Scale.getModeNames()
	C_Major_Scale[1].getName()
	C_Major_Scale[1].getNumeral()
	(C_Major_Scale + 2).getName()
	
	C_M7.getQuality()
	C_M7.getFiguredBass()
	C_M7.getNumeral()
	
	# Arithmetic
	C_Major_Scale + 3																										# Rotates the Scale by a Generic Interval of 3
	C_Major_Scale + m3																										# Transposes the Scale by a Specfic Interval of m3
	C_Major_Scale[1] + 3																									# Returns a Scale-Degree 3 Generic Intervals above the Tonic
	C_Major_Scale[1] + m3																									# Returns a Scale-Degree m3 Specific Intervals above the Tonic
	C_Major_Scale[1] + C_Major_Scale[3]																						# Creates a new Scale containing C and E
	C_Major_Scale[1:2] + C_Major_Scale[4]																					# Adds an F to the Scale <Scale I=C, II=D>
	C_Major_Scale[1:3] + C_Major_Scale[5:6]																					# Adds the Scale <Scale I=G, II=A> to <Scale I=C, II=D, III=E> => <Scale I=C, II=D, III=E, V=G, VI=A>
	
	C_Major_Scale[3] - C_Major_Scale[1]																						# Returns the Specific Interval between Scale-Degrees 3 and 1 => 3
	
	E - C																													# Returns the Specific Interval between the Tones E and C => b6
	C + m3																													# Returns the Tone a m3 above the Tone C => Eb
	P1 + m3																													# Returns the Sum of the Specific Intervals P1 and m3 => b3
	
	# Chord Inversions and Sub-Setting
	C_64 = C_M7[1:3].invert(2)																								# Returns the Second Inversion of a Chord => <Chord I=G, IV=C, vi=E>
	C_64.getInversion()																										# Returns the inversion number of the Chord in question => 2
	C_64.getFiguredBass()																									# Returns the Figure-Bass notation of the Chord in question => I 6/4
	C_53 = C_64.getRootPosition()																							# Returns the First Inversion of the Chord in question => <Chord I=C, iii=E, V=G>
	
	# Resolving Chords and Voice Leading
	F_643 = C_M7.resolveChord()																								# Returns the result of resolving the Chord in question using Voice Leading Rules => <Chord I=C, iii=E, IV=F, vi=A>
	F_643.getInversion()																									# Returns the inversion number of the Chord in question => 2
	G_643 = C_M7.resolveChordInto(C_Major_Scale[5].build(Chord))															# Returns the result of resolving the Chord in question into a specific Chord
	G_643.getInversion()
	
	# Transformations
	A_m7 = C_M7.getRelativeChord()																							# Returns the Relative-Chord of the Chord in question => <Chord i=A, biii=C, V=E, bVII=G>
	C_m7 = C_M7.getParallelChord()																							# Returns the Parallel-Chord of the Chord in question => <Chord i=C, biii=Eb, V=G, bVII=Bb>
	Ab_M7 = C_M7.getNegativeChord()																							# Returns the Negative-Chord of the Chord in question => <Chord I=Ab, iii=C, V=Eb, bvii=G>
	
	# Finding alternative Scales
	#C_M7.getPossibleParentScales()
	
	# Secondary Chords
	D_m7 = C_M7 + 2
	A_7 = D_m7.getSecondaryDominant()
	E_o7 = D_m7.getSecondarySubDominant()
	D_m7.getSecondaryTonic()
	D_m7.getSecondaryAugmentedSix()
	D_m7.getSecondaryTritoneSubstitution()
	
	# Complex Chord Building
	Chord(C, "mM11b5no9")
	Chord(C, "m9b5add6")
	Chord(C, "half-dim9sus4b9")
	'''
	
	C_Minor_Scale = Scale(C, lydian)
	
	C_Diminished_Scale = Scale(C, diminished)
	C_Chromatic_Scale = Scale(C, chromatic)
	A_Minor_Scale = C_Major_Scale + 6
	
	A_Melodic_Minor = Scale(A, melodic_minor_ascending)

	test = Scale(C, diminished_seventh)
	print(test.getIntervals())
	
	Cdim7 = C_Diminished_Scale[1].build(Chord, [1, 3, 4, 6])
	Bm7b5 = C_Major_Scale[7].build(Chord)
	G7 = C_Major_Scale[5].build(Chord)
	CM7 = C_Major_Scale[1].build(Chord)
	FM7 = C_Major_Scale[1].build(Chord, [1, 3, 4, 7])
	

	AmM7 = A_Melodic_Minor[1].build(Chord)

	test_chord = C_Major_Scale[7].build(Chord, [1, 3, 5, 6, 7, 11])

	print(Cdim7.getNegativeChord())

	print(Chord([E, B, F, C, G]).invert(5).getIntervals())



	#print(C_Major_Scale[3].build(Chord, diminished_seventh))

	#print(Cdim7.getNegativeChord())

	# Create a C Major Scale
	CMajorScale = Scale(C, Scale.decimalToPitchClass(major))

	print("Got Here" + CMajorScale[1].build(Chord).getSecondaryAugmentedSix())

	print(Chord(C, [P1, m3, P5, m7])[2])

	print(CMajorScale.printTones())

	print(Scale.scaleIntervalsByOrder([P1, M3, P5, M7, M2, P4, m6]))

	print(CMajorScale[2].buildScale()[2].findInParent().getInterval())

	print(Scale(C, Scale.decimalToPitchClass(diminished_seventh)))

	print("herere" + (CMajorScale[1].build(Chord)[1] + m3).getParentScale())
	
	CChromaticScale = Scale(G, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	
	print(CMajorScale[7] + CChromaticScale[3])

	print("result: " + Chord(C, [P1, M3, P5, M7])[2].build(Chord).getParentScale())

	Dorian = CMajorScale + 2
	print(CMajorScale[7].build(Chord).getSecondaryDominant())
	
	CM7 = CMajorScale[1].build(Chord, [P1, M3, aug5, m7, m9, P11])
	print(CM7.getParentChordQuality())
	
	print(Scale(B, Scale.scaleStepsToPitchClass([2, 2, 1, 2, 2, 2, 1])))

	print(Tone("G", 3).simplify())

	print(Scale(C, [P1, m2, m3, M3, aug4, P5, M6, m7]).getModeNames())
	
	Eb = CMajorScale[1] + m3
	print("The first degree of the C Major Scale + m3 is: " + Eb)

	print("The major scale converted to Decimal is: " + str(Scale.pitchClassToDecimal([P1, M2, M3, P4, P5, M6, M7])))
	
	print("The string dom7sus9no5b5 produces the pitch class " + str(Chord.stringToPitchClass("dom7sus9no5b5")))
	
	result = CMajorScale[1] - 4
	print("The root of the major scale - 4 is " + result)

	print(Chord(C, Chord.stringToPitchClass("min7")).printTones())
	print(CMajorScale[1].build(Chord)[2].buildPitchClass(-1, 2))
	
	# Build a scale off of a scale degree
	DDorianScale = CMajorScale[2].buildScale()
	print("The D Dorian Scale is: " + DDorianScale.printTones())

	# Build a chord off of a scale degree
	G9 = DDorianScale[4].build(Chord)
	print("The G Dominant chord is: " + G9.printTones())

	print("Converting the string #3 to an interval produces: " + Interval.stringToInterval("#3"))

	print("G7 with a flat third is: " + G9[2].transform("b").printTones())

	print("The roman numeral notation of the G9 chord is " + G9.getNumeralWithContext(True, 2))

	# Resolve the chord using a specific rule
	# CM7 = G9.resolveChord(circleOfFifths)
	# print("The result of resolving G9 is: " + CM7)

	# Find the relative chord of a chord
	Em7 = G9.getRelativeChord()
	print("The relative chord of G9 is Em7: " + Em7.printTones())

	# Get secondary dominant of a chord
	D7 = G9.getSecondaryDominant()
	print("The secondary dominant of G9 is D7: " + D7.printTones())
	
	# Transpose a scale up by semitones
	DMajorScale = CMajorScale + M2
	print("The D Major Scale is: " + DMajorScale.printTones())

	# Print the quality of a subset of a chord
	print("The chord resulting from subsetting G9 by 2-5 are: " + G9[2:3].printTones())

	# Properly print quality of a chord with accidentals
	Bhalfdim9 = CMajorScale[7].build(Chord)
	print("The quality of the 7th chord of the C major scale is: " + Bhalfdim9.getParentChordQuality())

	# Properly assign notes to non-major heptatonic scales
	AMelodicMinor = Scale(A, Scale.decimalToPitchClass(melodic_minor_ascending))
	print("The A Melodic Minor Scale is: " + AMelodicMinor.printTones())

	# Build a chord on a non-major heptatonic scale
	AM11b3 = AMelodicMinor[1].build(Chord)
	print("The first chord of the melodic minor scale is: " + AM11b3.printTones())

	# Properly print the quality of non-major diatonic chord
	print("The quality of this chord is: " + AM11b3.getParentChordQuality())

	# Print Roman Numerals with the Correct quality
	print("The jazz numeral notation of the 6th chord of A minor, with 7 notes is: " + Scale(A, Scale.decimalToPitchClass(minor))[6].build(Chord, 7).getNumeral(True, 2))

	print(CMajorScale[1].build(Chord, Chord.stringToPitchClass("half-dimmaj7")).getParentDegree().getParentScale().printTones())

	# Get properties of scale
	print("The number of imperfections in the C Major Scale is: " + str(CMajorScale.getImperfections()))
	print("The reflection axes of the C Major scale are: " + str(CMajorScale.getReflectionAxes()))

	# Build non-heptatonic scales
	CChromaticScale = Scale(C, [P1, m2, M2, m3, M3, P4, aug4, P5, m6, M6, m7, M7])
	print("The Chromatic Scale is: " + CChromaticScale.printTones())

	# build a chord on the chromatic scale
	chord = CChromaticScale[1].build(Chord, 5)
	print("the quality of the first chord in the C chromatic scale is: " + chord.getParentChordQuality() + chord)

	print(Chord.stringToPitchClass("half-dimmaj7"))

	# Build chord on non-heptatonic scales
	CDimScale = Scale(C, [P1, M2, m3, P4, dim5, m6, m7.transform("b"), M7])
	print("The first chord of the C Diminished Scale is: " + CDimScale[1].build(Chord).printTones())

	# build a chord on the c dim scale
	chord = CDimScale[1].build(Chord, 5)
	print("the quality of the first chord in the C Dim scale is: " + chord.getParentChordQuality() + chord)

	# Check if chord exists in a scale
	if G9 in CMajorScale:
		print("Check if G9 in C Major Scale: True")

	# Check if scale exists in a scale
	if DDorianScale in CMajorScale:
		print("Check if D Dorian Scale in C Major Scale: True")

	# Check if intervals exist in a scale
	if [P1, M3, P5] in CMajorScale:
		print("Check if [P1, M3, P5] in C Major Scale: True")
'''

if __name__ == "__main__":
	main()