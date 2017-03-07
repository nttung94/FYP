import Tkinter as Tk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.figure as fg
import matplotlib.backends.backend_tkagg as tkagg
import numpy
import matplotlib.pyplot as plt
import scipy.signal as sgl
import matplotlib.patches as patches

class Label:
    def __init__(self, frame, **kwargs):
        KEY_TEXT = 'text'
        KEY_SIDE = 'side'
        
        self.__label = Tk.Label(frame)
        try:    self.__label.config(text=kwargs[KEY_TEXT])
        except: pass
        try:    self.__label.pack(side=kwargs[KEY_SIDE])
        except: self.__label.pack()
                      
    def change_text(self, text):
        self.__label.config(text=text)
        
    def get_label(self):
        return self.__label
        
class LabelEntry:
    def __init__(self, frame, **kwargs):
        
        KEY_TEXT = 'text'
        KEY_ORIENT = 'orient'        
        KEY_LABELWIDTH = 'labelwidth'
        KEY_ENTRYWIDTH = 'entrywidth'
        KEY_COMMAND = 'command'
        KEY_DEFAULTVALUE = 'defaultvalue'
        KEY_SIDE = 'side'
        
        try:    orient = kwargs[KEY_ORIENT]
        except: orient = 'horizontal'
        if orient=='horizontal':
            self.__packSide = Tk.LEFT 
        else:
            self.__packSide = Tk.TOP
        
        self.mainFrame = Tk.Frame(frame)
        try:    self.mainFrame.pack(kwargs[KEY_SIDE])
        except: self.mainFrame.pack()
        
        self.__label = Tk.Label(self.mainFrame)
        self.__label.pack(side=self.__packSide)
        try:    self.__label.config(text=kwargs[KEY_TEXT])
        except: pass
        try:    self.__label.config(width=kwargs[KEY_LABELWIDTH])
        except: pass
        
        self.__entry = Tk.Entry(self.mainFrame)
        self.__entry.pack(side=self.__packSide)
        try:    self.__entry.config(width=kwargs[KEY_ENTRYWIDTH])
        except: pass
        try:    self.__entry.bind('<Return>', kwargs[KEY_COMMAND])
        except: pass
        try:    self.__entry.insert(0, kwargs[KEY_DEFAULTVALUE])
        except: pass
        
        
    #Get value of the entry
    def get(self):
        return self.__entry.get()
    
    #clear value of the entry
    def clear(self):
        self.__entry.delete(0, Tk.END)
        
    def change_label(self, text):
        self.__label.config(text=text)
        
    def change_value(self, value):
        self.__entry.delete(0, Tk.END)
        self.__entry.insert(0, value)
        
    def set_invisible(self):
        self.__label.pack_forget()
        self.__entry.pack_forget()
        self.mainFrame.pack_forget()
    
    def set_visible(self):
        self.__label.pack(side=self.__packSide)
        self.__entry.pack(side=self.__packSide)
        self.mainFrame.pack()
                
    def get_label(self):
        return self.__label
        
    def get_entry(self):
        return self.__entry

class Button:
    def __init__(self, frame, **kwargs):
        KEY_TEXT = 'text'
        KEY_COMMAND = 'command'            
        KEY_SIDE = 'side'
        
        self.__button = Tk.Button(frame)
        try:    self.__button.config(text=kwargs[KEY_TEXT])
        except: pass
        try:    self.__button.config(command=kwargs[KEY_COMMAND])
        except: pass
        try:    self.__button.pack(side=kwargs[KEY_SIDE])
        except: self.__button.pack()
                      
    def get_button(self):
        return self.__button
        
class Checkbutton:
    def __init__(self, frame, list, **kwargs):
        side=Tk.TOP
        if 'side' in kwargs:
            side = kwargs['side']
        mainFrame = Tk.Frame(frame)
        mainFrame.pack(side=side)        
        orient = 'horizontal'
        if 'orient' in kwargs:
            orient = kwargs['orient']
        packSide = Tk.TOP
        if orient == 'horizontal':
            packSide= Tk.LEFT
        command = None
        if 'command' in kwargs:
            command = kwargs['command']
        n= len(list)
        defaultValue=[]
        for i in range(n):
            defaultValue.append(0)
        if 'defaultvalue' in kwargs:
            defaultValue = kwargs['defaultvalue']
        self.CheckVar=[]
        for value in defaultValue:
            var = Tk.IntVar()
            var.set(value)
            self.CheckVar.append(var)
        self.checkButtonList =[]
        for i in range(n):
            cb = Tk.Checkbutton(mainFrame, text=list[i], variable=self.CheckVar[i], onvalue=1, offvalue=0, command=command)
            cb.pack(side=packSide)
            self.checkButtonList.append(cb)
            
    def get_value(self):
        value = []
        for element in self.CheckVar:
            value.append(element.get())
        return value
        
    def config_checkbutton(self, id, **kwargs):
        self.checkButtonList[id].config(**kwargs)
        
    def get_checkbutton(self, id):
        return self.checkButtonList[id]
        
class Entry:
    def __init__(self, frame, **kwargs):
        KEY_SIDE = 'side'  
        KEY_COMMAND = 'command'
        KEY_DEFAULTVALUE = 'defaultvalue'
        try:    command = kwargs.pop(KEY_COMMAND)
        except: command = None
        try:    side = kwargs.pop(KEY_SIDE)
        except: side = Tk.TOP
        try:    defaultValue = kwargs.pop(KEY_DEFAULTVALUE)
        except: defaultValue = None

        mainFrame = Tk.Frame(frame)
        mainFrame.pack(side=side)
        self.entry = Tk.Entry(mainFrame, **kwargs)
        self.entry.insert(0, defaultValue)
        self.entry.bind('<Return>', command)
        self.entry.pack()
        
    def get(self):
        return self.entry.get()
        
    def clear(self):
        self.entry.delete(0, Tk.END)
        
    def change_value(self, text):
        self.clear()
        self.insert(0, text)
        
    def config_entry(self, **kwargs):
        self.entry.config(**kwargs)
        
    def get_entry(self):
        return self.entry
        
class Listbox:
    def __init__(self, frame, list, width=20, **kwargs):
        command = None
        if 'command' in kwargs:
            command = kwargs['command']
     
        defaultValue =None
        if 'defaultvalue' in kwargs:
            defaultValue = kwargs['defaultvalue']
        
        height= len(list)
        if 'height' in kwargs:
            height = kwargs['height']
        yscrollcommand = None
        if height<len(list):
            scrollbar = Tk.Scrollbar(frame)
            scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
            yscrollcommand = scrollbar.set
        
        self.__selectmode = 'browse'
        if 'selectmode' in kwargs:
            self.__selectmode = kwargs['selectmode']
        if self.__selectmode == 'browse':
            select_config = Tk.BROWSE
        else:
            select_config = Tk.MULTIPLE
        if 'label' in kwargs:
            labelframe = Tk.LabelFrame(frame, text=kwargs['label'])
            labelframe.pack()
            self.listbox = Tk.Listbox(labelframe, exportselection=False,width=width, height=height, selectmode=select_config, yscrollcommand=yscrollcommand)
        else:
            self.listbox = Tk.Listbox(frame, exportselection=False, height=height, selectmode=select_config, yscrollcommand=yscrollcommand)
        try:
            scrollbar.config(command = self.listbox.yview)
        except:
            pass
        for element in list:
            self.listbox.insert(Tk.END, element)
        self.listbox.bind('<<ListboxSelect>>', command)
        if defaultValue!=None:        
            try:
                self.listbox.select_set(defaultValue)
            except:
                for value in defaultValue:
                    self.listbox.select_set(value)
        self.listbox.pack()
        
    def get_selection(self):
        try:
            if self.__selectmode=='browse':
                return self.listbox.curselection()[0]
            else:
                return self.listbox.curselection()
        except:
            return None
            
    def config_listbox(self, **kwargs):
        self.listbox.config(**kwargs)
        
    def get_listbox(self):
        return self.listbox
        
    def change_list(self, newList):
        self.listbox.delete(0, Tk.END)
        for element in newList:
            self.listbox.insert(Tk.END, element)
            
    def get_name_selection(self):
        select = self.listbox.curselection()[0]
        return self.listbox.get(select)
            
class Radiobutton:
    def __init__(self, frame, list, **kwargs):
        self.mainFrame=Tk.Frame(frame)
        self.mainFrame.pack()
        orient = 'horizontal'
        if 'orient' in kwargs:
            orient = kwargs['orient']
        self.packSide = Tk.TOP
        if orient == 'horizontal':
            self.packSide= Tk.LEFT
        command = None
        if 'command' in kwargs:
            command = kwargs['command']
        n= len(list)
        
        defaultValue=None
        if 'defaultvalue' in kwargs:
            defaultValue = kwargs['defaultvalue']
        self.__radioVar = Tk.IntVar()
        if defaultValue!=None:
            self.__radioVar.set(defaultValue)
        self.radioButtonList =[]
        for i in range(n):
            rb = Tk.Radiobutton(self.mainFrame, text=list[i], variable=self.__radioVar, value=i, command=command)
            rb.pack(side=self.packSide)
            self.radioButtonList.append(rb)
            
    def get_selection(self):
        return self.__radioVar.get()
        
    def config_radiobutton(self, id, **kwargs):
        self.radioButtonList[id].config(**kwargs)
        
    def get_radiobutton(self, id):
        return self.radioButtonList[id]
        
    def set_visible(self):
        self.mainFrame.pack()
        for rb in self.radioButtonList:
            rb.pack(side=self.packSide)
            
    def set_invisible(self):
        self.mainFrame.pack_forget()
        for rb in self.radioButtonList:
            rb.pack_forget()
        
class Figure:
    def __init__(self, frame, side='top', **kwargs):
        try:
            self.figsize = kwargs['figsize']
        except:
            self.figsize = None
        try:
            self.dpi = kwargs['dpi']
        except:
            self.dpi = None
        self.__frame = Tk.Frame(frame)
        self.__frame.pack(side=side)
        self.__figure = fg.Figure(figsize=self.figsize, dpi=self.dpi, facecolor='w')
        self.__canvas = tkagg.FigureCanvasTkAgg(self.__figure, self.__frame)
        self.__grid=[1,1]
        if 'grid' in kwargs:
             self.__grid = kwargs['grid']
        else:
            self.axAni = self.__figure.add_subplot(111)
        self.__canvas.show()
        self.__canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1)
        self.__canvas._tkcanvas.pack(fill=Tk.BOTH, expand=1)
        
    def plot(self, x, y, *args, **kwargs):
        if 'update' in args:
            self.reset()
#            try:
#                self.__canvas.get_tk_widget().destroy()
#                self.__figure = fg.Figure(figsize=self.figsize, dpi=self.dpi, facecolor='w')
#            except:
#                pass
        id=1
        if 'id' in kwargs:
            id = kwargs['id']
            ax = self.__figure.add_subplot(self.__grid[0], self.__grid[1], id)
        else:
            ax = self.axAni
        try:
            xlim = kwargs['xlim']
            ax.set_xlim(xlim[0], xlim[1])
        except:
            pass
        try:
            ylim = kwargs['ylim']
            ax.set_ylim(ylim[0], ylim[1])
        except:
            pass
        if 'title' in kwargs:
            ax.set_title(kwargs['title'])
        if 'xlabel' in kwargs:
            ax.set_xlabel(kwargs['xlabel'])
        if 'ylabel' in kwargs:
            ax.set_ylabel(kwargs['ylabel'])
        if 'color' in kwargs:
            color = kwargs['color']
        else:
            color = 'b'
        try:
            if kwargs['plot_type']=='stem':
                markerline, stemlines, baseline = ax.stem(x,y, color)
            if kwargs['plot_type']=='scatter':
                markerline, stemlines, baseline = ax.scatter(x,y, color)
        except:
            markerline, = ax.plot(x,y, color)
        
        if 'markeredgecolor' in kwargs:
            plt.setp(markerline, 'markeredgecolor', kwargs['markeredgecolor'])
        if 'markerfacecolor' in kwargs:
            plt.setp(markerline, 'markerfacecolor', kwargs['markerfacecolor'])
        if 'baseline' in kwargs:
            plt.setp(baseline, 'color', kwargs['baseline'])
        if 'stemline' in kwargs:
            plt.setp(stemlines, 'color', kwargs['stemlines'])
#        if 'update' in args:
#            self.__canvas = tkagg.FigureCanvasTkAgg(self.__figure, self.__frame)
#            self.__canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1)
#            self.__canvas._tkcanvas.pack(fill=Tk.BOTH, expand=1)
        self.__canvas.show()
        return markerline
   
    def get_lines(self, number, *args):
        lines = []
        if 'update' in args:
            if 'keep_ratio' in args:
                self.reset('keep_ratio')
            else:
                self.reset()
#        self.axAni = self.__figure.add_subplot(111)
#        self.axAni = self.__figure.add_subplot(1,1,1, adjustable='box', aspect=1)
        for i in range (number):
            if 'stem' in args:
                line, stemline, baseline =self.axAni.stem([0],[0])
                plt.setp(stemline, 'color', 'b')
                plt.setp(baseline, 'color', 'r')
            else:
                line, = self.axAni.plot([],[])
            lines.append(line)
        return lines
                 
    def startAnimation(self, callback, iterable, interval=10, xlim=[None, None], ylim=[None, None]):
        for i in iterable:
            self.__frame.after(interval, callback(i))
#            self.axAni.set_aspect('auto')
            self.axAni.relim()
            self.axAni.autoscale_view(True,True,True)
            self.axAni.set_xlim(xlim)
            self.axAni.set_ylim(ylim)
            self.__canvas.show()
    
    def get_canvas(self):
        return self.__canvas
        
    def get_ax(self):
        return self.axAni
        
    def plot_line(self, x, y, line, xlim=[None, None], ylim=[None, None], title="", xlabel="", ylabel=""):
        line.set_data(x,y)
        self.axAni.relim()
        self.axAni.autoscale_view(True,True,True)
        self.axAni.set_xlim(xlim)
        self.axAni.set_ylim(ylim)
        self.axAni.set_title(title)
        self.axAni.set_xlabel(xlabel)
        self.axAni.set_ylabel(ylabel)
        self.__canvas.show()
        
    def reset(self, *args):
        try:
            self.__canvas.get_tk_widget().destroy()
            self.__figure = fg.Figure(figsize=self.figsize, dpi=self.dpi, facecolor='w')
            self.__canvas = tkagg.FigureCanvasTkAgg(self.__figure, self.__frame)
            self.__canvas.get_tk_widget().pack(fill=Tk.BOTH, expand=1)
            if 'keep_ratio' in args:
                self.axAni = self.__figure.add_subplot(1,1,1, adjustable='box', aspect=1)
            else:
                self.axAni = self.__figure.add_subplot(111)
        except:
            pass
            
class EntryScale:
    def __init__(self, frame, **kwargs):
        mainFrame = Tk.Frame(frame)
        mainFrame.pack()
        try:
            text = kwargs['text']
        except:
            text = None
        try:
            defaultValue = kwargs['defaultvalue']
        except:
            defaultValue = 0
        try:
            from_ = kwargs['from']
            to = kwargs['to']
        except:
            from_ = -50
            to = 50
        try:
            orient = kwargs['orient']
        except:
            orient = 'horizontal'
        try:
            self.command = kwargs['command']
        except:
            self.command = None
        self.__entry = LabelEntry(mainFrame, text=text, defaultvalue=defaultValue, command=self.updateEntry)
        self.__scale = Tk.Scale(mainFrame, from_=from_, to=to, orient=orient)
        self.__scale.bind("<ButtonRelease-1>", self.updateScale)
        self.__scale.set(defaultValue)
        self.__scale.pack()
        
    def updateEntry(self, event):
        self.input = self.__entry.get()
        self.__scale.set(self.input)
        self.command()
        
    def updateScale(self, event):
        self.input = self.__scale.get()
        self.__entry.change_value(self.input)
        self.command()
        
    def get_input(self):
        return self.input
            
class DiscreteSignal:
    DEFAULT_VALUE = {'default_signal':0, 'length':10, 'delay':0, 'amplitude':1, 'period':10, 'phase':0, 'scaling_factor':1, 'exp_const': 0.5, 'causality':0, 'user_signal':[1,1,1,1]}
    def __init__(self, frame, **kwargs):
        if 'defaultvalue' in kwargs:
            defaultValue = kwargs['defaultvalue']
        else:
            defaultValue = {'default_signal':None, 'length':None, 'delay':None, 'amplitude':None, 'period':None, 'phase':None, 'scaling_factor':None, 'exp_const':None, 'causality':None, 'user_signal':None}
        signal_list = ['Sine', 'Exponential', 'Pulse', 'Unit Sample', 'User Signal']
        if 'command' in kwargs:
            self.__command = kwargs['command']
        else:
            self.__command = None
        if 'label' in kwargs:
            mainFrame = Tk.LabelFrame(frame, text=kwargs['label'])
            mainFrame.pack()
        else:
            mainFrame = Tk.Frame(frame)
            mainFrame.pack()
        self.__figure = Figure(mainFrame, figsize=[4,3])
        self.__listbox = Listbox(mainFrame, label='Signal', list=signal_list, defaultvalue=defaultValue['default_signal'], command=self.selectListbox)
        self.__amplitude = LabelEntry(mainFrame, text="Amplitude:", defaultvalue=defaultValue['amplitude'], command=self.updateFigure, labelwidth=25)
        self.__period = LabelEntry(mainFrame, text="Period:", defaultvalue=defaultValue['period'], command=self.updateFigure, labelwidth=25)
        self.__phase = LabelEntry(mainFrame, text="Phase:", defaultvalue=defaultValue['phase'], command=self.updateFigure, labelwidth=25)
        self.__length = LabelEntry(mainFrame, text="Length:", defaultvalue=defaultValue['length'], command=self.updateFigure, labelwidth=25)
        self.__delay = LabelEntry(mainFrame, text="Delay:", defaultvalue=defaultValue['delay'], command=self.updateFigure, labelwidth=25)
        self.__scaling_factor = LabelEntry(mainFrame, text="ScalingFactor:", defaultvalue=defaultValue['scaling_factor'], command=self.updateFigure, labelwidth=25)
        self.__exp_const = LabelEntry(mainFrame, text="Exponential Constant:", defaultvalue=defaultValue['exp_const'], command=self.updateFigure, labelwidth=25)
        self.__user_signal = LabelEntry(mainFrame, text="User Signal", defaultvalue=defaultValue['user_signal'], command=self.updateFigure, labelwidth=25)        
        self.__causality = Radiobutton(mainFrame, ['Causal', 'Anti-causal'], defaultvalue=defaultValue['causality'], command=self.updateFigure)
        
        if defaultValue['default_signal']!=None:
            self.selectListbox(None)
        
    def updateFigure(self, *args):
        self.calculating_xy()
        self.__figure.plot(self.__x, self.__y, 'update', plot_type='stem')
        self.__command()
        
    def selectListbox(self, event):
        signalIndex = self.__listbox.get_selection()
        if (signalIndex==1 or signalIndex==4):
            self.__amplitude.set_invisible()
        else:
            self.__amplitude.set_visible()
        if signalIndex==0:
            self.__period.set_visible()
            self.__phase.set_visible()
        else:
            self.__period.set_invisible()  
            self.__phase.set_invisible()
        if (signalIndex==3 or signalIndex==4):
            self.__length.set_invisible()
        else:
            self.__length.set_visible()
        if signalIndex==4:
            self.__user_signal.set_visible()
        else:
            self.__user_signal.set_invisible()
        if (signalIndex==1):
            self.__scaling_factor.set_visible()
            self.__exp_const.set_visible()
            self.__causality.set_visible()
        else:
            self.__scaling_factor.set_invisible()
            self.__exp_const.set_invisible()
            self.__causality.set_invisible()
        try:    
            self.updateFigure()
        except:
            pass
        
    def calculating_xy(self):
        signalIndex = self.__listbox.get_selection()
        amplitude = float(self.__amplitude.get())
        period = float(self.__period.get())
        phase = float(self.__phase.get())
        length = int(self.__length.get())
        delay = int(self.__delay.get())
        scaling_factor = float(self.__scaling_factor.get())
        exp_const = float(self.__exp_const.get())
        user_signal = eval(self.__user_signal.get())
        self.__x= None
        self.__y= None
        if signalIndex==0:
            
            self.__x= numpy.arange(delay, delay+length, 1)
            self.__y= amplitude*numpy.sin(2*numpy.pi/period* numpy.arange(0,length,1)+phase)
        if signalIndex==1:
            if self.__causality.get_selection()==0:
                self.__x = numpy.arange(delay, delay+length, 1)
                self.__y = scaling_factor*(exp_const)**numpy.arange(0,length,1)
            else:
                self.__x = numpy.arange(delay-length+1, delay+1, 1)
                self.__y = scaling_factor*(exp_const)**numpy.arange(length-1, -1, -1)
        if signalIndex==2:
            self.__x = numpy.arange(delay, delay+length, 1)
            self.__y = amplitude*numpy.ones(length)
        if signalIndex==3:
            self.__x = numpy.array([delay])
            self.__y = numpy.array([amplitude])
        if signalIndex==4:
            self.__x = numpy.arange(delay, delay+ len(user_signal), 1)
            self.__y = user_signal
            
    def get_xy(self):
        return [self.__x, self.__y]
        
class System:
    DEFAULT_VALUE = {'default_system':0, 'z':[1,2], 'p':[-1,-2], 'k':1, 'num':[1], 'den':[1,3,2]}
    def __init__(self, frame, **kwargs):
        try:
            defaultValue = kwargs['defaultvalue']
        except:
            defaultValue = {'default_system':0, 'z':None, 'p':None, 'k':None, 'num':None, 'den':None}
        try:
            self.command = kwargs['command']
        except:
            self.command = None
        try:
            label = kwargs['label']
            mainFrame = Tk.LabelFrame(frame, text=label)
        except:
            mainFrame = Tk.Frame(frame)
        mainFrame.pack()
        self.radiobutton = Radiobutton(mainFrame, ['Zero-Pole-Gain', 'Coefficient'], command=self.chooseRadio, defaultvalue=defaultValue['default_system'])
        self.__zeros = LabelEntry(mainFrame, text="Zeros:", defaultvalue=defaultValue['z'], command=self.command, labelwidth=25)
        self.__poles = LabelEntry(mainFrame, text="Poles:", defaultvalue=defaultValue['p'], command=self.command, labelwidth=25)
        self.__gain = LabelEntry(mainFrame, text="Gain (k):", defaultvalue=defaultValue['k'], command=self.command, labelwidth=25)
        self.__num = LabelEntry(mainFrame, text="Numerator:", defaultvalue=defaultValue['num'], command=self.command, labelwidth=25)
        self.__den = LabelEntry(mainFrame, text="Denominator", defaultvalue=defaultValue['den'], command=self.command, labelwidth=25)
        self.chooseRadio(None)        
        
    def chooseRadio(self, *args):
        system_index = self.radiobutton.get_selection()
        if system_index==0:
            self.__zeros.set_visible()
            self.__poles.set_visible()
            self.__gain.set_visible()
            self.__num.set_invisible()
            self.__den.set_invisible()
        else:
            self.__zeros.set_invisible()
            self.__poles.set_invisible()
            self.__gain.set_invisible()
            self.__num.set_visible()
            self.__den.set_visible()
        try:
            self.command()
        except:
            pass
        
class Waveform:
    DEFAULT_VALUE = {'default_wave':0, 'amplitude':1, 'frequency':4, 'start_time':0, 'end_time':1, 'delay':0, 'displacement':0}
    def __init__(self, frame, Figure, **kwargs):
        KEY_DEFAULTVALUE = 'defaultvalue'
        KEY_LABEL = 'label'
        KEY_COMMAND = 'command'
        KEY_SAMPLING = 'sampling'
        self.list = ['Sine', 'Square', 'Sawtooth', 'Triangle', 'User Function']
        try:    defaultValue = kwargs[KEY_DEFAULTVALUE]
        except: defaultValue = {'default_wave':0, 'amplitude':None, 'frequency':None, 'start_time':None, 'end_time':None, 'delay':None, 'sampling_frequency':None, 'displacement':0}
        try:
            label = kwargs[KEY_LABEL]
            mainFrame = Tk.LabelFrame(frame, text=label)
        except:
            mainFrame = Tk.Frame(frame)
        mainFrame.pack()
        try:    self.command = kwargs[KEY_COMMAND]
        except: self.command = None
        try:    self.sampling = kwargs[KEY_SAMPLING]
        except: self.sampling = 500
        
        self.figure = Figure
        self.wavelistbox = Listbox(mainFrame, self.list, label='Wave', defaultvalue=defaultValue['default_wave'], command=self.updateWaveform)
        self.amplitude = LabelEntry(mainFrame, text='Amplitude: ', defaultvalue=defaultValue['amplitude'], command=self.updateWaveform, labelwidth=25)
        self.frequency = LabelEntry(mainFrame, text='Frequency (Hz): ', defaultvalue=defaultValue['frequency'], command=self.updateWaveform, labelwidth=25)
        self.start_time = LabelEntry(mainFrame, text='Start time (s): ', defaultvalue=defaultValue['start_time'], command=self.updateWaveform, labelwidth=25)
        self.end_time = LabelEntry(mainFrame, text='End time (s): ', defaultvalue=defaultValue['end_time'], command=self.updateWaveform, labelwidth=25)
        self.delay = LabelEntry(mainFrame, text='Shift (s): ', defaultvalue=defaultValue['delay'], command=self.updateWaveform, labelwidth=25)
        self.displacement = LabelEntry(mainFrame, text='Displacement: ', defaultvalue=defaultValue['displacement'], command=self.updateWaveform, labelwidth=25)
        self.userSignal = LabelEntry(mainFrame, text ='User Function', defaultvalue='y=x**2 + 2*x + 1', command=self.updateWaveform, labelwidth=25)
    
    def calculate_signal(self, **kwargs):
        try: sampling = kwargs['sampling_rate']
        except: sampling = self.sampling
        waveIndex = self.wavelistbox.get_selection()
        st = float(self.start_time.get())
        et = float(self.end_time.get())
        a = float(self.amplitude.get())
        f = float(self.frequency.get())
        delay = float(self.delay.get())
        displacement = float(self.displacement.get())
        
        x = numpy.arange(st, et+1.0/sampling, 1.0/sampling)
        if (self.list[waveIndex] == 'Sine'):
            y = displacement + a*numpy.sin(2*numpy.pi*f*x - delay*f*numpy.pi)
        if (self.list[waveIndex] == 'Square'):
            y = displacement + a*sgl.square(2*numpy.pi *f*(x-delay))
        if (self.list[waveIndex] == 'Sawtooth'):
            y = displacement + a*sgl.sawtooth(2*numpy.pi *f*(x-delay))
        if (self.list[waveIndex] == 'Triangle'):
            y = displacement + a*sgl.sawtooth(2*numpy.pi *f*(x-delay), width=0.5)
        if (self.list[waveIndex] == 'User Function'):
            try:    exec(self.userSignal.get())
            except: pass
        return [x,y]
                
    def updateWaveform(self, *args):
        [x,y]=self.calculate_signal()
        self.figure.plot(x,y, 'update')
        self.command()
        
class DraggablePoint:
    
    lock = None  # only one can be animated at a time
    def __init__(self, figure, xy, *args, **kwargs):
        try:    self.command = kwargs.pop('command')
        except: self.command = None
        if 'single_drag' in args:
            self.optimize = True
        else:   self.optimize = False
        self.rect = self.getShape(figure, xy, **kwargs)
        self.press = None
        self.background = None
        self.connect()

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self)
    
    def __call__(self, event):
        if event.name =='button_press_event':
            self.on_press(event)
        if event.name =='button_release_event':
            self.on_release(event)
        if event.name =='motion_notify_event':
            self.on_motion(event)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        if (DraggablePoint.lock is not None) and self.optimize: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        x0, y0 = self.get_center()
        self.press = x0, y0, event.xdata, event.ydata
        if self.optimize:
            DraggablePoint.lock = self
            canvas = self.rect.figure.canvas
            axes = self.rect.axes
            self.rect.set_animated(True)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self.rect.axes.bbox)
            axes.draw_artist(self.rect)
            canvas.blit(axes.bbox)

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if (DraggablePoint.lock is not self) and self.optimize:
            return
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.set_center(x0+dx, y0+dy)
        self.command(self)
        if self.optimize:
            canvas = self.rect.figure.canvas
            axes = self.rect.axes
            canvas.restore_region(self.background)
            axes.draw_artist(self.rect)
            canvas.blit(axes.bbox)
        else:
            self.rect.figure.canvas.draw()
        
    def on_release(self, event):
        'on release we reset the press data'
        if (DraggablePoint.lock is not self) and self.optimize:
            return
        self.press = None
        if self.optimize:
            DraggablePoint.lock = None
            self.rect.set_animated(False)
            self.background = None
        self.rect.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)
        
    def getShape(self, figure, xy, **kwargs):
        try:    self.shape = kwargs['shape']
        except: self.shape = 'circle'
        ax = figure.get_ax()            
        if self.shape == 'circle':
            try:    radius = kwargs['radius']
            except: radius = 0.2
            return ax.add_patch(patches.Circle(xy, radius))
        if self.shape == 'rectangle':
            try:    width = kwargs['width']
            except: width = 0.2
            try:    height = kwargs['height']
            except: height = 0.2
            return ax.add_patch(patches.Rectangle((xy[0]-width/2, xy[1]-height/2), width, height))
            
    def get_center(self):
        if self.shape == 'circle':
            return self.rect.center
        if self.shape == 'rectangle':
            return self.rect.get_xy()
            
    def set_center(self, x, y):
        if self.shape == 'circle':
            self.rect.center = (x, y)
        if self.shape == 'rectangle':
            self.rect.set_xy((x,y))