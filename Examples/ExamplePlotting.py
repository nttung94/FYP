#When press the buttons, the plot will change to the x and y coordinates.
#Note that in the plot_line way, the view xlim and ylim will not be automatically adjusted
import Tkinter as Tk
import UIComponents as ui
import LayoutGenerating as lg

class abc:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.entryX = ui.LabelEntry(frame1, text='X coordinate', side='left', defaultvalue=[1,2,3], command=self.change_plot)
        self.entryY = ui.LabelEntry(frame1, text='Y coordinate', side='left', defaultvalue=[1,2,3], command=self.change_plot)
        self.figure = ui.Figure(frame2, figsize=(5,4))
        self.line = self.figure.plot([1,2,3],[1,3,2])
        button = ui.Button(frame3, side='left', text='PRESS BUTTON TO CHANGE PLOT', command=self.change_plot)
        button = ui.Button(frame3, side='left', text='ANOTHER WAY TO CHANGE PLOT', command=self.change_another_way)
        
    def change_plot(self, *args):
        x = eval(self.entryX.get())
        y = eval(self.entryY.get())
        self.figure.plot(x,y,'update')
        
    def change_another_way(self, *args):
        x = eval(self.entryX.get())
        y = eval(self.entryY.get())
        self.figure.plot_line(x,y, self.line)

root = Tk.Tk()
app= abc(root)
Tk.mainloop()
