#When pressing button or choose the listbox, the label on top will change to the selection of listbox
import Tkinter as Tk
import UIComponents as ui
import LayoutGenerating as lg

class abc:
    def __init__(self, master):
        [frame1, frame2, frame3] = lg.XMLread(master, 'layout1.xml').get_widgets()
        self.label = ui.Label(frame1, text='LABEL PLACED HERE')
        self.listBox = ui.Listbox(frame2, ['Option 0', 'Option 1', 'Option 2'], label='Choose 1 of these', defaultvalue=1, command=self.change_label)
        button = ui.Button(frame3, text='PRESS BUTTON TO CHANGE LABEL', command=self.change_label)
        
    def change_label(self, *args):
        current_value = self.listBox.get_selection()
        self.label.change_text('You choose option '+ str(current_value))

root = Tk.Tk()
app= abc(root)
Tk.mainloop()
