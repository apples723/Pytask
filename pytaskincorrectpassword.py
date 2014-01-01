import wx
from wx import *

class MainFrame(wx.Frame):
    def __init__(self, parent=None, id=-1):
        wx.Frame.__init__(self, parent, id, 'Correct Passowrd', size=(265,75))
        panel = wx.Panel(self)
        self.tbIcon = TrayIcon.CustomTaskBarIcon(self)
        self.image = wx.Bitmap('password.jpg')     
        EVT_PAINT(self, self.OnPaint)
        self.Hide()
        okbttn = wx.Button(self, label="Ok", pos = (155, 300))
        okbttn.Bind(wx.EVT_BUTTON, self.ok)
        self.ShowFullScreen(not self.IsFullScreen(),wx.FULLSCREEN_NOCAPTION)
        box = wx.TextEntryDialog(None, 'Please type your password:','Password')
        while True:
            if box.ShowModal() == wx.ID_OK:
                answer = box.GetValue()
            if answer != 'admin1234':
                pass
            else:
                break
                self.Hide()
    def ok(self, event):
        self.Destroy()
    def OnPaint(self, event): 
        self.Paint(wx.PaintDC(self)) 

    def Paint(self, dc): 
        dc.DrawBitmap(self.image, 0, 0) 
            
            
        
if __name__=='__main__':
    app = wx.App(0)
    frame = MainFrame()
    frame.Show()
    app.MainLoop()
