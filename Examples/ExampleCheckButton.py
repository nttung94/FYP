#When pressing button or change the checkbuttons, the label on top will change list of status of checkbutton
import Tkinter as Tk
import UIComponents as ui
import LayoutGenerating as lg

class abc:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.label = ui.Label(frame1, text='LABEL PLACED HERE')
        self.checkButton = ui.Checkbutton(frame2, ['Option 1', 'Option 2'], orient='vertical', defaultvalue=[0,1], command=self.change_label)
        button = ui.Button(frame3, text='PRESS BUTTON TO CHANGE LABEL', command=self.change_label)
        
    def change_label(self, *args):
#        Note that current value is a list type
        current_value = self.checkButton.get_value()
        self.label.change_text(current_value)

root = Tk.Tk()
app= abc(root)
Tk.mainloop()
