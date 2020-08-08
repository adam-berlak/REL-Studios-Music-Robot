# RELMusicTheory 
**A Music Theory Library for Python Programmers**

## 1. Project Goal:

The goal of this project is to create an artificial intelligence with a knowledge of Music Theory that can analyse music and potential produce new music

## 2. Components Required:

#### 2.1 Taxonomy
Establish a taxonomy by creating a cohesive music theory library. This will be the part of the AI that deals with knowledge representation in the form of newly created data structures. More specifically, Scales, Chords, Motifs, Structure and so on.
#### 2.2 Midi to Knowledge Representation Conversion
Find a library that can read a midi file intelligently. IE: Distinguish between left and right hand, beats, measures and note lengths. 
Create an algorithm that parses a midi file and converts it into a more logical representation. IE: The algorithm should be able to read a measure and say "the left hand plays this pattern four times and has the chord progression I-IV-V"
#### 2.3 Machine Learning
Use Machine learning to produce new music. The algorithm will take a collection of midi files as a data set and convert it into a knowledge representation it can understand, in this case Music Theory. Each midi file corresponds to a Song Object that contains
all the information of the piece the AI can understand. The Neural Network will try and build the Songs structure from scratch until the error is small enough when comparing it to the actual song. We will then run the algorithm ona large set of music until it builds a strong enough network of possible ways to construct a piece. 

<br>

## 0. Table of Contents
- [**1 - About this project**](#about)<br>
- [**2 - Usage**](#usage)<br>
- [**2.0 - Intervals**](#intervals)<br>
  - [**2.0.0 - Initialization**](#interval-initialization)<br>
  - [**2.0.1 - Representation**](#interval-representation)<br>
  - [**2.0.2 - Arithmetic**](#interval-arithmetic)<br>
  - [**2.0.3 - Transformation**](#interval-transformation)<br>
- [**2.1 - Tones**](#tones)<br>
  - [**2.1.0 - Initialization**](#tone-initialization)<br>
  - [**2.1.1 - Arithmetic**](#tone-arithmetic)<br>
- [**2.2 - Scales**](#scales)<br>
  - [**2.2.0 - Initialization**](#scale-initialization)<br>
  - [**2.2.1 - Representation**](#scale-representation)<br>
  - [**2.2.2 - Arithmetic**](#scale-arithmetic)<br>
  - [**2.2.3 - Transformation**](#scale-transformation)<br>
  - [**2.2.4 - Building Chords/Scales**](#scale-building)<br>
  - [**2.2.5 - Scale Properties**](#scale-propterties)<br>
- [**2.3 - Chords**](#chords)<br>
  - [**2.3.0 - Initialization**](#chord-initialization)<br>
  - [**2.3.1 - Representation**](#chord-representation)<br>
  - [**2.3.2 - Arithmetic**](#chord-arithmetic)<br>
  - [**2.3.3 - Transformation**](#chord-transformation)<br>
  - [**2.3.4 - Secondary Chords**](#chord-secondary)<br>
  - [**2.3.5 - Inversions**](#chord-inversions)<br>
  - [**2.3.6 - Polymorphism**](#chord-polymorphism)<br>
- [**2.4 - Configuration**](#configuration)<br>
- [**3 - Goals**](#goals)<br>

<a name="about"/>

## 1. About this project:

Looking through existing libraries for music theory, I noticed a recurring problem. Most of the existing music theory libraries
rely heavily on hardcoding of information. Things like Chord qualitys and properties of scales are often hardcoded in dictionaries
when they should be derived using logical formulas within a Scale object. As a result, these libraries are not very extensible, they limit your inputs and likely fall apart when you try to get more creative with your scales. As a goal for myself I attempted to limit all hardcoding to names, and reduce everything else that can be derived logically to methods. The result; less reliance on definitions, less constants, and greater extensibility.

<a name="usage"/>

## 2. Usage:

- Build Scales by/using: 
  - Specific Intervals: C_Major_Scale = Scale(C, [P1,M2,M3,P4,P5,M6,M7])
  - Generic Intervals: C_Pentatonic_Scale = C_Major_Scale[1,2,3,5,6]
  - Semitones: C_Major_Scale = Scale(C, [2,2,1,2,2,2,1])
  - Notes: C_Major_Scale = Scale([C,D,E,F,G,A,B])
  - Name: <!--- (C_Major_Scale = Scale(C, major))

<a name="intervals"/>

### 2.0. Intervals

<a name="interval-initialization"/>

#### 2.0.0. Initialization

Intervals require a numeral, and semitones. The Interval object can determine if the interval should be printed with an accidental automatically depending on what the user defined as the "unaltered intervals". In our case it is the Intervals of the Major Scale. Since an Interval with the numeral '5' and semitones '7' does not exist in the 'unaltered intervals' list, it is treated as an altered interval. You can change however which Intervals are considered altered.
```
>>> Interval(7, 5)
b5
```

<a name="interval-representation"/>

#### 2.0.1. Representation

You can convert a string into an Interval object using the static stringToInterval() method within the Interval object.
```
>>> m3 = Interval.stringToInterval("b3")
>>> m3.getSemitones()
3
>>> m3.getNumeral()
3
```

<a name="interval-arithmetic"/>

#### 2.0.2. Arithmetic

You can perform Interval arithmetic
```
>>> P5 + M3
7
>>> P5 - m2
#4
```

While the size of Intervals you can create is unlimited, the constants are limited to a P15. To use intervals beyond this you can just use arithmetic.
```
>>> M16 = P15 + M2
```

An important method I created is called simplify(). This method takes any Interval larger than a M7 and creates a simple Interval as opposed to a compound Interval.
```
>>> M10.simplify()
2
```

<a name="interval-transformation"/>

#### 2.0.3. Transformation

You can transform an Interval with accidentals.
```
>>> P5.transform("#")
#5
```

<a name="tones"/>

### 2.1. Tones

<a name="tone-initialization"/>

#### 2.1.0. Initialization

The Tone object is purely an abstraction and cannot be played, this functionality will be added to my Key object within the Keyboard class. The tones object allows you to deal with representation of Tones more accurately. 

You can create a Tone by simply establishing a Tone name.
```
>>> Tone("C")
"C"
```

You can apply accidentals in the second parameter by inputing a positive or negative integer. Positive = Sharp and Negative = Flat.
```
>>> Tone("C", 1)
"C#"
```

You can simplify an Tone in case you want compare Tones.
```
>>> Tone("G", 2)
"G##"
>>> Tone("G", 2).simplify()
"A"
```
<a name="tone-arithmetic"/>

#### 2.1.1. Arithmetic

You can also do arithmetic with Tones and Intervals
```
>>> Tone("C") + m3
"Eb"
```

You can find the distance between Tones using subtraction.
```
>>> Tone("E", -1) - Tone("C")
3b
```

<a name="scales"/>

### 2.2. Scales

<a name="scale-initialization"/>

#### 2.2.0. Initialization

Some ways to build a Scale object include
```
>>> C_Major_Scale = Scale(C, major)                                       # Decimal Number
>>> C_Major_Scale = Scale(C, [P1, M2, M3, P4, P5, M6, M7])                # Diatonic Intervals
>>> C_Major_Scale = Scale(C, [2, 2, 1, 2, 2, 2, 1])                       # Scale-Steps
>>> C_Major_Scale = Scale([C, D, E, F, G, A, B])                          # List of Tones
"<Scale I=C, ii=D, iii=E, IV=F, V=G, vi=A, VII=B>"
```

You can access any of the Scale-Degrees by using Intervals as indices. You can use both Diatonic and Generic Intervals.
```
>>> C_Major_Scale[1]
"C"
>>> C_Major_Scale[m3]
"Eb"
```

There are some other uses for indices.
```
>>> C_Major_Scale[1:5]
"<Scale I=C, ii=D, iii=E, IV=F, V=G>"
>>> C_Major_Scale[1, 3, 5, 7]
"<Scale I=C, iii=E, V=G, VII=B"
```

<a name="scale-representation"/>

#### 2.2.1. Representation

You can also print the name of a Scale. Since Scale names cannot be derived logically in contrast to Chord names, the names of all Scales are kept in ScalesDictionary.py. My algorithm converts the scale to its decimal representation then accesses the dictionary and retrieves the name associated with that number. 
```
>>> C_Major_Scale.getName()
Ionian/Major
>>> (C_Major_Scale + 2).getName()
Dorian
```

I also created a Static method called decimalToPitchClass() that converts a decimal number into a pitch-class-set. All pitch-class-sets have an associated decimal representation. As an example; Major = 2741. This is very useful for creating scales by name! You can create every scale that is named in the dictionary. 
```
>>> C_Major_Scale = Scale(C, Scale.decimalToPitchClass(major))
[C, D, E, F, G, A, B]
```

<a name="scale-arithmetic"/>

#### 2.2.2. Arithmetic

If you add an integer to a Scale-Degree it is treated as a Generic Interval while adding an Interval is treated like adding a Specific Interval.
```
>>> C_Major_Scale[1] + 4
F
>>> C_Major_Scale[1] + m3
Eb
```

I think its worth emphasizing that adding a Interval to a Degree, which produces a Degree that is not contained in the Principle-Scale will create a new Parent-Scale for the resulting Degree. EG: The second Degree of the C Major Scale is D, and the result of adding a M3 Interval to it is F#
```
>>> new_degree = C_Major_Scale[2] + M3 
>>> new_degree.getParentScale()
[C, D, E, F#, G, A, B]
```

You can also transpose a Scale up by adding integers or intervals to it. My library assigns pitchs and accidentals to the scales automatically without any hardcoding. The proccess is identical to how its done by theorists ensuring minimal accidentals are used. As an example: Db Major notation will be used over C# Major despite the latter also being valid. This is because Db Major has less accidentals. Despite this you can still create a C# Major Scale. An integer is treated as a Generic Interval, meaning the value represents scale steps as opposed to semitones. To transpose a scale by semitones you must add an interval to it. Adding an Integer to a scale will rotate the scale. IE: Adding a Generic Interval of 2 to the C Major Scale will produce the Dorian mode.
```
>>> D_Major_Scale = C_Major_Scale + 2
[D, E, F, G, A, B, C]
>>> D_Major_Scale = C_Major_Scale + M2
[D, E, F#, G, A, B, C#]
>>> Db_Major_Scale = C_Major_Scale + m2
[Db, Eb, F, Gb, Ab, Bb, C]
```

There is also support for Scale-Degree arithemtic. Adding a Scale-Degree to another Scale-Degree produces a new Scale. The leftmost Degree within the addition is treated as the Tonic of the new Scale and its tone is the tone corresponding to the new Scale.
```
>>> C_Major_Scale[1] + C_Major_Scale[3]
[C, E]
```

If the two Scale-Degrees come from different parent Scales both Degrees will be treated as if based on the leftmost Degrees Tonic Tone. As an example, the third Degree of the E Chromatic Scale is an F# Tone, but adding the third Degree to the first Degree of the C Major Scale adds a D natural Tone because that is the third Degree of the C Chromatic Scale.
```
>>> C_Major_Scale[1] + E_Chromatic_Scale[3]
[C, D]
```

Scales also have support for arithmetic with Scale-Degrees and behave similarly. This allows you to add multiple Degrees at a time, giving us an easy way to create new Chords manually!
```
>>> C_Major_Scale[1] + E_Chromatic_Scale[3] + C_Major_Scale[4]
[C, D, F]
```

<a name="scale-transformation"/>

#### 2.2.3. Transformation

You can modify an existing Scale to produce a new Scale by using the addInterval() method.
```
>>> new_scale = C_Major_Scale.addInterval(aug5)
[C, D, E, F, G, G#, A, B]
```

The Scale-Degrees can also be altered to produce new Scales
```
>>> C_Harmonic_Major_Scale = C_Major_Scale[6].transform("b")
[C, D, E, F, G, Ab, B]
```

<a name="scale-building"/>

#### 2.2.4. Building Chords/Scales

From a Scale-Degree you can build a new Scale or Chord
```
>>> D_Dorian_Scale = C_Major_Scale[2].buildScale()
[D, E, F, G, A, B, C]
```

Build a Scale on a Scale-Degree using a specific pitch-class-set
```
>>> D_Melodic_Minor = C_Major_Scale[2].buildScaleWithIntervals([P1, M2, m3, P4, P5, M6, M7])
[D, E, F, G, A, B, C#]
```

You can also check if a Scale contains a Chord, another Scale, or a pitch-class-set.
```
>>> D_Dorian_Scale in C_Major_Scale
True
>>> G9 in D_Dorian_Scale
True
>>> [P1, M3, P5] in C_Major_Scale
True
>>> P5 in C_Major_Scale
True
```

My Scale class also works with Non-heptatonic Scales. You can create a Chromatic Scale of 12 notes, or a Diminished Scale of 8. There is no limitation to the Scales you can create at this point.
```
>>> C_Chromatic_Scale = Scale(C, [P1, m2, M2, m3, M3, P4, aug4, P5, aug5, M6, aug6, M7])
[C, Db, D, Eb, E, F, F#, G, G#, A, A#, B]
```

<a name="scale-propterties"/>

#### 2.2.5. Scale Properties

The scale also has several methods for determining properties of scales. You can read about what these algorithms do at https://ianring.com/musictheory/scales/. Currently the properties supported are:
```
>>> Scale.getPrimeMode()
>>> Scale.isPrime()
>>> Scale.getCohemitonic()
>>> Scale.hasCohemitonia()
>>> Scale.isChiral()
>>> Scale.getIntervalVector()
>>> Scale.getReflectionAxes()
>>> Scale.getTritonia()
>>> Scale.getHemitonia()
>>> Scale.getRotationalSymmetry()
>>> Scale.getImperfections()
>>> Scale.getCardinality()
```

<a name="chords"/>

### 2.3. Chords

<a name="chord-initialization"/>

#### 2.3.0. Initialization

Build a chord off of a scale degree, the build chord method has two optional params, the amount of notes in the chord, and the generic interval between each degree, by default, chords are comprised of four notes with a generic interval of 3 (A third). In this case we are building a chord with five notes on the fifth scale degree of the C Major Scale. The succeeding chord is a quartal chord based off of the same degree.
```
>>> G9 = C_Major_Scale[5].build(Chord, 5)
[G, B, D, F, A]
>>> chord = C_Major_Scale[5].build(Chord, 5, 4)
[G, C, F, B, E]
```

You can use buildWithIntervals() to build a chord object with a specific pitch class. If the resulting Chord contains Tones that are note included within the Parent Scale the Parent Scale is altered. If the Parent Scale's Intervals are Distinct, meaning there are no two Intervals that share the same numeral, the Scale intervals will be altered. Otherwise if the Parent Scale is not Distinct, new intervals will be added. This is useful for deriving Secondary Dominants.
```
>>> E7 = C_Major_Scale[3].buildWithIntervals(Chord, [P1, M3, P5, m7])
[E, G#, B, D]
>>> E7.getParentScale()
[C, D, E, F, G#, A, B]
```

You can also build a Chord using Generic Intervals.
```
>>> E7 = C_Major_Scale[1].buildWithGenericIntervals(Chord, [1, 3, 4, 6])
[C, E, F, A]
```

Some more ways to build Chords:
```
>>> Chord(C, [P1, M3, P5, M7])
>>> Chord(C, [4, 3, 4])
>>> Chord([C, E, G, B])
>>> Chord(C, "maj7")
```

<a name="chord-representation"/>

#### 2.3.1. Representation

You can print the quality of the chord in three different ways. It is derived through an algorithm that emulates how music theorists derive chord qualities, so there is very little reliance on hardcoding and you can get the quality for almost any chord. The Parent Chord is the chord in question based exclusively off thirds, ignoring sus numerals. As a result the getParentChordQuality() method does not support sus.
```
>>> A_Melodic_Minor = Scale(A, Scale.demicalToPitchClass(melodic_minor_ascending))
>>> chord = A_Melodic_Minor[1].buildChord(6)
>>> chord.getParentChordQuality(3)
-Δ11
>>> chord.getParentChordQuality(2)
mM11
>>> chord.getParentChordQuality(1)
minmaj11
>>> chord.getParentChordQuality(0)
minormajor11
```

You can also slice chords in case you only want the quality of a certain part of the chord. Like with the scale, the indices start at 1 signifying the first degree of the chord. [1:2] will retrieve the first two intervals of the Chord.
```
>>> chord[1:2].getParentChordQuality(0)
minor3
```

If you want to print the exact quality of the Chord with support of add/sus intervals, you must use the getQuality() method.
```
>>> Chord(C, [P1, m3, aug4, M7]).getQuality()
mM7add#4no5
```

You can also print the Jazz Numeral Notation
```
>>> Scale(A, minor)[6].build(Chord, 7).printNumeral()
bVIM13#11
```

One problem I encountered was trying to figure out how to print the quality of quartal/quintal harmony and beyond that. The solution I found was to rearrange the intervals of said chords so that they are built on thirds and indicate the missing notes. 
```
>>> C_Major_Scale[1].buildChord(7, 4).printQuality()
M13
```

I also created a method called stringToPitchClass() which takes as input a string, and parses it with RegEx to generate a Pitch Class. There are no dictionaries for this besides the very basic naming conventions like "maj", "major". The pitch class is generated 100 percent logically. 
```
>>> Chord.stringToPitchClass("maj9b5#9")
[1, 3, b5, 7, #9]
```

You have full freedom to use any notation you like, and even combine notations
```
>>> Chord.stringToPitchClass("-M11b9")
[1, b3, 5, 7, b9, 11]
>>> Chord.stringToPitchClass("mmaj11b9")
[1, b3, 5, 7, b9, 11]
>>> Chord.stringToPitchClass("minmaj11b9")
[1, b3, 5, 7, b9, 11]
```

This can be very useful for creating chord objects with a specific pitch class
```
>>> Chord(C, Chord.stringToPitchClass("maj7b5"))
[C, E, Gb, B]
```

There is also support for sus chords. 
```
>>> Chord(C, Chord.stringToPitchClass("maj7b5sus4"))
[C, E, F, Gb, B]
```

As a bonus you can even use sus for altered intervals.
```
>>> Chord(C, Chord.stringToPitchClass("maj7b5sus#4"))
[C, E, #F, Gb, B]
```

You can use "no" to omit certain intervals from the pitch class
```
>>> Chord(C, Chord.stringToPitchClass("maj7b5no3"))
[C, Gb, B]
```

There is also support for Secondary Chords. Whenever you build a scale off of a degree, the degree is saved within the new scale object by reference. So you are able to print more accurate roman numeral symbols. EG
```
>>> D_Dorian_Scale = C_Major_Scale[2].buildScale()
>>> FM7 = D_Dorian_Scale[3].buildChord()
>>> FM7.jazzNumeralNotation()
IIIM7/ii
```

<a name="chord-arithmetic"/>

#### 2.3.2. Arithmetic

There are a lot of arithmetic options for a Chord. Adding an Interval to a Chord is just like adding one to a Scale. It shifts the Chord. However adding a generic interval to a Chord rotates it along its parent Scale, assuming a parent Scale is defined.
```
>>> CM7 + 2
[D, F, A, C]
```

<a name="chord-transformation"/>

#### 2.3.3. Transformation

You can transform a Chord just like a Scale with either an Accidental or ontop of that you can use a generic interval. When you alter a Chord with an interval, if there is a parent scale assigned to the Chord, the Parent-Scale will also be altered.
```
>>> CmM7 = CM7[2].transform("b")
[C, Eb, G, B]
>>> CmM7.getParentScale()
[C, D, Eb, F, G, A, B]
CM7[2].transformWithGenericInterval(2)
[C, F, G, B]
```

I also created some sugar methods for getting the Parallel and Relative Chords of a Chord. To get the Relative Chord of a Chord, you must either translate the Chord up or down a Generic Interval of 3. Whether its up or down depends on the Parent-Scale of the Chord. As an example: If our Chord is C Major and the Parent-Scale is C Major the Relative Chord is A Minor. However if The Parent-Scale is A Minor, then the Relative Chord is E Minor. 
```
>>> CM7 = C_Major_Scale[1].build(Chord)
>>> CM7.getRelativeChord()
[A, C, E, G]
>>> Am7 = A_Minor_Scale[1].build(Chord)
>>> Am7.getRelativeChord()
[C, E, G, B]
```

The same idea applies to Parallel Chords.
```
>>> CM7 = C_Major_Scale[1].build(Chord)
>>> CM7.getParallelChord()
[C, Eb, G, Bb]
>>> Cm7 = C_Minor_Scale[1].build(Chord)
>>> Cm7.getParallelChord()
[C, E, G, B]
```

<a name="chord-secondary"/>

#### 2.3.4. Secondary Chords

You can very easily create secondary Chords from scratch
```
>>> C_Major_Scale[2].buildScale()[5].buildWithIntervals(Chord, [P1, M3, P5, m7])
[A, C#, E, G]
```

Despite this I have created some Sugar Methods for creating certain Secondary Chords including:
```
>>> Chord.getSecondaryDominant()
>>> Chord.getSecondarySubDominant()
>>> Chord.getSecondaryTonic()
>>> Chord.getSecondaryNeopolitan()
>>> Chord.getSecondaryAugmentedSix()
>>> Chord.getSecondaryTritoneSubstitution()
```

<a name="chord-inversions"/>

#### 2.3.5. Inversions

My Chord class has several methods useful for dealing with Chord Inversions, including invert(), getInversion(), getFirstInversion(), getFiguredBass() and for the Chord-Degrees there is a getPositionInFirstInversion()
```
>>> inverted_chord = CM7.invert(3)
[G, B, C, E]
>>> inverted_chord.getInversion()
3
>>> inverted_chord.getFirstInversion()
[C, E, G, B]
>>> inverted_chord[2].getPositionInFirstInversion()
4
>>> Chord(C, [P1, M3, P5]).invert(3).getFiguredBass()
I6/4
```

<a name="chord-voice-leading"/>

#### 2.3.6. Voice Leading

There is also some support for voice-leading even with unique Chord voicings. 
```
>>> Dm7 = C_Major_Scale[2].buildWithGenericIntervals(Chord, [1, 5, 7, 10])
[D, A, C, F]
>>> Dm7.resolveChord()
[D, G, B, F]
```

<a name="chord-polymorphism"/>

#### 2.3.7. Polymorphism

Deciding how to build and represent the Chord object was very difficult. Traditionally a Chord is thought of as a Scale nested within another Scale, built on generic intervals. As an example, the Cmaj7 chord is the result of applying the generic intervals 1-3-5-7 to the major scale. Applying the same generic intervals to the minor scale produces a Cmin7 chord. Givin this, it wouldnt be unreasonable to think that the Chord object should have a strict dependancy on the Scale object, IE every Chord has a parent Scale. Despite this many people like to implement their libraries in such a way that the Chord is a distinct object from the Scale and has no reference or direct relationship with any Scale object. There are bennifits and drawbacks to both approaches. In the former approach you are givin context for the Chord in the form of a position within a Scale. This is useful for printing roman numerals and deriving related Chords. However in the latter implementation you have the freedom to build any Chord without first instantiating a parent Scale. How can we achieve both? 

My Chord object uses polymorphism to achieve both capabilities. The Chord object is a Subclass of the scale object and inherits all of its methods and attributes. When you create a Chord object without a parent Scale the Chord behaves like a normal Scale, but with some added methods like printQuality(). However if you build a Chord object off of a Scale Degree or you assign a parent Degree to a Chord the Chord object behaves differently. Some Examples:

Ex. 1: Generic intervals behave differently. A generic interval is typically thought of as the number of Scale Degrees between two Degrees. IE the distance between C and E in the C Major Scale is a Generic interval of 3. For a Chord without context, in which there is no assigned parent Scale, there are no hidden degrees between each Chord Degree and the Chord object is treated like a Scale. IE:
```
>>> CM7 = Chord(C, Chord.stringToPitchClass("maj7"))
>>> CM7[1] + 2
E
```

However in a chord with context the object understands that there is a D between the C and the E Tones.
```
>>> CM7 = C_Major_Scale[1].build(Chord)
>>> CM7[1] + 2
D
```

Ex. 2: Many methods within the Scale._Degree Class are overridden. An example includes the build() Method.
```
>>> CM7 = Chord(C, Chord.stringToPitchClass("maj7"))
>>> CM7[2].build(Chord, 4, 2)
[E, G, B, D]
```

For a chord with context, the generic interval of 2 is interpreted differently:
```
>>> CM7 = C_Major_Scale[1].build(Chord)
>>> CM7[2].build(Chord, 4, 2)
[E, F, G, A]
```

In case you want a Chord with context to behave like a Scale you can access super() methods.
```
>>> CM7 = C_Major_Scale[1].build(Chord)
>>> super(type(CM7[2]), CM7[2]).build(Chord, 4, 2)
[E, G, B, D]
```

<a name="configuration"/>

### 2.4. Configuration [WIP]:

```
ACCIDENTAL_LIMIT = 1
```
This constant changes the limit on the number of accidentals allowed for algorithm-generated intervals, specifically in the Scale.scaleStepsToPitchClass() method. Changing this constant will alter behaviour in some of the conversion methods.

<a name="goals"/>

## 3. Goals:

A lot of Chord functionality will be added. There is a lot of things I plan to add to this project. Scales and Chords are only the beginning. Some things I plan to create:
```
- I am currently working on a Keyboard and Tone class to translate scale objects into midi recognizable tones
- Motif, Sentence, Period, Phrase Objects for structural components of music
- A more fleshed out Note object that keeps track of octaves
- A progression object that keeps track of a pieces chord progression
- Just as how many people manually create midi files based on sheet music, once I am complete this library I 
  will translate many classical pieces into object form. The library should be able to reproduce a piece from 
  scratch using the concepts within its library. Doing this manually will be tedious but after a decent 
  quantity of pieces are described it might be sufficient to teach an AI to describe the pieces automatically.
```
