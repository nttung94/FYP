import Tkinter as tk
import UIComponents as ui
import LayoutGenerating as lg
import numpy

class DTC:
    def __init__(self, master):
        [frameX, frameH, frameFigure1, frameN, frameFigure2] = lg.XMLread(master, 'layout2.xml').get_widgets()
        self.widgetX = ui.DiscreteSignal(frameX, command=self.updateFigures, label='Get X[n]', defaultvalue=ui.DiscreteSignal.DEFAULT_VALUE)
        self.widgetH = ui.DiscreteSignal(frameH, command=self.updateFigures, label='Get H[n]', defaultvalue=ui.DiscreteSignal.DEFAULT_VALUE)
        self.figure1 = ui.Figure(frameFigure1, figsize=[5,2])
        self.widgetN = ui.EntryScale(frameN, command=self.updateFigures, text='n: ', defaultvalue=5)
        self.widgetFlip = ui.Radiobutton(frameN, ['Flip x[n]', 'Flip h[n]'], command=self.updateFigures, defaultvalue=1)
        self.figure2 = ui.Figure(frameFigure2, grid=[2,1], figsize=[5,5])

    def updateFigures(self, *args):        
        self.calculate()
        self.figure1.plot(self.xData_x_C, self.yData_x, 'update', plot_type='stem', color='b', markeredgecolor='b', baseline='g', markerfacecolor='w')
        self.figure1.plot(self.xData_h_C, self.yData_h, plot_type='stem', color='r', markeredgecolor='r', baseline='g', markerfacecolor='w')
        self.figure2.plot(self.t, self.convResult, 'update', id=2, plot_type='stem', title='Convolution Result', markerfacecolor='y', markeredgecolor='k', baseline='g')
        if len(self.yN>0):
            self.figure2.plot([self.n], self.yN, id=2, plot_type='stem', color='r' )  
        if len(self.xMultiplication>0):
            self.figure2.plot(self.xMultiplication, self.yMultiplication, plot_type='stem', title='Multiplication x[k]h[n-k]')
        
    def calculate(self):
        [xData_x, self.yData_x] = self.widgetX.get_xy()
        [xData_h, self.yData_h] = self.widgetH.get_xy()
        self.n = int(self.widgetN.get_input())
        if self.widgetFlip.get_selection()==1:
            self.xData_h_C = self.n - xData_h
            self.xData_x_C = xData_x
        else:
            self.xData_x_C = self.n - xData_x
            self.xData_h_C = xData_h
        minData = min(xData_x) + min(xData_h)
        maxData = max(xData_x) + max(xData_h)        
        self.t = numpy.arange(minData, maxData+1, 1)
        self.convResult = numpy.convolve(self.yData_x, self.yData_h)
        self.yN = self.convResult[numpy.where(self.t==self.n)]
        self.xMultiplication = numpy.intersect1d(self.xData_h_C, self.xData_x_C)
        self.yMultiplication = []
        for element in self.xMultiplication:
            z = self.yData_h[numpy.where(self.xData_h_C==element)]*self.yData_x[numpy.where(self.xData_x_C==element)]
            self.yMultiplication = numpy.append(self.yMultiplication, z)
        
root = tk.Tk()
app = DTC(root)
root.mainloop()