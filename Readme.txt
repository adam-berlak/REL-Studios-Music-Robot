The goal of this project is to create an artificial intelligence with a knowledge of Music Theory that can analyse music and potential produce new music

Components Required:
[1] Establish a taxonomy by either creating a new Music Theory Library or finding one online. This will be the part of the AI that deals with knowledge representation in the form of newly created data structures. 
    More specifically, Scales, Chords, Motifs, Structure and so on.
[2] Find a library that can read a midi file intelligently. IE: Distinguish between left and right hand, beats, measures and note lengths.
[3] Create an algorithm that parses a midi file and converts it into a more logical representation. IE: The algorithm should be able to read a measure and say "the left hand plays this pattern four times and has the chord progression I-IV-V"
[4] Use Machine learning to produce new music. The algorithm will take a collection of midi files as a data set and convert it into a knowledge representation it can understand, in this case Music Theory. Each midi file corresponds to a Song Object that contains
    all the information of the piece the AI can understand. The Neural Network will try and build the Songs structure from scratch until the error is small enough when comparing it to the actual song. We will then run the algorithm on
    a large set of music until it builds a strong enough network of possible ways to construct a piece. 