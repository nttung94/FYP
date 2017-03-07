import Tkinter as tk
import UIComponents as ui
import LayoutGenerating as lg
import numpy

Xdefault = [1, 2, 4, 1, 2, 1, 2, 2, 3, 2, 3]

class DFT:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.figureX = ui.Figure(frame1, figsize=[8,3])
        self.inputFrame = ui.LabelEntry(frame2, text='Sequence X:', defaultvalue = Xdefault, command=self.updateFigures, entrywidth=30)
        self.figureResult = ui.Figure(frame3, grid=[1,2], figsize=[8,3])        

        
    def updateFigures(self, event):
        sequenceX = eval(self.inputFrame.get())
        [t, result] = self.calculate(sequenceX)
        self.figureX.plot(t, sequenceX, 'update', plot_type='stem')
        self.figureResult.plot(t, numpy.abs(result), 'update', id=1, ylabel='Amplitude', plot_type='stem')
        self.figureResult.plot(t, numpy.angle(result), id=2, ylabel='Angle', plot_type='stem')

    def calculate(self, sequenceX):
        t = numpy.arange(0, len(sequenceX), 1)
        result = numpy.fft.fft(sequenceX)
        return [t, result]
        
root = tk.Tk()
app = DFT(root)
root.mainloop()