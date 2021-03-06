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
# 07/16/2020 - IntervalList	 :: [FTR] Updated build so it now uses indexing to build sub-lists and degree arithmetic, now supports lists that mix generic and specific intervals
# 07/16/2020 - IntervalList	 :: [BUG] Item arithmetic now retains parent item
# 07/16/2020 - IntervalList	 :: [BUG] Transform and addInterval method now retains attributes for items
# 07/16/2020 - IntervalList	 :: [FTR] Updated Typcasting for IntervalList objects
# 07/16/2020 - Interval		 :: [FTR] Adding Interval + Semtiones logic
# 07/16/2020 - Interval		 :: [FTR] Added getParentIntervalList() method that references an item it belongs to, useful for interval arithmetic, also added intervalToTypeDict() in IntervalListUtilities() that utilises this
 
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
# Add IntervalList Item in degree uses remove to remove first item in list but in intervallist we do this manually
# all use of in should be replaced with contains_BL in IntervalList, Scale and Chord
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

# Optional Features and Bug Fixes that can be delayed

# Functionality Issues:
	# - [Functionality Issue] When we decide whether a Chord Part is enharmonic we need to check whether its altered in the quality not the parent
	# - [Functionality Issue] Unaltered Intervals in Chord might not need to be based of the quality, just the parent, however in this case it might be confusing when we try to determine whether a Part is altered in the sense that it is Chromatic or not in the parent and whether we want to know whether its altered in the Chord
	# - [Functionality Issue] Should Rotate input numbers be treated as generic intervals? Right now they are treated as whatever the user specified for the parameters but what if we want the input number to be treated like a generic interval but not ignore the altered intervals when building?
	# - [Functionality Issue] Shouldnt the get negative in Chord and related methods just use the same logic as the getNegativeScale() method in Scale?
	# - [Functionality Issue] When we are building a Chord object off of a Scale Degree we need to check if the parent scales unaltered intervals match the child Chords unaltered intervals (Assuming they specified a quality like major) but we should only check if the unaltered intervals in the chord which are included in the chord, for example if we build a major chord off of the fourth scale degree of C major, even the the corresponding scale has a raised fourth in the parent, since we are only build a 7th chord all the unaltered intervals match and we dont need to create a new parant, however we need to decide how to handle cases where a user references the fourth of the chord and wants to check if its altered or unaltered, in this case what do we say?
	# - [Functionality Issue] For the algorithm that tries to assign scales to a list of notes we must simplify all the notes
	# - [Functionality Issue] For the algorithm that tries to assign scales to a list of notes if the subset of notes doesnt have 7 distinct notes then we should see whether its closest to the previous or next scale and assign it based off that
	# - [Functionality Issue] Issue with adding an interval greater than a Childs roof and how it affects the parent IntervalList, does my fix work?
	# - [Functionality Issue] Right now build doesnt pass through whether something is a subset or not, need to fix this
	# - [Functionality Issue] Right now in getParallelScale() it will get rid of temp items when we add a generic interval or index it / Need to fix issue where indexing via generic interval erases other temporary items, also right now if we do not ignore the parent in next or previous then it wont erase temp items, need to make this consistant
	# - [Functionality Issue] Right now slicing an intervallist object doesnt really use those special parameters, IE ignore parent and ignore altered, only for the reference point
	# - [Functionality Issue] Right now if an IntervalList is a sublist, if an item is chromatic in the parent it wont be in the child, should this be the case? / If sublist we just grab the type dict of the parent, need to update logic for determining if un altered

# Bugs:
	# - [BUG] Right now invert in chord does not retain the unaltered intervals
	# - [BUG] Just realised that when getting parallel intervallist the unaltered intervals does not change, so we need to find a way to grab the current unaltered intervals when building a new intervallist
	# - [BUG] Right now we dont print whether a numeral is lowercase or not correctly because we use a cap of 2 which will only include one interval
	# - [BUG] Get parrallel is broken, last thing I changed is how we add to the parent item when we add an interval to an intervallist and I updated the unaltered intervals logic in Scale
	# - [BUG] Right now the key assignment algorithm references -1 and -2, this might cause errors
	# - [BUG] If the Unaltered Intervals of a Chord and its Parent Scale are different than we need to build a Scale off of the Parent Degree that contains the required unaltered Intervals
	# - [BUG] Right now transpose in the item object calls getItems() instead shouldnt we use getitems_BL?
	# - [BUG] Need to fix rotate in Scale, this references transpose right now
	# - [BUG] Also the configure parent item method assumes that the parent is not greater than a P8 but this is not always the case
	# - [BUG] When you add an interval to an intervalist we should check if a compound or simplified version of the same exists and is un-altered and in this case we should also make the new interval un-altered
	# - [BUG] How does an IntervalList behave relative to its P8 limit when we have a dim8, since we only transpose the parent intervallist when we add something greater than a P8, a dim8 is less than a P8 so it will not transpose the intervallist

# New Features:
	# - [Feature] Instead of having a Parent Voice with a Position we should have a list of Input Parts and Output Parts that a Part ties to and we can call a getParentVoices() method that will return a list of possible Voice objects
	# - [Feature] Need to add ability to put the quality into the find root method as a parameter to get more the more likely root position in case a user specified a quality but not a root
	# - [Feature] We should also add the ability for a Chord Part to have multiple parant voice for the rare case where voices overlap
	# - [Feature] When dealing with the logic behind Suspension and Retardando, the fact that our Chord parts have both Horizontal and Vertical context in the form of a Parent Chord and a Parent Voice allows us to check if the immediate predecessor to a Part is actually harmonic, this can help us to decide whether a Chord Part is a Suspension, Retardando or whether its neither. I also think it is important to point out that there is a distinction between the suspension in Chord Quality music notation and the one mentioned here since Chord qualities dont have any Horizontal context
	# - [Feature] We dont need to add a harmonic_intervals list, since right now we assume all intervals with a numeral greater than a M7 or are chromatic are non harmonic
	# - [Feature] Because of the below concept we must also add a harmonic intervals that behaves similarly to the unaltered intervals, unlike a chromatic interval however an Appoggiatura can resolve into an interval with a different numeral if an Appoggiatura is above a missing harmonic interval it is a suspension however if it is below one it is a retardando, it could be both, there are some other conditions however that should also be considered, like whether the previous voice note is tied (optional) to it and it is harmonic in that previous chord
	# - [Feature] Some theory I learned today, the distinction between a Chromatic note and an Appoggiatura is that a Chromatic note resolves into an item with the same numeral, however Appoggiaturas can resolve by step into a different numeral IE 4 into a 3, this is similar to a suspension or a retardation except in a suspension the note is usually borrowed from a previous chord 

# Code Cleanliness:
	# - [Code Cleanliness] Chord Constructor references Scale.Item and Scale.Degree
	# - [Code Cleanliness] In Chord Constructor we should be using the tonesToPitchClass() method
	# - [Code Cleanliness] Start point for Key Object in Config should be its own Constant
	# - [Code Cleanliness] Worth pointing out that it doesnt make sense to call super next in scale and then omit of chromatic assuming we arent ignoring the parent
	# - [Code Cleanliness] Maybe we should rename getAccidentalAsSemitones() to getAlteration()
	# - [Code Cleanliness] Change references to p_args into *p_args
	# - [Code Cleanliness] Logic in replaceAtNumeralWith_BL is outdated, we dont seem to be using this method in IntervalList
	# - [Code Cleanliness] Right now when we generate the possible prefixes in string to pitch class we double these, why?

# Completed Tasks/Issues:

# Error happens when we use new_generic_intervals = [i + 1 for i in range(0, (Interval(1, p_item_2 - 1) * p_item_1).getNumeral() + 2, p_item_2 - 1)] in buildPitchClass
# Resolve Chord is wrong right now
# We should be using a change intervals method that does all the type dict method instead of doing this everytime we change intervals
# Chord doesnt have correct integer addition right now, we need to put the parent integer addition into intervallist
# After implementing BL for each object we should get rid of references to super
# All methods that override business logic methods should be there own BL methods with the class name as a prefix, they will then use wrapper methods that call these
# sortIntervals() wont work if you input something like [aug2.transform(2), M3], aug2 should still be first but M3 is first in our result
# Verify if build on thirds still works as it should since I changed the code
# In Chord Constructor self.parent_item.add_BL() might not be compatible with the return result of get inversion
# len(self.getIntervals()) does not work when using build if some intervals in the parent are Chromatic
# Just like how parent scales have chromatic notes to reference notes in subscales, we should have omitted notes in subscales that refer to notes in the parent
# Right now we are passing ignore parent interval list as a param for any method that uses add, i think it would be easier if this sublist using parant lists generic intervals functionality should only be applied to scale and chord exluding intervallist just so we can use super if we dont want to interact with parant
# getPosition() should add 1
# Make sure getitem and add logic is sound and up to date for IntervalList objects, aswell as add logic and addInterval/Transform
# Make sure decimal works for build in IntervalList
# Make sure Add logic and all intervalList.item objects is up to date and the logic is sound, aswell as next(), ignore parent needs to be applied
# Need to fix build method so it just puts all the parameters specified into the new object instead of creating a sublist
# Right now build method first parameter is the max numeral not, the amount of numerals ie 4, 3 = [1, 3] instead of [1, 3, 5, 7]
# By default maybe Scale should always use the same method for converting semitones to Intervals instead of varying depending on the accidental limit
# Interval / Tone :: next and previous logic in interval and tone wont work for items with accidental greater than 2
# Interval / Tone :: ACCIDENTAL_LIMIT should limit the accidentals users can use in Interval and Tone
# Tone :: Tone + Semtiones arithmetic doest work for intervals where the next interval has less semitones than the current interval
# Interval :: Intervals with 0 numeral print incorrectly
# Interval :: Fix printing of aug1
# Interval :: Add Interval - Semtiones 
# Interval :: Interval + Semitones arithmetic doesnt work for intervals where the next interval has less semitones than the current interval
# IntervalList :: What happens if you sub a IntervalList.Item by another IntervalList.Item that is higher than itself, also should we retain the subbed items attributes? What differentiates this from add? 
# IntervalList :: getAttributes type_dict is incorrect when you add an interval thats below P1 since all intervals above get changed
# IntervalList :: type_dict is incorrect when using transform if we are transforming the first item
# Unalterted Tones and Tone Names should be combined
# IntervalList :: In the console if we add an interval to the parent degree it returns none within add interval method
# IntervalList :: fix Contains logic
# IntervalList :: Need to test new version of transform method for both Chord and IntervalList
# IntervalList :: Issue, if we specify type_dict in getAttributes but we use a modified interval list then the assignments in type dict will not make sense, one solution is to add logic for updating the type dict and generate a new one
# IntervalList :: Check that transform for Chord and Scale work as intended
# IntervalList :: Adding an interval that has same numeral as the tonic of a scale or chord will modulate the tonic, it should be chromatic
# Chord / Scale :: We don't need a reference to the Intervals list aswell as the individual Intervals with the Degree objects in both Chord and Scale
# Chord / Scale :: Remove all instances of setParentDegree()
# Scale :: Scale Degree arithmetic does not retain parentItem if set
# Scale :: Update Scale so all new Scale objects pass the attributes of the current Scale and Scale.Degrees as parameters
# Scale :: Create a method for deriving omitted intervals
# Scale :: Remove wrappers for the Scale class
# Scale	:: Add logic in Scale.Degree shouldn't modulate the parent Scale
# Chord :: Chord slice should use generic intervals
# Chord :: Printing of negative interval are wrong when running through resolve chord
# Chord :: Chord(C4, "dom7b3")[1].move(3) is wrong, there is an error in one of the unaltered intervals methods
# Chord :: When the abs in new_accidental = (abs(p_other.getSemitones()) - (semitones_count - 1)) * sign is removed in Tone __add__ method there is an error in move()
# Chord :: getItem_BL logic is flawed when used in Chord because it calls the build_BL method which is flawed, build_BL needs to build on the parent Scales degree
# Chord :: When we were overridding build_BL methods in chord the indexing logic in IntervalList would call it causing an error, this was fixed but I should revisit this to figure out why the exception occured
# Chord :: GetInversion() only gets the inversion of the current chord not the parentChord()
# Chord :: Fix getFiguredBass()
# Chord :: getSecondaryDominant() in chord should be using the transform() method
# Chord :: Instead of passing a chords getAttributes() results we should be overriding this
# Chord :: Update Chord so all new Chord objects pass the attributes of the current chord as parameters
# Chord :: root attribute of Chords should be an Interval instead of a TonedObject
# Chord :: Parent Chord should contain omitted intervals that are associated with a degree. The degree should have an omitted boolean

# [Revised] Every interval list has a parent which is the interval list based off the unaltered intervals
# [Done] Tone :: fix D_flat.getRelatives()
# [Done] IntervalListUtilities :: binaryToIntervalListUtilitiesSteps Should have the name fixed
# [Done] Scale(C, major)[1].build(Chord, 7, 3)[3].move(-3) is wrong
# [Done] We need to replace all instances of P8 in the IntervalList object aswell as the subclasses, and methods in IntervalListUtilities with a reference to fixed invert, also in build we must pass this parameter into the child object if the childs roof decreases, however if the childs roof increases, say if we build a Chord off a Scale, then the object will have a new fixed invert, in IntervalListUtilities we will also need to add parameters for fixed invert in methods like scaleIntervalsByOrder
# [Done] Update Chord Build_BL method
# [Done] Scale(C, major)[2].build(Scale, [P1,M2,M3,P4,P5,M6,M7])[3] is wrong
# [Done] Scale(C, major)[1,2,3,5,6].rotate()[3] is wrong
# [Done] Right now when we do Scale(C, major)[5].build(Chord, "dom7addb3") we get an incorrect result, this is because it thinks b3 is an alteration, we need to somehow ignore alterations that are prefixed by add or sus, might be able to do this with a negative look-behind but we cant use negative look-behinds with wildcards, could do a positive look-ahead (\d+[#b]*(?![#b]*(dda|sus))) but this only grabs one correct item at a time. The closest RegEx I could create is (\d+[b#]*(?!((?<![b#])\d*)|([b#]*)(dda|sus))). To use this we must invert the input string and also the add/sus strings
# [Done] need to create two getIntervals(), one that always returns the intervals of the current intervallist and another that has the logic of the new getIntervals method
# [Done] Remove references to chromatic in Scale
# [Done] Instead of each item having an attribute altered, we should be consistant and have a list of un-altered intervals in the parent interval list, also the unaltered intervals list in the config should be renamed to unaltered semitones
# [Done] For some reason I think we had a Parent that was greater than a P8, this should not be possible right now, need to add a check in the constructor and find out why this occurs
# [Done] This caused an error reference_point = reference_point.add_BL(counter, p_ignore_parent, p_cascade_args, p_ignore_altered, *p_args)
# [Done] Need to add configureTypeDict() method that makes sure that multiple intervals with the same numeral arent unaltered unless they are the same simplified, need to add a check for this in getUnalteredIntervalsTypeDict() to right now it will only make one of them unaltered
# [Done] We should then create a transpose method, we should also be able to transpose individual items. The behavior in this case is similar to the next logic in Interval currently. Next should always resolve into the closest un-altered object, while transpose should retain the accidental
# [Done] It is also important that we make a distinction between altered/temp intervals, instead of assuming that all altered intervals are temp. Intervals are only temp when we perfom interval addition on an intervallist and retreive an item with an interval not in the parent intervallist, this could be an omitted interval (IE doesn't share it's numeral with any other items in the intervallist) or a altered interval (Which does)
# [Done] Just like how Intervals have reference to un-altered intervals when deciding whether intervals are flat or not, intervallists should also identify which items are un-altered or altered. The difference here however is that with intervals this is constant and is typically the major diatonic scale and with intervallists this varies intervallist to intervallist. If somebody creates an intervallist object with intervals that share a numeral, and they have not specified whether it is altered or not we can create an algorithm that asigns un-altered status to the interval with the least accidentals with respect to the interval item. However its important to note that just because an interval is altered doesnt mean the item itself is altered, take for example the minor scale, this scale has a m3 interval but in this case it is diatonic, and playing a M3 is chromatic/altered.
# [Done] New Chromatic logic, only items that have a numeral that already exist in the intervallist will be considered Chromatic, otherwise they will be omitted since every scale object is a subset of the major scale. For chords chromatic items are instead called appogaturas 
# [Done] Instead of omitting items from next by checking if chromatic there should be a boolean called temp. Omitted and Chromatic items are by default temporary, also this temp attribute should be in intervallist instead of one of the subclasses, this allows us to remove the overriden next method in scale.
# [Done] Need to fix how we generate the size of a new interval list when we build on an item
# [Done] Need to create a transpose method, this is called when you add to an interval list object. Unlike build, instead of rotating the interval list, chromatic items move with each rotation
# [Done] Need to add a parameter to build called preserve parant that dictates whether building on an item should make that item the parent of the new object
# [Done] Get Parallel has a problem where it needs to get an item using generic intervals that reference the parent interval list but it needs to build an interval list ingoring the parent and including the chromatic items, this is a case where we need to do seperate calls to add and build instead of just adding to the interval list object
# [Done] If the ignore parent is false in the next and previous logic we shouldnt be checking if the result is chromatic or not, and just return the result
# [Done] Need to add logic in item where an item that has an interval which includes a numeral that exists in the interval list object is considered chromatic and can reference the interval that it alters, you can also derive by how much its altered. In addition to this, when we reference an interval that does not occur in the parent interval list and the numeral does not either it is considered omitted? (Should this be the case)
# [Done] [Code Cleanliness] Sub should replicate add logic in Tone
# [Done] [Code Cleanliness] In Scale, we shouldnt be referencing Part, but instead Item and use method names with Part as wrappers
# [Done] [Code Cleanliness] In Chord, we shouldnt be referencing Part, but instead Item and use method names with Part as wrappers
# [Done] [Code Cleanliness] In IntervalList, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] [Code Cleanliness] In Scale, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] [Code Cleanliness] In Chord, getitem_BL/__getitem__(1) should be replaced with getItems()[0]
# [Done] [Code Cleanliness] getComponents() should be getItems()
# [Done] [Code Cleanliness] Ensure consistant use of getitem_BL over [] in Scale 
# [Done] [Code Cleanliness] Ensure consistant use of getitem_BL over [] in Chord 
# [Done] [Code Cleanliness] Ensure consistant use of getitem_BL over [] in IntervalList 
# [Done] [Code Cleanliness] Ensure consistant use of add_BL and sub_BL over +/- in Scale 
# [Done] [Code Cleanliness] Ensure consistant use of add_BL and sub_BL over +/- in Chord (If we want to use the overriden add logic in the Chord BL I am now using __add__, in the future if I want to update this add logic I need to go through and replace any references of add_Bl that I might need to) Might need to rethink how we do this, should be referencing either __add__ or add_BL consistantly, we need to be able to change how numeral arithmetic works dynamically, or dont use add when accessing degrees
# [Done] [Code Cleanliness] Ensure consistant use of add_BL and sub_BL over +/- in IntervalList 
# [Done] [Code Cleanliness] Make sure whenever we check instance of lists we check length first in IntervalList (Check if all references of 0 check len first)
# [Done] [Code Cleanliness] Make sure whenever we check instance of lists we check length first in Chord (Check if all references of 0 check len first)
# [Done] [Code Cleanliness] Make sure whenever we check instance of lists we check length first in Scale (Check if all references of 0 check len first)
# [Done] Right now its printing that we cant find the generic interval when it should be finding it
# [Done] need to create a getGenericIntervals() method for sublists, this is used when transposing diatonically in the intervallist add method
# [Done] Chord next and previous does not work correctly, we shouldnt be overriding add logic methods we should be overriding next, the one in intervallist should have a parameter that allows us to decide whether we do or do not ignore the parent, in the scale class we can override this to also include a param that decides whether we do or do not ignore chromatic notes
# [Done] Fix generic interval addition in build, we need to add a getGenericInterval() method
# [Done] Scale(C, major)[1,m3,4,aug4,5,m7] is wrong
# [Done] Remove if isinstance(p_item_1, Tone): p_item_1 = Key(p_item_1, 4)
# [Done] Secondary Scales should behave similarly to Chords built of scale degrees, IE they should call configure parent degree and generic intervals should refer to the parent
# [Done] What happens when you submit a list of tones into an IntervalList object? Since we set a tone to be a key with octave 4
# [Done] For some reason getQuality of Dominant Chords returns Mm7, Fix: In this case Mm7 has same evaluation as dom7, now if the qualities of the bass and extensions arent the same then we add an eval
# [Done] Still need to fix degree attribute logic getting lost when calling getParallelChord() and related methods
# [Done] Chord :: Update transform in Chord.Degree
# [Done] Chord :: next() and previous() in Chord should not return parent scale degrees
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
	Scale(C, major)[1].build(Chord, 5, 3)
	#print(Chord(C4, "dom7b3")[1].move(3))
	Scale(C, major)[1].build(Chord, 7, 3)[3].move(-3)
	Scale(C, major)[1,2,3,5,6].rotate()
	Scale(C, major)[1,2,3,5,6].getRelativeScale()
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
	Scale(C, major).getParallelScale()
	print(Scale(C, major)[1,2,m3,5,6][m3].buildPitchClass_BL(2, 3))
	Scale(C, major)[1,2,m3,5,6].getParallelScale()
	Scale(C, major)[1,2,m3,5,6].getParallelScale()[2]
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
	'''
	(Scale(C, major)[1].build(Chord, 7, 3)[2] + 2).getParentChord()
	C_Major_Scale = Scale(C, major)
	C_Major_Scale_2 = Scale(C, [P1, M2, M3, P4, P5, M6, M7])
	C_Major_Scale_3 = Scale(C, [2, 2, 1, 2, 2, 2, 1])
	C_Major_Scale_4 = Scale([C, D, E, F, G, A, B])
	
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
	
	# Transformations7
	Ab_M7 = C_M7.getNegativeChord()																							# Returns the Negative-Chord of the Chord in question => <Chord I=Ab, iii=C, V=Eb, bvii=G>
	C_m7 = C_M7.getParallelChord()																							# Returns the Parallel-Chord of the Chord in question => <Chord i=C, biii=Eb, V=G, bVII=Bb>
	A_m7 = C_M7.getRelativeChord()																							# Returns the Relative-Chord of the Chord in question => <Chord i=A, biii=C, V=E, bVII=G>
																								
	# Finding alternative Scales
	#C_M7.getPossibleParentScales()
	
	# Secondary Chords
	D_m7 = C_M7 + 2
	A_7 = D_m7.getSecondaryDominant()
	E_o7 = D_m7.getSecondarySubDominant()
	D_m5 = D_m7.getSecondaryTonic()
	E_dom7_b5 = D_m7.getSecondaryAugmentedSix()
	A_dom7_b5 = D_m7.getSecondaryTritoneSubstitution()
	
	# Complex Chord Building
	Chord(C, "mM11b5no9")
	Chord(C, "m9b5add6")
	Chord(C, "half-dim9sus4b9")

if __name__ == "__main__":
	main()