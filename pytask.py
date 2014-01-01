import psutil
import wx
from ObjectListView import ObjectListView, ColumnDefn
import TrayIcon
import win32con
import ctypes
import pytaskpassword
class Process(object):

    def __init__(self, name, pid, exe, user, cpu, mem, desc=None):
        
        self.name = name
        self.pid = pid
        self.exe = exe
        self.user = user
        self.cpu = cpu
        self.mem = mem
 
class MainPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.procs = []
        self.procmonOlv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.setProcs()
        endProcBtn = wx.Button(self, label="End Process")
        endProcBtn.Bind(wx.EVT_BUTTON, self.onKillProc)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.procmonOlv, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(endProcBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizer(mainSizer)
        self.updateDisplay()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(150000)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)
    def onKey(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.GetParent().Close()
        else:
            event.Skip()
    def setProcs(self):
        """"""
        cols = [
            ColumnDefn("Name", "left", 150, "name"),
            ColumnDefn("EXE Location", "left", 100, "exe"),
            ColumnDefn("Username", "left", 75, "user"),
            #ColumnDefn("cpu", "left", 75, "cpu"),
            ColumnDefn("Mem", "left", 75, "mem")
            ]
        self.procmonOlv.SetColumns(cols)
        self.procmonOlv.SetObjects(self.procs)
 
    def update(self, event):
        
        self.updateDisplay()

    def updateDisplay(self):
        
        pids = psutil.get_pid_list()
        for pid in pids:
 
            try:
                p = psutil.Process(pid)
                new_proc = Process(p.name,
                                   str(p.pid),
                                   p.exe,
                                   p.username,
                                   str(p.get_cpu_percent()),
                                   str(p.get_memory_percent())
                                   )
                self.procs.append(new_proc)
            except:
                pass
 
        self.setProcs()
    def onKillProc(self, event):
       
        obj = self.procmonOlv.GetSelectedObject()
        print
        pid = int(obj.pid)
        try:
            p = psutil.Process(pid)
            p.terminate()
            self.update("")
        except Exception, e:
            pass
    def onSelect(self, event):
        
        item = event.GetItem()
        itemId = item.GetId()
        self.currentSelection = itemId
        print
class Panel2(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.procs = []
        self.procmonOlv = ObjectListView(self, style=wx.LC_REPORT|wx.SUNKEN_BORDER)
        self.setProcs()
        endProcBtn = wx.Button(self, label="End Process")
        endProcBtn.Bind(wx.EVT_BUTTON, self.onKillProc)
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.procmonOlv, 1, wx.EXPAND|wx.ALL, 5)
        mainSizer.Add(endProcBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5)
        self.SetSizer(mainSizer)
        self.updateDisplay()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(150000)
        self.Bind(wx.EVT_KEY_DOWN, self.onKey)
    def onKey(self, event):
        key_code = event.GetKeyCode()
        if key_code == wx.WXK_ESCAPE:
            self.GetParent().Close()
        else:
            event.Skip()
    def setProcs(self):
        """"""
        cols = [
            ColumnDefn("Name", "left", 150, "name"),
            ColumnDefn("username", "left", 75, "user")
            ]
        self.procmonOlv.SetColumns(cols)
        self.procmonOlv.SetObjects(self.procs)
 
    def update(self, event):
        
        self.updateDisplay()

    def updateDisplay(self):
        
        pids = psutil.get_pid_list()
        for pid in pids:
 
            try:
                p = psutil.Process(pid)
                new_proc = Process(p.name,
                                   str(p.pid),
                                   p.exe,
                                   p.username,
                                   str(p.get_cpu_percent()),
                                   str(p.get_memory_percent())
                                   )
                self.procs.append(new_proc)
            except:
                pass
 
        self.setProcs()
    def onKillProc(self, event):
       
        obj = self.procmonOlv.GetSelectedObject()
        print
        pid = int(obj.pid)
        try:
            p = psutil.Process(pid)
            p.terminate()
            self.update("")
        except Exception, e:
            pass
    def onSelect(self, event):
        
        item = event.GetItem()
        itemId = item.GetId()
        self.currentSelection = itemId
        print

    
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="PyTask", style = wx.DEFAULT_FRAME_STYLE)
        self.panelone = MainPanel(self)
        self.paneltwo = Panel2(self)
        self.panelone.Hide()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.panelone, 1, wx.EXPAND)
        self.sizer.Add(self.paneltwo, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        self.menubar = wx.MenuBar()
        self.file = wx.Menu()
        self.SetMenuBar(self.menubar)
        self.menubar.Append(self.file,'&File')
        self.get = self.file.Append(wx.ID_ANY,'&Run\tCtrl+R')
        self.getlock = self.file.Append(wx.ID_ANY, '&Lock\tCtrl+L')
        self.getexit = self.file.Append(wx.ID_ANY, '&Exit and Minimize\tCtrl+Q')
        self.getexittotal = self.file.Append(wx.ID_ANY, '&Exit and Quit\tCtrl+Shift+Q')
        self.Bind(wx.EVT_MENU,self.GetApp,self.get)
        self.Bind(wx.EVT_MENU,self.lock,self.getlock)
        self.Bind(wx.EVT_MENU,self.exitm,self.getexit)
        self.Bind(wx.EVT_MENU,self.exitt,self.getexittotal)
        self.view = wx.Menu()
        self.menubar.Append(self.view,'&View')
        self.lesspanel = self.view.Append(wx.ID_ANY, '&Less Detail\tCtrl+N', 'Less Detail View', wx.ITEM_RADIO)
        self.switchpanel = self.view.Append(wx.ID_ANY, '&More Detail\tCtrl+M', 'Detailed View', wx.ITEM_RADIO)
        self.refresh = self.view.Append(wx.ID_ANY, '&Refresh\tCtrl+A')
        self.defaultview = self.view.Append(wx.ID_ANY, "&Normal Display\tCtrl+D", "Normal Display", wx.ITEM_RADIO)
        self.ontopview = self.view.Append(wx.ID_ANY, "&Always On Top\tCtrl+T", "On Top", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU,self.lessview,self.lesspanel)
        self.Bind(wx.EVT_MENU,self.moreview,self.switchpanel)
        self.Bind(wx.EVT_MENU,self.ontop,self.ontopview)
        self.Bind(wx.EVT_MENU,self.normview,self.defaultview)
        self.Bind(wx.EVT_MENU,self.GetRefresh,self.refresh)
        self.updates = wx.Menu()
        self.Normal = self.updates.Append(wx.ID_ANY, "&Update Time - Normal\tCtrl+U", "Update every 2 minutes", wx.ITEM_RADIO) 
        self.fs = self.updates.Append(wx.ID_ANY, "&Update Time - 15 Seconds\tCtrl+1", "Update every 15 seconds", wx.ITEM_RADIO)
        self.ts = self.updates.Append(wx.ID_ANY, "&Update Time - 30 Seconds\tCtrl+2", "Update every 30 seconds", wx.ITEM_RADIO)
        self.ss = self.updates.Append(wx.ID_ANY,"&Update Time - 60 Seconds\tCtrl+3", "Update every 60 seconds", wx.ITEM_RADIO)
        self.ns = self.updates.Append(wx.ID_ANY, "&Update Time - 90 Seconds\tCtrl+4", "Update every 90 seconds", wx.ITEM_RADIO)
        self.Bind(wx.EVT_MENU,self.Default,self.Normal)
        self.Bind(wx.EVT_MENU,self.fsec,self.fs)
        self.Bind(wx.EVT_MENU,self.tsec,self.ts)
        self.Bind(wx.EVT_MENU,self.ssec,self.ss)
        self.Bind(wx.EVT_MENU,self.nsec,self.ns)
        self.menubar.Append(self.updates, '&Update Options')
        self.help = wx.Menu()
        self.helpd = self.help.Append(wx.ID_ANY, '&Help\tCtrl+H')
        self.about = self.help.Append(wx.ID_ANY, '&About\tCtrl+A')
        self.Bind(wx.EVT_MENU,self.onHelp,self.helpd)
        self.Bind(wx.EVT_MENU,self.onabt,self.about)
        self.menubar.Append(self.help, '&Help')
        self.tbIcon = TrayIcon.CustomTaskBarIcon(self)
        self.Bind(wx.EVT_ICONIZE, self.onMinimize)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Size = (442, 573)
        iconFile = "pytask.ico"
        icon1 = wx.Icon(iconFile, wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon1)
        self.regHotKey()
        self.Bind(wx.EVT_HOTKEY, self.handleHotKey, id=self.hotKeyId)
        self.Show()
    def lock(self, event):
        self.MainFrame = pytaskpassword.Main()
    def regHotKey(self):
        self.hotKeyId = 100
        self.RegisterHotKey(
            self.hotKeyId,
            win32con.MOD_CONTROL,
            win32con.VK_F6) 
    def handleHotKey(self, evt):
        if self.pannelone.IsShown():
            self.Hide()
        else:
            self.Show()
            self.Raise()
    def onClose(self, event):
        self.Hide()
    def onMinimize(self, event):
        self.Hide()
    def moreview(self, event):
        self.panelone.Show()
        self.paneltwo.Hide()
        self.Layout()
    def lessview(self, event):
        self.paneltwo.Show()
        self.panelone.Hide()
        self.Layout()
    def normview(self,event):
        style = wx.DEFAULT_FRAME_STYLE
        self.SetWindowStyle( style )
    def ontop(self,event):
        style = self.GetWindowStyle()
        self.SetWindowStyle( style | wx.STAY_ON_TOP )
    def Default(self,event):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(120000)
    def fsec(self,event):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(15000)
    def tsec(self,event):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(30000)
    def ssec(self,event):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(60000)
    def nsec(self,event):
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(90000)
    def GetRefresh(self,event):
        self.updateDisplay()
    def GetApp(self, event):
        try:
            openFileDialog = wx.FileDialog(self, "Open EXE file", "", "",
                                       "EXE files (*.exe)|*.exe", wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if openFileDialog.ShowModal() == wx.ID_CANCEL:
                return     
            apppath = openFileDialog.GetPath()
            subprocess.Popen("%s" % (apppath))
        except WindowsError:
            pass
    def exitt(self,event):
        self.tbIcon.RemoveIcon()
        self.tbIcon.Destroy()
        self.Destroy()
    def exitm(self,event):
        self.Hide()

    def update(self, event):
        self.updateDisplay()
    def updateDisplay(self):
        pids = psutil.get_pid_list()
        for pid in pids:

            try:
                p = psutil.Process(pid)
                new_proc = Process(p.name,
                                   str(p.pid),
                                   p.exe,
                                   p.username,
                                   str(p.get_cpu_percent()),
                                   str(p.get_memory_percent())
                                   )
                self.procs.append(new_proc)
            except:
                pass

        
    def onabt(self, e):
    
        description = """PyTask is an task manager written in Python.
It GUI was made using the module wxPython.
Some features that are included are:
Powere to end task and run new tasks.
Also you can customize the window as wells as updating options.
It displays all process being ran on the computer.
It is also cross platform and has been tested on Windows and Linux,
but it should work on Mac.
"""

        licence = """Pytask is free software"""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('PyTask.png', wx.BITMAP_TYPE_PNG))
        info.SetName('PyTask')
        info.SetVersion('1.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2013 Grant')
        info.SetLicence(licence)
        info.AddDeveloper('Grant')
        wx.AboutBox(info)
    def onHelp(self, event):
        description = """
Welcome to PyTask Help!
Let's get started then.
PyTask has many functions I'll guide you trough them now.
Starting in the file menu you have "Run". With that you can select
a EXE file and pytask will atempt to run it. next you have an exit option.
Next you have view the first option is "Less Detail" if you choose that
it will display only the name of the process and the user who's running that process
next you have "More Detail" that will display a bunch of other things I will not list them off
you can check that out on your own.
Next you have "Refresh" that will refresh the process list.
Next you have normal view where the window will go behind other windows and then you have the oppisite of that.
in update options you can define the update time the default update time is 2 minutes.
Now will jump to the buttom where you have a button that if you select a process you can click end process.
Becarefull with this as it if you don't choose wisely you can end a system process.
That what you can do with PyTask. Also one more inport  thing is that when you close this program it
will minimuse to the task bar and it has an icon to close it right click the icon. to reopen it left click it."""
        info = wx.AboutDialogInfo()
        info.SetName('PyTask')
        info.SetVersion('1.1')
        info.SetDescription(description)
        wx.AboutBox(info)
    

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
