# REL STUDIOS - RELMusicTheory for Python Guide

## 1. About this project:

Looking through existing libraries for music theory, I noticed a recurring problem. Most of the existing music theory libraries
rely heavily on hardcoding of information. Things like Chord qualitys and properties of scales are often hardcoded in dictionaries
when they should be derived using logical formulas within a Scale object. As a result, these libraries are not very extensible, they limit your inputs and likely fall apart when you try to get more creative with your scales. As a goal for myself I attempted to limit all hardcoding to names, and reduce everything else that can be derived logically to methods. The result; less reliance on definitions, less constants, and greater extensibility.

## 2. How to use this library:

#### 2.1. Scales

A Scale Object requires a note for the Tonic, and a list of Intervals organized as a Pitch Class Set
```
>>> major = [P1, M2, M3, P4, P5, M6, M7]
>>> C_Major_Scale = Scale("C", major)
[C, D, E, F, G, A, B]
```

You can access any of the scale degrees by using an index. The indices start at 1 as opposed to 0
```
>>> C_Major_Scale[1]
C
```
If you add an integer to a scale degree it is treated as a generic interval while adding an interval is treated like adding a specific interval.
```
>>> C_Major_Scale[1] + 4
F
>>> C_Major_Scale[1] + m3
Eb
```

I think its worth emphasizing that adding a interval to a degree, which produces a degree that is not contained in the principle scale will create a new parent scale for the resulting degree. EG:
```
>>> new_degree = C_Major_Scale[2] + M3 # The second degree of the C Major Scale is D, and the result of adding a M3 Interval to it is F#
>>> new_degree.getParentScale()
[C, D, E, F, F#, G, A, B]
```

You can modify an existing scale to produce a new scale by using the addInterval() method.
```
>>> new_scale = C_Major_Scale.addInterval(aug5)
[C, D, E, F, G, G#, A, B]
```

The scale degrees can also be altered to produce new scales
```
>>> C_Harmonic_Major_Scale = C_Major_Scale[6].transform("b")
[C, D, E, F, G, Ab, B]
```

From a scale degree you can build a new Scale or Chord
```
>>> D_Dorian_Scale = C_Major_Scale[2].buildScale()
[D, E, F, G, A, B, C]
```

Build a scale on a scale degree using a specific pitch class set
```
>>> D_Melodic_Minor = C_Major_Scale[2].buildScaleWithIntervals([P1, M2, m3, P4, P5, M6, M7])
[D, E, F, G, A, B, C#]
```

You can also transpose a Scale up by adding integers or intervals to it. My library assigns pitchs and accidentals to the scales automatically without any hardcoding. The proccess is identical to how its done by theorists ensuring minimal accidentals are used. As an example: Db Major notation will be used over C# Major despite the latter also being valid. This is because Db Major has less accidentals. Despite this you can still create a C# Major Scale. An integer is treated as a Generic Interval, meaning the value represents scale steps as opposed to semitones. To transpose a scale by semitones you must add an interval to it
```
>>> D_Major_Scale = C_Major_Scale + 2
[D, E, F#, G, A, B, C#]
>>> D_Major_Scale = C_Major_Scale + M2
[D, E, F#, G, A, B, C#]
>>> Db_Major_Scale = C_Major_Scale + m2
[Db, Eb, F, Gb, Ab, Bb, C]
```

You can also check if a Scale contains a Chord, another Scale, or a Pitch Class
```
>>> D_Dorian_Scale in C_Major_Scale
True
>>> G9 in D_Dorian_Scale
True
>>> [P1, M3, P5] in C_Major_Scale
True
```

My Scale class also works with non-heptatonic scales. You can create a Chromatic scale of 12 notes, or a diminished scale of 8. There is no limitation to the scales you can create at this point.
```
>>> C_Chromatic_Scale = Scale("C", [P1, m2, M2, m3, M3, P4, aug4, P5, aug5, M6, aug6, M7])
[C, Db, D, Eb, E, F, F#, G, G#, A, A#, B]
```

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
#### 2.2. Chords

Build a chord off of a scale degree, the build chord method has two optional params, the amount of notes in the chord, and the skip size, by default, chords are comprised of four notes with a skip size of two. In this case we are building a chord with five notes on the fifth scale degree of the C Major Scale. The following chord is a quartal chord based of the first degree of C Major.
```
>>> G9 = C_Major_Scale[5].buildChord(5)
[G, B, D, F, A]
>>> chord = C_Major_Scale[1].buildChord(5, 3)
[C, F, B, E, A]
```
You can print the quality of the chord in three different ways. It is derived through an algorithm that emulates how music theorists derive chord qualities, so there is very little reliance on hardcoding and you can get the quality for almost any chord.
```
>>> AMelodicMinor = Scale("A", melodicMinor)
>>> chord = AMelodicMinor[1].buildChord(6)
>>> chord.printQuality(2)
M11b3
>>> chord.printQuality(1)
maj11b3
>>> chord.printQuality(0)
major11b3
```

You can also slice chords in case you only want the quality of a certain part of the chord. Like with the scale, the indices start at 1 signifying the first degree of the chord. [1:3] will retrieve notes one through and including three of the chord.
```
>>> chord[1:3].printQuality(0)
minor3
```

You can also print the Jazz Numeral Notation or just the Numeral of the chord by itself
```
>>> Scale("A", minor)[6].buildChord(7).printNumeral()
bVI
>>> Scale("A", minor)[6].buildChord(7).jazzNumeralNotation()
bVIM13#11
```

You can resolve a chord using a certain rule
```
>>> G7.resolveChord(circleOfFifths)
[C, E, G, B]
```

One problem I encountered was trying to figure out how to print the quality of quartal/quintal harmony and beyond that. The solution I found was to rearrange the intervals of said chords so that they are built on thirds and indicate the missing notes. 
```
>>> C_Major_Scale[1].buildChord(7, 3).printQuality()
M13
```

I also created a method called stringToPitchClass() which takes as input a string, and parses it with RegEx to generate a Pitch Class
```
>>> Chord.StringToPitchClass("maj9b5#9")
[1, 3, b5, 7, #9]
```

There is also support for Secondary Chords. Whenever you build a scale off of a degree, the degree is saved within the new scale object by reference. So you are able to print more accurate roman numeral symbols. EG
```
>>> D_Dorian_Scale = C_Major_Scale[2].buildScale()
>>> FM7 = D_Dorian_Scale[3].buildChord()
>>> FM7.jazzNumeralNotation()
III7/ii
```

## 3. Goals:

A lot of Chord functionality will be added. There is a lot of things I plan to add to this project. Scales and Chords are only the beginning. Some things I plan to create:
```
- Motif, Sentance, Period, Phrase Objects for structural components of music
- A more fleshed out Note object that keeps track of octaves
- A progression object that uses artificial intelligence to analyse a chord progression
```
