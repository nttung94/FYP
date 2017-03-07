import Tkinter as tk
import UIComponents as ui
import numpy
import scipy.signal as signal

class ZeroPoleDragging:
    def __init__(self, master):
        self.positionLabel = ui.Label(master)
        self.ZPFigure = ui.Figure(master, figsize=[4,4], side='left')
        self.FrequencyResponseFigure = ui.Figure(master, figsize=[8,4], side='right')
        ui.Button(master, text='ADD ZERO', command = self.addZero)
        ui.Button(master, text='REMOVE ZERO', command = self.removeZero)
        ui.Button(master, text='ADD POLE', command = self.addPole)
        ui.Button(master, text='REMOVE POLE', command = self.removePole,)
        [self.line1, self.line2] = self.FrequencyResponseFigure.get_lines(2)
        self.zeroList = [0.3+ 0.4j, 0.3- 0.4j]
        self.poleList = [0.6+ 0.7j, 0.6- 0.7j]
        self.drawZeroPoleFigure()
        
    def drawZeroPoleFigure(self):
        self.ZPFigure.reset()
        self.zeroPoints = []
        self.polePoints = []
        for zero in self.zeroList:
            self.zeroPoints.append(ui.DraggablePoint(self.ZPFigure,(numpy.real(zero),numpy.imag(zero)),command=self.updateDragging, shape='circle', radius=0.11))
        for pole in self.poleList:
            self.polePoints.append(ui.DraggablePoint(self.ZPFigure,(numpy.real(pole),numpy.imag(pole)), command=self.updateDragging, shape='rectangle', width=0.1, height=0.1))
        t = numpy.linspace(0, 2*numpy.pi, 100)
        self.ZPFigure.plot(numpy.sin(t), numpy.cos(t))
        
    def updateDragging(self, draggingPoint):
        self.moveSymmetricPoint(draggingPoint)
        self.positionLabel.change_text('Selected Position: '+str(draggingPoint.get_center()))
        self.drawFrequencyResponse()
        
    def moveSymmetricPoint(self, draggingPoint):
        (x, y) = draggingPoint.get_center()
        if draggingPoint in self.zeroPoints:
            index = (self.zeroPoints).index(draggingPoint)
            symmetricIndex = self.findSymmetricIndex(index)
            self.zeroPoints[symmetricIndex].set_center(x, -y)
            self.zeroList[index] = x+y*1j
            self.zeroList[symmetricIndex] = x-y*1j
        if draggingPoint in self.polePoints:
            index = (self.polePoints).index(draggingPoint)
            symmetricIndex = self.findSymmetricIndex(index)
            self.polePoints[symmetricIndex].set_center(x, -y)
            self.poleList[index] = x+y*1j
            self.poleList[symmetricIndex] = x-y*1j
            
    def drawFrequencyResponse(self):
        num, den = signal.zpk2tf(self.zeroList, self.poleList, 1)
        w, h = signal.freqz(num, den)
        angles = numpy.unwrap(numpy.angle(h))
        self.FrequencyResponseFigure.plot_line(w, 20*numpy.log10(abs(h)), self.line1, ylim=[-20,40],  title='FREQUENCY RESPONSE', xlabel='Frequency (rad/sample)', ylabel='Amplitude (dB)')
        self.FrequencyResponseFigure.plot_line(w, angles, self.line2, ylim=[-20,40],  title='FREQUENCY RESPONSE', xlabel='Frequency (rad/sample)', ylabel='Amplitude (dB)')
        
    def findSymmetricIndex(self, index):
        if index%2 ==0:
            return index+1
        else:
            return index-1
            
    def addZero(self):
        self.zeroList += [0.5, 0.5]
        self.drawZeroPoleFigure()
        
    def removeZero(self):
        self.zeroList.pop()
        self.zeroList.pop()
        self.drawZeroPoleFigure()
        
    def addPole(self):
        self.poleList += [0.5, 0.5]
        self.drawZeroPoleFigure()
        
    def removePole(self):
        self.poleList.pop()
        self.poleList.pop()
        self.drawZeroPoleFigure()
root=tk.Tk()
app=ZeroPoleDragging(root)
tk.mainloop()