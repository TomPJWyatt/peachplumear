import random

from mingus.containers import Track
from mingus.containers import Bar
from mingus.containers import NoteContainer
from mingus.containers import Note
import mingus.core.chords as chords
import mingus.core.keys as keys
import mingus.core.notes as notes
import mingus.core.progressions as progressions
import mingus.midi.fluidsynth as fluidsynth


# omit the keys which are duplicates to give just 12 keys
omit = ('Gb','C#','Cb')
keys12 = [k for k in keys.keys if k[0] not in omit]
modes = ('Scale','Chord')


class Challenge():
    """This represents an interval challenge for the user."""
    def __init__(
        self,
        key=None,
        keyTypes = (0,1),
        intervals=None,
        mode='Scale',
        nIntervals=1,
        validInts=[i for i in range(1,8)],
        inversion = False,
        octave = False
    ):
        
        """
        Represents a interval challenge.
        
        Parameters
        ----------
        key : str 
            The key we are in. Must be a str corresponding to mingus key.
        intervals : list of int [1,7]
        keyTypes : tuple of int
            Tuple containing all types of key to include in the challenge. 
            0 for major, 1 for minor.
        mode : {'Scale','Chord'}
            What sort of challenge. Scale is just notes. Chord is chord 
            sequence.
        NIntervals : int > 0
            The number of intervals in the test if intervals isn's specified.
        validInts : list of ints
            The intervals that you pick from if you are doing random choice.
        """
        
        if key:
            self.key = key
        else:
            i = random.randint(0,11)
            q = random.choice(keyTypes)
            self.key = keys12[i][q]
        assert self.key in [q for k in keys12 for q in k],'invalid key'  
        
        assert isinstance(nIntervals,int),'nIntervals must be an int'
        
        if intervals:
            self.intervals = intervals
        else:
            self.intervals = [random.choice(validInts) for i in range(nIntervals)]
        self.chords = []
        self.chordNames = []
        
        assert isinstance(self.intervals,list),'intervals must be a list'
        intQ = [isinstance(i,int) and i>0 and i<8 for i in self.intervals]
        assert all(intQ),'intervals elements must be ints between 1-7'
        
        self.scale = keys.get_notes(self.key)
        self.scale = self.scale + [self.scale[0]]
        # the fundamental note (different from key b/c key=e -> Fund=E)
        self.root = self.scale[0]
        self.rootI = int(Note(self.root))
        
        self.mode = mode
        assert self.mode in modes,'mode must be in: '+str(modes)
        
        self.inversion = inversion
        self.octave = octave
        
        self.scaleBar = self.makeScaleBar()
        self.rootBar = self.makeRootBar()
        self.testTrack = self.makeTestTrack()
        self.track = self.makeFullTrack()
        
        self.answer = self.makeAnswer()

        
    def makeAnswer(self):
        ans = 'The key is: ' + self.key
        ans += '. \nThe sequence is: I-' + self.intervals2str()
        ans += '\n(' 
        if self.mode=='Scale':
            prog = [self.root]+[self.scale[i-1] for i in self.intervals]
        else:
            prog = self.chordNames
        ans += '-'.join(prog) + ')'
        return ans
        
        
    def intervals2str(self):
        """Convert intervals to roman numerals strings for display."""
        out = [int2str[i] for i in self.intervals]
        out = '-'.join(out)
        return out

    
    def makeScaleBar(self):
        """Makes a mingus.Bar object of the scale of the key."""
        
        sc = [int(Note(s)) for s in self.scale]
        sc = [s if s>=self.rootI else s+12 for s in sc]+[self.rootI+12]
        bar = Bar(self.key,(4,4))
        for s in sc:
            bar.place_notes(Note(s),8)
        return bar
    
    
    def makeRootBar(self):
        """Makes a mingus.Bar object playing the root and root chord."""
        bar = Bar(self.key,(4,4))
        bar.place_notes(NoteContainer(self.root),4)
        bar.place_notes(NoteContainer(chords.I(self.key)),4)
        bar.place_notes(NoteContainer(self.root),4)
        bar.place_notes(NoteContainer(chords.I(self.key)),4)
        return bar
        
    
    def makeTestTrack(self):
        """
        Makes a mingus.Bar object playing the root chord then interval chord.
        """
        track = Track()
        if self.mode=='Chord':
            self.chords = ['I']+[int2str[n] for n in self.intervals]
            self.chords = progressions.to_chords(self.chords,self.key)
            self.chordNames = [chords.determine(c,shorthand=True)[0] 
                               for c in self.chords]
            if self.inversion:
                for i,p in enumerate(self.chords):
                    r = random.choice([0,1,2])
                    if r==1:
                        self.chords[i] = chords.first_inversion(p)
                        # do ourself b/c chords.determine doesn't always work
                        self.chordNames[i] += '_inv1' 
                    elif r==2:
                        self.chords[i] = chords.second_inversion(p)
                        self.chordNames[i] += '_inv2'
            self.chords = [notes2Ascending(c,self.root) for c in self.chords]
            if self.octave:
                for i,c in enumerate(self.chords):
                    if i==0:
                        continue
                    if random.choice([0,1]):
                        for n in c:
                            n.octave_down()
            for p in self.chords:
                track.add_notes(p,4)
                track.add_notes(p,4)
        else:
            track.add_notes(NoteContainer(self.root),4)
            for i in self.intervals:
                N = Note(self.scale[i-1])
                if int(N)<self.rootI or i==1:
                    N = Note(int(N)+12)
                if self.octave and random.choice([0,1]):
                    N.octave_down()
                track.add_notes(NoteContainer(N),4)
        return track
    

    def makeFullTrack(self):
        """
        Makes a mingus.Track object containing the scaleBar then the rootBar 
        then the test track twice.
        """
        track = Track()
        track.add_bar(self.scaleBar)
        track.add_bar(self.rootBar)
        for b in self.testTrack.bars:
            track.add_bar(b)
        for b in self.testTrack.bars:
            track.add_bar(b)
        return track
    
    
int2str = {
    1:'I',
    2:'II',
    3:'III',
    4:'IV',
    5:'V',
    6:'VI',
    7:'VII',
    8:'I'
}


def notes2Ascending(notesList,fundamental,octave=4):
    """
    This turns a mingus notes notesList (i.e. just the letters) into a 
    NoteContainer of Notes which starts within the octave following 
    Note(fundamental,octave).
    
    Parameters
    ----------
    notesList : list of str
        Should be a list of notes.
    fundamental : str
        The note which defines the octave that the notesList starts in.
    octave : int
        The octave of the fundamental.
    """
    assert isinstance(octave,int),'octave must be an int'
    assert isinstance(fundamental,str),'fundamental must be a str'
    assert isinstance(notesList,list),'notesList must be a list'
    
    fund = int(Note(fundamental,octave))
    n0 = int(Note(notesList[0],octave))
    if n0<fund:
        n0+=12
    n0b = notes.note_to_int(notesList[0])

    notesList_diff = [notes.note_to_int(n)-n0b for n in notesList]
    notesList_diff = [n+12 if n<0 else n for n in notesList_diff]
    out = [n0+n for n in notesList_diff]

    for i,n in enumerate(out):
        if i==0:
            continue
        if out[i]<=out[i-1]:
            out[i]+=12*(1+((out[i-1]-out[i])//12))
    return NoteContainer([Note(n) for n in out])