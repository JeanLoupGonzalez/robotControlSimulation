"""
Created 12/17/2022

@author: Jean-Loup Gonzalez
"""

import tkinter as tk

import modelisation as md
import numpy as np
import math as m

# initialisation parametres
# parametres
l1 = 1
l2 = 2
l3 = 1
l4 = 1
l5 = 1
h1 = 1
h2 = 1

# inputs
theta = 30
pointA = [6, 1, 3]
pointB = [6, 1, 3]

# variables intermediaires
Ax, Ay, Az, Bx, By, Bz = 0, 0, 0, 0, 0, 0
root = tk.Tk()
root.title("Modelisation du robot RRPR")

# setting the windows size
root.geometry("500x300")

# declaring string variable
# for storing name and password
Ax_stock = tk.StringVar()
Ay_stock = tk.StringVar()
Az_stock = tk.StringVar()

Bx_stock = tk.StringVar()
By_stock = tk.StringVar()
Bz_stock = tk.StringVar()

l1_stock = tk.StringVar()
l2_stock = tk.StringVar()
l3_stock = tk.StringVar()
l4_stock = tk.StringVar()
l5_stock = tk.StringVar()

h1_stock = tk.StringVar()
h2_stock = tk.StringVar()


# defining a function that will
# get the name and password and
# print them on the screen
def submit():
    global l1, l2, l3, l4, l5, h1, h2, Ax, Ay, Az, Bx, By, Bz, pointA, pointB

    Ax = float(Ax_stock.get())
    Ay = float(Ay_stock.get())
    Az = float(Az_stock.get())
    Bx = float(Bx_stock.get())
    By = float(By_stock.get())
    Bz = float(Bz_stock.get())
    pointA = [Ax, Ay, Az]
    pointB = [Bx, By, Bz]

    l1 = float(l1_stock.get())
    l2 = float(l2_stock.get())
    l3 = float(l3_stock.get())
    l4 = float(l4_stock.get())
    l5 = float(l5_stock.get())

    h1 = float(h1_stock.get())
    h2 = float(h2_stock.get())

    # vide les variables pour saisie future
    Ax_stock.set("")
    Ay_stock.set("")
    Az_stock.set("")
    Bx_stock.set("")
    By_stock.set("")
    Bz_stock.set("")
    l1_stock.set("")
    l2_stock.set("")
    l3_stock.set("")
    l4_stock.set("")
    l5_stock.set("")
    h1_stock.set("")
    h2_stock.set("")


def lancerMod():
    submit()
    print(f"A saisi: {pointA}")
    print(f"B saisi: {pointB}")
    print(f"l1 saisi: {l1}")
    print(f"l2 saisi: {l2}")
    print(f"l3 saisi: {l3}")
    print(f"l4 saisi: {l4}")
    print(f"l5 saisi: {l5}")
    print(f"h1 saisi: {h1}")
    print(f"h2 saisi: {h2}")
    mod = md.Modelisation()
    mod.setParametres(l1, l2, l3, l4, l5, h1, h2)
    mod.setInputs(pointA, pointB, theta)


# creating labels for name using widget Label
param_label = tk.Label(root, text='Saisir TOUS les parametres puis valider avec le bouton : ',
                       font=('calibre', 10, 'bold'))
A_label = tk.Label(root, text='(saisir X Y Z, un par case) point A = ', font=('calibre', 10, 'bold'))
B_label = tk.Label(root, text='(saisir X Y Z, un par case) point B = ', font=('calibre', 10, 'bold'))
l1_label = tk.Label(root, text='l1 = ', font=('calibre', 10, 'bold'))
l2_label = tk.Label(root, text='l2 = ', font=('calibre', 10, 'bold'))
l3_label = tk.Label(root, text='l3 = ', font=('calibre', 10, 'bold'))
l4_label = tk.Label(root, text='l4 = ', font=('calibre', 10, 'bold'))
l5_label = tk.Label(root, text='l5 = ', font=('calibre', 10, 'bold'))
h1_label = tk.Label(root, text='h1 = ', font=('calibre', 10, 'bold'))
h2_label = tk.Label(root, text='h2 = ', font=('calibre', 10, 'bold'))

# creating entries for input name using widget Entry
Ax_entry = tk.Entry(root, width=5, textvariable=Ax_stock, font=('calibre', 10, 'normal'))
Ay_entry = tk.Entry(root, width=5, textvariable=Ay_stock, font=('calibre', 10, 'normal'))
Az_entry = tk.Entry(root, width=5, textvariable=Az_stock, font=('calibre', 10, 'normal'))
Bx_entry = tk.Entry(root, width=5, textvariable=Bx_stock, font=('calibre', 10, 'normal'))
By_entry = tk.Entry(root, width=5, textvariable=By_stock, font=('calibre', 10, 'normal'))
Bz_entry = tk.Entry(root, width=5, textvariable=Bz_stock, font=('calibre', 10, 'normal'))
l1_entry = tk.Entry(root, width=5, textvariable=l1_stock, font=('calibre', 10, 'normal'))
l2_entry = tk.Entry(root, width=5, textvariable=l2_stock, font=('calibre', 10, 'normal'))
l3_entry = tk.Entry(root, width=5, textvariable=l3_stock, font=('calibre', 10, 'normal'))
l4_entry = tk.Entry(root, width=5, textvariable=l4_stock, font=('calibre', 10, 'normal'))
l5_entry = tk.Entry(root, width=5, textvariable=l5_stock, font=('calibre', 10, 'normal'))
h1_entry = tk.Entry(root, width=5, textvariable=h1_stock, font=('calibre', 10, 'normal'))
h2_entry = tk.Entry(root, width=5, textvariable=h2_stock, font=('calibre', 10, 'normal'))

# creating a button using the widget Button that will call the submit function
sub_btn = tk.Button(root, text='Valider les valeurs saisies', command=submit)
lancerModelisation_btn = tk.Button(root, text="Valider les parametres et lancer la modelisation", command=lancerMod)

# placing the label and entry in the required position using grid method
param_label.grid(row=0, column=0)

A_label.grid(row=1, column=0)
Ax_entry.grid(row=1, column=1)
Ay_entry.grid(row=1, column=2)
Az_entry.grid(row=1, column=3)

B_label.grid(row=2, column=0)
Bx_entry.grid(row=2, column=1)
By_entry.grid(row=2, column=2)
Bz_entry.grid(row=2, column=3)

l1_label.grid(row=3, column=0)
l1_entry.grid(row=3, column=1)

l2_label.grid(row=4, column=0)
l2_entry.grid(row=4, column=1)

l3_label.grid(row=5, column=0)
l3_entry.grid(row=5, column=1)

l4_label.grid(row=6, column=0)
l4_entry.grid(row=6, column=1)

l5_label.grid(row=7, column=0)
l5_entry.grid(row=7, column=1)

h1_label.grid(row=8, column=0)
h1_entry.grid(row=8, column=1)

h2_label.grid(row=9, column=0)
h2_entry.grid(row=9, column=1)

sub_btn.grid(row=10, column=0)
lancerModelisation_btn.grid(row=10, column=0)

# performing an infinite loop
# for the window to display
root.mainloop()
