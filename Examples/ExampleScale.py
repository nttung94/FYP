#When pressing button or slide the slider or enter in the entry, the label on top will change to the selection of input
import Tkinter as Tk
import UIComponents as ui
import LayoutGenerating as lg

class abc:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.label = ui.Label(frame1, text='LABEL PLACED HERE')
        self.entryScale = ui.EntryScale(frame2, text='Enter n ', orient='horizontal', defaultvalue=0, from_=-10, to=10, command=self.change_label)
        button = ui.Button(frame3, text='PRESS BUTTON TO CHANGE LABEL', command=self.change_label)
        
    def change_label(self, *args):
        current_value = self.entryScale.get_input()
        self.label.change_text('The number is '+ str(current_value))

root = Tk.Tk()
app= abc(root)
Tk.mainloop()
