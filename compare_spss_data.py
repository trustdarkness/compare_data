#!/usr/bin/env python
#Boa:App:BoaApp

import wx

import main_gui

modules ={'main_gui': [1, 'Main Application Window', u'main_gui.py']}

class BoaApp(wx.App):
    def OnInit(self):
        self.main = main_gui.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = BoaApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
