from __future__ import division
import pyscreeze
import os
import time
import win32gui
import cv2
from numpy import where
import math
import win32con
import Tkinter as tk
import threading
import Queue
dots = ""
inQueue = True


class GUI(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.gameType = tk.IntVar()
        self.radio1 = tk.Radiobutton(self, text = "Normal" ,variable = self.gameType, value = 1, indicatoron=0, width = 18, bd=1)
        self.radio1.grid(row=0, column = 0)
        self.radio2 = tk.Radiobutton(self, text = "Ranked" ,variable = self.gameType, value = 2, indicatoron=0, width = 18, bd=1)
        self.radio2.grid(row=0, column = 1)

        self.label1 = tk.Label(self, text="1st Ban Pref.")
        self.label1.grid(row=1, column = 0)
        self.label2 = tk.Label(self, text="2st Ban Pref.")
        self.label2.grid(row=2, column = 0)

        self.rawban1 = tk.StringVar()
        self.entry1 = tk.Entry(self, bd =1, textvariable = self.rawban1, width = 22)
        self.entry1.grid(row=1, column=1)
        self.rawban2 = tk.StringVar()
        self.entry2 = tk.Entry(self, bd =1, textvariable = self.rawban2, width = 22)
        self.entry2.grid(row=2, column=1)

        self.button = tk.Button(self, text = "Start", command = main, width = 37, bd=1)
        self.button.grid(row=3, columnspan=2)

        self.msg = tk.StringVar()
        self.label3 = tk.Label(self, textvariable = self.msg, width = 37)
        self.label3.grid(row = 4, columnspan=2)


def main():
    win32gui.EnumWindows(callback, None)


def callback(hwnd, extra):
    global windowW
    global windowH
    global windowX
    global windowY
    global scale
    name = win32gui.GetWindowText(hwnd)
    visible = win32gui.IsWindowVisible(hwnd)
    if name == 'League Client' and visible == 1:
        placement = win32gui.GetWindowPlacement(hwnd)
        (left, top, right, bottom) = placement[4]
        win32gui.ShowWindow(hwnd,4)
        win32gui.SetForegroundWindow(hwnd)
        windowW = right - left
        windowH = bottom - top
        windowX = int((left + right) / 2)
        windowY = int((top + bottom) / 2)
        scale = windowW/1280
        print(windowW)
        print(windowH)
        if left < 0:
            win32gui.ShowWindow(hwnd,4)
            win32gui.SetForegroundWindow(hwnd)
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, windowW, windowH, 0)
        getBans()
        checkingLoop()


def getBans():
    ban1 = app.rawban1.get()
    ban2 = app.rawban2.get()
    global banList
    banList = [ban1, ban2, 'Aatrox', 'Morde', 'Sona']
    global NorR
    NorR = app.gameType.get()
    print(NorR)


def checkingLoop():
    dots = ""
    global inQueue
    inQueue = True
    while True:
        if inQueue == True:
            DotMsg = '\rChecking Queue{dotNo}'.format(dotNo = dots)
            os.system('cls' if os.name == 'nt' else 'clear')
            app.msg.set(DotMsg)
            app.update_idletasks()
            screenGrab()
            template('AcceptButton')
            if templateMatch == True:   
                from pymouse import PyMouse
                m = PyMouse()
                m.click(templatex, templatey)
                inQueue = False
                othersAccept()
            time.sleep(4)
        else:
            break




def template(file):
    global templateMatch
    global templatex
    global templatey
    fileName = '{Name}.jpg'.format(Name = file)
    img_rgb = cv2.imread(os.getcwd() + '\\Templates' + '\\LeagueGrab.jpg')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    acceptButton = cv2.imread(os.getcwd() + '\\Templates\\' + fileName,0)
    template = cv2.resize(acceptButton, (0,0), fx=scale, fy=scale) 
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = where( res >= threshold)
    elements = len(loc[0])
    if elements == 0:
        templateMatch = False
    else:
        templateMatch
        templateMatch = True
    for pt in zip(*loc[::-1]):
        templatex = int((pt[0] + pt[0] + w) / 2)
        templatey = int((pt[1] + pt[1] + h) / 2)


def screenGrab():
    pyscreeze.screenshot(os.getcwd() + '\\Templates' + '\\LeagueGrab.jpg')


def othersAccept():
    time.sleep(1)
    champSelect = False
    for x in range(1,11):
        screenGrab()
        template('MatchAccepted')
        if templateMatch == False:
            time.sleep(2)
            template('QueueIcon')
            if templateMatch == False:
                template('AcceptButton')
                if templateMatch == True:
                    champSelect = False
                else:
                    champSelect = True
                break
            else:
                champSelect = False
                break
        time.sleep(3)
    if champSelect == True:
        if NorR == 2:
            banWait()
    else:
        checkingLoop()


def banWait():
    banning = False
    for x in range(1,46):
        screenGrab()
        template('BanTime')
        if templateMatch == True:
            banning = True
            break
        else:
            time.sleep(4)
    if banning == True:
        ban()


def ban():
    for x in range(0,5): 
        from pykeyboard import PyKeyboard
        k = PyKeyboard()
        k.tap_key(k.tab_key,n=2,interval=0.2)
        time.sleep(0.5)
        k.type_string(banList[x])
        squarex = int(windowX - (windowW/4.8659))
        squarey = int(windowY - (windowH/3.3188))
        time.sleep(1)
        from pymouse import PyMouse
        m = PyMouse()
        m.move(squarex, squarey)
        time.sleep(1)
        screenGrab()
        template('BanTest')
        m.click(squarex, squarey)
        if templateMatch == False:
            template('BanButton')
            from pymouse import PyMouse
            m = PyMouse()
            m.click(templatex, templatey)
            break
    


app = GUI()
app.mainloop()
