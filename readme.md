ChordProgTrainer
================

This programme provides a simple user interface which helps you train your ear to musical intervals by generating and playing 'challenges'.

The challenges are either 'scale' (just notes) or 'chords' (triads).
Each challenge starts on the root note of the key and plays a sequence of notes or triads from that key.

You can play either just the challenge notes or add an introductory 2 bars playing the scale and root chords to introduce the key to your ear.

The root note is currently always in octave 4 and by default the notes (or root notes of the chords) of the challenge will all lie within the first octave above the root note. You can allow for notes in the octave below to be included.

You can also control:
- the numbers of intervals in the sequence
- the bpm of the play back
- which intervals can be included in the challenge
- whether to include chord inversions
- whether to change key for the next challenge or note

The user interface also allows you to play the notes of the scale over 2 octaves.



Requirements
------------

- mingus
- fluidsynth
