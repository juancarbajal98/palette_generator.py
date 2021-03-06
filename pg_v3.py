"""
Remade on Fri Mar 5 2021

@author: Juan Carbajal
Program to allow user to enter file name,
have image load,
and click on x different locations (specified with grid param)
after x clicks should be given another button or choice to conclude
and save palette picture
@update
Adding a fixed frame preconditioning and making different windows for button
to ensure same sized, cropped, cookie-cutter palettes
"""
from packages.app import App
import tkinter as Tk

if __name__=="__main__":
    file_name = input("Picture file name: ")
    root = Tk.Tk()
    root.withdraw()
    # instantiater = App(root,file_name,orientation, int(grid))
    # initializer only takes root and file 
    # orientation is either calculated or demanded along with grid 
    instantiater = App(file_name)
    print(instantiater.calc_orientation)
    # depending on orien, we ask for direction
    if(instantiater.calc_orientation == 'vertical'):
        direction = input("Direction(W/E): ")
    elif(instantiater.calc_orientation == 'up_to_user'):
        direction = input("Direction(N/W/S/E): ")
    else:
        direction = input("Direction(N/S): ")
    # ask grid size
    grid = input("Grid #: ")
    instantiater.launchPalette(root,direction,int(grid))
    root.deiconify()
    root.mainloop()