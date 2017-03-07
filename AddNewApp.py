import UIComponents as ui
import Tkinter as Tk
import tkFileDialog
import os
import xml.etree.cElementTree as ET
import tkMessageBox

class AddNewApp:
    def __init__(self, master):
        self.master = master
        self.courseEntry = ui.LabelEntry(master, text='Course: ', labelwidth=20, entrywidth=40)
        self.topicEntry = ui.LabelEntry(master, text='Topic: ' , labelwidth=20, entrywidth=40)
        self.subTopicEntry = ui.LabelEntry(master, text='SubTopic: ' , labelwidth=20, entrywidth=40)
        self.descriptionEntry = ui.LabelEntry(master, text='Description: ', labelwidth=20, entrywidth=40)
        self.browseButton = ui.Button(master, text='Choose file...', command=self.openfile)
        self.fileLabel = ui.Label(master)
        self.mainClassEntry = ui.LabelEntry(master, text='Main Class Name:' , labelwidth=20, entrywidth=40) 
        self.addAppButton = ui.Button(master, text='ADD', command=self.addApp)       
        
    def openfile(self):
        self.file = tkFileDialog.askopenfile(parent= self.master ,mode='rb',title='Choose a Python file')
        self.fileLabel.change_text(self.file.name)
        
    def addApp(self):
        try:
            appfile = os.path.split(self.file.name)[1][0:-3]
            directory = str(os.path.split(self.file.name)[0]).split('/')
            cwd = os.getcwd().split('\\')
            relativeDirectory = directory[len(cwd):]
            string = '.\\' + '\\'.join(relativeDirectory)
            root = ET.Element("structure")
            ET.SubElement(root, "course").text = self.courseEntry.get()
            ET.SubElement(root, 'topic').text = self.topicEntry.get()
            ET.SubElement(root, 'subtopic').text = self.subTopicEntry.get()
            ET.SubElement(root, "appfile").text = appfile
            ET.SubElement(root, "directory").text =string
            ET.SubElement(root, "description").text =self.descriptionEntry.get()
            tree = ET.ElementTree(root)
            tree.write(string + "\\ "+ appfile+".xml")
            tkMessageBox.showinfo("Add New App", "Adding Successfully")
        except: pass
            
#root=Tk.Tk()
#app = AddNewApp(root)
#root.mainloop()