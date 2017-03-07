import Tkinter as tk
import UIComponents as ui
import numpy

class FourierSeriesAnimation:
    def __init__(self, master):
        self.nListEntry = ui.LabelEntry(master, text='n: ', defaultvalue=[1,3,5,7], command=self.startAnimation, labelwidth=15, entrywidth=30)
        self.aListEntry = ui.LabelEntry(master, text='Amplitude:', defaultvalue='[4.0/1, 4.0/3, 4.0/5, 4.0/7]', command=self.startAnimation, labelwidth=15, entrywidth=30)
        self.signalListbox = ui.Listbox(master, ['Square', 'Triangle', 'Sawtooth'], command=self.chooseListbox, defaultvalue=0)
        startButton = ui.Button(master, text='START', command=self.startAnimation)
        self.NameLabel = ui.Label(master)
        self.AnimationFigure = ui.Figure(master, figsize=[15,6])
        
    def startAnimation(self, *args):
        self.nList = eval(self.nListEntry.get())
        self.aList = eval(self.aListEntry.get())
        self.displaySignalText()
        [self.line1, self.line2, self.line3] = self.AnimationFigure.get_lines(3, 'update', 'keep_ratio')
        self.lineCircle = self.AnimationFigure.get_lines(len(self.nList))     
        self.initialization()
        self.AnimationFigure.startAnimation(self.update_data, self.thetaList, xlim=[-8, max(self.thetaList)], ylim=[-2,2])        
        
    def initialization(self):
        self.thetaList = numpy.arange(0, 3/min(self.nList)*numpy.pi,0.05)
        self.xLine1 = self.yLine1 = []
        self.xLine3 = self.yLine3 = []

    def update_data(self, theta):
        currentPoint = [-4,0]
        for i in range(len(self.nList)):
            currentPoint = self.drawCircle(self.lineCircle[i], currentPoint, i, theta)
        self.drawLine1(currentPoint, theta)    
        self.drawLine2(currentPoint, theta)
        self.drawLine3(currentPoint)
                
    def drawCircle(self, line, center, circle_id, theta):
        x = [center[0]]
        y = [center[1]]
        angleList = numpy.arange(theta, theta+2*numpy.pi + numpy.pi/18, numpy.pi/18)
        for angle in angleList:
            x = x + [center[0] + self.aList[circle_id] * numpy.cos(self.nList[circle_id]*angle)/numpy.pi]
            y = y + [center[1] + self.aList[circle_id] * numpy.sin(self.nList[circle_id]*angle)/numpy.pi]
        line.set_data(x,y)
        return [x[1], y[1]]
    
    def drawLine1(self, currentPoint, theta):
        self.xLine1 = self.xLine1 + [theta]
        self.yLine1 = [currentPoint[1]] + self.yLine1
        self.line1.set_data(self.xLine1, self.yLine1)
        
    def drawLine2(self, currentPoint, theta):
        x = [currentPoint[0], 0]
        y = [currentPoint[1], currentPoint[1]]
        self.line2.set_data(x, y)
        
    def drawLine3(self, currentPoint):
        self.xLine3 = self.xLine3 + [currentPoint[0]]
        self.yLine3 = self.yLine3 + [currentPoint[1]]
        self.line3.set_data(self.xLine3, self.yLine3)
        
    def displaySignalText(self):
        theta = u"\u03B8"
        pi = u"\u03C0"
        text = ""
        for i in range(len(self.nList)):
            text = text+ " + " +str(self.aList[i])+ "*sin(" +str(self.nList[i])+theta+ ")/"+pi
        self.NameLabel.change_text(text)  
        
    def chooseListbox(self, event):
        if (self.signalListbox.get_selection()==0):
            self.nListEntry.change_value([1,3,5,7])
            self.aListEntry.change_value('[4.0/1, 4.0/3, 4.0/5, 4.0/7]')
        if (self.signalListbox.get_selection()==1):
            self.nListEntry.change_value([1,3,5,7])
            self.aListEntry.change_value([2.545, -0.283, 0.102, -0.052])
        if (self.signalListbox.get_selection()==2):
            self.nListEntry.change_value([1,2,3,4,5])
            self.aListEntry.change_value('[2.0/1, 2.0/2, 2.0/3, 2.0/4, 2.0/5]')
        self.startAnimation()
        
        
root = tk.Tk()
app = FourierSeriesAnimation(root)
root.mainloop()