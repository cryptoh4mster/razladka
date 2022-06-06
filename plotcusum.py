# -*- coding: utf8 -*-
import wx
from mainwindow import MainWindow


class PlotCusum(wx.App):
    def __init__(self, *args, **kwds):
        wx.App.__init__(self, *args, **kwds)

    def OnInit(self):
        wx.InitAllImageHandlers()

        mainWnd = MainWindow(None, -1, "")
        mainWnd.Show()

        self.SetTopWindow(mainWnd)

        return True


if __name__ == "__main__":
    application = PlotCusum(False)
    application.MainLoop()
