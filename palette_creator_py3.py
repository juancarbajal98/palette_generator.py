"""
Remade on Mon Feb 22 2021

@author: Juan Carbajal
Program to allow user to enter file name,
have image load,
and click on x different locations (specified with grid param)
after x clicks should be given another button or choice to conclude
and save palette picture
"""
from packages.app import App
import tkinter as Tk

if __name__=="__main__":
    file_name = input("Picture file name: ")
    orientation = input("Orientation(N/W/S/E): ")
    grid = input("Grid #: ")
    root = Tk.Tk()
    #grid = 4
    instantiater = App(root,file_name,orientation, int(grid))
    root.mainloop()