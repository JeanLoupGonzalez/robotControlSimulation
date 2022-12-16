# tentative de faire un jeu Picolo avec interface graphique

from tkinter import *


def accueil():
    frame = Frame(root)
    txt1 = Label(frame, text="MGI", fg="black")
    txt1.pack()
    bt1 = Button(frame, text="btn1", command=root.destroy)
    bt2 = Button(frame, text="tbn2", command=fction1)
    bt1.pack()
    bt2.pack()
    return frame


def fction1():
    print("ds fction1")
    frame = Frame(root)
    frame_accueil.destroy()
    frame.pack()
    txt = Label(frame, text="qsdqsd")
    txt.pack()
    nbPlayers = Listbox(frame, )
    nbPlayers.insert(1, "1")
    nbPlayers.insert(2, "2")
    nbPlayers.insert(3, "3")
    nbPlayers.pack()
    return frame


root = Tk()
root.wm_title("BE")

frame_accueil = accueil()
frame_accueil.pack()

root.mainloop()
