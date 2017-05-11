import UIComponents as ui
import Tkinter as Tk
import os
import xml.etree.ElementTree as ET
import fnmatch
import sys
#print sys.path
#print os.getcwd()
import AddNewApp as AddNewApp

class MainProgram():    
    Structure = {}    
    def __init__(self, master):
        self.master = master
        xmlList = self.findAllXMLFiles()
        for xmlFile in xmlList:
            self.processXMLFile(xmlFile)
        
        self.courseListbox = ui.Listbox(master, self.findAllCourse(), command=self.selectCourse, height=5, width=30, label='COURSE LIST')
        self.topicListbox = ui.Listbox(master, [], command=self.selectTopic, height=5, width=30, label='TOPIC LIST')
        self.subTopicListbox = ui.Listbox(master, [], command=self.selectSubTopic, height=5, width=30, label='SUBTOPIC LIST')
        self.descriptionLabel = ui.Label(master, text='Description')
        self.startButton = ui.Button(master, text='START APP', command=self.startApp)
        self.addNewAppButton = ui.Button(master, text='ADD NEW APP', command=self.addNewApp)        
        
    def findAllXMLFiles(self):
        matches = []
        for root, dirnames, filenames in os.walk('.'):
            for filename in fnmatch.filter(filenames, '*.xml'):
                matches.append(os.path.join(root, filename))
        return matches
        
    def processXMLFile(self, xmlFile):
        try:
            tree = ET.parse(xmlFile)
            root = tree.getroot()
            if root.tag=='structure':
                course = root.find('course').text
                topic = root.find('topic').text
                subtopic = root.find('subtopic').text
                MainProgram.Structure[root] = subtopic
                MainProgram.Structure[subtopic] = topic
                MainProgram.Structure[topic] = course
                MainProgram.Structure[course] = 'course'
        except: pass
    
    def findAllCourse(self):
        courseList = []
        for item, parent in MainProgram.Structure.items():
            if parent == 'course':
                courseList.append(item)
        return courseList
        
    def selectCourse(self, *args):
        courseSelection = self.courseListbox.get_name_selection()
        topicList = []
        for item, parent in MainProgram.Structure.items():
            if parent == courseSelection:
                topicList.append(item)
        self.topicListbox.change_list(topicList)
        
    def selectTopic(self, *args):
        topicSelection = self.topicListbox.get_name_selection()
        subTopicList = []
        for item, parent in MainProgram.Structure.items():
            if parent == topicSelection:
                subTopicList.append(item)
        self.subTopicListbox.change_list(subTopicList)
        
    def selectSubTopic(self, *args):
        subTopicSelection = self.subTopicListbox.get_name_selection()
        for item, parent in MainProgram.Structure.items():
            if parent == subTopicSelection:            
                self.app = item
        self.descriptionLabel.change_text('DESCRIPTION: '+str(self.app.find('description').text))
        
    def startApp(self):
        try:
            sys.path.append(os.path.abspath(self.app.find('directory').text))
            exec('import '+self.app.find('appfile').text+ ' as NewApp')
            newWindow = Tk.Toplevel(self.master)
            exec('new = NewApp.'+ self.app.find('mainclass').text+ '(newWindow)')
        except: pass
    
    def addNewApp(self):
        newWindow = Tk.Toplevel(self.master)
        new = AddNewApp.AddNewApp(newWindow)
        
root=Tk.Tk()
mainapp = MainProgram(root)
Tk.mainloop()
