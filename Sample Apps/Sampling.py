import Tkinter as tk
import UIComponents as ui
import numpy
import LayoutGenerating as lg

class Sampling:
    def __init__(self, master):
        [frame1, frame2, frame3, frame4] = lg.XMLread(master, 'layout4.xml').get_widgets()
        WaveFigure = ui.Figure(frame3, figsize=[8,3])
        self.SignalFrame = ui.Waveform(frame1, WaveFigure, command=self.startSampling, label='Waveform Parameters', defaultvalue=ui.Waveform.DEFAULT_VALUE)
        self.FsInput = ui.LabelEntry(frame2, command=self.startSampling, text='Sampling Frequency: ', defaultvalue=16)
        self.AnimateButton = ui.Button(frame2, text='ANIMATION', command=self.startAnimation)
        self.SamplingFigure = ui.Figure(frame4, figsize=[8,3])        
        
    def startSampling(self, *args):
        self.fs = float(self.FsInput.get())
        [self.x, self.y] = self.SignalFrame.calculate_signal()
        [self.n, self.v] = self.SignalFrame.calculate_signal(sampling_rate=self.fs)
        self.SamplingFigure.plot(range(len(self.n)), self.v, 'update', plot_type='stem')

    def startAnimation(self):
        [self.line1] = self.SamplingFigure.get_lines(1, 'update')
        [self.line2] = self.SamplingFigure.get_lines(1, 'stem')
        self.SamplingFigure.startAnimation(self.animate, range(len(self.x)), interval=1, xlim=[0,len(self.n)-1], ylim=[min(self.y), max(self.y)])
        
    def animate(self, i):
        self.line1.set_data(numpy.array(self.x[0:i])*self.fs, self.y[0:i])
        t = int(float(i)/len(self.x)*(len(self.n)-1))+1
        self.line2.set_data(range(t), self.v[0:t])
        
#root=tk.Tk()
#app=Sampling(root)
#tk.mainloop()