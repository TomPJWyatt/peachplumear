import os
import random
from tkinter import Canvas,PhotoImage,Button,StringVar,Radiobutton,Label,Entry,Frame,LEFT,TOP,RIGHT,NW

from mingus.containers import Track
from mingus.containers import NoteContainer
from mingus.containers import Note
import mingus.core.progressions as progressions
import mingus.midi.fluidsynth as fluidsynth

import challenge

defaultSF2 = r"C:\Users\Tom\FluidSynth\FluidR3_GM.sf2"

class GUI():
    def __init__(self,root,sf2=defaultSF2):
        # given parameters
        self.root = root
        self.root.geometry('430x285')

        self.playFrame = Frame(self.root,bg='white')
        self.playIntFrame = Frame(self.root,bg='white')
        self.playInt2Frame = Frame(self.root,bg='white')
        self.playInt2Frame.pack(side=TOP,padx=(102,0),anchor=NW)
        self.playIntFrame.pack(side=TOP,padx=(102,0),anchor=NW)
        self.intervalFrame = Frame(self.root,bg='white')
        self.intervalFrame.pack(side=TOP,anchor=NW)
        self.playFrame.pack(side=TOP,anchor=NW)
        self.BPMFrame = Frame(self.playFrame,bg='white')
        self.BPMFrame.pack(side=RIGHT)
        self.NintFrame = Frame(self.playFrame,bg='white')
        self.NintFrame.pack(side=RIGHT)

        self.sf2 = sf2
        fluidsynth.init(self.sf2)

        self.key = None

        self.BPM = StringVar(value='120')
        self.Nint = StringVar(value='1')
        self.keyLock = False
        self.maj = True
        self.min = True
        self.I = True
        self.II = True
        self.III = True
        self.IV = True
        self.V = True
        self.VI = True
        self.VII = True
        self.inversion = False
        self.oct = False
        self.intervals = [i for i in range(1,8)]

        self.challenge = None
        self.mode = StringVar(self.root,"Scale")

        # main window
        self.root.title("Interval Trainer")
        self.root.iconbitmap(r'Images/icon.ico')
        self.root.configure(background='white')

        # images for buttons
        self.keyLockIm = PhotoImage(file=r'Images/keyLock.png')
        self.newIm = PhotoImage(file=r'Images/New.png')
        self.playIm = PhotoImage(file=r'Images/PlayB.png')
        self.playChIm = PhotoImage(file=r'Images/PlayChB.png')
        self.revealIm = PhotoImage(file=r'Images/RevealB.png')
        self.BPMupIm = PhotoImage(file=r'Images/BPMupB.png')
        self.BPMdownIm = PhotoImage(file=r'Images/BPMdownB.png')
        self.majIm = PhotoImage(file=r'Images/maj.png')
        self.minIm = PhotoImage(file=r'Images/min.png')
        self.playIntIm = PhotoImage(file=r'Images/playInt.png')
        self.I_Im = PhotoImage(file=r'Images/I.png')
        self.II_Im = PhotoImage(file=r'Images/II.png')
        self.III_Im = PhotoImage(file=r'Images/III.png')
        self.IV_Im = PhotoImage(file=r'Images/IV.png')
        self.V_Im = PhotoImage(file=r'Images/V.png')
        self.VI_Im = PhotoImage(file=r'Images/VI.png')
        self.VII_Im = PhotoImage(file=r'Images/VII.png')
        self.inv_Im = PhotoImage(file=r'Images/inv.png')
        self.oct_Im = PhotoImage(file=r'Images/8ave.png')
        self.scaleIm = PhotoImage(file=r'Images/scale.png')
        self.chordIm = PhotoImage(file=r'Images/chord.png')

        # making buttons
        self.keyLockB = Button(
            self.root,
            height=25,
            width=25,
            image=self.keyLockIm,
            command=self.keyLock_f)
        self.newB = Button(
            self.playFrame,
            height=75,
            width=75,
            image=self.newIm,
            command=self.new)
        self.playB = Button(
            self.playFrame,
            height=75,
            width=75,
            image=self.playIm,
            command=self.playChallenge)
        self.playChB = Button(
            self.playFrame,
            height=75,
            width=75,
            image=self.playChIm,
            command=self.playJustChallenge)
        self.revealB = Button(
            self.playFrame,
            height=75,
            width=75,
            image=self.revealIm,
            command=self.revealAnswer)
        self.BPMupB = Button(
            self.BPMFrame,
            height=10,
            width=20,
            image=self.BPMupIm,
            command=self.BPMup)
        self.BPMdownB = Button(
            self.BPMFrame,
            height=10,
            width=20,
            image=self.BPMdownIm,
            command=self.BPMdown)
        self.NintUpB = Button(
            self.NintFrame,
            height=10,
            width=20,
            image=self.BPMupIm,
            command=self.NintUp)
        self.NintDownB = Button(
            self.NintFrame,
            height=10,
            width=20,
            image=self.BPMdownIm,
            command=self.NintDown)
        self.majB = Button(
            self.intervalFrame,
            height=25,
            width=35,
            image=self.majIm,
            command=self.maj_f)
        self.minB = Button(
            self.intervalFrame,
            height=25,
            width=35,
            image=self.minIm,
            command=self.min_f)
        self.I_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.I_Im,
            command=self.I_f)
        self.II_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.II_Im,
            command=self.II_f)
        self.III_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.III_Im,
            command=self.III_f)
        self.IV_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.IV_Im,
            command=self.IV_f)
        self.V_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.V_Im,
            command=self.V_f)
        self.VI_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.VI_Im,
            command=self.VI_f)
        self.VII_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.VII_Im,
            command=self.VII_f)
        self.inv_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.inv_Im,
            command=self.inv_f)
        self.oct_B = Button(
            self.intervalFrame,
            height=25,
            width=25,
            image=self.oct_Im,
            command=self.oct_f)
        self.playIntFs = [self.playIntI,self.playIntII,self.playIntIII,
                          self.playIntIV,self.playIntV,self.playIntVI,
                          self.playIntVII,self.playIntVIII]
        self.playInt2Fs = [self.playInt2I,self.playInt2II,self.playInt2III,
                          self.playInt2IV,self.playInt2V,self.playInt2VI,
                          self.playInt2VII,self.playInt2VIII]
        self.playIntBs = [Button(self.playIntFrame,height=25,width=25,
                                  image=self.playIntIm,
                                  command=f) for f in self.playIntFs]
        self.playInt2Bs = [Button(self.playInt2Frame,height=25,width=25,
                                  image=self.playIntIm,
                                  command=f) for f in self.playInt2Fs]
        # setting button parameters
        self.allButts = [self.newB,self.playB,self.playChB,self.revealB,
                         self.I_B,self.II_B,self.III_B,self.IV_B,self.V_B,
                         self.VI_B,self.VII_B,self.inv_B,self.majB,
                         self.minB,self.keyLockB,self.oct_B] + self.playIntBs
        self.allNumeralBs = [self.I_B,self.II_B,self.III_B,self.IV_B,self.V_B,
                             self.VI_B,self.VII_B,self.majB,self.minB]
        [butt.config(bg='white') for butt in self.allButts]
        [butt.config(relief='sunken') for butt in self.allNumeralBs]
        self.playB.config(state='disabled')
        self.playChB.config(state='disabled')
        self.revealB.config(state='disabled')
        [b.config(state='disabled') for b in self.playIntBs]
        [b.config(state='disabled') for b in self.playInt2Bs]

        # entry boxes
        self.BPMEntry = Entry(self.BPMFrame,width=3,textvariable=self.BPM)
        self.NintEntry = Entry(self.NintFrame,width=3,textvariable=self.Nint)

        # mode radio buttons
        self.modeFrame = Frame(self.root,bg='white')
        self.scaleB = Radiobutton(
            self.modeFrame,
            image=self.scaleIm,
            variable=self.mode,
            value='Scale',
            indicatoron=1,
            bg='white')
        self.chordB = Radiobutton(
            self.modeFrame,
            image=self.chordIm,
            variable=self.mode,
            value='Chord',
            indicatoron=1,
            bg='white')

        # packing the widgets
        self.keyLockB.pack(side=LEFT,anchor=NW)
        [b.pack(side=LEFT) for b in self.playInt2Bs]
        [b.pack(side=LEFT) for b in self.playIntBs]
        self.newB.pack(side=LEFT,padx=(6,0))
        self.playB.pack(side=LEFT)
        self.playChB.pack(side=LEFT)
        self.revealB.pack(side=LEFT)
        self.BPMupB.pack(side=TOP)
        self.BPMEntry.pack(side=TOP)
        self.BPMdownB.pack(side=TOP)
        self.NintUpB.pack(side=TOP)
        self.NintEntry.pack(side=TOP)
        self.NintDownB.pack(side=TOP)
        self.majB.pack(side=LEFT,padx=(15,0))
        self.minB.pack(side=LEFT,padx=(0,5))
        self.I_B.pack(side=LEFT)
        self.II_B.pack(side=LEFT)
        self.III_B.pack(side=LEFT)
        self.IV_B.pack(side=LEFT)
        self.V_B.pack(side=LEFT)
        self.VI_B.pack(side=LEFT)
        self.VII_B.pack(side=LEFT)
        self.inv_B.pack(side=LEFT,padx=15)
        self.oct_B.pack(side=LEFT)
        self.scaleB.pack(side=LEFT,padx=(6,0))
        self.chordB.pack(side=LEFT)

        # make canvases for BPM and Nint images
        self.BPMCanvas = Canvas(self.BPMFrame,width=25,height=12,bg='white')
        self.BPMCanvas.pack(side=LEFT)
        self.BPMIm = PhotoImage(file=r'Images/BPM.png')
        self.BPMCanvas.create_image(14,7,image=self.BPMIm)
        self.NintCanvas = Canvas(self.NintFrame,width=25,height=12,bg='white')
        self.NintCanvas.pack(side=LEFT)
        self.NintIm = PhotoImage(file=r'Images/Nint.png')
        self.NintCanvas.create_image(14,7,image=self.NintIm)

        self.modeFrame.pack(side=TOP,anchor=NW)

        # space for the answer reveal
        self.answerLab = Label(self.root,text='',bg='white')
        self.answerLab.pack(side=TOP)

        # closing behaviour
        self.root.protocol("WM_DELETE_WINDOW",self.on_closing)

        self.root.bind('a', lambda event:self.playChallenge())
        self.root.bind('<space>', lambda event:self.playJustChallenge())
        self.root.bind('=', lambda event:self.revealAnswer())
        self.root.bind('n', lambda event:self.new())
        self.root.bind('1', lambda event:self.I_f())
        self.root.bind('2', lambda event:self.II_f())
        self.root.bind('3', lambda event:self.III_f())
        self.root.bind('4', lambda event:self.IV_f())
        self.root.bind('5', lambda event:self.V_f())
        self.root.bind('6', lambda event:self.VI_f())
        self.root.bind('7', lambda event:self.VII_f())
        self.root.bind('7', lambda event:self.oct_f())
        self.root.bind('q', lambda event:self.playIntI())
        self.root.bind('w', lambda event:self.playIntII())
        self.root.bind('e', lambda event:self.playIntIII())
        self.root.bind('r', lambda event:self.playIntIV())
        self.root.bind('t', lambda event:self.playIntV())
        self.root.bind('y', lambda event:self.playIntVI())
        self.root.bind('u', lambda event:self.playIntVII())
        self.root.bind('i', lambda event:self.playIntVIII())
        self.root.bind('Q', lambda event:self.playInt2I())
        self.root.bind('W', lambda event:self.playInt2II())
        self.root.bind('E', lambda event:self.playInt2III())
        self.root.bind('R', lambda event:self.playInt2IV())
        self.root.bind('T', lambda event:self.playInt2V())
        self.root.bind('Y', lambda event:self.playInt2VI())
        self.root.bind('U', lambda event:self.playInt2VII())
        self.root.bind('I', lambda event:self.playInt2VIII())        
        self.root.bind('m', lambda event:self.min_f())
        self.root.bind('M', lambda event:self.maj_f())
        self.root.bind('<Return>', lambda event:self.refocus())

    def refocus(self):
        self.root.focus_set()

    def keyLock_f(self):
        """Whether or not to change key when you create a new challenge."""
        self.keyLock = not self.keyLock
        if self.keyLock:
            self.keyLockB.config(relief='sunken')
        else:
            self.keyLockB.config(relief='raised')

    def new(self):
        """Sets a new challenge."""
        if not self.key or not self.keyLock:
            kt = tuple([i for i,m in enumerate([self.maj,self.min]) if m])
            i = random.randint(0,11)
            q = random.choice(kt)
            self.key = challenge.keys12[i][q]
        self.answerLab.config(text='')
        if not any([self.I,self.II,self.III,self.IV,self.V,self.VI,self.VII]):
            self.I_f()
        if not any([self.maj,self.min]):
            self.maj_f()
        self.challenge = challenge.Challenge(key=self.key,
                                             mode=self.mode.get(),
                                             validInts=self.intervals,
                                             nIntervals=int(self.Nint.get()),
                                             inversion=self.inversion,
                                             octave = self.oct)
        self.playB.config(state='normal')
        self.playChB.config(state='normal')
        self.revealB.config(state='normal')
        [b.config(state='normal') for b in self.playIntBs+self.playInt2Bs]

    def playChallenge(self):
        """Play whole Track of challenge."""
        if int(self.BPM.get()) < 40:
            self.BPM.set('40')
        BPM = int(self.BPM.get())
        fluidsynth.play_Track(self.challenge.track,1,BPM)

    def playJustChallenge(self):
        """Play just the interval bars of the challenge."""
        if int(self.BPM.get()) < 40:
            self.BPM.set('40')
        track = Track()
        for b in self.challenge.testTrack.bars:
            track.add_bar(b)
        for b in self.challenge.testTrack.bars:
            track.add_bar(b)
        BPM = int(self.BPM.get())
        fluidsynth.play_Track(track,1,BPM)

    def stop(self):
        fluidsynth.stop_Track()

    def revealAnswer(self):
        """Prints the answer to the gui."""
        self.answerLab.config(text=self.challenge.answer)

    def BPMup(self):
        """Increases the BPM by one."""
        self.BPM.set(str(int(self.BPM.get())+1))

    def BPMdown(self):
        """Reductes the BPM by 1 (minumim is 40)."""
        if int(self.BPM.get())<=40:
            return
        self.BPM.set(str(int(self.BPM.get())-1))

    def NintUp(self):
        """Increases the number of intervals by one."""
        self.Nint.set(str(int(self.Nint.get())+1))

    def NintDown(self):
        """Reductes the number of intervals by 1 (minumim is 1)."""
        if int(self.Nint.get())<=1:
            return
        self.Nint.set(str(int(self.Nint.get())-1))

    def maj_f(self):
        """Whether or not to include this major keys."""
        self.maj = not self.maj
        if self.maj:
            self.majB.config(relief='sunken')
        else:
            self.majB.config(relief='raised')

    def min_f(self):
        """Whether or not to include this minor keys."""
        self.min = not self.min
        if self.min:
            self.minB.config(relief='sunken')
        else:
            self.minB.config(relief='raised')

    def playInt(self,interval,octave=False):
        """Play inteval."""
        track = Track()
        if self.mode.get()=='Scale':
            N = Note(self.challenge.scale[interval-1])
            if self.challenge.rootI>int(N):
                N = Note(int(N)+12)
            if interval==8:
                N.octave_up()
            if octave:
                N.octave_down()
            track.add_notes(N,4)
        else:
            p = [challenge.int2str[interval]]
            p = progressions.to_chords(p,self.challenge.key)
            p = challenge.notes2Ascending(p[0],self.challenge.root)
            if interval==8:
                for n in p:
                    n.octave_up()
            if octave:
                for n in p:
                    n.octave_down()
            track.add_notes(p,4)
        fluidsynth.play_Track(track,1,120)
    def playIntI(self):
        self.playInt(1)
    def playIntII(self):
        self.playInt(2)
    def playIntIII(self):
        self.playInt(3)
    def playIntIV(self):
        self.playInt(4)
    def playIntV(self):
        self.playInt(5)
    def playIntVI(self):
        self.playInt(6)
    def playIntVII(self):
        self.playInt(7)
    def playIntVIII(self):
        self.playInt(8)
    def playInt2I(self):
        self.playInt(1,octave=True)
    def playInt2II(self):
        self.playInt(2,octave=True)
    def playInt2III(self):
        self.playInt(3,octave=True)
    def playInt2IV(self):
        self.playInt(4,octave=True)
    def playInt2V(self):
        self.playInt(5,octave=True)
    def playInt2VI(self):
        self.playInt(6,octave=True)
    def playInt2VII(self):
        self.playInt(7,octave=True)
    def playInt2VIII(self):
        self.playInt(8,octave=True)
    def I_f(self):
        """Whether or not to include this interval."""
        self.I = not self.I
        if self.I:
            self.intervals.append(1)
            self.I_B.config(relief='sunken')
        else:
            self.intervals.remove(1)
            self.I_B.config(relief='raised')

    def II_f(self):
        """Whether or not to include this interval."""
        self.II = not self.II
        if self.II:
            self.intervals.append(2)
            self.II_B.config(relief='sunken')
        else:
            self.intervals.remove(2)
            self.II_B.config(relief='raised')

    def III_f(self):
        """Whether or not to include this interval."""
        self.III = not self.III
        if self.III:
            self.intervals.append(3)
            self.III_B.config(relief='sunken')
        else:
            self.intervals.remove(3)
            self.III_B.config(relief='raised')

    def IV_f(self):
        """Whether or not to include this interval."""
        self.IV = not self.IV
        if self.IV:
            self.intervals.append(4)
            self.IV_B.config(relief='sunken')
        else:
            self.intervals.remove(4)
            self.IV_B.config(relief='raised')

    def V_f(self):
        """Whether or not to include this interval."""
        self.V = not self.V
        if self.V:
            self.intervals.append(5)
            self.V_B.config(relief='sunken')
        else:
            self.intervals.remove(5)
            self.V_B.config(relief='raised')

    def VI_f(self):
        """Whether or not to include this interval."""
        self.VI = not self.VI
        if self.VI:
            self.intervals.append(6)
            self.VI_B.config(relief='sunken')
        else:
            self.intervals.remove(6)
            self.VI_B.config(relief='raised')

    def VII_f(self):
        """Whether or not to include this interval."""
        self.VII = not self.VII
        if self.VII:
            self.intervals.append(7)
            self.VII_B.config(relief='sunken')
        else:
            self.intervals.remove(7)
            self.VII_B.config(relief='raised')

    def inv_f(self):
        """Whether or not to include inversions."""
        self.inversion = not self.inversion
        if self.inversion:
            self.inv_B.config(relief='sunken')
        else:
            self.inv_B.config(relief='raised')

    def oct_f(self):
        """Whether or not to include octave below."""
        self.oct = not self.oct
        if self.oct:
            self.oct_B.config(relief='sunken')
        else:
            self.oct_B.config(relief='raised')

    def on_closing(self):
        self.root.destroy()
