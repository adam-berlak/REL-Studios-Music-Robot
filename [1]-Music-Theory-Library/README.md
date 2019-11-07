# REL STUDIOS - pyMusicTheory Guide

## 1. About this project:

Lookng through existing libraries for music theory, I noticed a recurring problem. Most of the existing music theory libraries
rely heavily on hardcoding of information. Things like Chord qualitys and properties of scales are often hardcoded in dictionaries
when they should be derived using logical formulas within a Scale object. As a result, these libraries are not very extensible, they limit your inputs and likely fall apart when you try to get more creative with your scales. As a goal for myself I attempted to limit all hardcoding to names, and reduce everything else that can be derived logically to methods. The result; less reliance on definitions, less constants, and greater extensibility.

## 2. How to use this library:

A Scale Object requires a note for the Tonic, and a list of Intervals organized as a Pitch Class Set
```
>>> major = [P1, M2, M3, P4, P5, M6, M7]
>>> C_Major_Scale = Scale("C", major)
>>> print(C_Major_Scale)
[C, D, E, F, G, A, B]
```

You can access any of the scale degrees by using an index. The indices start at 1 as opposed to 0
```
>>> print(C_Major_Scale[1])
C
```
