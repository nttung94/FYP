import Tkinter as tk
import UIComponents as ui
import LayoutGenerating as lg
import scipy

class CTFT:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout3.xml').get_widgets()
        waveformFigure = ui.Figure(frame2, figsize=[8,3])        
        self.waveInputFrame = ui.Waveform(frame1, waveformFigure, sampling=1000, command=self.startCTFT, label='Waveform Parameters', defaultvalue=ui.Waveform.DEFAULT_VALUE)        
        self.CTFTFigure = ui.Figure(frame3, figsize=[8,3])
        self.xlim = ui.LabelEntry(frame3, text='xlim',defaultvalue=[-500,500], command=self.startCTFT)
        
    def startCTFT(self, *args):
        xlim = eval(self.xlim.get())
        [t,f] = self.waveInputFrame.calculate_signal()
        X = scipy.fftpack.fft(f)
        freqs = scipy.fftpack.fftfreq(len(t)) /(t[1]-t[0])        
        self.CTFTFigure.plot(freqs, X, 'update', xlim=xlim)

root = tk.Tk()
app = CTFT(root)
root.mainloop()