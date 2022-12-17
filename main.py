"""
Created 12/17/2022

@author: Jean-Loup Gonzalez
"""

import tkinter as tk

import modelisation as md
import numpy as np
import math as m

# initialisation parametres
#parametres
L1 = 1
L2 = 2
L3 = 1
L4 = 1
L5 = 1
h1 = 1
h2 = 1

# inputs
theta = 30
pointA = [6, 1, 3]
pointB = [6, 1, 3]


root = tk.Tk()
root.title("Modelisation du robot RRPR")

# setting the windows size
root.geometry("600x400")

# declaring string variable
# for storing name and password
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
    global l1, l2, l3, l4, l5, h1, h2
    l1 = int(l1_stock.get())
    l2 = int(l2_stock.get())
    l3 = int(l3_stock.get())
    l4 = int(l4_stock.get())
    l5 = int(l5_stock.get())
    h1 = int(h1_stock.get())
    h2 = int(h2_stock.get())

    print(f"l1 saisi: {l1}")
    print(f"l2 saisi: {l2}")
    print(f"l3 saisi: {l3}")
    print(f"l4 saisi: {l4}")
    print(f"l5 saisi: {l5}")
    print(f"h1 saisi: {h1}")
    print(f"h2 saisi: {h2}")

    # vide les variables pour saisie future
    l1_stock.set("")
    l2_stock.set("")
    l3_stock.set("")
    l4_stock.set("")
    l5_stock.set("")
    h1_stock.set("")
    h2_stock.set("")


def lancerMod():
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
l1_label = tk.Label(root, text='l1 = ', font=('calibre', 10, 'bold'))
l2_label = tk.Label(root, text='l2 = ', font=('calibre', 10, 'bold'))
l3_label = tk.Label(root, text='l3 = ', font=('calibre', 10, 'bold'))
l4_label = tk.Label(root, text='l4 = ', font=('calibre', 10, 'bold'))
l5_label = tk.Label(root, text='l5 = ', font=('calibre', 10, 'bold'))
h1_label = tk.Label(root, text='h1 = ', font=('calibre', 10, 'bold'))
h2_label = tk.Label(root, text='h2 = ', font=('calibre', 10, 'bold'))

# creating entries for input name using widget Entry
l1_entry = tk.Entry(root, textvariable=l1_stock, font=('calibre', 10, 'normal'))
l2_entry = tk.Entry(root, textvariable=l2_stock, font=('calibre', 10, 'normal'))
l3_entry = tk.Entry(root, textvariable=l3_stock, font=('calibre', 10, 'normal'))
l4_entry = tk.Entry(root, textvariable=l4_stock, font=('calibre', 10, 'normal'))
l5_entry = tk.Entry(root, textvariable=l5_stock, font=('calibre', 10, 'normal'))
h1_entry = tk.Entry(root, textvariable=h1_stock, font=('calibre', 10, 'normal'))
h2_entry = tk.Entry(root, textvariable=h2_stock, font=('calibre', 10, 'normal'))

# creating a button using the widget Button that will call the submit function
sub_btn = tk.Button(root, text='Valider les valeurs saisies', command=submit)
lancerModelisation_btn = tk.Button(root, text="Lancer la modelisation (apres initialisation)", command=lancerMod)

# placing the label and entry in the required position using grid method
param_label.grid(row=0, column=0)

l1_label.grid(row=1, column=0)
l1_entry.grid(row=1, column=1)

l2_label.grid(row=2, column=0)
l2_entry.grid(row=2, column=1)

l3_label.grid(row=3, column=0)
l3_entry.grid(row=3, column=1)

l4_label.grid(row=4, column=0)
l4_entry.grid(row=4, column=1)

l5_label.grid(row=5, column=0)
l5_entry.grid(row=5, column=1)

h1_label.grid(row=6, column=0)
h1_entry.grid(row=6, column=1)

h2_label.grid(row=7, column=0)
h2_entry.grid(row=7, column=1)

sub_btn.grid(row=8, column=1)
lancerModelisation_btn.grid(row=9, column=1)

# performing an infinite loop
# for the window to display
root.mainloop()
