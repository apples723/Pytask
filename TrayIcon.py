import wx




class CustomTaskBarIcon(wx.TaskBarIcon):
    def __init__(self, frame):
        wx.TaskBarIcon.__init__(self)
        self.frame = frame
        img = wx.Image("pytask.ico", wx.BITMAP_TYPE_ANY)
        bmp = wx.BitmapFromImage(img)
        self.icon = wx.EmptyIcon()
        self.icon.CopyFromBitmap(bmp)
        self.SetIcon(self.icon, "PyTask: Left click to restore. Right click to close.")
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.OnLeftClick)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.OnRightClick)
    def OnRightClick(self, evt):
        self.RemoveIcon()
        self.Destroy()
    def OnTaskBarActivate(self, evt): 
        pass
    def OnTaskBarClose(self, evt):
        self.frame.Close()
    def OnLeftClick(self, evt):
        self.frame.Show()
