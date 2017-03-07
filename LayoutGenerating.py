import xml.etree.ElementTree as ET
import Tkinter
import collections

class XMLread:
    def __init__(self, root, xml_file):
        header = ET.parse(xml_file).getroot()
        self.widget_list = collections.OrderedDict()
        self.scan(root, header)
    
    def scan(self, master, element):
        options = element.attrib
        try:
            side = options.pop('side')
        except:
            side = 'top'
        
        widget_factory = getattr(Tkinter, element.tag.capitalize())
        widget = widget_factory(master, **options)
        widget.pack(side=side)
        if 'name' in options:
            name = options['name']
            self.widget_list[name] = widget
        
        for subelement in element:
            self.scan(widget, subelement)
            
    def get_widget_list(self):
        return self.widget_list
        
    def get_widgets(self):
        return self.widget_list.values()