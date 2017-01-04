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

inQueue = True


top = tk.Tk()

def screenGrab():
    pyscreeze.screenshot(os.getcwd() + '\\Templates' + '\\LeagueGrab.jpg')



def othersAccept():
    global top
    top.after(1000)
    champSelect = False
    for x in range(1,11):
        screenGrab()
        template('MatchAccepted')
        if templateMatch == False:
            top.after(2000)
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
        top.after(3000)
    if champSelect == True:
        if NorR == 2:
            banWait()
    else:
        checkingLoop()  
    


        
def askBans():
    #global NorR
    #NorR = raw_input('N or R: ')
    #if NorR == 'r':
        #ban1 = raw_input('Enter first ban preference: ')
        #ban2 = raw_input('Enter second ban preference: ')
        #global banList
        #banList = [ban1, ban2, 'Aatrox', 'Morde', 'Sona']
    ban1 = rawban1.get()
    ban2 = rawban2.get()
    global banList
    banList = [ban1, ban2, 'Aatrox', 'Morde', 'Sona']
    global NorR
    NorR = gameType.get()
    

def banWait():
    global top
    banning = False
    for x in range(1,46):
        screenGrab()
        template('BanTime')
        if templateMatch == True:
            banning = True
            break
        else:
            top.after(4000)
    if banning == True:
        ban()
        


def ban():
    global top
    for x in range(0,5): 
        from pykeyboard import PyKeyboard
        k = PyKeyboard()
        k.tap_key(k.tab_key,n=2,interval=0.2)
        top.after(500)
        k.type_string(banList[x])
        squarex = int(centrex - (windowW/4.8659))
        squarey = int(centrey + (windowH/3.3188))
        top.after(1000)
        from pymouse import PyMouse
        m = PyMouse()
        m.move(squarex, squarey)
        top.after(1000)
        screenGrab()
        template('BanTest')
        m.click(squarex, squarey)
        if templateMatch == False:
            template('BanButton')
            from pymouse import PyMouse
            m = PyMouse()
            m.click(templatex, templatey)
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



def callback(hwnd, extra):
    name = win32gui.GetWindowText(hwnd)
    visible = win32gui.IsWindowVisible(hwnd)
    if name == 'League Client' and visible == 1:
        placement = win32gui.GetWindowPlacement(hwnd)
        (left, top, right, bottom) = placement[4]
        win32gui.ShowWindow(hwnd,4)
        win32gui.SetForegroundWindow(hwnd)
        global windowW
        windowW = right - left
        global windowH
        windowH = bottom - top
        global centrex
        centrex = int((left + right) / 2)
        global centrey
        centrey = int((top + bottom) / 2)
        global scale
        scale = windowW/1280
        if left < 0:
            win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, windowW, windowH, 0)
        askBans()
        checkingLoop()



def checkingLoop():
    dots = ""
    global top
    global inQueue
    inQueue = True
    while True:
        if inQueue == True:
            DotMsg = '\rChecking Queue{dotNo}'.format(dotNo = dots)
            os.system('cls' if os.name == 'nt' else 'clear')
            #msg.set(DotMsg)
           # top.update_idletasks()
            screenGrab()
            template('AcceptButton')
            if templateMatch == True:   
                from pymouse import PyMouse
                m = PyMouse()
                m.click(templatex, templatey)
                inQueue = False
                othersAccept()
                top.destroy()
            top.after(4000)
            if dots == " . . .":
                dots = ""
            else:
                dots = dots + " ."
    print("Forever loop broken")


               
def main():
    win32gui.EnumWindows(callback, None)


gameType = tk.IntVar()
c1 = tk.Radiobutton(top, text = "Ranked" ,variable = gameType, value = 1, indicatoron=0, width = 18, bd=1)
c2 = tk.Radiobutton(top, text = "Normal" ,variable = gameType, value = 2, indicatoron=0, width = 18, bd=1)
c1.grid(row=0, column = 0)
c2.grid(row=0, column = 1)

l1 = tk.Label( top, text="1st Ban Pref.")
l1.grid(row=1, column = 0)
l2 = tk.Label( top, text="2nd Ban Pref.")
l2.grid(row=2, column = 0)

rawban1 = tk.StringVar()
e1 = tk.Entry(top, bd =1, textvariable = rawban1, width = 22)
rawban2 = tk.StringVar()
e2 = tk.Entry(top, bd =1, textvariable = rawban2, width = 22)

e1.grid(row=1, column=1)
e2.grid(row=2, column=1)

b1 = tk.Button(top, text = "Start", command = main, width = 37, bd=1)
b1.grid(row=3, columnspan=2)

msg = tk.StringVar()
l3 = tk.Label( top, textvariable = msg, width = 37)
l3.grid(row = 4, columnspan=2)


top.mainloop()


    

    
#if __name__ == '__main__':
    #main()
