#When pressing button or pressing Enter key in entry field, the label on top will change to text in the entry field
import Tkinter as Tk
import UIComponents as ui
import LayoutGenerating as lg

class abc:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.label = ui.Label(frame1, text='LABEL PLACED HERE')
        self.entry = ui.LabelEntry(frame2, text='Enter something here', defaultvalue='blahblah', command=self.change_label)
        button = ui.Button(frame3, text='PRESS BUTTON TO CHANGE LABEL', command=self.change_label)
        
    def change_label(self, *args):
        current_text = self.entry.get()
        self.label.change_text(current_text)

root = Tk.Tk()
app= abc(root)
Tk.mainloop()
