# REL STUDIOS - RELMusicTheory Guide

## 1. About this project:

Lookng through existing libraries for music theory, I noticed a recurring problem. Most of the existing music theory libraries
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

From a scale degree you can build a new scale or chord
```
>>> D_Dorian_Scale = C_Major_Scale[2].buildScale()
[D, E, F, G, A, B, C]
```
You can also transpose a Scale up by adding integers to it. My library assigns pitchs and accidentals to the scales automatically without any hardcoding. The proccess is identical to how its done by theorists ensuring minimal accidentals are used. As an example:
Db Major notation will be used over C# Major despite the latter also being valid. This is because Db Major has less accidentals. Despite this you can still create a C# Major Scale.
```
>>> D_Major_Scale = C_Major_Scale + 2
[D, E, F#, G, A, B, C#]
```
You can also preform addition with degrees. When adding an integer x to a scale degree, the integer is treated as a generic interval, meaning a degree x number of diatonic notes above the principle degree will be returned. In the future it may be treated as a specific interval.
```
>>> C_Major_Scale[1] + 2
E
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

Build a chord off of a scale degree, the build chord method has two optional params, the amount of notes in the chord, and the skip size, by default, chords are comprised of four notes with a skip size of two. In this case we are building a chord with five notes on the fourth scale degree of the dorian scale/mode.
```
>>> G9 = D_Dorian_Scale[4].buildChord(5)
[G, B, D, F, A]
```
You can print the quality of the chord in three different ways. The quality is derived through an algorithm that emulates how music theorists method, so there is very little reliance on hardcoding and you can get the quality for almost any chord.
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
minor
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
## 3. Goals:

A lot of Chord functionality will be added. There is a lot of things I plan to add to this project. Scales and Chords are only the beginning. Some things I plan to create:
```
- Motif, Sentance, Period, Phrase Objects for structural components of music
- A more fleshed out Note object that keeps track of octaves
- A progression object that uses artificial intelligence to analyse a chord progression
```
